pipeline {
    agent any 

    environment {
        // האזור שבו נמצא ה-ECR שלך
        AWS_DEFAULT_REGION = 'us-east-1' 
        
        // הכתובת של המחסן שיצרת באמזון
        ECR_REGISTRY = '066380525112.dkr.ecr.us-east-1.amazonaws.com' 
        
        // שם ה-Repository
        ECR_REPOSITORY = 'wordface-api'
        IMAGE_TAG = '1.0'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo "Creating Python Virtual Environment and installing dependencies..."
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt' 
            }
        }

        stage('AI Security & K8s Review') {
            steps {
                echo "Running AI Reviewer..."
                withCredentials([string(credentialsId: 'openai-api-key', variable: 'OPENAI_API_KEY')]) {
                    sh './venv/bin/python ai_reviewer.py'
                }
            }
        }

        stage('Build & Push to AWS ECR') {
            steps {
                echo "AI approved the code! Proceeding to build the Docker image..."
                
                // שימוש בפלאגין הייעודי של AWS שקורא ישירות את הסוד שיצרת
                withAWS(credentials: 'aws-creds', region: "${AWS_DEFAULT_REGION}") {
                    sh '''
                        # 1. Login to AWS ECR
                        aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        
                        # 2. Build the Docker Image
                        docker build -t ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} .
                        
                        # 3. Push the Image to ECR
                        docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                    '''
                }
            }
        }
    }
    
    post {
        failure {
            echo "Pipeline failed! Sending alert to Slack..."
        }
        success {
            echo "Pipeline succeeded! Image pushed to ECR."
        }
    }
}