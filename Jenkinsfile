pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        sh '''cp /example/workspace /src
cp /example/config/config_create_problem.py /src
cp /example/config/config_stress.py /src
python3 /src/workspace/stress.py
python3 /src/workspace/config_stress.py'''
      }
    }

  }
}