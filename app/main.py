from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"game": "WordFace: AI Celebrity Quiz", "status": "Magic! Automated with Webhooks 3.0!"}