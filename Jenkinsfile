node {
    def startTime = System.currentTimeMillis()

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

        stage('Post Slack') {
            slackSend(channel: '#build-notification', color: 'warning', message: "Build started: ${env.JOB_NAME} build ${env.BUILD_NUMBER}")
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
    }

    post {
        always {
            def endTime = System.currentTimeMillis()
            def duration = (endTime - startTime) / 1000
            def durationStr = String.format("%d min, %d sec", duration / 60, duration % 60)
        }

        success {
            slackSend(channel: '#build-notification', color: 'good', message: "Deployment succeeded: ${env.JOB_NAME} build ${env.BUILD_NUMBER} in ${durationStr}")
        }
        failure {
            script {
                def failedStage = currentBuild.rawBuild.getLog(10).find { it.contains('Stage') }
                slackSend(channel: '#build-notification', color: 'danger', message: "Deployment failed: ${env.JOB_NAME} build ${env.BUILD_NUMBER} in ${durationStr}\nFailure reason: ${currentBuild.description ?: 'Unknown reason'}\nFailed stage: ${failedStage}")
            }
        }
    }
}
