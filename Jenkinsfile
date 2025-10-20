pipeline{
    agent any

    stages{
        stage('cloning github repo to jenkins') {
            steps {
                script{
                    echo 'cloning github repo to jenkins'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token1', url: 'https://github.com/aorontryintomakeitinlife/mlops-hotelreservation.git']])
                }
            }
        }
    }
}