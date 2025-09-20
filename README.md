# MCP Spotify Vercel

Clean MCP (Model Context Protocol) server for Spotify integration, deployed on Vercel.

## Environment Variables

Set these in your Vercel project:

- `SPOTIFY_CLIENT_ID` - Your Spotify app client ID
- `SPOTIFY_CLIENT_SECRET` - Your Spotify app client secret  
- `SPOTIFY_REFRESH_TOKEN` - (Optional) For user-specific operations

## Endpoints

- `/api/test` - Simple test endpoint
- `/api/index` - MCP JSON-RPC endpoint for Poke integration

## Usage in Poke

Server URL: `https://your-vercel-url.vercel.app/api/index`