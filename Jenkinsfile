pipeline {
    agent none

    stages {
        stage('Validate') {
            agent any
            steps {
                script {
                    def files = [
                        'example/config/config_stress.py',
                        'example/config/config_create_problem.py',
                        'example/workspace/checker.cpp',
                        'example/workspace/contestant.cpp',
                        'example/workspace/judge.cpp',
                        'example/workspace/testgen_testlib.cpp',
                        'example/workspace/testgen.cpp'
                    ]

                    for (file in files) {
                        if (!fileExists(file)) {
                            error "File ${file} does not exist"
                        }
                    }
                }
            }
        }

        stage('Run sample test (Windows)') {
            agent any
            steps {
                script {
                    if (unix()) {
                        sh 'git submodule update --init'
                        sh 'cp example/config/* src'
                        sh 'cp -r example/workspace src'
                        sh 'python src/stress.py'
                        sh 'python src/create_problem.py'
                } else {
                        bat 'git submodule update --init'
                        bat 'xcopy example\\config\\* src'
                        bat 'xcopy example\\workspace src\\workspace'
                        bat 'python src/stress.py'
                        bat 'python src/create_problem.py'
                    }
                }
            }
        }
    }
}
