node {
    git branch: 'main', poll: true, url: 'https://github.com/GNU-connect/studentID_OCR.git'

    withCredentials([
        [$class: 'UsernamePasswordMultiBinding',
         credentialsId: 'docker-hub-flask',
         usernameVariable: 'DOCKER_USER_ID', 
         passwordVariable: 'DOCKER_USER_PASSWORD']
    ]) {
        try {
            stage('Pull') {
                git branch: 'main', url: 'https://github.com/GNU-connect/studentID_OCR.git' 
            }

            stage('Post Slack') {
                slackSend(channel: '#build-notification', color: 'warning', message: "빌드 시작: 지누가 ${env.JOB_NAME} 서버 ${env.BUILD_NUMBER} 버전을 열심히 빌드중이야!")
            }

            stage('Unit Test') {
                //sh 'pytest -e PYTEST_DEBUG=true'
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
                sh(script: 'docker-compose up -d backend_flask_server')
            }

            stage('Post Slack') {
                slackSend(channel: '#build-notification', color: 'good', message: "빌드 성공: 야호! ${env.JOB_NAME} 서버 ${env.BUILD_NUMBER} 버전이 성공적으로 배포되었어!")
            }
        } catch (Exception e) {
            slackSend(channel: '#build-notification', color: 'danger', message: "빌드 실패: 이런... ${env.JOB_NAME} 서버 ${env.BUILD_NUMBER} 버전 빌드에 실패했어 ㅜㅜ\n사유: ${e.getMessage()}")
            throw e
        }   
    }
}
