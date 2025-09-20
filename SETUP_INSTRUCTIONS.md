# 🎧 Spotify MCP Server - Setup Instructions

## Quick Start to Test Top 10 Songs

### Step 1: Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the details:
   - **App Name**: `My Spotify MCP Server` (or any name you prefer)
   - **App Description**: `Testing Spotify API integration`
   - **Redirect URI**: `http://localhost:8888/callback`
   - **API/SDKs**: Check "Web API"
5. Click "Save"
6. Copy your **Client ID** and **Client Secret**

### Step 2: Create Environment File

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and replace the placeholders:
   ```bash
   SPOTIFY_CLIENT_ID=your_actual_client_id_here
   SPOTIFY_CLIENT_SECRET=your_actual_client_secret_here
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   ```

### Step 3: Test Your Top 10 Songs

Run the test script:
```bash
python3 test_top_songs.py
```

This will:
1. ✅ Validate your configuration
2. 🔐 Start the Spotify authentication process
3. 🎵 Fetch your top 10 tracks
4. 🎶 Show your 5 most recent songs as a bonus

### What to Expect

1. **First Run**: You'll be prompted to visit a URL to authorize the app
2. **Authorization**: Copy the authorization code from the callback URL
3. **Results**: See your personalized top 10 songs with details like:
   - Song name and artist
   - Album name
   - Duration
   - Popularity score

### Troubleshooting

- **No top tracks found**: Make sure you've listened to music on Spotify recently
- **Authentication failed**: Double-check your Client ID and Client Secret
- **Permission denied**: Ensure your Spotify app has the correct redirect URI
- **Module not found**: Run `pip install -r requirements.txt`

### Alternative Test Scripts

- `python3 test_connection.py` - Basic connection test
- `python3 main.py` - Full MCP server (for advanced usage)

## 🎉 That's it!

Once you see your top 10 songs, the Spotify integration is working perfectly!
