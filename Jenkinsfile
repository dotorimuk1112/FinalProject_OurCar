node { 
    withCredentials([[$class: 'UsernamePasswordMultiBinding', 
        credentialsId: 'Docker-hub-credential', 
        usernameVariable: 'DOCKER_USER_ID', 
        passwordVariable: 'DOCKER_USER_PASSWORD']]) 
    
    { 
     stage('Pull') {
           git branch: 'master', credentialsId: 'Github-credential', url: 'https://github.com/dotorimuk1112/Final_Project.git'
        }
       

      stage('Build') {
            sh(script: '''yes | sudo docker image prune -a''') 
            sh(script: '''sudo docker build -f /var/lib/jenkins/workspace/OurCar_django/final_project/Dockerfile -t ourcar_test .''')
        }

      stage('Tag') {
              sh(script: '''sudo docker tag ourcar_test ${DOCKER_USER_ID}/ourcar_test:${BUILD_NUMBER}''') 
            }

      stage('Push') {
            sh(script: 'sudo docker login -u ${DOCKER_USER_ID} -p ${DOCKER_USER_PASSWORD}') 
            sh(script: 'sudo docker push ${DOCKER_USER_ID}/ourcar_test:${BUILD_NUMBER}') 
        }
      
      stage('Deploy') {
            sshagent(credentials: ['AWS_EC2_Ourcar_Server']) {
                sh(script: 'ssh -o StrictHostKeyChecking=no ubuntu@3.34.74.38 "sudo docker rm -f ourcar_test"')
                sh(script: 'ssh ubuntu@3.34.74.38 "sudo docker run --name ourcar_test -d -v /home/ubuntu/.env:/app/.env -v /home/ubuntu/ai_models:/app/final_project/ai_models -e TZ=Asia/Seoul -p 8000:8000 ${DOCKER_USER_ID}/ourcar_test:${BUILD_NUMBER}"')
        }
    }

    stage('Cleaning up') { 
              sh "sudo docker rmi ${DOCKER_USER_ID}/ourcar_test:${BUILD_NUMBER}" // sudo docker image 제거
      } 
    }
  }