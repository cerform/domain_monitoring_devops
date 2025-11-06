pipeline {
    agent { label 'Slave' }

    environment {
        REGISTRY = "symmetramain"
        IMAGE_NAME = "etcsys"
        REPO_URL = "https://github.com/cerform/domain_monitoring_devops.git"
        CONTAINER_NAME = "temp_container_${env.BUILD_NUMBER}"
        DOCKER_RUN_NAME = "${WORKSPACE}"
        DOCKER_IMAGE = "${REGISTRY}/${IMAGE_NAME}"
    }

    options { timestamps() }

    stages {

        stage('Verify Docker Availability') {
            steps {
                echo "🔍 Проверка установки Docker..."
                sh 'which docker || echo "❌ Docker не найден в PATH"'
                sh 'docker --version || echo "❌ Docker не установлен или не запущен"'
            }
        }

        stage('Получить последний коммит') {
            steps {
                script {
                    TAG = sh(
                        script: "git ls-remote ${REPO_URL} refs/heads/main | cut -f1 | tr -d '\\n' | tr -d '\\r'",
                        returnStdout: true
                    ).trim()

                    if (!TAG?.trim()) {
                        error("❌ Commit ID не найден — остановка сборки.")
                    }
                    echo "✅ Последний commit ID: '${TAG}'"
                }
            }
        }

        stage('Клонировать репозиторий') {
            steps {
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Собрать Docker-образ') {
            steps {
                echo "🐳 Сборка временного Docker-образа с тегом ${TAG}"
                retry(2) {
                    sh "docker build -t $REGISTRY/$IMAGE_NAME:${TAG} ."
                }
            }
        }

        stage('Запустить контейнер для тестов') {
            steps {
                echo "🚀 Запуск временного контейнера..."
                sh '''
                docker rm -f $CONTAINER_NAME || true
                docker run -d --name $CONTAINER_NAME $REGISTRY/$IMAGE_NAME:${TAG} tail -f /dev/null
                '''
            }
        }

        stage('Выполнить backend-e2e тесты') {
            steps {
                echo "🧪 Запуск e2e тестов в изолированном контейнере..."
                sh '''
                echo "🔍 Проверка node_modules и Nx..."
                docker run --rm -v $DOCKER_RUN_NAME:/app $DOCKER_IMAGE:$TAG \
                sh -c 'cd /app && ls node_modules && npx nx --version'

                echo "🚦 Запуск тестов и логирование..."
                docker run --rm -v $DOCKER_RUN_NAME:/app $DOCKER_IMAGE:$TAG \
                sh -c 'cd /app && npm run test:e2e' > e2e_output.log || (echo "❌ Тесты завершились с ошибкой. Лог:" && cat e2e_output.log && exit 1)
                '''
            }
        }

        stage('Промоут версии и пуш в DockerHub') {
            when { expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' } }
            steps {
                script {
                    def currentVersion = sh(
                        script: "git tag --sort=-v:refname | grep -Eo 'v[0-9]+\\.[0-9]+\\.[0-9]+' | head -n1 || echo 'v0.0.0'",
                        returnStdout: true
                    ).trim()

                    echo "📌 Текущая версия: ${currentVersion}"

                    def (major, minor, patch) = currentVersion.replace('v','').tokenize('.')
                    def newVersion = "v${major}.${minor}.${patch.toInteger() + 1}"
                    echo "🚀 Повышение версии до ${newVersion}"

                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker tag $REGISTRY/$IMAGE_NAME:${TAG} $DOCKER_USER/$IMAGE_NAME:${newVersion}
                        docker tag $REGISTRY/$IMAGE_NAME:${TAG} $DOCKER_USER/$IMAGE_NAME:latest
                        docker push $DOCKER_USER/$IMAGE_NAME:${newVersion}
                        docker push $DOCKER_USER/$IMAGE_NAME:latest
                        """
                    }

                    sh "git tag -a ${newVersion} -m 'Release ${newVersion}'"
                    sh "git push origin ${newVersion}"
                }
            }
        }
    }

    post {
        failure {
            echo "❌ Тесты завершились с ошибкой. Вывод логов контейнера..."
            sh "docker logs $CONTAINER_NAME || true"
        }
        always {
            echo "🧹 Очистка Docker-среды..."
            sh '''
            echo "📋 Список контейнеров перед очисткой:"
            docker ps -a || true

            echo "📋 Список образов перед очисткой:"
            docker images || true

            docker rm -f $CONTAINER_NAME || true
            docker rmi $REGISTRY/$IMAGE_NAME:${TAG} || true
            docker system prune -f || true
            '''
            deleteDir()
        }
    }
}