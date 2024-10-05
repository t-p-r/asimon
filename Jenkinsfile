pipeline {
    agent any
    stages {
        stage('Validate') {
            steps {
                fileExists 'example/config/config_stress.py'
                fileExists 'example/config/config_create_problem.py'
            }
        }
    }
}
