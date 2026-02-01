#!/usr/bin/env python3

import os
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from colorama import Fore, Style

def is_valid_youtube_url(url):
    """Validate if the URL is a valid YouTube URL"""
    if not url:
        return False
    
    patterns = [
        r'(https?://)?(www\.)?(youtube\.com/watch\?v=[\w-]+)',
        r'(https?://)?(www\.)?(youtu\.be/[\w-]+)',
        r'(https?://)?(www\.)?(youtube\.com/playlist\?list=[\w-]+)'
    ]
    
    return any(re.match(pattern, url, re.IGNORECASE) for pattern in patterns)

def is_playlist(url):
    """Check if URL is a YouTube playlist"""
    return 'playlist?list=' in url.lower()

def sanitize_filename(filename):
    """Sanitize filename for filesystem compatibility"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Remove multiple spaces and replace with single space
    filename = re.sub(r'\s+', ' ', filename).strip()
    
    # Remove leading/trailing dots
    filename = filename.strip('.')
    
    # Ensure filename is not empty
    if not filename:
        filename = "untitled"
    
    return filename

def format_size(bytes_size):
    """Format bytes to human readable format"""
    if bytes_size == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(bytes_size)
    
    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024
        i += 1
    
    return f"{size:.1f} {size_names[i]}"

def format_duration(seconds):
    """Format seconds to human readable duration"""
    if not seconds:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def format_number(num):
    """Format large numbers with commas"""
    return f"{num:,}" if num else "0"

def print_success(message):
    """Print success message in green"""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message):
    """Print error message in red"""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_info(message):
    """Print info message in cyan"""
    print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print warning message in yellow"""
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")

def print_verbose(message, verbose=False):
    """Print verbose message if verbose mode is enabled"""
    if verbose:
        print(f"{Fore.MAGENTA}🔍 {message}{Style.RESET_ALL}")

def truncate_string(text, max_length=50):
    """Truncate string if it's too long"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

# Export function for use in other modules
__all__ = [
    'is_valid_youtube_url', 'is_playlist', 'get_video_id', 'sanitize_filename',
    'format_size', 'format_duration', 'format_number', 'print_success', 
    'print_error', 'print_info', 'print_warning', 'print_verbose', 
    'truncate_string'
]