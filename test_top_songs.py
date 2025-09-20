#!/usr/bin/env python3
"""Test script to get top 10 songs from Spotify."""

import sys
import logging
from spotify_client import SpotifyClient
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_track_info(track):
    """Format track information for display."""
    name = track.get('name', 'Unknown')
    artists = ', '.join([artist['name'] for artist in track.get('artists', [])])
    album = track.get('album', {}).get('name', 'Unknown Album')
    popularity = track.get('popularity', 0)
    duration_ms = track.get('duration_ms', 0)
    duration_min = duration_ms // 60000
    duration_sec = (duration_ms % 60000) // 1000
    
    return f"🎵 {name} by {artists}\n   Album: {album}\n   Duration: {duration_min}:{duration_sec:02d} | Popularity: {popularity}/100"

def main():
    """Main function to test getting top 10 songs."""
    try:
        print("🎧 Spotify Top Songs Test")
        print("=" * 50)
        
        # Validate configuration
        try:
            config.validate()
            print("✅ Configuration validated")
        except ValueError as e:
            print(f"❌ Configuration error: {e}")
            print("\n📝 To fix this:")
            print("1. Copy .env.example to .env")
            print("2. Get your Spotify credentials from https://developer.spotify.com/dashboard/")
            print("3. Fill in your SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env")
            return
        
        # Initialize Spotify client
        print("\n🔐 Initializing Spotify client...")
        client = SpotifyClient()
        
        # Get user's top tracks
        print("\n🎵 Getting your top 10 tracks...")
        top_tracks = client.get_user_top_tracks(time_range="medium_term", limit=10)
        
        if not top_tracks:
            print("❌ No top tracks found. Make sure you have listened to music on Spotify!")
            return
        
        print(f"\n🏆 Your Top {len(top_tracks)} Songs:")
        print("=" * 50)
        
        for i, track in enumerate(top_tracks, 1):
            print(f"\n{i}. {format_track_info(track)}")
        
        print(f"\n✅ Successfully retrieved {len(top_tracks)} top songs!")
        
        # Also try to get recently played as an alternative
        print("\n🕒 Getting recently played tracks as bonus...")
        recent_tracks = client.get_recently_played(limit=5)
        
        if recent_tracks:
            print(f"\n🎶 Your 5 Most Recent Songs:")
            print("=" * 30)
            for i, item in enumerate(recent_tracks, 1):
                track = item.get('track', {})
                played_at = item.get('played_at', 'Unknown time')
                print(f"\n{i}. {format_track_info(track)}")
                print(f"   Played at: {played_at}")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        print(f"\n❌ An error occurred: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure you have a .env file with valid Spotify credentials")
        print("2. Ensure you have an active Spotify account")
        print("3. Check that you've listened to music on Spotify recently")
        print("4. Verify your internet connection")

if __name__ == "__main__":
    main()
