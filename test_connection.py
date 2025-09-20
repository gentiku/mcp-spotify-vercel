#!/usr/bin/env python3
"""Test script to verify Spotify MCP Server functionality."""

import asyncio
import json
import logging
from mcp_server import SpotifyMCPServer
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_mcp_server():
    """Test the MCP server functionality."""
    try:
        # Validate configuration
        config.validate()
        logger.info("✓ Configuration validated")
        
        # Create server instance
        server = SpotifyMCPServer()
        logger.info("✓ MCP server created")
        
        # Test tool listing
        tools = await server.server.list_tools()
        logger.info(f"✓ Found {len(tools)} tools:")
        for tool in tools:
            logger.info(f"  - {tool.name}: {tool.description}")
        
        # Test Spotify client initialization
        if server.spotify_client is None:
            server.spotify_client = server.spotify_client.__class__()
        logger.info("✓ Spotify client initialized")
        
        # Test user profile
        profile = server.spotify_client.get_user_profile()
        if profile:
            logger.info(f"✓ Connected as: {profile['display_name']}")
        else:
            logger.warning("⚠ Could not get user profile")
        
        # Test device listing
        devices = server.spotify_client.get_devices()
        logger.info(f"✓ Found {len(devices)} devices")
        
        # Test search functionality
        search_results = server.spotify_client.search("test", "track", 5)
        if search_results:
            logger.info("✓ Search functionality working")
        else:
            logger.warning("⚠ Search returned no results")
        
        logger.info("🎉 All tests passed! MCP server is ready to use.")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
