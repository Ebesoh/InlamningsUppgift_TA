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
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                bat '''
                where python
                python --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                python -m pip install --upgrade pip
                python -m pip install selenium pytest playwright pytest-playwright
                python -m playwright install
                pip install pytest pytest-cov requests
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat '''
                python -m pytest Del_2-Inloggningsfunktion/test_inloggningsfunktion_Selenium.py
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                bat '''
                python -m pytest Del_2-Inloggningsfunktion/test_inloggningsfunktion_playwright.py
                '''
            }
        }

        stage('Run Integration Tests') {
            steps {
                bat '''
                python -m pytest Del_3-Inloggningsfunktion/test_integrationstester.py
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
