import cv2
import time
import sys
import os
import threading
from queue import Queue
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import shutil
import numpy as np

class VideoToAscii:
    def __init__(self, video_path, use_true_fps=False, use_color=False):
        self.video_path = video_path
        self.use_color = use_color
        self._video_capture = cv2.VideoCapture(video_path)

        if not self._video_capture.isOpened():
            print(f"Error: Could not open video file {video_path}")
            sys.exit(1)

        self.original_width = int(self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.original_height = int(self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self._video_capture.get(cv2.CAP_PROP_FPS) if use_true_fps else 30.0
        if self.fps <= 0:
            print("Warning: FPS value is invalid. Defaulting to 30.0 FPS.")
            self.fps = 30.0

        self.width, self.height = self._get_terminal_size()
        self.audio_temp_file = None
        self.frame_queue = Queue(maxsize=10)
        self.stop_event = threading.Event()

    def __del__(self):
        if self._video_capture.isOpened():
            self._video_capture.release()
        if self.audio_temp_file and os.path.exists(self.audio_temp_file):
            os.remove(self.audio_temp_file)

    def _get_terminal_size(self):
        size = shutil.get_terminal_size((80, 24))
        width = size.columns
        height = size.lines - 1
        return width, height

    def extract_audio(self):
        print("Extracting audio...")
        try:
            if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
                raise FileNotFoundError("FFmpeg and/or FFprobe not found. Please install FFmpeg.")

            audio = AudioSegment.from_file(self.video_path)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                self.audio_temp_file = temp_audio.name
                audio.export(self.audio_temp_file, format="mp3")
            print(f"Audio extracted to temporary file: {self.audio_temp_file}")
        except Exception as e:
            print(f"Error extracting audio: {e}")
            sys.exit(1)

    def play_audio(self):
        if self.audio_temp_file:
            try:
                print(f"Playing audio from file: {self.audio_temp_file}")
                audio = AudioSegment.from_file(self.audio_temp_file)
                play(audio)
            except Exception as e:
                print(f"Error playing audio: {e}")
                sys.exit(1)

    def _load_frame(self):
        ret, frame = self._video_capture.read()
        if not ret:
            return None

        aspect_ratio = self.original_width / self.original_height
        term_aspect_ratio = self.width / self.height / 0.45

        if term_aspect_ratio < aspect_ratio:
            new_width = self.width
            new_height = int(new_width / aspect_ratio / 0.45)
        else:
            new_height = self.height
            new_width = int(new_height * aspect_ratio * 0.45)
            new_width = self.width
            new_height = int(new_width / aspect_ratio * 0.45)

        if new_height > self.height:
            new_height = self.height
            new_width = int(self.height * aspect_ratio / 0.45)

        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

        return resized_frame

    def _pixel_to_ascii(self, pixel):
        r, g, b = pixel
        brightness = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255  # Calculate perceived brightness
        ascii_chars = "@%#*+=-:. "  # ASCII characters from darkest to lightest
        char = ascii_chars[int(brightness * (len(ascii_chars) - 1))]
        if self.use_color:
            return f"\033[38;2;{r};{g};{b}m{char}\033[0m"  # Apply color and reset immediately
        else:
            return char

    def _frame_to_ascii(self, frame):
        rows, cols, _ = frame.shape
        # Use numpy for faster processing
        frame_array = np.apply_along_axis(self._pixel_to_ascii, 2, frame)
        ascii_frame = "\n".join(["".join(frame_array[row]) for row in range(rows)])
        return ascii_frame

    def frame_worker(self):
        while not self.stop_event.is_set():
            frame = self._load_frame()
            if frame is None:
                self.stop_event.set()
                break
            ascii_frame = self._frame_to_ascii(frame)
            self.frame_queue.put(ascii_frame)

    def load_video_ascii(self):
        try:
            self.extract_audio()
        except Exception as e:
            print(f"Error during audio extraction: {e}")

        frame_delay = 1.0 / self.fps
        audio_thread = threading.Thread(target=self.play_audio)
        frame_thread = threading.Thread(target=self.frame_worker)

        audio_thread.start()
        frame_thread.start()

        try:
            while not self.stop_event.is_set():
                start_time = time.time()

                if self.frame_queue.empty():
                    time.sleep(0.01)
                    continue

                ascii_frame = self.frame_queue.get()

                print("\033c", end="", flush=True)
                print(ascii_frame, end="", flush=True)

                elapsed = time.time() - start_time
                if elapsed < frame_delay:
                    time.sleep(frame_delay - elapsed)

        except KeyboardInterrupt:
            print("Video playback interrupted.")
            self.stop_event.set()

        audio_thread.join()
        frame_thread.join()
        self._video_capture.release()

if __name__ == "__main__":
    import argparse
    import glob

    parser = argparse.ArgumentParser(description="Convert video to ASCII and play with sound.")
    parser.add_argument("video", nargs="?", help="Path to the video file.")
    parser.add_argument("--color", action="store_true", help="Use colored ASCII output.")
    parser.add_argument("--true-fps", action="store_true", help="Use the video's true FPS.")
    args = parser.parse_args()

    video_path = args.video

    if not video_path:
        mp4_files = glob.glob("*.mp4")
        if not mp4_files:
            print("No .mp4 files found in the current directory.")
            sys.exit(1)
        video_path = mp4_files[0]
        print(f"No video file provided. Using first .mp4 file found: {video_path}")

    video_to_ascii = VideoToAscii(video_path, use_true_fps=args.true_fps, use_color=args.color)
    video_to_ascii.load_video_ascii()