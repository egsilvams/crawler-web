pipeline {
    agent any

    environment {
        IMAGE_NAME = "crawler-web"
        CONTAINER_NAME = "crawler-web-container"
        PORT = "5000"  // Porta que o app Flask irá expor
    }

    stages {
        stage('Clonar Projeto') {
            steps {
                git 'https://github.com/egsilvams/crawler-web.git'
            }
        }

        stage('Build da Imagem Docker') {
            steps {
                sh "docker build -t $IMAGE_NAME ."
            }
        }

        stage('Parar e Remover Container Antigo') {
            steps {
                sh """
                if [ \$(docker ps -q -f name=$CONTAINER_NAME) ]; then
                    docker stop $CONTAINER_NAME
                fi
                if [ \$(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
                    docker rm $CONTAINER_NAME
                fi
                """
            }
        }

        stage('Remover Imagem Antiga (opcional)') {
            steps {
                sh "docker image prune -f"
            }
        }

        stage('Subir Novo Container') {
            steps {
                sh """
                docker run -d \
                  --name $CONTAINER_NAME \
                  -p $PORT:$PORT \
                  $IMAGE_NAME
                """
            }
        }
    }
}
