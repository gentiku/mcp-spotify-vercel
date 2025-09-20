"""Configuration management for the Spotify MCP Server."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Spotify MCP Server."""
    
    # Spotify API Configuration
    SPOTIFY_CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID", "")
    SPOTIFY_CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET", "")
    SPOTIFY_REDIRECT_URI: str = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")
    
    # MCP Server Configuration
    MCP_SERVER_NAME: str = os.getenv("MCP_SERVER_NAME", "spotify-mcp-server")
    MCP_SERVER_VERSION: str = os.getenv("MCP_SERVER_VERSION", "1.0.0")
    MCP_SERVER_DESCRIPTION: str = os.getenv("MCP_SERVER_DESCRIPTION", "Spotify API integration via MCP")
    
    # Cache Configuration
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Spotify API Scopes
    SPOTIFY_SCOPES: list = [
        "user-read-playback-state",
        "user-modify-playback-state",
        "user-read-currently-playing",
        "playlist-read-private",
        "playlist-modify-public",
        "playlist-modify-private",
        "user-top-read",
        "user-read-recently-played",
        "user-library-read",
        "user-library-modify"
    ]
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.SPOTIFY_CLIENT_ID:
            raise ValueError("SPOTIFY_CLIENT_ID is required")
        if not cls.SPOTIFY_CLIENT_SECRET:
            raise ValueError("SPOTIFY_CLIENT_SECRET is required")
        return True

# Global config instance
config = Config()
