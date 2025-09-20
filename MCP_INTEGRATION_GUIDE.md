# 🎧 Spotify MCP Server → Railway → Poke Integration

## The Complete Flow

1. **Deploy to Railway** → Get public MCP server URL
2. **Add to Poke by Interaction** → Connect to your Railway MCP server
3. **Use Spotify tools in Poke** → Access your music data through MCP

## Step 1: Deploy to Railway

1. **Push to GitHub** and **deploy on Railway** (as described in RAILWAY_DEPLOYMENT.md)
2. **Get your Railway URL**: `https://your-app-name.railway.app`
3. **Test the MCP endpoints**:
   - `https://your-app-name.railway.app/tools` - List available tools
   - `https://your-app-name.railway.app/call_tool` - Execute MCP tools

## Step 2: Add to Poke by Interaction

In Poke, add a new MCP server:

```json
{
  "name": "spotify-mcp-server",
  "url": "https://your-app-name.railway.app",
  "description": "Spotify API integration via MCP"
}
```

## Step 3: Available MCP Tools in Poke

Once connected, you'll have these Spotify tools available:

### 🎵 **Music Discovery**
- `spotify_search` - Search for tracks, albums, artists
- `spotify_get_user_top_tracks` - Get your top songs
- `spotify_get_recently_played` - Get recently played tracks

### 🎮 **Playback Control**
- `spotify_play` - Start playback
- `spotify_pause` - Pause playback
- `spotify_resume` - Resume playback
- `spotify_skip_next` - Skip to next track
- `spotify_skip_previous` - Skip to previous track
- `spotify_set_volume` - Control volume

### 📱 **Device Management**
- `spotify_get_devices` - List available devices
- `spotify_get_current_track` - Get currently playing track

### 📚 **Playlist Management**
- `spotify_get_user_playlists` - Get your playlists
- `spotify_create_playlist` - Create new playlist
- `spotify_add_to_playlist` - Add tracks to playlist

### 👤 **User Info**
- `spotify_get_user_profile` - Get your profile info

## Example Usage in Poke

Once connected, you can ask Poke things like:

- *"What are my top 10 songs?"* → Uses `spotify_get_user_top_tracks`
- *"Search for songs by Burna Boy"* → Uses `spotify_search`
- *"What's currently playing?"* → Uses `spotify_get_current_track`
- *"Create a playlist called 'My Favorites'"* → Uses `spotify_create_playlist`
- *"Pause the music"* → Uses `spotify_pause`

## 🔧 MCP Server Endpoints

Your Railway deployment provides these MCP-specific endpoints:

- **`GET /tools`** - List all available MCP tools
- **`POST /call_tool`** - Execute an MCP tool with parameters
- **`GET /health`** - Health check for the server
- **`GET /`** - Server info and status

## 🎯 The Power of This Setup

- **☁️ Cloud-hosted** - Your MCP server runs 24/7 on Railway
- **🔐 Authenticated** - Uses your personal Spotify account
- **🚀 Fast** - Direct API calls, no local setup needed
- **🔄 Always updated** - Real-time data from Spotify
- **🛠️ Full MCP compatibility** - Works with any MCP client

## 🚀 Ready for Poke!

Your Spotify MCP server is now ready to be used as a cloud service in Poke by Interaction!
