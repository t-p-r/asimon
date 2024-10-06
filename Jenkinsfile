pipeline {
    agent any

    stages {
        stage('Validate') {
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
            steps {
                bat script: 'set'
                fileOperations([
                    folderCopyOperation(sourceFolderPath: 'example/workspace', destinationFolderPath: 'src')
                ])
                fileOperations([
                    fileCopyOperation(includes: 'example/config/*', targetLocation: 'src')
                ])
            }
        }

        stage('Run stress.py (Windows)') {
            steps {
                bat encoding: 'utf-8', returnStdout: true, script: "${env.PY} src/stress.py"
            }
        }

        stage('Run create_problem.py (Windows)') {
            steps {
                bat encoding: 'utf-8', returnStdout: true, script: "${env.PY} src/create_problem.py"
            }
        }
    }
}
