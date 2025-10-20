pipeline{
    agent any
    environment{
        VENV_DIR='venv'
    }

    stages{
        stage('cloning github repo to jenkins') {
            steps {
                script{
                    echo 'cloning github repo to jenkins'
                    
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token1', url: 'https://github.com/aorontryintomakeitinlife/mlops-hotelreservation.git']])
                }
            }
        }
        stage('setting up our virtual enviroment and installing dependencies') {
            steps {
                script{
                    echo 'cloning github repo to jenkins''setting up our virtual enviroment and installing dependencies'
                    sh '''
                    python -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/activated
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}