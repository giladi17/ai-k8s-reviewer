# 1. תמונת הבסיס - אנחנו לוקחים לינוקס רזה עם פייתון מותקן עליו
FROM python:3.10-slim

# 2. הגדרת תיקיית העבודה בתוך הקונטיינר
WORKDIR /app

# 3. העתקת קובץ הדרישות והתקנתן (עושים את זה קודם כדי לנצל את ה-Cache של דוקר)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. העתקת שאר קוד האפליקציה פנימה
COPY app/ .

# 5. חשיפת הפורט שעליו השרת ירוץ
EXPOSE 8000

# 6. הפקודה שתרוץ כשהקונטיינר נדלק
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]