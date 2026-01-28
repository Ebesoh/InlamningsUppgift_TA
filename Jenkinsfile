// Denna pipeline automatiserar webbtestning med Python, Selenium, Playwright och Pytest
// och genererar en detaljerad HTML-rapport som kan arkiveras i Jenkins
pipeline {
    agent any // Körs på alla tillgängliga Jenkins-agenter/exekutorer

    options {
        timestamps() // Lägger till tidsstämplar på alla rader i konsolutdata
    }

    environment {
        PYTHONUNBUFFERED = '1'            // Tvingar Python att skriva ut output direkt (ingen buffring)
        PLAYWRIGHT_BROWSERS_PATH = '0'    // Använder Playwrights standardplats för webbläsare
        PLAYWRIGHT_HEADLESS = '1'         // Kör webbläsare i headless-läge (krav i CI)
        REPORT_DIR = 'reports'             // Katalog för HTML-testrapporter
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
                REM Bekräftar att rätt Python-miljö används innan tester körs
                echo === Python detection ===
                where python
                python --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                REM Installerar och uppdaterar Python-beroenden
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

                REM Laddar ner Playwright-webbläsare (Chromium, Firefox, WebKit)
                echo === Installing Playwright browsers ===
                python -m playwright install
                '''
            }
        }

        stage('Run Tests & Generate HTML Report') {
            steps {
                bat '''
                echo === Running tests ===

                REM Skapar rapportkatalog om den inte redan finns
                if not exist %REPORT_DIR% mkdir %REPORT_DIR%

                REM Kör tester med extra detaljnivå:
                REM -v              : Visar varje test och dess resultat i konsolen
                REM --durations=10  : Visar de långsammaste testerna (bra för CI-analys)
                REM HTML-rapporten är självständig och enkel att dela

                python -m pytest ^
                    -v ^
                    --durations=10 ^
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
