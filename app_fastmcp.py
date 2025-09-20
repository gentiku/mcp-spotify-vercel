#!/usr/bin/env python3
"""FastMCP-based Spotify MCP Server for Render deployment."""

import os
import logging
from typing import Any, Sequence
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from mcp.server.models import InitializationOptions
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
from pydantic import AnyUrl

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("Spotify MCP Server")

# Global Spotify client
spotify_client = None

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

@mcp.tool()
def spotify_get_user_top_tracks(limit: int = 10) -> dict:
    """Get user's top tracks from Spotify."""
    try:
        client = get_spotify_client()
        if not client:
            return {"error": "Spotify client not available"}
        
        tracks = client.get_user_top_tracks(limit=limit)
        formatted_tracks = []
        
        for i, track in enumerate(tracks, 1):
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
        logger.error(f"Error getting top tracks: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def spotify_get_recently_played(limit: int = 10) -> dict:
    """Get recently played tracks from Spotify."""
    try:
        client = get_spotify_client()
        if not client:
            return {"error": "Spotify client not available"}
        
        recent_tracks = client.get_recently_played(limit=limit)
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
        logger.error(f"Error getting recent tracks: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def spotify_search(query: str, search_type: str = "track", limit: int = 20) -> dict:
    """Search for tracks, albums, artists, or playlists on Spotify."""
    try:
        client = get_spotify_client()
        if not client:
            return {"error": "Spotify client not available"}
        
        results = client.search(query, search_type, limit)
        return {"success": True, "results": results}
    except Exception as e:
        logger.error(f"Error searching: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def spotify_get_user_profile() -> dict:
    """Get current user's Spotify profile."""
    try:
        client = get_spotify_client()
        if not client:
            return {"error": "Spotify client not available"}
        
        profile = client.get_user_profile()
        return {"success": True, "profile": profile}
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        return {"success": False, "error": str(e)}

# Create FastAPI app and mount MCP
app = FastAPI(title="Spotify MCP Server")
app.mount("/mcp", mcp.create_app())

# Add health check endpoint
@app.get("/")
def root():
    return {"status": "running", "message": "Spotify MCP Server with FastMCP"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
