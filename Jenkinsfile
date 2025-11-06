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

        stage('On Push → Get Latest Commit ID') {
    steps {
        script {
            TAG = sh(
                script: "git ls-remote ${REPO_URL} refs/heads/main | cut -f1 | tr -d '\\n' | tr -d '\\r'",
                returnStdout: true
            ).trim()

            if (!TAG?.trim()) {
                error("Commit ID not found — cannot continue build.")
            }
            echo "🆕 Latest commit ID: '${TAG}'"
                }
            }
        }

        stage('Checkout Source Code') {
            steps {
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image (temp)') {
            steps {
                echo "Building temporary Docker image with tag ${TAG}"
                sh "docker build -t $REGISTRY/$IMAGE_NAME:${TAG} ."
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
                    // Get latest semantic version (vX.Y.Z)
                    def currentVersion = sh(
                        script: "git tag --sort=-v:refname | grep -Eo 'v[0-9]+\\.[0-9]+\\.[0-9]+' | head -n1 || echo 'v0.0.0'",
                        returnStdout: true
                    ).trim()

                    echo "Current version: ${currentVersion}"

                    // Bump patch version
                    def (major, minor, patch) = currentVersion.replace('v','').tokenize('.')
                    def newVersion = "v${major}.${minor}.${patch.toInteger() + 1}"
                    echo "Promoting image version to ${newVersion}"

                    // Push new version to DockerHub
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker tag $REGISTRY/$IMAGE_NAME:${TAG} $DOCKER_USER/$IMAGE_NAME:${newVersion}
                        docker tag $REGISTRY/$IMAGE_NAME:${TAG} $DOCKER_USER/$IMAGE_NAME:latest
                        docker push $DOCKER_USER/$IMAGE_NAME:${newVersion}
                        docker push $DOCKER_USER/$IMAGE_NAME:latest
                        """
                    }

                    // Tag release in GitHub
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
    }
}
