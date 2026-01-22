pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        PYTHONUNBUFFERED = '1'
        PLAYWRIGHT_BROWSERS_PATH = '0'
        PLAYWRIGHT_HEADLESS = '1'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code'
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                bat '''
                python --version
                pip --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                pip install --upgrade pip
                pip install selenium pytest playwright pytest-playwright
                python -m playwright install
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat '''
                pytest Del_2-Inloggningsfunktion/test_inloggningsfunktion_Selenium.py
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                bat '''
                pytest Del_2-Inloggningsfunktion/test_inloggningsfunktion_playwright.py
                '''
            }
        }
    }

    post {
        success {
            echo 'CI PIPELINE SUCCESS: All tests passed'
        }
        failure {
            echo 'CI PIPELINE FAILURE: One or more tests failed'
        }
        always {
            echo 'CI run completed'
        }
    }
}
