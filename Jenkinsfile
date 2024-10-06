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

        stage('Run stress.py (Windows)') {
            agent {
                label 'windows'
            }
            steps {
                bat 'git submodule update --init'
                bat 'xcopy example\\config\\* src'
                bat 'xcopy example\\workspace src\\workspace'
                bat 'python src/stress.py'
            }
        }

        stage('Run create_problem.py (Windows)') {
            agent {
                label 'windows'
            }
            steps {
                bat 'git submodule update --init'
                bat 'xcopy example\\config\\* src'
                bat 'xcopy example\\workspace src\\workspace'
                bat 'python src/create_problem.py'
            }
        }
    }
}
