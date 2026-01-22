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
                echo === Python detection ===
                where python
                python --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                echo === Installing Python dependencies ===
                python -m pip install --upgrade pip

                python -m pip install ^
                    selenium ^
                    pytest ^
                    pytest-cov ^
                    pytest-html ^
                    playwright ^
                    pytest-playwright ^
                    requests

                echo === Installing Playwright browsers ===
                python -m playwright install
                '''
            }
        }

        stage('Run Tests & Generate HTML Report') {
            steps {
                bat '''
                echo === Running tests ===

                if not exist %REPORT_DIR% mkdir %REPORT_DIR%

                python -m pytest ^
                    --html=%REPORT_DIR%\\report.html ^
                    --self-contained-html ^
                    Del_2-Inloggningsfunktion ^
                    Del_3-Integrationstester
                '''
            }
        }

        stage('Generate PDF Report (optional)') {
            steps {
                bat '''
                echo === Attempting PDF generation ===

                where wkhtmltopdf || (
                    echo wkhtmltopdf not installed - skipping PDF generation
                    exit /b 0
                )

                wkhtmltopdf ^
                    %REPORT_DIR%\\report.html ^
                    %REPORT_DIR%\\test-report.pdf
                '''
            }
        }
    }

    post {
        always {
            echo '=== Archiving reports ==='
            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
            archiveArtifacts artifacts: 'reports/*.pdf', fingerprint: true
        }

        success {
            echo 'CI PIPELINE SUCCESS: All tests passed'
        }

        failure {
            echo 'CI PIPELINE FAILURE: One or more tests failed'
        }
    }
}
