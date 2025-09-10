pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = credentials('dockerhub-credentials')   // Jenkins credential ID
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/YadavAbhishek03/text-to-voice.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("text-to-voice")
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKERHUB_CREDENTIALS}") {
                        docker.image("text-to-voice").push("latest")
                    }
                }
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f text-to-voice || true
                docker run -d --name text-to-voice -p 5000:5000 text-to-voice:latest
                '''
            }
        }
    }
}

