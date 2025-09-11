
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials') 
        DOCKER_IMAGE = "abhiyadav260/text-to-voice"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YadavAbhishek03/text-to-voice.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE:latest .'
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                script {
                    sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    sh 'docker push $DOCKER_IMAGE:latest'
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    // Stop old container (if running)
                    sh 'docker rm -f text-to-voice || true'
                    
                    // Run new container
                    sh 'docker run -d -p 5000:5000 --name text-to-voice $DOCKER_IMAGE:latest'
                }
            }
        }
    }
}
