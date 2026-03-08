pipeline {
    agent any

    environment {
        JMETER_HOME = "D:\\apache-jmeter-5.6.3"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/virpari/performance-monitoring.git'
            }
        }

        stage('Verify Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run JMeter Test') {
            steps {
                bat "\"%JMETER_HOME%\\bin\\jmeter.bat\" -n -t Test_Executions.jmx -l current_results.jtl"
            }
        }

        stage('Compare Performance') {
            steps {
                bat 'if exist baseline_results.jtl (python compare_runs.py baseline_results.jtl current_results.jtl)'
            }
        }

        stage('Update Baseline') {
            steps {
                bat 'copy current_results.jtl baseline_results.jtl /Y'
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML([
                    reportDir: '.',
                    reportFiles: 'performance_report.html',
                    reportName: 'Performance Report'
                ])
            }
        }
        stage('Performance Trend Graph') {
    steps {
        plot csvFileName: 'p99_trend.csv',
             group: 'Performance Trends',
             title: 'P99 Response Time Trend'
                }
            }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: '*.html, *.png, *.csv, *.jtl', fingerprint: true
            }
        }
    }

    post {

        success {
            echo 'Performance Test Passed ✅'
        }

        failure {
            echo 'Performance Regression Detected ❌'
        }

    }
}
