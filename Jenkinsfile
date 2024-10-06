pipeline {
    agent none

    stages {
        stage('Validate') {
            agent any
            steps {
                fileExists 'example/config/config_stress.py'
                fileExists 'example/config/config_create_problem.py'
                fileExists 'example/workspace/checker.cpp'
                fileExists 'example/workspace/contestant.cpp'
                fileExists 'example/workspace/judge.cpp'
                fileExists 'example/workspace/testgen_testlib.cpp'
                fileExists 'example/workspace/testgen.cpp'
            }
        }

        stage('Prepare files') {
            agent any
            steps {
                bat returnStdout: true, script = 'xcopy example\\config\\* src'
                bat returnStdout: true, script = 'xcopy example\\workspace src\\workspace'
            }
        }

        stage('Run stress.py (Windows)') {
            agent {
                label 'windows'
            }
            steps {
                bat encoding: 'utf-8', returnStdout: true, script: 'python src/stress.py'
            }
        }

        stage('Run create_problem.py (Windows)') {
            agent {
                label 'windows'
            }
            steps {
                bat encoding: 'utf-8', returnStdout: true, script: 'python src/create_problem.py'
            }
        }
    }
}
