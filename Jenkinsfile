pipeline {
    agent any

    stages {

	    stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/virpari/performance-monitoring.git'
            }
        }


		stage('Install Python Libraries') {
    		steps {
        		bat 'python -m pip install pandas numpy matplotlib'
    		}
		}

        stage('Run JMeter Test') {
            steps {
                bat 'jmeter -n -t Test_Executions.jmx -l current_results.jtl'
            }
        }

        stage('Compare Performance') {
            steps {
                bat 'python compare_runs.py baseline_results.jtl current_results.jtl'
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: '*.html, *.png, *.csv', fingerprint: true
            }
        }
    }
}
