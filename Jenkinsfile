pipeline{
    agent any
    environment{
        VENV_DIR='venv'
        GCP_PROJECT= "heroic-overview-474512-s9"
        GCLOUD_PATH= "/var/jenkins_home/google-cloud-sdk/bin"
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
                    python -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -e .
                    '''
                }
            }
        }
        stage('building and pushing docker image to gcr') {
            steps {
                withCredentials([file(credentialsId:'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'building and pushing docker image to gcr...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure --quiet 
                        
                        docker build -t gcr.io/$(GCP_PROJECT)/ml_project_latest .
                        docker push gcr.io/$(GCP_PROJECT)/ml_project_latest
                        '''
                    }
                        }
                    }
            }
        }
    }
}