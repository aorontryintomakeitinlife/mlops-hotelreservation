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
                    echo 'cloning github repo to jenkins and setting up virtual environment'

                    sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    '''
                }
            }
        }
    }
}