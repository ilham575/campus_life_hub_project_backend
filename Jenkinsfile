pipeline {
    agent {
        docker {
            image 'docker:24.0.7-dind'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    environment {
        POSTGRESQL_DATABASE_URL = credentials('POSTGRESQL_DATABASE_URL')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm   // ใช้ของ declarative pipeline
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
