import os
import sys
import requests

# נגדיר את הנתיב לקובץ ה-YAML שאנחנו רוצים לבדוק
yaml_file_path = "k8s/deployment.yaml"

# מוודאים שהקובץ בכלל קיים לפני שמתחילים
if not os.path.exists(yaml_file_path):
    print(f"Error: Could not find {yaml_file_path}")
    sys.exit(1)

# קוראים את התוכן של הקובץ
with open(yaml_file_path, 'r') as file:
    yaml_content = file.read()

# שולפים את מפתח ה-API ממשתני הסביבה של ג'נקינס (חוק ברזל: לא שומרים ססמאות בקוד!)
api_key = os.environ.get("OPENAI_API_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# הפרומפט שלנו - כאן אנחנו הופכים את המודל למומחה קוברנטיס
prompt = f"""
You are a Kubernetes and DevSecOps expert. 
Please review the following Kubernetes YAML file. 
Look for security risks, bad practices, or missing configurations (like missing resource limits, running as root, etc.).
If the file is completely fine and safe for production, output exactly: 'PASS'. 
If there are issues, output 'FAIL' followed by a short explanation of the problems.

YAML Content:
{yaml_content}
"""

payload = {
    "model": "gpt-4o-mini", # מודל מהיר וזול שמתאים למשימה
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.2 # טמפרטורה נמוכה כדי לקבל תשובות עקביות וטכניות ולא "יצירתיות" מדי
}

print("Sending YAML to AI for review...")
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
result = response.json()
ai_review = result['choices'][0]['message']['content']

print("\n--- AI Review Results ---")
print(ai_review)
print("-------------------------\n")

# החלק הכי חשוב לג'נקינס - קבלת ההחלטה
if "FAIL" in ai_review:
    print("AI found issues! Failing the pipeline.")
    sys.exit(1) # קוד יציאה 1 אומר לג'נקינס: "הייתה שגיאה, תעצור הכל ותצבע את הריצה באדום!"
else:
    print("AI approved the YAML. Proceeding with deployment...")
    sys.exit(0) # קוד יציאה 0 אומר לג'נקינס: "הכל תקין, תמשיך לשלב הבא"
