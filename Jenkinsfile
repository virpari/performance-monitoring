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
                bat 'python compare_runs.py baseline_results.jtl current_results.jtl'
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

        always {
            cleanWs()
        }
    }
}
