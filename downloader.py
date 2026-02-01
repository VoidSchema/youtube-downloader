#!/usr/bin/env python3

import os
import re
from pathlib import Path
from colorama import Fore, Style
from tqdm import tqdm
import time

try:
    from pytubefix import YouTube, Playlist
    from pytubefix.cli import on_progress
except ImportError:
    print("Error: pytubefix not installed. Please run: pip install pytubefix")
    exit(1)

try:
    from pydub import AudioSegment
except ImportError:
    print("Warning: pydub not installed. Audio conversion may not work.")
    AudioSegment = None

from utils import (
    sanitize_filename, format_size, format_duration, format_number,
    print_success, print_error, print_info, print_warning, print_verbose,
    truncate_string
)

class YouTubeDownloader:
    def __init__(self, output_path='.'):
        """Initialize the downloader with output path"""
        self.output_path = Path(output_path)
        self.create_directories()
    
    def create_directories(self):
        """Create necessary directories"""
        self.videos_path = self.output_path / 'videos'
        self.audio_path = self.output_path / 'audio'
        
        self.videos_path.mkdir(parents=True, exist_ok=True)
        self.audio_path.mkdir(parents=True, exist_ok=True)
        
        print_verbose(f"Created directories: {self.videos_path}, {self.audio_path}")
    
    def progress_callback(self, stream, chunk, bytes_remaining):
        """Progress callback for downloads"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        
        # This will be used by tqdm, so we don't print here to avoid conflicts
        pass
    
    def download_video(self, url, quality=None, verbose=False):
        """Download a single video"""
        try:
            print_info(f"Processing video: {url}")
            
            # Create YouTube object with progress callback
            yt = YouTube(url, on_progress_callback=self.progress_callback)
            
            if verbose:
                print(f"{Fore.YELLOW}Title: {yt.title}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Duration: {format_duration(yt.length)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Views: {format_number(yt.views)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Channel: {yt.author}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Upload Date: {yt.publish_date}{Style.RESET_ALL}")
            
            # Get appropriate stream
            stream = self._get_video_stream(yt, quality)
            
            if not stream:
                print_error(f"No stream found for the requested quality")
                return None
            
            # Sanitize filename and prepare download path
            safe_title = sanitize_filename(yt.title)
            extension = stream.mime_type.split('/')[1] if hasattr(stream, 'mime_type') and stream.mime_type else "mp4"
            download_path = self.videos_path / f"{safe_title}.{extension}"
            
            # Download with progress bar
            print_info(f"Downloading video: {safe_title}")
            print(f"Quality: {stream.resolution} | Size: {format_size(stream.filesize)}")
            
            filename = stream.download(
                output_path=str(self.videos_path),
                filename=f"{safe_title}.{extension}"
            )
            
            print_success(f"Video downloaded: {filename}")
            return filename
            
        except Exception as e:
            print_error(f"Failed to download video: {str(e)}")
            return None
    
    def download_audio(self, url, verbose=False):
        """Download audio only and convert to MP3"""
        try:
            print_info(f"Processing audio: {url}")
            
            # Create YouTube object
            yt = YouTube(url, on_progress_callback=self.progress_callback)
            
            if verbose:
                print(f"{Fore.YELLOW}Title: {yt.title}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Duration: {format_duration(yt.length)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Channel: {yt.author}{Style.RESET_ALL}")
            
            # Get audio stream
            audio_stream = yt.streams.get_audio_only()
            
            if not audio_stream:
                print_error("No audio stream found")
                return None
            
            safe_title = sanitize_filename(yt.title)
            extension = audio_stream.mime_type.split('/')[1] if hasattr(audio_stream, 'mime_type') and audio_stream.mime_type else "mp4"
            temp_file = self.audio_path / f"{safe_title}_temp.{extension}"
            mp3_file = self.audio_path / f"{safe_title}.mp3"
            
            print_info(f"Downloading audio: {safe_title}")
            print(f"Size: {format_size(audio_stream.filesize)}")
            
            # Download audio
            temp_filename = audio_stream.download(
                output_path=str(self.audio_path),
                filename=f"{safe_title}_temp.{extension}"
            )
            
            # Convert to MP3 if pydub is available
            if AudioSegment:
                print_info("Converting to MP3...")
                try:
                    audio = AudioSegment.from_file(temp_filename)
                    audio.export(str(mp3_file), format='mp3', bitrate='192k')
                    
                    # Remove temporary file
                    os.remove(temp_filename)
                    
                    print_success(f"MP3 downloaded: {mp3_file}")
                    return str(mp3_file)
                    
                except Exception as e:
                    print_error(f"Failed to convert to MP3: {str(e)}")
                    # Return the original audio file if conversion fails
                    print_warning(f"Returning original audio format: {temp_filename}")
                    return temp_filename
            else:
                print_warning("pydub not available, returning original audio format")
                return temp_filename
                
        except Exception as e:
            print_error(f"Failed to download audio: {str(e)}")
            return None
    
    def _get_video_stream(self, yt, quality=None):
        """Get the appropriate video stream based on quality preference"""
        try:
            if quality:
                # Try to get specific resolution
                stream = yt.streams.filter(
                    res=f"{quality}p", 
                    progressive=True,  # Video + audio together
                    file_extension="mp4"
                ).first()
                
                if stream:
                    return stream
                
                # Try progressive with any extension
                stream = yt.streams.filter(
                    res=f"{quality}p",
                    progressive=True
                ).first()
                
                if stream:
                    return stream
                
                # Try any stream with that resolution
                stream = yt.streams.filter(res=f"{quality}p").order_by('resolution').desc().first()
                
                if stream:
                    return stream
            
            # If no quality specified or preferred quality not found, get highest resolution
            return yt.streams.get_highest_resolution()
            
        except Exception as e:
            print_error(f"Error getting video stream: {str(e)}")
            return None
    
    def list_qualities(self, url):
        """List all available video qualities"""
        try:
            print_info(f"Fetching available qualities for: {url}")
            
            yt = YouTube(url)
            streams = yt.streams.filter(progressive=True).order_by('resolution').desc()
            
            if not streams:
                print_warning("No progressive streams found. Showing all streams:")
                streams = yt.streams.order_by('resolution').desc()
            
            print(f"\n{Fore.CYAN}Available qualities for: {truncate_string(yt.title, 60)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Duration: {format_duration(yt.length)}{Style.RESET_ALL}")
            print(f"\n{Fore.GREEN}{'Resolution':<12} {'FPS':<6} {'File Size':<12} {'Extension':<10}{'Progressive':<12}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'-'*12} {'-'*6} {'-'*12} {'-'*10}{'-'*12}{Style.RESET_ALL}")
            
            shown_qualities = set()
            for i, stream in enumerate(streams):
                resolution = stream.resolution or "Audio"
                if resolution in shown_qualities and resolution != "Audio":
                    continue
                shown_qualities.add(resolution)
                
                size = format_size(stream.filesize) if stream.filesize else "Unknown"
                fps = str(stream.fps) if stream.fps else "N/A"
                progressive = "Yes" if stream.is_progressive else "No"
                extension = stream.mime_type.split('/')[1] if hasattr(stream, 'mime_type') and stream.mime_type else "unknown"
                
                print(f"{resolution:<12} {fps:<6} {size:<12} {extension:<10}{progressive:<12}")
            
            print(f"\n{Fore.YELLOW}Note: Progressive streams contain both video and audio{Style.RESET_ALL}")
            
        except Exception as e:
            print_error(f"Failed to list qualities: {str(e)}")
    
    def download_playlist(self, url, quality=None, audio_only=False, verbose=False):
        """Download entire playlist"""
        try:
            print_info(f"Processing playlist: {url}")
            
            playlist = Playlist(url)
            
            print(f"{Fore.CYAN}📼 Playlist: {truncate_string(playlist.title, 60)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📊 Total videos: {len(playlist.video_urls)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}👤 Channel: {playlist.owner}{Style.RESET_ALL}")
            
            if verbose:
                print(f"{Fore.YELLOW}📝 Description: {truncate_string(playlist.description, 100)}{Style.RESET_ALL}")
            
            successful = 0
            failed = []
            
            with tqdm(total=len(playlist.video_urls), desc="Downloading playlist", unit="video") as pbar:
                for i, video_url in enumerate(playlist.video_urls):
                    try:
                        if verbose:
                            print(f"\n{Fore.MAGENTA}[{i+1}/{len(playlist.video_urls)}] Processing video...{Style.RESET_ALL}")
                        
                        if audio_only:
                            result = self.download_audio(video_url, verbose=verbose)
                        else:
                            result = self.download_video(video_url, quality=quality, verbose=verbose)
                        
                        if result:
                            successful += 1
                        else:
                            failed.append(f"Video {i+1}: Failed to download")
                            
                    except Exception as e:
                        error_msg = f"Video {i+1}: {str(e)}"
                        failed.append(error_msg)
                        print_error(error_msg)
                    
                    pbar.update(1)
                    # Small delay to avoid rate limiting
                    time.sleep(0.5)
            
            # Summary
            print(f"\n{Fore.GREEN}✅ Playlist download completed!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}📊 Successfully downloaded: {successful}/{len(playlist.video_urls)} videos{Style.RESET_ALL}")
            
            if failed:
                print(f"{Fore.RED}❌ Failed downloads: {len(failed)}{Style.RESET_ALL}")
                if verbose:
                    for failure in failed[:5]:  # Show first 5 failures
                        print(f"{Fore.RED}   - {failure}{Style.RESET_ALL}")
                    if len(failed) > 5:
                        print(f"{Fore.RED}   ... and {len(failed) - 5} more failures{Style.RESET_ALL}")
            
            return successful, failed
            
        except Exception as e:
            print_error(f"Failed to download playlist: {str(e)}")
            return 0, [str(e)]