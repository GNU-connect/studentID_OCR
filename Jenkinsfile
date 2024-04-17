node {
    git branch: 'main', poll: true, url: 'https://github.com/GNU-connect/studentID_OCR.git'

    withCredentials([
        [$class: 'UsernamePasswordMultiBinding',
         credentialsId: 'docker-hub-flask',
         usernameVariable: 'DOCKER_USER_ID', 
         passwordVariable: 'DOCKER_USER_PASSWORD']
    ]) {
        stage('Pull') {
            git branch: 'main', url: 'https://github.com/GNU-connect/studentID_OCR.git' 
        }

        stage('Unit Test') {
            // Add unit tests if needed
        }

        stage('Build') {
            sh(script: 'docker-compose build backend_flask_server')
        }

        stage('Tag') {
            sh(script: '''
                docker tag dongho18/connect-gnu-flask \
                ${DOCKER_USER_ID}/connect-gnu-flask:${BUILD_NUMBER}
            ''')
        }

        stage('Push') {
            sh(script: 'docker login -u ${DOCKER_USER_ID} -p ${DOCKER_USER_PASSWORD}') 
            sh(script: 'docker push ${DOCKER_USER_ID}/connect-gnu-flask:${BUILD_NUMBER}') 
            sh(script: 'docker push ${DOCKER_USER_ID}/connect-gnu-flask:latest')
        }

        stage('Deploy') {
            sh(script: 'docker-compose down')
            sh(script: 'docker-compose up -d')
        }
    } 
}
