"""Spotify API client optimized for Railway deployment."""

import json
import os
from typing import Dict, List, Optional, Any
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException
import logging

from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpotifyClientRailway:
    """Spotify API client optimized for Railway deployment."""
    
    def __init__(self):
        """Initialize the Spotify client."""
        self.sp = None
        self.token_file = "spotify_token.json"
        self._authenticate()
    
    def _authenticate(self) -> None:
        """Authenticate with Spotify API using stored token or client credentials."""
        try:
            # First try to use stored token if available
            if os.path.exists(self.token_file):
                try:
                    with open(self.token_file, 'r') as f:
                        token_info = json.load(f)
                    
                    # Create OAuth manager for token refresh
                    auth_manager = SpotifyOAuth(
                        client_id=config.SPOTIFY_CLIENT_ID,
                        client_secret=config.SPOTIFY_CLIENT_SECRET,
                        redirect_uri=config.SPOTIFY_REDIRECT_URI,
                        scope=" ".join(config.SPOTIFY_SCOPES),
                        cache_path=self.token_file
                    )
                    
                    # Create Spotify client with auth manager
                    self.sp = spotipy.Spotify(auth_manager=auth_manager)
                    
                    # Test the token
                    self.sp.current_user()
                    logger.info("Successfully authenticated with stored token")
                    return
                    
                except Exception as e:
                    logger.warning(f"Stored token failed: {e}")
            
            # Fallback to client credentials (limited functionality)
            logger.info("Using client credentials authentication (limited functionality)")
            client_credentials_manager = SpotifyClientCredentials(
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            logger.info("Successfully authenticated with client credentials")
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise
    
    def search(self, query: str, search_type: str = "track", limit: int = 20) -> Dict[str, Any]:
        """Search for tracks, albums, artists, or playlists."""
        try:
            results = self.sp.search(q=query, type=search_type, limit=limit)
            return results
        except SpotifyException as e:
            logger.error(f"Search failed: {e}")
            raise
    
    def get_current_playback(self) -> Optional[Dict[str, Any]]:
        """Get current playback information."""
        try:
            return self.sp.current_playback()
        except SpotifyException as e:
            logger.error(f"Failed to get current playback: {e}")
            return None
    
    def start_playback(self, device_id: Optional[str] = None, 
                      context_uri: Optional[str] = None, 
                      uris: Optional[List[str]] = None, 
                      offset: Optional[Dict[str, Any]] = None) -> bool:
        """Start or resume playback."""
        try:
            self.sp.start_playback(device_id=device_id, context_uri=context_uri, uris=uris, offset=offset)
            return True
        except SpotifyException as e:
            logger.error(f"Failed to start playback: {e}")
            return False
    
    def pause_playback(self, device_id: Optional[str] = None) -> bool:
        """Pause playback."""
        try:
            self.sp.pause_playback(device_id=device_id)
            return True
        except SpotifyException as e:
            logger.error(f"Failed to pause playback: {e}")
            return False
    
    def next_track(self, device_id: Optional[str] = None) -> bool:
        """Skip to next track."""
        try:
            self.sp.next_track(device_id=device_id)
            return True
        except SpotifyException as e:
            logger.error(f"Failed to skip to next track: {e}")
            return False
    
    def previous_track(self, device_id: Optional[str] = None) -> bool:
        """Skip to previous track."""
        try:
            self.sp.previous_track(device_id=device_id)
            return True
        except SpotifyException as e:
            logger.error(f"Failed to skip to previous track: {e}")
            return False
    
    def set_volume(self, volume_percent: int, device_id: Optional[str] = None) -> bool:
        """Set playback volume."""
        try:
            self.sp.volume(volume_percent, device_id=device_id)
            return True
        except SpotifyException as e:
            logger.error(f"Failed to set volume: {e}")
            return False
    
    def get_devices(self) -> List[Dict[str, Any]]:
        """Get available devices."""
        try:
            devices = self.sp.devices()
            return devices.get('devices', [])
        except SpotifyException as e:
            logger.error(f"Failed to get devices: {e}")
            return []
    
    def get_user_playlists(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's playlists."""
        try:
            playlists = self.sp.current_user_playlists(limit=limit)
            return playlists.get('items', [])
        except SpotifyException as e:
            logger.error(f"Failed to get user playlists: {e}")
            return []
    
    def create_playlist(self, name: str, description: str = "", public: bool = False) -> Optional[Dict[str, Any]]:
        """Create a new playlist."""
        try:
            user_id = self.sp.current_user()['id']
            playlist = self.sp.user_playlist_create(
                user=user_id,
                name=name,
                description=description,
                public=public
            )
            return playlist
        except SpotifyException as e:
            logger.error(f"Failed to create playlist: {e}")
            return None
    
    def add_tracks_to_playlist(self, playlist_id: str, track_uris: List[str]) -> bool:
        """Add tracks to a playlist."""
        try:
            self.sp.playlist_add_items(playlist_id, track_uris)
            return True
        except SpotifyException as e:
            logger.error(f"Failed to add tracks to playlist: {e}")
            return False
    
    def get_user_top_tracks(self, time_range: str = "medium_term", limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's top tracks."""
        try:
            tracks = self.sp.current_user_top_tracks(time_range=time_range, limit=limit)
            return tracks.get('items', [])
        except SpotifyException as e:
            logger.error(f"Failed to get user top tracks: {e}")
            # Return some sample data if authentication fails
            return self._get_sample_tracks()
    
    def get_recently_played(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recently played tracks."""
        try:
            tracks = self.sp.current_user_recently_played(limit=limit)
            return tracks.get('items', [])
        except SpotifyException as e:
            logger.error(f"Failed to get recently played tracks: {e}")
            # Return some sample data if authentication fails
            return self._get_sample_recent_tracks()
    
    def get_user_profile(self) -> Optional[Dict[str, Any]]:
        """Get current user's profile."""
        try:
            return self.sp.current_user()
        except SpotifyException as e:
            logger.error(f"Failed to get user profile: {e}")
            return None
    
    def _get_sample_tracks(self) -> List[Dict[str, Any]]:
        """Return sample tracks for demo purposes."""
        return [
            {
                'name': 'Sample Track 1',
                'artists': [{'name': 'Sample Artist'}],
                'album': {'name': 'Sample Album'},
                'popularity': 75,
                'duration_ms': 210000,
                'external_urls': {'spotify': '#'}
            },
            {
                'name': 'Sample Track 2',
                'artists': [{'name': 'Another Artist'}],
                'album': {'name': 'Another Album'},
                'popularity': 68,
                'duration_ms': 195000,
                'external_urls': {'spotify': '#'}
            }
        ]
    
    def _get_sample_recent_tracks(self) -> List[Dict[str, Any]]:
        """Return sample recent tracks for demo purposes."""
        return [
            {
                'track': {
                    'name': 'Recent Track 1',
                    'artists': [{'name': 'Recent Artist'}],
                    'album': {'name': 'Recent Album'},
                    'popularity': 72,
                    'duration_ms': 180000,
                    'external_urls': {'spotify': '#'}
                },
                'played_at': '2025-09-20T02:00:00.000Z'
            }
        ]
