"""MCP Server implementation for Spotify API integration."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Sequence
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

from spotify_client import SpotifyClient
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpotifyMCPServer:
    """MCP Server for Spotify API integration."""
    
    def __init__(self):
        """Initialize the MCP server."""
        self.server = Server(config.MCP_SERVER_NAME)
        self.spotify_client = None
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available Spotify tools."""
            return [
                Tool(
                    name="spotify_search",
                    description="Search for tracks, albums, artists, or playlists on Spotify",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "search_type": {
                                "type": "string",
                                "enum": ["track", "album", "artist", "playlist"],
                                "description": "Type of content to search for",
                                "default": "track"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of results to return",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="spotify_play",
                    description="Start or resume Spotify playback",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_uri": {
                                "type": "string",
                                "description": "Spotify URI of the track to play (optional)"
                            },
                            "playlist_uri": {
                                "type": "string",
                                "description": "Spotify URI of the playlist to play (optional)"
                            },
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to play on (optional)"
                            }
                        }
                    }
                ),
                Tool(
                    name="spotify_pause",
                    description="Pause Spotify playback",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to pause on (optional)"
                            }
                        }
                    }
                ),
                Tool(
                    name="spotify_resume",
                    description="Resume paused Spotify playback",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to resume on (optional)"
                            }
                        }
                    }
                ),
                Tool(
                    name="spotify_skip_next",
                    description="Skip to the next track",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to skip on (optional)"
                            }
                        }
                    }
                ),
                Tool(
                    name="spotify_skip_previous",
                    description="Skip to the previous track",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to skip on (optional)"
                            }
                        }
                    }
                ),
                Tool(
                    name="spotify_set_volume",
                    description="Set Spotify playback volume",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "volume": {
                                "type": "integer",
                                "description": "Volume percentage (0-100)",
                                "minimum": 0,
                                "maximum": 100
                            },
                            "device_id": {
                                "type": "string",
                                "description": "Device ID to set volume on (optional)"
                            }
                        },
                        "required": ["volume"]
                    }
                ),
                Tool(
                    name="spotify_get_current_track",
                    description="Get information about the currently playing track",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="spotify_get_devices",
                    description="Get available Spotify devices",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="spotify_get_user_playlists",
                    description="Get user's playlists",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of playlists to return",
                                "default": 50,
                                "minimum": 1,
                                "maximum": 50
                            }
                        }
                    }
                ),
                Tool(
                    name="spotify_create_playlist",
                    description="Create a new playlist",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Playlist name"
                            },
                            "description": {
                                "type": "string",
                                "description": "Playlist description",
                                "default": ""
                            },
                            "public": {
                                "type": "boolean",
                                "description": "Whether the playlist should be public",
                                "default": False
                            }
                        },
                        "required": ["name"]
                    }
                ),
                Tool(
                    name="spotify_add_to_playlist",
                    description="Add tracks to a playlist",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "playlist_id": {
                                "type": "string",
                                "description": "Spotify playlist ID"
                            },
                            "track_uris": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of Spotify track URIs to add"
                            }
                        },
                        "required": ["playlist_id", "track_uris"]
                    }
                ),
                Tool(
                    name="spotify_get_user_top_tracks",
                    description="Get user's top tracks",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "time_range": {
                                "type": "string",
                                "enum": ["short_term", "medium_term", "long_term"],
                                "description": "Time range for top tracks",
                                "default": "medium_term"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of tracks to return",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50
                            }
                        }
                    }
                ),
                Tool(
                    name="spotify_get_recently_played",
                    description="Get recently played tracks",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of tracks to return",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 50
                            }
                        }
                    }
                ),
                Tool(
                    name="spotify_get_user_profile",
                    description="Get current user's profile information",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls."""
            try:
                # Initialize Spotify client if not already done
                if self.spotify_client is None:
                    self.spotify_client = SpotifyClient()
                
                # Route to appropriate handler
                if name == "spotify_search":
                    return await self._handle_search(arguments)
                elif name == "spotify_play":
                    return await self._handle_play(arguments)
                elif name == "spotify_pause":
                    return await self._handle_pause(arguments)
                elif name == "spotify_resume":
                    return await self._handle_resume(arguments)
                elif name == "spotify_skip_next":
                    return await self._handle_skip_next(arguments)
                elif name == "spotify_skip_previous":
                    return await self._handle_skip_previous(arguments)
                elif name == "spotify_set_volume":
                    return await self._handle_set_volume(arguments)
                elif name == "spotify_get_current_track":
                    return await self._handle_get_current_track(arguments)
                elif name == "spotify_get_devices":
                    return await self._handle_get_devices(arguments)
                elif name == "spotify_get_user_playlists":
                    return await self._handle_get_user_playlists(arguments)
                elif name == "spotify_create_playlist":
                    return await self._handle_create_playlist(arguments)
                elif name == "spotify_add_to_playlist":
                    return await self._handle_add_to_playlist(arguments)
                elif name == "spotify_get_user_top_tracks":
                    return await self._handle_get_user_top_tracks(arguments)
                elif name == "spotify_get_recently_played":
                    return await self._handle_get_recently_played(arguments)
                elif name == "spotify_get_user_profile":
                    return await self._handle_get_user_profile(arguments)
                else:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Unknown tool: {name}")]
                    )
            
            except Exception as e:
                logger.error(f"Error handling tool call {name}: {e}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")]
                )
    
    async def _handle_search(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle search tool call."""
        query = arguments.get("query", "")
        search_type = arguments.get("search_type", "track")
        limit = arguments.get("limit", 20)
        
        results = self.spotify_client.search(query, search_type, limit)
        
        # Format results for display
        formatted_results = self._format_search_results(results, search_type)
        
        return CallToolResult(
            content=[TextContent(type="text", text=formatted_results)]
        )
    
    async def _handle_play(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle play tool call."""
        track_uri = arguments.get("track_uri")
        playlist_uri = arguments.get("playlist_uri")
        device_id = arguments.get("device_id")
        
        if track_uri:
            success = self.spotify_client.start_playback(device_id=device_id, uris=[track_uri])
            message = f"Playing track: {track_uri}" if success else "Failed to play track"
        elif playlist_uri:
            success = self.spotify_client.start_playback(device_id=device_id, context_uri=playlist_uri)
            message = f"Playing playlist: {playlist_uri}" if success else "Failed to play playlist"
        else:
            success = self.spotify_client.start_playback(device_id=device_id)
            message = "Resumed playback" if success else "Failed to resume playback"
        
        return CallToolResult(
            content=[TextContent(type="text", text=message)]
        )
    
    async def _handle_pause(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle pause tool call."""
        device_id = arguments.get("device_id")
        success = self.spotify_client.pause_playback(device_id=device_id)
        message = "Playback paused" if success else "Failed to pause playback"
        
        return CallToolResult(
            content=[TextContent(type="text", text=message)]
        )
    
    async def _handle_resume(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle resume tool call."""
        device_id = arguments.get("device_id")
        success = self.spotify_client.start_playback(device_id=device_id)
        message = "Playback resumed" if success else "Failed to resume playback"
        
        return CallToolResult(
            content=[TextContent(type="text", text=message)]
        )
    
    async def _handle_skip_next(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle skip next tool call."""
        device_id = arguments.get("device_id")
        success = self.spotify_client.next_track(device_id=device_id)
        message = "Skipped to next track" if success else "Failed to skip to next track"
        
        return CallToolResult(
            content=[TextContent(type="text", text=message)]
        )
    
    async def _handle_skip_previous(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle skip previous tool call."""
        device_id = arguments.get("device_id")
        success = self.spotify_client.previous_track(device_id=device_id)
        message = "Skipped to previous track" if success else "Failed to skip to previous track"
        
        return CallToolResult(
            content=[TextContent(type="text", text=message)]
        )
    
    async def _handle_set_volume(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle set volume tool call."""
        volume = arguments.get("volume", 50)
        device_id = arguments.get("device_id")
        success = self.spotify_client.set_volume(volume, device_id=device_id)
        message = f"Volume set to {volume}%" if success else "Failed to set volume"
        
        return CallToolResult(
            content=[TextContent(type="text", text=message)]
        )
    
    async def _handle_get_current_track(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get current track tool call."""
        playback = self.spotify_client.get_current_playback()
        
        if not playback or not playback.get('item'):
            return CallToolResult(
                content=[TextContent(type="text", text="No track currently playing")]
            )
        
        track = playback['item']
        track_info = f"Currently playing: {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"
        
        return CallToolResult(
            content=[TextContent(type="text", text=track_info)]
        )
    
    async def _handle_get_devices(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get devices tool call."""
        devices = self.spotify_client.get_devices()
        
        if not devices:
            return CallToolResult(
                content=[TextContent(type="text", text="No devices found")]
            )
        
        device_list = "\n".join([
            f"- {device['name']} ({device['type']}) - {'Active' if device['is_active'] else 'Inactive'}"
            for device in devices
        ])
        
        return CallToolResult(
            content=[TextContent(type="text", text=f"Available devices:\n{device_list}")]
        )
    
    async def _handle_get_user_playlists(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get user playlists tool call."""
        limit = arguments.get("limit", 50)
        playlists = self.spotify_client.get_user_playlists(limit=limit)
        
        if not playlists:
            return CallToolResult(
                content=[TextContent(type="text", text="No playlists found")]
            )
        
        playlist_list = "\n".join([
            f"- {playlist['name']} ({playlist['tracks']['total']} tracks)"
            for playlist in playlists
        ])
        
        return CallToolResult(
            content=[TextContent(type="text", text=f"Your playlists:\n{playlist_list}")]
        )
    
    async def _handle_create_playlist(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle create playlist tool call."""
        name = arguments.get("name", "")
        description = arguments.get("description", "")
        public = arguments.get("public", False)
        
        playlist = self.spotify_client.create_playlist(name, description, public)
        
        if playlist:
            message = f"Created playlist: {playlist['name']} (ID: {playlist['id']})"
        else:
            message = "Failed to create playlist"
        
        return CallToolResult(
            content=[TextContent(type="text", text=message)]
        )
    
    async def _handle_add_to_playlist(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle add to playlist tool call."""
        playlist_id = arguments.get("playlist_id", "")
        track_uris = arguments.get("track_uris", [])
        
        success = self.spotify_client.add_tracks_to_playlist(playlist_id, track_uris)
        message = f"Added {len(track_uris)} tracks to playlist" if success else "Failed to add tracks to playlist"
        
        return CallToolResult(
            content=[TextContent(type="text", text=message)]
        )
    
    async def _handle_get_user_top_tracks(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get user top tracks tool call."""
        time_range = arguments.get("time_range", "medium_term")
        limit = arguments.get("limit", 20)
        
        tracks = self.spotify_client.get_user_top_tracks(time_range, limit)
        
        if not tracks:
            return CallToolResult(
                content=[TextContent(type="text", text="No top tracks found")]
            )
        
        track_list = "\n".join([
            f"- {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"
            for track in tracks
        ])
        
        return CallToolResult(
            content=[TextContent(type="text", text=f"Your top tracks ({time_range}):\n{track_list}")]
        )
    
    async def _handle_get_recently_played(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get recently played tool call."""
        limit = arguments.get("limit", 20)
        tracks = self.spotify_client.get_recently_played(limit)
        
        if not tracks:
            return CallToolResult(
                content=[TextContent(type="text", text="No recently played tracks found")]
            )
        
        track_list = "\n".join([
            f"- {track['track']['name']} by {', '.join([artist['name'] for artist in track['track']['artists']])}"
            for track in tracks
        ])
        
        return CallToolResult(
            content=[TextContent(type="text", text=f"Recently played tracks:\n{track_list}")]
        )
    
    async def _handle_get_user_profile(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get user profile tool call."""
        profile = self.spotify_client.get_user_profile()
        
        if not profile:
            return CallToolResult(
                content=[TextContent(type="text", text="Failed to get user profile")]
            )
        
        profile_info = f"User: {profile['display_name']}\nFollowers: {profile['followers']['total']}\nCountry: {profile['country']}"
        
        return CallToolResult(
            content=[TextContent(type="text", text=profile_info)]
        )
    
    async def _handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Handle tool calls for HTTP API."""
        try:
            # Initialize Spotify client if not already done
            if self.spotify_client is None:
                self.spotify_client = SpotifyClient()
            
            # Route to appropriate handler
            if name == "spotify_search":
                return await self._handle_search(arguments)
            elif name == "spotify_play":
                return await self._handle_play(arguments)
            elif name == "spotify_pause":
                return await self._handle_pause(arguments)
            elif name == "spotify_resume":
                return await self._handle_resume(arguments)
            elif name == "spotify_skip_next":
                return await self._handle_skip_next(arguments)
            elif name == "spotify_skip_previous":
                return await self._handle_skip_previous(arguments)
            elif name == "spotify_set_volume":
                return await self._handle_set_volume(arguments)
            elif name == "spotify_get_current_track":
                return await self._handle_get_current_track(arguments)
            elif name == "spotify_get_devices":
                return await self._handle_get_devices(arguments)
            elif name == "spotify_get_user_playlists":
                return await self._handle_get_user_playlists(arguments)
            elif name == "spotify_create_playlist":
                return await self._handle_create_playlist(arguments)
            elif name == "spotify_add_to_playlist":
                return await self._handle_add_to_playlist(arguments)
            elif name == "spotify_get_user_top_tracks":
                return await self._handle_get_user_top_tracks(arguments)
            elif name == "spotify_get_recently_played":
                return await self._handle_get_recently_played(arguments)
            elif name == "spotify_get_user_profile":
                return await self._handle_get_user_profile(arguments)
            else:
                return {"error": f"Unknown tool: {name}"}
        
        except Exception as e:
            logger.error(f"Error handling tool call {name}: {e}")
            return {"error": str(e)}

    def _format_search_results(self, results: Dict[str, Any], search_type: str) -> str:
        """Format search results for display."""
        if search_type == "track":
            items = results.get('tracks', {}).get('items', [])
            if not items:
                return "No tracks found"
            
            track_list = "\n".join([
                f"- {track['name']} by {', '.join([artist['name'] for artist in track['artists']])} (Album: {track['album']['name']})"
                for track in items
            ])
            return f"Found {len(items)} tracks:\n{track_list}"
        
        elif search_type == "album":
            items = results.get('albums', {}).get('items', [])
            if not items:
                return "No albums found"
            
            album_list = "\n".join([
                f"- {album['name']} by {', '.join([artist['name'] for artist in album['artists']])} ({album['total_tracks']} tracks)"
                for album in items
            ])
            return f"Found {len(items)} albums:\n{album_list}"
        
        elif search_type == "artist":
            items = results.get('artists', {}).get('items', [])
            if not items:
                return "No artists found"
            
            artist_list = "\n".join([
                f"- {artist['name']} ({artist['followers']['total']} followers)"
                for artist in items
            ])
            return f"Found {len(items)} artists:\n{artist_list}"
        
        elif search_type == "playlist":
            items = results.get('playlists', {}).get('items', [])
            if not items:
                return "No playlists found"
            
            playlist_list = "\n".join([
                f"- {playlist['name']} by {playlist['owner']['display_name']} ({playlist['tracks']['total']} tracks)"
                for playlist in items
            ])
            return f"Found {len(items)} playlists:\n{playlist_list}"
        
        return "Invalid search type"
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=config.MCP_SERVER_NAME,
                    server_version=config.MCP_SERVER_VERSION,
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )
