from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from Face Recognition API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API funcionando correctamente"}

@app.post("/recognize/")
async def recognize_face():
    # Mock response for testing
    return {
        "recognized": True,
        "user": {
            "id": "test-123",
            "name": "Test User",
            "unique_code": "TEST001",
            "requested": False
        },
        "confidence": 0.95,
        "distance": 0.05,
        "alert_triggered": False
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 