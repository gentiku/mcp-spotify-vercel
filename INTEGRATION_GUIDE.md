# Poke by Interaction Integration Guide

This guide explains how to integrate the Spotify MCP Server with Poke by Interaction.

## Prerequisites

1. **Spotify MCP Server** - Follow the setup instructions in README.md
2. **Poke by Interaction** - Ensure you have Poke by Interaction installed and configured
3. **Spotify Account** - Active Spotify Premium account (required for playback control)

## Integration Steps

### 1. Configure MCP Server

First, ensure your Spotify MCP Server is properly configured:

```bash
# Navigate to your poke directory
cd /path/to/poke

# Run the setup script
python setup.py

# Edit your .env file with Spotify credentials
nano .env
```

### 2. Test MCP Server

Verify the server works correctly:

```bash
# Test the connection
python test_connection.py

# Start the server
python main.py
```

### 3. Configure Poke by Interaction

Add the MCP server to your Poke by Interaction configuration:

#### Option A: Direct Integration
If Poke by Interaction supports direct MCP server connections:

1. Add the server configuration to your Poke by Interaction settings
2. Point to the MCP server endpoint (typically `stdio` for local servers)
3. Configure the server path: `/path/to/poke/main.py`

#### Option B: HTTP Endpoint
If you need an HTTP endpoint, create a simple HTTP wrapper:

```python
# http_server.py
from fastapi import FastAPI
from mcp_server import SpotifyMCPServer
import asyncio

app = FastAPI()
mcp_server = SpotifyMCPServer()

@app.post("/mcp/call_tool")
async def call_tool(tool_name: str, arguments: dict):
    # Implement HTTP wrapper for MCP tool calls
    pass
```

### 4. Natural Language Commands

Once integrated, you can use natural language commands with Poke by Interaction:

#### Music Playback
- "Play some jazz music"
- "Start playing my Discover Weekly playlist"
- "Play the song 'Bohemian Rhapsody'"
- "Resume playback"
- "Pause the music"

#### Search & Discovery
- "Search for Taylor Swift songs"
- "Find jazz albums from the 1960s"
- "Show me my top tracks from this month"
- "What was I listening to recently?"

#### Playlist Management
- "Create a new playlist called 'Workout Music'"
- "Add this song to my 'Favorites' playlist"
- "Show me all my playlists"
- "Add the current song to my queue"

#### Volume & Device Control
- "Set volume to 50%"
- "Turn up the volume"
- "Skip to the next track"
- "Go back to the previous song"
- "Show me available devices"

### 5. Example Interactions

Here are some example conversations with Poke by Interaction:

**User**: "I want to listen to some relaxing music"
**Poke by Interaction**: *Uses `spotify_search` to find relaxing music, then `spotify_play` to start playback*

**User**: "Create a playlist for my morning workout"
**Poke by Interaction**: *Uses `spotify_create_playlist` to create a new playlist, then `spotify_search` to find workout music*

**User**: "What's currently playing?"
**Poke by Interaction**: *Uses `spotify_get_current_track` to get current playback information*

**User**: "Skip this song"
**Poke by Interaction**: *Uses `spotify_skip_next` to skip to the next track*

## Troubleshooting

### Common Integration Issues

1. **MCP Server Not Found**
   - Ensure the server is running: `python main.py`
   - Check that Poke by Interaction can access the server path
   - Verify file permissions

2. **Authentication Errors**
   - Run `python test_connection.py` to verify Spotify authentication
   - Check your `.env` file for correct credentials
   - Ensure your Spotify app has the required scopes

3. **No Response from Tools**
   - Check server logs for errors
   - Verify that Spotify is open on at least one device
   - Ensure you have Spotify Premium for playback control

4. **Permission Denied**
   - Make sure your Spotify app has all required scopes enabled
   - Re-authenticate if you've changed scopes
   - Check that your Spotify account has the necessary permissions

### Debug Mode

Enable debug logging to troubleshoot issues:

```bash
# Run with debug logging
PYTHONPATH=. python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
import main
"
```

## Advanced Configuration

### Custom Tool Responses

You can customize how the MCP server responds to tool calls by modifying the handlers in `mcp_server.py`:

```python
async def _handle_search(self, arguments: Dict[str, Any]) -> CallToolResult:
    # Customize search result formatting
    results = self.spotify_client.search(query, search_type, limit)
    formatted_results = self._custom_format_results(results)
    return CallToolResult(content=[TextContent(type="text", text=formatted_results)])
```

### Adding New Commands

To add support for new Spotify features:

1. Add the tool definition in `mcp_server.py`
2. Implement the handler function
3. Add the corresponding method in `spotify_client.py`
4. Update this integration guide

## Security Considerations

- Keep your Spotify API credentials secure
- Use environment variables for sensitive configuration
- Regularly rotate your API credentials
- Monitor API usage to avoid rate limits

## Support

For issues with:
- **Spotify MCP Server**: Check the main README.md
- **Poke by Interaction**: Consult Poke by Interaction documentation
- **Spotify API**: Visit the [Spotify Developer Documentation](https://developer.spotify.com/documentation/)

## Contributing

Contributions to improve the integration are welcome! Please:
1. Test your changes thoroughly
2. Update documentation as needed
3. Follow the existing code style
4. Submit pull requests with clear descriptions
