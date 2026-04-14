pipeline {
    agent any 

    stages {
        stage('Install Dependencies') {
            steps {
                echo "Creating Python Virtual Environment and installing dependencies..."
                // צעד 1: יצירת הבועה - תיקייה חדשה בשם venv
                sh 'python3 -m venv venv'
                
                // צעד 2: התקנת הספריות בעזרת ה-pip שנמצא *בתוך* הבועה שלנו
                sh './venv/bin/pip install -r requirements.txt' 
            }
        }

        stage('AI Security & K8s Review') {
            steps {
                echo "Running AI Reviewer..."
                withCredentials([string(credentialsId: 'openai-api-key', variable: 'OPENAI_API_KEY')]) {
                    // צעד 3: הרצת הסקריפט בעזרת הפייתון שנמצא *בתוך* הבועה
                    sh './venv/bin/python ai_reviewer.py'
                }
            }
        }

        stage('Build & Push to AWS ECR') {
            steps {
                echo "AI approved the code! Proceeding to build the Docker image..."
            }
        }
    }
    
    post {
        failure {
            echo "Pipeline failed! The AI found issues. Sending alert to Slack..."
        }
        success {
            echo "Pipeline succeeded! Ready for CD to deploy to Kubernetes..."
        }
    }
}