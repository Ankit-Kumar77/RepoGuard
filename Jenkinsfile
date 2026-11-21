
pipeline {
    agent any

    stages {

        stage('Environment Check') {
            steps {
                echo 'Checking build environment...'

                bat 'git --version'

                bat '"C:\\Users\\WINDOWS\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing project dependencies...'

                bat '"C:\\Users\\WINDOWS\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Tests') {
            steps {
                echo 'Running RepoGuard tests...'

                bat '"C:\\Users\\WINDOWS\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pytest tests -v'
            }
        }

        stage('Repository Scan') {
            steps {
                script {
                    env.SCAN_OUTPUT = bat(
                        script: '''
                            @echo off
                            "C:\\Users\\WINDOWS\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -c "from repoguard.scanner import scan_repository; result=scan_repository('.'); print('QUALITY_SCORE=' + str(result['score']))"
                        ''',
                        returnStdout: true
                    ).trim()

                    echo env.SCAN_OUTPUT
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    def matcher = env.SCAN_OUTPUT =~ /QUALITY_SCORE=(\d+)/

                    if (matcher.find()) {
                        def qualityScore = matcher.group(1).toInteger()

                        echo "RepoGuard Quality Score: ${qualityScore}/100"

                        if (qualityScore >= 80) {
                            echo 'QUALITY GATE PASSED'
                        } else {
                            error("QUALITY GATE FAILED: Score ${qualityScore} is below 80")
                        }

                    } else {
                        error('Could not extract quality score from RepoGuard output')
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'RepoGuard CI completed successfully.'
        }

        failure {
            echo 'RepoGuard CI failed.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
