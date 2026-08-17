pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out EssayIQ source code...'
            }
        }

        stage('Install Backend Dependencies') {
            steps {
                bat '''
                    cd backend
                    python -m pip install -r requirements.txt
                    python -m pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    cd backend
                    python -m pytest
                '''
            }
        }

        stage('Build Frontend') {
            steps {
                bat '''
                    cd frontend
                    npm install
                    npm run build
                '''
            }
        }
    }

    post {
        success {
            echo 'EssayIQ CI Pipeline completed successfully!'
        }

        failure {
            echo 'EssayIQ CI Pipeline failed!'
        }
    }
}