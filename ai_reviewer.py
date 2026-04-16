import os
import requests
import sys

# נתיב לקובץ ה-YAML שנרצה לבדוק
yaml_file_path = 'k8s/deployment.yaml'

# קריאת תוכן הקובץ
if not os.path.exists(yaml_file_path):
    print(f"Error: {yaml_file_path} not found.")
    sys.exit(1)

with open(yaml_file_path, 'r') as file:
    yaml_content = file.read()

# משיכת ה-API Key ממשתני הסביבה (מוגדר בג'נקינס)
api_key = os.environ.get('OPENAI_API_KEY')

if not api_key:
    print("Error: OPENAI_API_KEY not set.")
    sys.exit(1)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# ההנחיה המעודכנת ל-AI - דורשת אבטחה בסיסית אך מאפשרת PASS אם הכל תקין
prompt = (
    f"You are a DevOps Security Expert. Review this Kubernetes YAML for security best practices.\n"
    f"1. If it has runAsNonRoot, limits/requests, and no critical errors, output ONLY the word 'PASS'.\n"
    f"2. If there is a critical security risk (like running as root), output 'FAIL:' followed by a short explanation.\n"
    f"Keep it simple and don't be overly strict about NetworkPolicies for now.\n\n"
    f"YAML Content:\n{yaml_content}"
)

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are a helpful DevOps assistant."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.2
}

print("Sending YAML to AI for review...")

try:
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    
    result = response.json()['choices'][0]['message']['content'].strip()
    
    print("\n--- AI Review Results ---")
    print(result)
    print("-------------------------\n")

    if "PASS" in result.upper():
        print("AI approved the YAML. Proceeding with deployment...")
        sys.exit(0)
    else:
        print("AI found issues! Failing the pipeline.")
        sys.exit(1)

except Exception as e:
    print(f"Error communicating with OpenAI: {e}")
    sys.exit(1)