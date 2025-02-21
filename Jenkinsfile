pipeline {
    agent none

    stages {
        stage('Validate') {
            agent any
            steps {
                script {
                    if (!fileExists('example/config/config_stress.py')) {
                        error 'File example/config/config_stress.py does not exist'
                    }
                    if (!fileExists('example/config/config_create_problem.py')) {
                        error 'File example/config/config_create_problem.py does not exist'
                    }
                    if (!fileExists('example/workspace/checker.cpp')) {
                        error 'File example/workspace/checker.cpp does not exist'
                    }
                    if (!fileExists('example/workspace/contestant.cpp')) {
                        error 'File example/workspace/contestant.cpp does not exist'
                    }
                    if (!fileExists('example/workspace/judge.cpp')) {
                        error 'File example/workspace/judge.cpp does not exist'
                    }
                    if (!fileExists('example/workspace/testgen_testlib.cpp')) {
                        error 'File example/workspace/testgen_testlib.cpp does not exist'
                    }
                    if (!fileExists('example/workspace/testgen.cpp')) {
                        error 'File example/workspace/testgen.cpp does not exist'
                    }
                }
            }
        }

        stage('Run sample test (Windows)') {
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

        stage('Run sample test (Linux)') {
            agent {
                label 'linux'
            }
            steps {
                sh 'git submodule update --init'
                sh 'cp example/config/* src'
                sh 'cp -r example/workspace src'
                sh 'python src/stress.py'
                sh 'python src/create_problem.py'
            }
        }
    }
}
