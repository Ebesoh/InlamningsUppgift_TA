// Denna pipeline automatiserar webbtestning med Python, Selenium, Playwright och Pytest med HTML-rapportering
pipeline {
    agent any // Körs på alla tillgängliga Jenkins-agenter/exekutorer

    options {
        timestamps() // Lägger till tidsstämplar på alla rader i konsolutdata
    }

    environment {
        PYTHONUNBUFFERED = '1'            // Tvingar Python att skriva ut output omedelbart (ingen buffring)
        PLAYWRIGHT_BROWSERS_PATH = '0'    // Lagrar Playwright-webbläsare på standardplatsen
        PLAYWRIGHT_HEADLESS = '1'         // Kör webbläsare i headless-läge (utan grafiskt gränssnitt)
        REPORT_DIR = 'reports'             // Mappnamn för att lagra testrapporter
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm // Hämtar källkoden från versionshanteringssystemet (SCM)
            }
        }

        stage('Verify Environment') {
            steps {
                bat '''
                REM Felsökning – bekräftar korrekt Python-miljö innan tester körs
                echo === Python detection ===
                where python
                python --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                REM Installerar Python-beroenden
                echo === Installing Python dependencies ===
                python -m pip install --upgrade pip

                REM Installerar test- och automationsbibliotek
                python -m pip install ^
                    selenium ^
                    pytest ^
                    pytest-cov ^
                    pytest-html ^
                    playwright ^
                    pytest-playwright ^
                    requests

                REM Installerar Playwright-webbläsare
                echo === Installing Playwright browsers ===
                python -m playwright install
                '''
            }
        }

        stage('Run Tests & Generate HTML Report') {
            steps {
                bat '''
                echo === Running tests ===

                REM Skapar rapportkatalog om den inte finns
                if not exist %REPORT_DIR% mkdir %REPORT_DIR%

                REM Kör pytest och genererar HTML-rapport
                REM --self-contained-html inkluderar CSS/JS i samma fil

                python -m pytest ^
                    --html=%REPORT_DIR%\\report.html ^
                    --self-contained-html ^
                    Del_2-Inloggningsfunktion ^
                    Del_3-Integrationstester
                '''
            }
        }
    }

    post {
        always {
            echo '=== Archiving reports ==='
            archiveArtifacts artifacts: 'reports/*.html',
                             fingerprint: true
        }

        success {
            echo 'CI PIPELINE SUCCESS: All tests passed'
        }

        failure {
            echo 'CI PIPELINE FAILURE: One or more tests failed'
        }
    }
}
