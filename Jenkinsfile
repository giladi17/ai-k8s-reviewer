pipeline {
    // מגדיר לג'נקינס שהוא יכול להריץ את ה-Pipeline על כל שרת (Agent) פנוי שיש לו
    agent any 

    stages {
        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                // ג'נקינס מריץ את הפקודה הזו בטרמינל שלו כדי להתקין את הספריות
                sh 'pip3 install -r requirements.txt' 
            }
        }

        stage('AI Security & K8s Review') {
            steps {
                echo "Running AI Reviewer..."
                
                // כאן קורה הקסם של האבטחה:
                // אנחנו שולפים את הסוד מתוך הכספת של ג'נקינס (Credentials)
                // ומזריקים אותו כמשתנה סביבה אך ורק לזמן הריצה של הבלוק הזה
                withCredentials([string(credentialsId: 'openai-api-key', variable: 'OPENAI_API_KEY')]) {
                    sh 'python3 ai_reviewer.py'
                }
            }
        }

        // השלב הזה ירוץ *אך ורק* אם השלב של ה-AI עבר בהצלחה!
        stage('Build & Push to AWS ECR') {
            steps {
                echo "AI approved the code! Proceeding to build the Docker image..."
                // כאן בהמשך נוסיף את הפקודות של Docker build ודחיפה ל-ECR
            }
        }
    }
    
    // מה קורה בסוף הריצה? (תמיד קורה, בלי קשר להצלחה או כישלון)
    post {
        failure {
            echo "Pipeline failed! The AI found issues. Sending alert to Slack..."
        }
        success {
            echo "Pipeline succeeded! Ready for CD to deploy to Kubernetes..."
        }
    }
}