#!/usr/bin/env python3
"""Minimal FastAPI application for Railway deployment."""

import os
import logging
from fastapi import FastAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Spotify MCP Server")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "status": "running",
        "message": "Spotify MCP Server is alive!",
        "port": os.environ.get("PORT", "8000")
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"ping": "pong"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
