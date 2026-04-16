from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"game": "WordFace: AI Celebrity Quiz", "status": "Backend is running securely!", "version": "1.0"}