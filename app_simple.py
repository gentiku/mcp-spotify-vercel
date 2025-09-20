#!/usr/bin/env python3
"""Simplified FastAPI application for Railway deployment."""

import os
import logging
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Global Spotify client
spotify_client = None

class ToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any] = {}

class ToolCallResponse(BaseModel):
    success: bool
    result: Any = None
    error: str = None

def get_spotify_client():
    """Get or create Spotify client."""
    global spotify_client
    if spotify_client is None:
        try:
            from spotify_client_railway import SpotifyClientRailway
            spotify_client = SpotifyClientRailway()
            logger.info("Spotify client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Spotify client: {e}")
            spotify_client = None
    return spotify_client

@app.get("/")
async def root():
    """Root endpoint with server information."""
    return {
        "name": "spotify-mcp-server",
        "version": "1.0.0",
        "description": "Spotify API integration via MCP",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "tools": "/tools",
            "call_tool": "/call_tool",
            "dashboard": "/dashboard",
            "top-songs": "/top-songs",
            "recent-songs": "/recent-songs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "server": "spotify-mcp-server",
        "version": "1.0.0",
        "timestamp": "2025-09-20T04:20:00Z"
    }

@app.get("/tools")
async def list_tools():
    """List all available MCP tools."""
    tools = [
        {"name": "spotify_search", "description": "Search for tracks, albums, artists"},
        {"name": "spotify_play", "description": "Start playback"},
        {"name": "spotify_pause", "description": "Pause playback"},
        {"name": "spotify_resume", "description": "Resume playback"},
        {"name": "spotify_skip_next", "description": "Skip to next track"},
        {"name": "spotify_skip_previous", "description": "Skip to previous track"},
        {"name": "spotify_set_volume", "description": "Set playback volume"},
        {"name": "spotify_get_current_track", "description": "Get current track"},
        {"name": "spotify_get_devices", "description": "Get available devices"},
        {"name": "spotify_get_user_playlists", "description": "Get user playlists"},
        {"name": "spotify_create_playlist", "description": "Create new playlist"},
        {"name": "spotify_add_to_playlist", "description": "Add tracks to playlist"},
        {"name": "spotify_get_user_top_tracks", "description": "Get user's top tracks"},
        {"name": "spotify_get_recently_played", "description": "Get recently played tracks"},
        {"name": "spotify_get_user_profile", "description": "Get user profile"}
    ]
    
    return {
        "tools": tools,
        "count": len(tools)
    }

@app.post("/call_tool", response_model=ToolCallResponse)
async def call_tool(request: ToolCallRequest):
    """Call an MCP tool with the given arguments."""
    try:
        client = get_spotify_client()
        if client is None:
            return ToolCallResponse(
                success=False,
                error="Spotify client not available"
            )
        
        # Route to appropriate handler based on tool name
        if request.name == "spotify_get_user_top_tracks":
            limit = request.arguments.get("limit", 10)
            result = client.get_user_top_tracks(limit=limit)
        elif request.name == "spotify_get_recently_played":
            limit = request.arguments.get("limit", 10)
            result = client.get_recently_played(limit=limit)
        elif request.name == "spotify_search":
            query = request.arguments.get("query", "")
            search_type = request.arguments.get("type", "track")
            limit = request.arguments.get("limit", 20)
            result = client.search(query, search_type, limit)
        elif request.name == "spotify_get_user_profile":
            result = client.get_user_profile()
        else:
            return ToolCallResponse(
                success=False,
                error=f"Tool {request.name} not implemented"
            )
        
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

@app.get("/top-songs")
async def get_top_songs():
    """Get user's top songs."""
    try:
        client = get_spotify_client()
        if client is None:
            raise HTTPException(status_code=500, detail="Spotify client not available")
        
        top_tracks = client.get_user_top_tracks(limit=10)
        
        formatted_tracks = []
        for i, track in enumerate(top_tracks, 1):
            formatted_tracks.append({
                "rank": i,
                "name": track.get('name', 'Unknown'),
                "artists": [artist['name'] for artist in track.get('artists', [])],
                "album": track.get('album', {}).get('name', 'Unknown Album'),
                "popularity": track.get('popularity', 0),
                "duration_ms": track.get('duration_ms', 0),
                "external_urls": track.get('external_urls', {})
            })
        
        return {
            "success": True,
            "tracks": formatted_tracks,
            "count": len(formatted_tracks)
        }
        
    except Exception as e:
        logger.error(f"Error getting top songs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recent-songs")
async def get_recent_songs():
    """Get user's recently played songs."""
    try:
        client = get_spotify_client()
        if client is None:
            raise HTTPException(status_code=500, detail="Spotify client not available")
        
        recent_tracks = client.get_recently_played(limit=10)
        
        formatted_tracks = []
        for i, item in enumerate(recent_tracks, 1):
            track = item.get('track', {})
            formatted_tracks.append({
                "rank": i,
                "name": track.get('name', 'Unknown'),
                "artists": [artist['name'] for artist in track.get('artists', [])],
                "album": track.get('album', {}).get('name', 'Unknown Album'),
                "played_at": item.get('played_at', 'Unknown time'),
                "popularity": track.get('popularity', 0),
                "duration_ms": track.get('duration_ms', 0),
                "external_urls": track.get('external_urls', {})
            })
        
        return {
            "success": True,
            "tracks": formatted_tracks,
            "count": len(formatted_tracks)
        }
        
    except Exception as e:
        logger.error(f"Error getting recent songs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Simple HTML dashboard to display top songs."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎧 Spotify Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #1DB954, #191414);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .header h1 {
                font-size: 3em;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            .section {
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
                backdrop-filter: blur(10px);
            }
            .section h2 {
                color: #1DB954;
                border-bottom: 2px solid #1DB954;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }
            .track {
                background: rgba(255,255,255,0.05);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                border-left: 4px solid #1DB954;
            }
            .track-name {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .track-info {
                color: #ccc;
                font-size: 0.9em;
            }
            .loading {
                text-align: center;
                font-size: 1.2em;
                color: #1DB954;
            }
            .error {
                background: rgba(255,0,0,0.2);
                border-left-color: #ff4444;
                color: #ffcccc;
            }
            .refresh-btn {
                background: #1DB954;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1em;
                margin: 10px;
            }
            .refresh-btn:hover {
                background: #1ed760;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎧 Your Spotify Dashboard</h1>
                <button class="refresh-btn" onclick="loadData()">🔄 Refresh</button>
            </div>
            
            <div class="section">
                <h2>🏆 Your Top 10 Songs</h2>
                <div id="top-songs" class="loading">Loading your top songs...</div>
            </div>
            
            <div class="section">
                <h2>🕒 Recently Played</h2>
                <div id="recent-songs" class="loading">Loading recent songs...</div>
            </div>
        </div>
        
        <script>
            function formatDuration(ms) {
                const minutes = Math.floor(ms / 60000);
                const seconds = Math.floor((ms % 60000) / 1000);
                return `${minutes}:${seconds.toString().padStart(2, '0')}`;
            }
            
            function renderTracks(tracks, containerId, showPlayedAt = false) {
                const container = document.getElementById(containerId);
                if (!tracks || tracks.length === 0) {
                    container.innerHTML = '<div class="track error">No tracks found</div>';
                    return;
                }
                
                container.innerHTML = tracks.map(track => `
                    <div class="track">
                        <div class="track-name">
                            ${track.rank}. ${track.name}
                        </div>
                        <div class="track-info">
                            👤 ${track.artists.join(', ')} | 
                            💿 ${track.album} | 
                            ⏱️ ${formatDuration(track.duration_ms)} | 
                            📊 ${track.popularity}/100
                            ${showPlayedAt && track.played_at ? `<br>🕒 ${new Date(track.played_at).toLocaleString()}` : ''}
                        </div>
                    </div>
                `).join('');
            }
            
            async function loadTopSongs() {
                try {
                    const response = await fetch('/top-songs');
                    const data = await response.json();
                    if (data.success) {
                        renderTracks(data.tracks, 'top-songs');
                    } else {
                        document.getElementById('top-songs').innerHTML = '<div class="track error">Failed to load top songs</div>';
                    }
                } catch (error) {
                    document.getElementById('top-songs').innerHTML = '<div class="track error">Error loading top songs: ' + error.message + '</div>';
                }
            }
            
            async function loadRecentSongs() {
                try {
                    const response = await fetch('/recent-songs');
                    const data = await response.json();
                    if (data.success) {
                        renderTracks(data.tracks, 'recent-songs', true);
                    } else {
                        document.getElementById('recent-songs').innerHTML = '<div class="track error">Failed to load recent songs</div>';
                    }
                } catch (error) {
                    document.getElementById('recent-songs').innerHTML = '<div class="track error">Error loading recent songs: ' + error.message + '</div>';
                }
            }
            
            function loadData() {
                loadTopSongs();
                loadRecentSongs();
            }
            
            // Load data when page loads
            loadData();
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
