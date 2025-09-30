pipeline {
    agent any
    environment {
        POSTGRESQL_DATABASE_URL = credentials('POSTGRESQL_DATABASE_URL') 
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/username/repo.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }
        stage('Run') {
            steps {
                sh 'docker compose up -d'
            }
        }
    }
}
