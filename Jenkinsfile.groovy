pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        PYTHONUNBUFFERED = '1'
        PLAYWRIGHT_BROWSERS_PATH = '0'
        PLAYWRIGHT_HEADLESS = '1'
        REPORT_DIR = 'reports'
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
                python -m pip install \
                    selenium \
                    pytest \
                    pytest-cov \
                    pytest-html \
                    playwright \
                    pytest-playwright \
                    requests

                python -m playwright install
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                if not exist %REPORT_DIR% mkdir %REPORT_DIR%

                python -m pytest ^
                  --html=%REPORT_DIR%\\report.html ^
                  --self-contained-html ^
                  Del_2-Inloggningsfunktion ^
                  Del_3-Integrationstester
                '''
            }
        }

        stage('Generate PDF Report') {
            steps {
                bat '''
                wkhtmltopdf ^
                  %REPORT_DIR%\\report.html ^
                  %REPORT_DIR%\\test-report.pdf
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/*.pdf', fingerprint: true
            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
            echo 'Reports archived'
        }

        success {
            echo 'CI PIPELINE SUCCESS'
        }

        failure {
            echo 'CI PIPELINE FAILURE'
        }
    }
}
