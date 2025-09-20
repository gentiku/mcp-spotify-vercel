#!/usr/bin/env python3
"""FastAPI application for Spotify MCP Server on Vercel."""

import os
import json
import logging
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mcp_server import SpotifyMCPServer
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Spotify MCP Server",
    description="Model Context Protocol server for Spotify API integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global MCP server instance
mcp_server = None

class ToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any] = {}

class ToolCallResponse(BaseModel):
    success: bool
    result: Any = None
    error: str = None

@app.on_event("startup")
async def startup_event():
    """Initialize the MCP server on startup."""
    global mcp_server
    try:
        logger.info("Initializing Spotify MCP Server...")
        mcp_server = SpotifyMCPServer()
        logger.info("MCP Server initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize MCP server: {e}")

@app.get("/")
async def root():
    """Root endpoint with server information."""
    return {
        "name": config.MCP_SERVER_NAME,
        "version": config.MCP_SERVER_VERSION,
        "description": config.MCP_SERVER_DESCRIPTION,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "tools": "/tools",
            "call_tool": "/call_tool"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "server": config.MCP_SERVER_NAME,
        "version": config.MCP_SERVER_VERSION
    }

@app.get("/tools")
async def list_tools():
    """List all available MCP tools."""
    try:
        if mcp_server is None:
            raise HTTPException(status_code=500, detail="MCP server not initialized")
        
        # Get tools from the MCP server
        tools = []
        expected_tools = [
            'spotify_search', 'spotify_play', 'spotify_pause', 'spotify_resume',
            'spotify_skip_next', 'spotify_skip_previous', 'spotify_set_volume',
            'spotify_get_current_track', 'spotify_get_devices', 'spotify_get_user_playlists',
            'spotify_create_playlist', 'spotify_add_to_playlist', 'spotify_get_user_top_tracks',
            'spotify_get_recently_played', 'spotify_get_user_profile'
        ]
        
        for tool_name in expected_tools:
            tools.append({
                "name": tool_name,
                "description": f"Spotify {tool_name.replace('spotify_', '').replace('_', ' ')} functionality"
            })
        
        return {
            "tools": tools,
            "count": len(tools)
        }
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/call_tool", response_model=ToolCallResponse)
async def call_tool(request: ToolCallRequest):
    """Call an MCP tool with the given arguments."""
    try:
        if mcp_server is None:
            raise HTTPException(status_code=500, detail="MCP server not initialized")
        
        # Initialize Spotify client if needed
        if mcp_server.spotify_client is None:
            from spotify_client import SpotifyClient
            mcp_server.spotify_client = SpotifyClient()
        
        # Route to appropriate handler
        result = await mcp_server._handle_tool_call(request.name, request.arguments)
        
        return ToolCallResponse(
            success=True,
            result=result
        )
        
    except Exception as e:
        logger.error(f"Error calling tool {request.name}: {e}")
        return ToolCallResponse(
            success=False,
            error=str(e)
        )

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint."""
    return {
        "message": "Spotify MCP Server is running!",
        "status": "success",
        "server": config.MCP_SERVER_NAME
    }

# For Vercel deployment
def handler(request):
    """Vercel serverless function handler."""
    return app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
