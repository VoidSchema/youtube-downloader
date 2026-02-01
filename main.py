#!/usr/bin/env python3

import argparse
import sys
import os
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init()

# Import our modules
from downloader import YouTubeDownloader
from utils import is_valid_youtube_url, is_playlist, print_error, print_info, print_success, print_warning

def create_parser():
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        prog='youtube-downloader',
        description=f'{Fore.GREEN}📹 YouTube Video Downloader CLI{Style.RESET_ALL}',
        epilog=f'{Fore.CYAN}Examples:\n'
               f'  python main.py "https://youtube.com/watch?v=xxxx"\n'
               f'  python main.py "URL" --audio-only\n'
               f'  python main.py "URL" --quality 1080\n'
               f'  python main.py "PLAYLIST_URL" --playlist{Style.RESET_ALL}',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Positional argument
    parser.add_argument('url', help='YouTube video or playlist URL')
    
    # Download options
    parser.add_argument('--audio-only', action='store_true', 
                       help='Download audio only (MP3)')
    
    parser.add_argument('--quality', type=int, choices=[144, 240, 360, 480, 720, 1080],
                       help='Video resolution (default: highest available)')
    
    parser.add_argument('--list-quality', action='store_true',
                       help='List all available video qualities')
    
    parser.add_argument('--playlist', action='store_true',
                       help='Download entire playlist')
    
    parser.add_argument('--output', default='.',
                       help='Output directory (default: current directory)')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output with detailed information')
    
    return parser

def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate URL
    if not is_valid_youtube_url(args.url):
        print_error("Invalid YouTube URL. Please provide a valid YouTube video or playlist URL.")
        sys.exit(1)
    
    # Check if playlist when --playlist flag is used
    if args.playlist and not is_playlist(args.url):
        print_warning("URL doesn't appear to be a playlist. Continuing with single video download.")
    
    # Initialize downloader
    try:
        downloader = YouTubeDownloader(output_path=args.output)
        print_success("YouTube Downloader initialized successfully")
    except Exception as e:
        print_error(f"Failed to initialize downloader: {str(e)}")
        sys.exit(1)
    
    # Handle list quality option
    if args.list_quality:
        try:
            downloader.list_qualities(args.url)
        except Exception as e:
            print_error(f"Failed to list qualities: {str(e)}")
            sys.exit(1)
        return
    
    # Determine if this is a playlist download
    is_playlist_download = args.playlist or is_playlist(args.url)
    
    if is_playlist_download:
        print_info(f"Starting playlist download...")
        try:
            downloader.download_playlist(
                url=args.url,
                quality=args.quality,
                audio_only=args.audio_only,
                verbose=args.verbose
            )
        except Exception as e:
            print_error(f"Playlist download failed: {str(e)}")
            sys.exit(1)
    else:
        # Single video download
        print_info(f"Starting video download...")
        try:
            if args.audio_only:
                downloader.download_audio(args.url, verbose=args.verbose)
            else:
                downloader.download_video(args.url, quality=args.quality, verbose=args.verbose)
        except Exception as e:
            print_error(f"Video download failed: {str(e)}")
            sys.exit(1)
    
    print_success("Download completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\nDownload cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)