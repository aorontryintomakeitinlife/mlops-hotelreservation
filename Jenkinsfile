pipeline {
    agent any
    environment {
        VENV_DIR="venv"
        GCP_PROJECT="heroic-overview-474512-s9"
        GCLOUD_PATH="/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {
        stage('Cloning GitHub repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token1',
                            url: 'https://github.com/aorontryintomakeitinlife/mlops-hotelreservation.git'
                        ]]
                    )
                }
            }
        }

        stage('Setup virtual environment and install dependencies') {
            steps {
                script {
                    echo 'Setting up virtual environment and installing dependencies'
                    sh '''
                        python3 -m venv ${VENV_DIR}
                        ${VENV_DIR}/bin/pip install --upgrade pip
                        ${VENV_DIR}/bin/pip install -e .
                    '''
                }
            }
        }

        stage('Build and push Docker image to GCR') {
            steps {
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and pushing Docker image to GCR'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT}/ml_project_latest .
                            docker push gcr.io/${GCP_PROJECT}/ml_project_latest
                        '''
                    }
                }
            }
        }
    }
}
