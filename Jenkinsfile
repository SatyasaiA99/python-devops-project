pipeline {
    agent any

    environment {
        APP_NAME = "python-devops-app"
        IMAGE_NAME = "satyasaia99/python-devops-app"
        IMAGE_TAG = "v1"

        SONARQUBE_ENV = "sq"
        NEXUS_URL = "http://YOUR_NEXUS_IP:8081"
        NEXUS_REPO = "python-repo"
        NEXUS_USER = "admin"
        NEXUS_PASS = "admin123"
    }

    stages {

        /* ---------------- CHECKOUT ---------------- */
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/SatyasaiA99/python-devops-project.git'
            }
        }

        /* ---------------- INSTALL DEPENDENCIES ---------------- */
        stage('Install Dependencies') {
            steps {
                sh '''
                python3 --version
                pip3 install -r requirements.txt
                '''
            }
        }

        /* ---------------- SONARQUBE ANALYSIS ---------------- */
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh '''
                    /opt/sonar-scanner/bin/sonar-scanner \
                    -Dsonar.projectKey=python-devops \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=$SONAR_HOST_URL \
                    -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        /* ---------------- QUALITY GATE ---------------- */
        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        /* ---------------- BUILD DOCKER IMAGE ---------------- */
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        /* ---------------- PUSH TO DOCKER HUB ---------------- */
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'Dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh """
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }
        /* ---------------- UPLOAD TO NEXUS ---------------- */
        stage('Upload to Nexus') {
            steps {
                sh """
                echo "Uploading artifact to Nexus..."

                zip -r app.zip .

                curl -u ${NEXUS_USER}:${NEXUS_PASS} \
                --upload-file app.zip \
                ${NEXUS_URL}/repository/${NEXUS_REPO}/app-${IMAGE_TAG}.zip
                """
            }
        }

        /* ---------------- RUN CONTAINER ---------------- */
        stage('Run Container') {
            steps {
                sh '''
                docker stop python-app || true
                docker rm python-app || true
                docker run -d -p 5000:5000 --name python-app ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        /* ---------------- VERIFY ---------------- */
        stage('Verify') {
            steps {
                sh '''
                sleep 5
                curl http://localhost:5000
                '''
            }
        }
    }

    post {
        success {
            echo "🚀 Pipeline Success"
        }
        failure {
            echo "❌ Pipeline Failed"
        }
    }
}
