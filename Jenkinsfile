pipeline {
    agent { label 'Slave' }

    environment {
        IMAGE_NAME = "monitoring-system"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        REGISTRY = "docker.io/symmetramain/"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/cerform/domain_monitoring_devops.git'
            }
        }

        stage('Build temporary image') {
            steps {
                sh '''
                echo " Building temporary Docker image..."
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Run temporary container for tests') {
            steps {
                sh '''
                echo "Starting container for test execution..."
                docker run --rm -d --name test_container $IMAGE_NAME:$IMAGE_TAG tail -f /dev/null
                '''
            }
        }

        stage('Testing Suite') {
            steps {
                sh '''
                echo "Running Selenium & Pytest tests..."
                docker exec test_container pytest tests/ --maxfail=1 --disable-warnings -q || exit 1
                '''
            }
        }

        stage('Publish or Report') {
            steps {
                script {
                    try {
                        sh '''
                        echo "Tests passed. Pushing image to DockerHub..."
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker tag $IMAGE_NAME:$IMAGE_TAG $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
                        docker push $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
                        '''
                    } catch (err) {
                        echo "Tests failed. Creating failure report..."
                        sh 'echo "Build #${BUILD_NUMBER} failed" > failure_report.txt'
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                echo "Cleaning temporary resources..."
                docker rm -f test_container || true
                docker rmi $IMAGE_NAME:$IMAGE_TAG || true
                '''
            }
        }
    }

    post {
        success {
            echo "Build completed successfully"
        }
        failure {
            echo "Build failed — check failure_report.txt"
        }
    }
}
