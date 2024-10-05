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
    }
}
