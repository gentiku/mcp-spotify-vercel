import SpotifyWebApi from 'spotify-web-api-node';

// Initialize Spotify client
function getSpotifyClient() {
  const spotify = new SpotifyWebApi({
    clientId: process.env.SPOTIFY_CLIENT_ID,
    clientSecret: process.env.SPOTIFY_CLIENT_SECRET
  });
  
  if (process.env.SPOTIFY_REFRESH_TOKEN) {
    spotify.setRefreshToken(process.env.SPOTIFY_REFRESH_TOKEN);
  }
  
  return spotify;
}

// Authenticate with Spotify
async function authenticateSpotify(spotify) {
  try {
    if (process.env.SPOTIFY_REFRESH_TOKEN) {
      const data = await spotify.refreshAccessToken();
      spotify.setAccessToken(data.body.access_token);
    } else {
      const data = await spotify.clientCredentialsGrant();
      spotify.setAccessToken(data.body.access_token);
    }
  } catch (error) {
    console.error('Spotify auth failed:', error);
    throw error;
  }
}

// Get tools list
function getTools() {
  return [
    {
      name: 'search_music',
      description: 'Search for tracks, artists, or albums on Spotify',
      inputSchema: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'Search query' },
          type: { type: 'string', enum: ['track', 'artist', 'album'], default: 'track' },
          limit: { type: 'number', minimum: 1, maximum: 50, default: 10 }
        },
        required: ['query']
      }
    },
    {
      name: 'get_current_playback',
      description: 'Get information about the current playback state'
    },
    {
      name: 'control_playback',
      description: 'Control music playback (play, pause, next, previous)',
      inputSchema: {
        type: 'object',
        properties: {
          action: { type: 'string', enum: ['play', 'pause', 'next', 'previous'] },
          trackUri: { type: 'string', description: 'Spotify URI to play (optional)' }
        },
        required: ['action']
      }
    }
  ];
}

// Execute tool
async function executeTool(toolName, args, spotify) {
  await authenticateSpotify(spotify);
  
  switch (toolName) {
    case 'search_music':
      const { query, type = 'track', limit = 10 } = args;
      const results = await spotify.search(query, [type], { limit });
      return {
        content: [{ type: 'text', text: JSON.stringify(results.body, null, 2) }]
      };
      
    case 'get_current_playback':
      try {
        const playback = await spotify.getMyCurrentPlaybackState();
        return {
          content: [{ type: 'text', text: playback.body ? JSON.stringify(playback.body, null, 2) : 'No active playback' }]
        };
      } catch (error) {
        return {
          content: [{ type: 'text', text: 'No active playback or insufficient permissions' }]
        };
      }
      
    case 'control_playback':
      const { action, trackUri } = args;
      try {
        switch (action) {
          case 'play':
            if (trackUri) {
              await spotify.play({ uris: [trackUri] });
            } else {
              await spotify.play();
            }
            break;
          case 'pause':
            await spotify.pause();
            break;
          case 'next':
            await spotify.skipToNext();
            break;
          case 'previous':
            await spotify.skipToPrevious();
            break;
        }
        return {
          content: [{ type: 'text', text: `Playback ${action} executed successfully` }]
        };
      } catch (error) {
        return {
          content: [{ type: 'text', text: `Failed to ${action}: ${error.message}` }]
        };
      }
      
    default:
      throw new Error(`Unknown tool: ${toolName}`);
  }
}

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only handle POST requests for MCP JSON-RPC
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Check for required environment variables
    if (!process.env.SPOTIFY_CLIENT_ID || !process.env.SPOTIFY_CLIENT_SECRET) {
      return res.status(500).json({ 
        error: 'Missing required environment variables: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET' 
      });
    }

    const spotify = getSpotifyClient();
    const { jsonrpc, method, params, id } = req.body;
    
    if (jsonrpc !== '2.0') {
      return res.json({ jsonrpc: '2.0', error: { code: -32600, message: 'Invalid Request' }, id });
    }

    let result;
    
    switch (method) {
      case 'initialize':
        result = {
          protocolVersion: '2024-11-05',
          capabilities: { tools: {} },
          serverInfo: { name: 'mcp-spotify-vercel', version: '1.0.0' }
        };
        break;
        
      case 'tools/list':
        result = { tools: getTools() };
        break;
        
      case 'tools/call':
        const { name, arguments: args } = params;
        result = await executeTool(name, args || {}, spotify);
        break;
        
      default:
        return res.json({ 
          jsonrpc: '2.0', 
          error: { code: -32601, message: `Method not found: ${method}` }, 
          id 
        });
    }
    
    return res.json({ jsonrpc: '2.0', result, id });
    
  } catch (error) {
    console.error('Vercel function error:', error);
    return res.status(500).json({ 
      jsonrpc: '2.0', 
      error: { 
        code: -32603, 
        message: 'Internal error', 
        data: error.message 
      }, 
      id: req.body?.id 
    });
  }
}