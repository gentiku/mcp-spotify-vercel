import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "port": os.getenv("PORT", "unknown")}

@app.get("/health")
def health_check():
    return {"status": "ok"}
