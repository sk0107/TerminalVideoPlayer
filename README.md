# Terminal Video Player

The **Terminal Video Player** is a rudimentary Python-based tool that converts video files into ASCII art and plays them directly in the terminal, synchronized with their audio. It supports both monochrome and colored ASCII output, making it a fun way to watch videos in a terminal environment. This is a **work in progress** so there are still a lot of bugs to fix and optimizations and features to be implemented!

## Features
- Converts video frames to ASCII art.
- Plays audio alongside the ASCII video.
- Supports optional colored ASCII output.
- Adjustable FPS based on the video's true FPS.

## Requirements

The following Python packages are required to run the Terminal Video Player:

```
opencv-python==4.10.0.84
pydub==0.25.1
pyaudio==0.2.14
ffmpeg-python==0.2.0
```

You also need **FFmpeg** installed on your system. Ensure that `ffmpeg` and `ffprobe` are accessible from the command line.

## Installation

1. **Install Git** (if not already installed):
   ```bash
   # For Debian/Ubuntu
   sudo apt update && sudo apt install git
   
   # For macOS (using Homebrew)
   brew install git
   
   # For Windows
   # Download and install Git from https://git-scm.com/
   ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/sk0107/TerminalVideoPlayer.git
   cd TerminalVideoPlayer
   ```

3. **Install Conda** (if not already installed):
   - Download and install Miniconda from [Miniconda Downloads](https://docs.conda.io/en/latest/miniconda.html).

4. **Create a Conda Environment**:
   ```bash
   conda create -n video_to_ascii python=3.10 -y
   conda activate video_to_ascii
   ```

5. **Install the Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Ensure FFmpeg is Installed**:
   ```bash
   # For Debian/Ubuntu
   sudo apt update && sudo apt install ffmpeg

   # For macOS (using Homebrew)
   brew install ffmpeg

   # For Windows
   # Download from https://ffmpeg.org/download.html and add it to your PATH
   ```

## Usage

Run the script with the path to the video file as an argument:

```bash
python video_to_ascii.py [video] [--color] [--true-fps]
```

### Arguments
- `video`: Path to the video file to play. If not specified, the script will look for `.mp4` files in the current directory.
- `--color`: Enable colored ASCII output.
- `--true-fps`: Use the video's true FPS for playback.

### Example
```bash
python video_to_ascii.py myvideo.mp4 --color --true-fps
```

## How It Works

1. **Video to ASCII Conversion**:
   - Each frame of the video is resized to fit the terminal dimensions.
   - Pixels are converted to ASCII characters based on brightness levels.
   - If the `--color` flag is set, characters are colorized using their pixel color values.

2. **Audio Playback**:
   - The audio is extracted from the video using FFmpeg.
   - The `pydub` library is used to play the audio.

3. **Synchronization**:
   - Frames are displayed in the terminal at a rate matching the video's FPS.

## Limitations
- Requires a sufficiently large terminal window for better visual quality.
- Playback performance may vary based on terminal and system capabilities.

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve this project.

## Contact
Please contact me at sohamkonar28@gmail.com with any questions or concerns.

## Inspiration
My two brain cells are fried beyond repair but this TikTok (https://www.tiktok.com/t/ZP8N7bwwT/) created a brief spark that led to the creation of this abomination. The goal was to create a video player on par with the one found here (https://github.com/maxcurzi/tplay) and clearly I did a great job of doing that.

## Final Thoughts
I started this project at 11 PM on December 24th, 2024 and I am writing this at 3 AM on December 25th, 2024 after throwing this code at ChatGPT for the past 3.5 hours. Given that I am trying to write a high-performance Python-based (oxymoron intended) terminal video player, I think I did an alright job.