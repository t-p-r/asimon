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

        stage('Run tools (Windows)') {
            agent {
                label 'windows'
            }
            steps {
                bat 'git submodule update --init'
                bat 'xcopy example\\config\\* src'
                bat 'xcopy example\\workspace src\\workspace'
                bat 'python src/stress.py'
                bat 'python src/create_problem.py'
            }
        }

        stage('Run tools (Linux)') {
            agent {
                label 'linux'
            }
            steps {
                sh 'git submodule update --init'
                sh 'copy -r example\\config\\* src'
                sh 'copy -r example\\workspace src\\workspace'
                sh 'python src/stress.py'
                sh 'python src/create_problem.py'
            }
        }
    }
}
