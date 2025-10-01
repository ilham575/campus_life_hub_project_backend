pipeline {
    agent {
        docker {
            image 'docker/compose:1.29.2'
            args '-v /var/run/docker.sock:/var/run/docker.sock -u root'
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
                sh 'docker-compose -f docker-compose.yml build'
            }
        }
        stage('Run') {
            steps {
                sh 'docker-compose -f docker-compose.yml up -d'
            }
        }
    }
}
