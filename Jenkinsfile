pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/cerform/domain_monitoring_devops.git', branch: 'main'
            }
        }
        stage('Build') {
            steps {
                echo "✅ Build triggered by webhook!"
            }
        }
    }
}
