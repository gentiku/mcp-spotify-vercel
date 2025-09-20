#!/usr/bin/env python3
"""Main entry point for the Spotify MCP Server."""

import asyncio
import logging
import sys
from mcp_server import SpotifyMCPServer
from config import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to run the MCP server."""
    try:
        # Validate configuration
        config.validate()
        logger.info("Configuration validated successfully")
        
        # Create and run the MCP server
        server = SpotifyMCPServer()
        logger.info(f"Starting {config.MCP_SERVER_NAME} v{config.MCP_SERVER_VERSION}")
        logger.info(f"Description: {config.MCP_SERVER_DESCRIPTION}")
        
        await server.run()
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please check your .env file and ensure all required variables are set")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
