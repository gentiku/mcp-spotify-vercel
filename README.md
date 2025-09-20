# Spotify MCP Server

A Model Context Protocol (MCP) server that provides seamless integration between applications and the Spotify API. This server enables Poke by Interaction and other MCP-compatible applications to control Spotify playback, search for music, and manage playlists through natural language commands.

## Features

- **🔐 Authentication**: OAuth2 flow for secure Spotify API access
- **🎵 Playback Control**: Play, pause, skip, seek, volume control
- **🔍 Search**: Find tracks, albums, artists, and playlists
- **📋 Playlist Management**: Create, modify, and manage playlists
- **👤 User Data**: Access user's top tracks, recently played, and profile
- **📱 Device Management**: Control playback on different devices
- **🎯 Smart Integration**: Natural language commands for music control

## Quick Start

### 1. Automated Setup
```bash
# Clone or download this project
cd poke

# Run the setup script
python setup.py
```

### 2. Manual Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Spotify API Setup**:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Note your Client ID and Client Secret
   - Set Redirect URI to `http://localhost:8888/callback`

3. **Configuration**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your Spotify credentials
   nano .env  # or use your preferred editor
   ```

4. **Test the Connection**:
   ```bash
   python test_connection.py
   ```

5. **Run the Server**:
   ```bash
   python main.py
   ```

## MCP Tools Available

### 🎵 Playback Control
- `spotify_play` - Start playback of a track or playlist
- `spotify_pause` - Pause current playback
- `spotify_resume` - Resume paused playback
- `spotify_skip_next` - Skip to next track
- `spotify_skip_previous` - Skip to previous track
- `spotify_set_volume` - Set playback volume (0-100%)

### 🔍 Search & Discovery
- `spotify_search` - Search for tracks, albums, artists, playlists
- `spotify_get_user_top_tracks` - Get user's top tracks
- `spotify_get_recently_played` - Get recently played tracks

### 📋 Playlist Management
- `spotify_get_user_playlists` - Get user's playlists
- `spotify_create_playlist` - Create a new playlist
- `spotify_add_to_playlist` - Add tracks to a playlist

### 📱 Device & Status
- `spotify_get_current_track` - Get currently playing track info
- `spotify_get_devices` - Get available Spotify devices
- `spotify_get_user_profile` - Get current user's profile

## Usage Examples

### With Poke by Interaction
Once integrated, you can use natural language commands like:
- "Play some jazz music"
- "Search for Taylor Swift songs"
- "Create a playlist called 'Workout Music'"
- "Skip to the next track"
- "Set volume to 50%"
- "Show me my top tracks from this month"

### Direct MCP Tool Calls
```json
{
  "name": "spotify_search",
  "arguments": {
    "query": "jazz",
    "search_type": "track",
    "limit": 10
  }
}
```

## Configuration

The server uses environment variables for configuration. Key settings in `.env`:

```env
# Required: Spotify API credentials
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

# Optional: Server configuration
MCP_SERVER_NAME=spotify-mcp-server
MCP_SERVER_VERSION=1.0.0
CACHE_TTL=3600
```

## Integration with Poke by Interaction

This MCP server is designed to work seamlessly with Poke by Interaction:

1. **Install the MCP server** following the setup instructions above
2. **Configure Poke by Interaction** to connect to this MCP server
3. **Use natural language** to control Spotify through Poke by Interaction

The server provides a comprehensive set of tools that enable Poke by Interaction to:
- Understand music-related queries
- Execute Spotify API operations
- Provide rich responses with track information
- Manage user's music library and playlists

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify your Spotify API credentials in `.env`
   - Ensure redirect URI matches your Spotify app settings
   - Check that your Spotify app has the required scopes

2. **No Devices Found**:
   - Make sure Spotify is open on at least one device
   - Check that the device is active and connected to the internet

3. **Permission Errors**:
   - Ensure your Spotify app has all required scopes enabled
   - Re-authenticate if you've changed scopes

### Debug Mode
Run with debug logging:
```bash
PYTHONPATH=. python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
import main
"
```

## Development

### Project Structure
```
poke/
├── main.py              # Main entry point
├── mcp_server.py        # MCP server implementation
├── spotify_client.py    # Spotify API client
├── config.py           # Configuration management
├── test_connection.py  # Test script
├── setup.py           # Setup script
├── requirements.txt   # Python dependencies
├── .env.example      # Environment variables template
└── README.md         # This file
```

### Adding New Tools
To add new Spotify functionality:

1. Add the tool definition in `mcp_server.py` `handle_list_tools()`
2. Implement the handler in `mcp_server.py` `handle_call_tool()`
3. Add the corresponding method in `spotify_client.py`
4. Update this README with the new tool documentation

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.
