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
                    // Get current commit ID
                    def tag = sh(script: "git rev-parse HEAD", returnStdout: true).trim()
                    echo "Commit ID: ${tag}"

                    // Use safe build number
                    def buildNum = (env.BUILD_NUMBER ?: "0").toInteger()
                    def shortTag = tag.take(8)
                    VERSION_TAG = "build-${buildNum}-${shortTag}"
                    echo "Build version: ${VERSION_TAG}"

                    env.VERSION_TAG = VERSION_TAG
                    env.TAG = shortTag
                }
            }
        }

        stage('Build Docker Image (temp)') {
            steps {
                echo "Building Docker image: ${REGISTRY}/${IMAGE_NAME}:${TAG}"
                sh """
                docker build -t $REGISTRY/$IMAGE_NAME:${TAG} .
                """
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
                    echo "Promoting image version..."

                    // Get current latest version tag
                    def currentVersion = sh(
                        script: "git tag --sort=-v:refname | grep -Eo 'v[0-9]+\\.[0-9]+\\.[0-9]+' | head -n1 || echo 'v0.0.0'",
                        returnStdout: true
                    ).trim()

                    echo "Current version: ${currentVersion}"

                    // Parse safely
                    def parts = currentVersion.replace('v', '').tokenize('.')
                    def major = parts.size() > 0 ? parts[0].toInteger() : 0
                    def minor = parts.size() > 1 ? parts[1].toInteger() : 0
                    def patch = parts.size() > 2 ? parts[2].toInteger() : 0
                    def newVersion = "v${major}.${minor}.${patch + 1}"
                    echo "New version: ${newVersion}"

                    // Push Docker image securely
                    withDockerRegistry([credentialsId: 'dockerhub-creds', url: 'https://index.docker.io/v1/']) {
                        sh """
                        docker tag $REGISTRY/$IMAGE_NAME:${TAG} $REGISTRY/$IMAGE_NAME:${newVersion}
                        docker tag $REGISTRY/$IMAGE_NAME:${TAG} $REGISTRY/$IMAGE_NAME:latest
                        docker push $REGISTRY/$IMAGE_NAME:${newVersion}
                        docker push $REGISTRY/$IMAGE_NAME:latest
                        """
                    }

                    // Push Git tag securely to GitHub
                    withCredentials([usernamePassword(credentialsId: 'github-token',
                                                     usernameVariable: 'GIT_USER',
                                                     passwordVariable: 'GIT_TOKEN')]) {
                        sh """
                        git config --global user.email "jenkins@ci.local"
                        git config --global user.name "Jenkins CI"
                        git tag -a ${newVersion} -m 'Release ${newVersion}'
                        git push https://${GIT_USER}:${GIT_TOKEN}@github.com/cerform/domain_monitoring_devops.git ${newVersion}
                        """
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "Tests failed. Displaying container logs..."
            sh "docker logs $CONTAINER_NAME || true"
        }
        always {
            echo "Cleaning up environment..."
            sh '''
            docker rm -f $CONTAINER_NAME || true
            docker rmi $REGISTRY/$IMAGE_NAME:${TAG} || true
            docker system prune -af --volumes || true
            '''
            deleteDir()
        }
    }
}
