// Denna pipeline automatiserar webbtestning med Python, Selenium, Playwright och Pytest
// och genererar en tydlig, detaljerad HTML-rapport med testnamn, status och loggar
pipeline {
    agent any // Körs på alla tillgängliga Jenkins-agenter/exekutorer

    options {
        timestamps() // Lägger till tidsstämplar på alla rader i konsolutdata
    }

    environment {
        PYTHONUNBUFFERED = '1'            // Omedelbar Python-output (ingen buffring)
        PLAYWRIGHT_BROWSERS_PATH = '0'    // Standardplats för Playwright-webbläsare
        PLAYWRIGHT_HEADLESS = '1'         // Headless-läge (krävs i CI)
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

                REM Laddar ner Playwright-webbläsare
                echo === Installing Playwright browsers ===
                python -m playwright install
                '''
            }
        }

        stage('Run Tests & Generate Detailed HTML Report') {
            steps {
                bat '''
                echo === Running tests ===

                REM Skapar rapportkatalog om den inte finns
                if not exist %REPORT_DIR% mkdir %REPORT_DIR%

                REM Testkörning med hög synlighet:
                REM -v                   : Visar varje test i Jenkins-loggen
                REM --durations=10       : Visar långsamma tester
                REM --capture=tee-sys    : Loggar per test inkluderas i HTML-rapporten
                REM HTML-rapporten innehåller testnamn, status och detaljer

                python -m pytest ^
                    -v ^
                    --durations=10 ^
                    --capture=tee-sys ^
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
            echo '=== Archiving HTML report ==='
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
