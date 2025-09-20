#!/usr/bin/env python3
"""Setup script for Spotify MCP Server."""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Spotify MCP Server...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("""# Spotify API Credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

# MCP Server Configuration
MCP_SERVER_NAME=spotify-mcp-server
MCP_SERVER_VERSION=1.0.0
MCP_SERVER_DESCRIPTION=Spotify API integration via MCP

# Optional: Cache settings
CACHE_TTL=3600
""")
        print("✅ .env file created")
        print("⚠️  Please edit .env file with your Spotify API credentials")
    else:
        print("✅ .env file already exists")
    
    # Make scripts executable
    scripts = ["main.py", "test_connection.py", "setup.py"]
    for script in scripts:
        if os.path.exists(script):
            os.chmod(script, 0o755)
    
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Get Spotify API credentials from https://developer.spotify.com/dashboard")
    print("2. Edit .env file with your credentials")
    print("3. Run: python test_connection.py")
    print("4. Run: python main.py")

if __name__ == "__main__":
    main()
