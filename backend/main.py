from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "QuantEdge AI – PN Labs API Running 🚀"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "system": "QuantEdge AI",
        "version": "v1"
    }
