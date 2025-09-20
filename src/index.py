from js import Response, fetch
import json
import asyncio

# Spotify credentials from environment
SPOTIFY_CLIENT_ID = ""  # Set in Workers environment
SPOTIFY_CLIENT_SECRET = ""  # Set in Workers environment

class SpotifyMCPWorker:
    def __init__(self):
        self.access_token = None
    
    async def get_access_token(self):
        """Get Spotify access token using client credentials."""
        if self.access_token:
            return self.access_token
            
        auth_url = "https://accounts.spotify.com/api/token"
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET
        }
        
        try:
            response = await fetch(auth_url, {
                "method": "POST",
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "body": "&".join([f"{k}={v}" for k, v in auth_data.items()])
            })
            data = await response.json()
            self.access_token = data.get("access_token")
            return self.access_token
        except Exception as e:
            print(f"Auth error: {e}")
            return None
    
    async def spotify_request(self, endpoint):
        """Make authenticated Spotify API request."""
        token = await self.get_access_token()
        if not token:
            return {"error": "No access token"}
        
        try:
            response = await fetch(f"https://api.spotify.com/v1{endpoint}", {
                "headers": {"Authorization": f"Bearer {token}"}
            })
            return await response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def handle_mcp_request(self, request_data):
        """Handle MCP protocol requests."""
        method = request_data.get("method")
        params = request_data.get("params", {})
        
        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_data.get("id"),
                "result": {
                    "tools": [
                        {
                            "name": "spotify_search",
                            "description": "Search for tracks, albums, artists",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string"},
                                    "type": {"type": "string", "default": "track"}
                                }
                            }
                        },
                        {
                            "name": "get_featured_playlists",
                            "description": "Get featured playlists",
                            "inputSchema": {"type": "object", "properties": {}}
                        }
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name == "spotify_search":
                query = tool_args.get("query", "")
                search_type = tool_args.get("type", "track")
                result = await self.spotify_request(f"/search?q={query}&type={search_type}&limit=10")
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_data.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            
            elif tool_name == "get_featured_playlists":
                result = await self.spotify_request("/browse/featured-playlists?limit=10")
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_data.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
        
        return {
            "jsonrpc": "2.0",
            "id": request_data.get("id"),
            "error": {"code": -32601, "message": "Method not found"}
        }

# Global worker instance
worker = SpotifyMCPWorker()

async def on_fetch(request):
    """Main Worker fetch handler."""
    url = request.url
    method = request.method
    
    # Handle CORS
    if method == "OPTIONS":
        return Response.new("", {
            "status": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        })
    
    # Root endpoint
    if url.endswith("/"):
        return Response.new(json.dumps({
            "name": "Spotify MCP Worker",
            "version": "1.0.0",
            "status": "running"
        }), {
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        })
    
    # Health check
    if url.endswith("/health"):
        return Response.new(json.dumps({"status": "healthy"}), {
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        })
    
    # MCP endpoint
    if method == "POST":
        try:
            request_data = await request.json()
            result = await worker.handle_mcp_request(request_data)
            
            return Response.new(json.dumps(result), {
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            })
        except Exception as e:
            return Response.new(json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }), {
                "status": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            })
    
    return Response.new("Not Found", {"status": 404})
