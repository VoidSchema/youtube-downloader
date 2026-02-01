# 📹 YouTube Downloader CLI

A powerful and feature-rich Python CLI tool for downloading YouTube videos and playlists with advanced options and beautiful terminal output.

## 🚀 Quick Setup

### One-Command Setup
```bash
# Clone or download the project
git clone <repository-url>
cd youtube-downloader

# Run the automatic setup
bash setup.sh

# Activate the virtual environment
source activate.sh

# Start downloading!
python main.py "https://youtube.com/watch?v=xxxx"
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## 📋 Features

- 🎥 **Video Downloads** - Download in various resolutions (144p to 1080p+)
- 🎵 **Audio Extraction** - Extract audio and convert to MP3
- 📼 **Playlist Support** - Download entire playlists with progress tracking
- 🎛️ **Quality Selection** - Choose specific video quality or auto-select best
- 📊 **Progress Tracking** - Real-time progress bars with detailed information
- 🎨 **Beautiful Output** - Colored terminal output with clear status messages
- 🗂️ **Smart Organization** - Automatic organization into videos/ and audio/ folders
- 🔍 **Quality Listing** - List all available video qualities before downloading
- ⚡ **Batch Processing** - Efficient playlist downloads with error handling

## 📖 Usage Examples

### Basic Video Download
```bash
python main.py "https://youtube.com/watch?v=VIDEO_ID"
```

### Download Audio Only (MP3)
```bash
python main.py "URL" --audio-only
```

### Download Specific Quality
```bash
python main.py "URL" --quality 720
# Available: 144, 240, 360, 480, 720, 1080
```

### List Available Qualities
```bash
python main.py "URL" --list-quality
```

### Download Entire Playlist
```bash
python main.py "PLAYLIST_URL" --playlist
```

### Download Playlist as Audio
```bash
python main.py "PLAYLIST_URL" --playlist --audio-only
```

### Custom Output Directory
```bash
python main.py "URL" --output ~/Downloads/youtube
```

### Verbose Output
```bash
python main.py "URL" --verbose
```

## 🛠️ Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `url` | YouTube video or playlist URL (required) | `"https://youtube.com/watch?v=xxxx"` |
| `--audio-only` | Download audio only (MP3) | `--audio-only` |
| `--quality` | Video resolution | `--quality 720` |
| `--list-quality` | List available qualities | `--list-quality` |
| `--playlist` | Download entire playlist | `--playlist` |
| `--output` | Custom output directory | `--output ./downloads` |
| `--verbose, -v` | Verbose output | `--verbose` |

## 📁 Project Structure

```
youtube-downloader/
├── .venv/                  # Virtual environment
├── videos/                  # Downloaded videos
├── audio/                   # Downloaded audio
├── main.py                  # CLI entry point
├── downloader.py            # Core download logic
├── utils.py                 # Helper functions
├── requirements.txt         # Python dependencies
├── setup.sh                # Automated setup script
├── activate.sh              # Environment activation
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## 🔧 Dependencies

- **pytubefix** - Enhanced YouTube download library
- **tqdm** - Beautiful progress bars
- **colorama** - Cross-platform colored terminal output
- **pydub** - Audio conversion and processing

## 🎯 Supported URLs

### Video URLs
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

### Playlist URLs
- `https://www.youtube.com/playlist?list=PLAYLIST_ID`
- `https://youtube.com/playlist?list=PLAYLIST_ID`

## 📊 Output Examples

### Video Download Output
```
✅ YouTube Downloader initialized successfully
ℹ️  Starting video download...
ℹ️  Processing video: https://youtube.com/watch?v=xxxx
🔍 Title: Amazing Video Title
🔍 Duration: 05:23
🔍 Channel: Awesome Creator
ℹ️  Downloading video: Amazing Video Title
Quality: 720p | Size: 25.3 MB
✅ Video downloaded: ./videos/Amazing Video Title.mp4
✅ Download completed!
```

### Playlist Download Output
```
ℹ️  Processing playlist: https://youtube.com/playlist?list=xxxx
📼 Playlist: Amazing Playlist Title
📊 Total videos: 15
👤 Channel: Awesome Channel
Downloading playlist: 100%|████████| 15/15 [02:45<00:00, 11.2s/video]

✅ Playlist download completed!
📊 Successfully downloaded: 15/15 videos
```

## 🔍 Quality Options

| Resolution | Description | File Size (Typical) |
|------------|-------------|-------------------|
| 144p | Lowest quality, minimal storage | 5-15 MB |
| 240p | Low quality, good for slow connections | 10-25 MB |
| 360p | Standard quality | 20-50 MB |
| 480p | Enhanced quality | 30-80 MB |
| 720p | HD quality | 50-150 MB |
| 1080p | Full HD | 100-300 MB |

## ⚠️ Important Notes

1. **FFmpeg Requirement**: For audio conversion to MP3, FFmpeg needs to be installed on your system
2. **Network Connection**: Stable internet connection required for downloads
3. **Storage Space**: Ensure sufficient disk space for large downloads
4. **Private Videos**: Cannot download private or restricted videos
5. **Copyright**: Download only content you have rights to download

## 🐛 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Solution: Install dependencies properly
pip install -r requirements.txt
```

#### Audio Conversion Failed
```bash
# Solution: Install FFmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows: Download from https://ffmpeg.org/
```

#### Network Errors
- Check your internet connection
- Try again after a few minutes
- Use VPN if YouTube is restricted in your region

#### Permission Errors
```bash
# Solution: Check file permissions
chmod +x setup.sh activate.sh
```

### Debug Mode
Use `--verbose` flag for detailed error messages:
```bash
python main.py "URL" --verbose
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please respect YouTube's Terms of Service and copyright laws.

## 🙋‍♂️ Support

If you encounter any issues:
1. Check the troubleshooting section
2. Try with `--verbose` flag for more details
3. Create an issue with detailed information

---

**Happy Downloading!** 🎬✨