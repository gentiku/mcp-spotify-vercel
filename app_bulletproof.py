import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Spotify MCP Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "running", "message": "Spotify MCP Server", "port": os.getenv("PORT")}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {"name": "spotify_get_user_top_tracks", "description": "Get user's top tracks"},
            {"name": "spotify_get_recently_played", "description": "Get recently played tracks"},
            {"name": "spotify_search", "description": "Search for tracks, albums, artists"}
        ],
        "count": 3
    }

@app.post("/call_tool")
def call_tool(request: dict):
    try:
        # Lazy import to avoid startup failures
        from spotify_client_railway import SpotifyClientRailway
        client = SpotifyClientRailway()
        
        tool_name = request.get("name")
        if tool_name == "spotify_get_user_top_tracks":
            result = client.get_user_top_tracks(limit=10)
            return {"success": True, "result": result}
        else:
            return {"success": False, "error": f"Tool {tool_name} not implemented"}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/top-songs")
def get_top_songs():
    try:
        from spotify_client_railway import SpotifyClientRailway
        client = SpotifyClientRailway()
        tracks = client.get_user_top_tracks(limit=10)
        return {"success": True, "tracks": tracks}
    except Exception as e:
        return {"success": False, "error": str(e)}
