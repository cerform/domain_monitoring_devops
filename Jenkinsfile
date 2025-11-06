pipeline {
    agent { label 'Slave' }

    environment {
        REGISTRY = "symmetramain"
        IMAGE_NAME = "etcsys"
        REPO_URL = "https://github.com/cerform/domain_monitoring_devops.git"
        CONTAINER_NAME = "temp_container_${env.BUILD_NUMBER}"
    }

    options { timestamps() }

    stages {

        stage('Checkout Source Code') {
            steps {
                echo "Cloning repository from GitHub..."
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Get Commit ID') {
            steps {
                script {
                    env.TAG = sh(
                        script: "git rev-parse HEAD | tr -d '\\n' | tr -d '\\r'",
                        returnStdout: true
                    ).trim()

                    if (!env.TAG?.trim()) {
                        error("Commit ID not found — cannot continue build.")
                    }

                    echo "Docker image tag (commit ID): '${env.TAG}'"
                }
            }
        }

        stage('Build Docker Image (temp)') {
            steps {
                echo "Building temporary Docker image with tag ${env.TAG}"
                sh "docker build -t $REGISTRY/$IMAGE_NAME:${env.TAG} ."
            }
        }

        stage('Run Container for Tests') {
            steps {
                echo "Starting temporary container..."
                sh '''
                docker rm -f $CONTAINER_NAME || true
                docker run -d --name $CONTAINER_NAME $REGISTRY/$IMAGE_NAME:${TAG} tail -f /dev/null
                '''
            }
        }

        stage('Execute Test Suite') {
            parallel {
                stage('Backend API Tests') {
                    steps {
                        echo "Running backend Pytest tests..."
                        sh '''
                        docker exec $CONTAINER_NAME pytest tests/api_tests --maxfail=1 --disable-warnings -q || exit 1
                        '''
                    }
                }
                stage('UI Selenium Tests') {
                    steps {
                        echo "Running Selenium UI tests..."
                        sh '''
                        docker exec $CONTAINER_NAME pytest tests/selenium_tests --maxfail=1 --disable-warnings -q || exit 1
                        '''
                    }
                }
            }
        }

        stage('Promote Version and Push to DockerHub') {
            when { expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' } }
            steps {
                script {
                    def currentVersion = sh(
                        script: "git tag --sort=-v:refname | grep -Eo 'v[0-9]+\\.[0-9]+\\.[0-9]+' | head -n1 || echo 'v0.0.0'",
                        returnStdout: true
                    ).trim()

                    echo "Current version: ${currentVersion}"

                    def (major, minor, patch) = currentVersion.replace('v','').tokenize('.')
                    def newVersion = "v${major}.${minor}.${patch.toInteger() + 1}"
                    echo "Promoting image version to ${newVersion}"

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
            echo "Tests failed. Displaying logs..."
            sh "docker logs $CONTAINER_NAME || true"
        }
        always {
            echo "Cleaning up Docker environment..."
            sh '''
            docker rm -f $CONTAINER_NAME || true
            docker rmi $REGISTRY/$IMAGE_NAME:${TAG} || true
            docker system prune -f || true
            '''
            deleteDir()
        }
        success {
            echo " Build, tests, and push completed successfully for commit ${TAG}"
        }
    }
}
