# YouTube Video Downloader

This is a simple desktop application that allows you to download YouTube videos based on an Excel file input. The Excel file should contain the video names and links. The application provides real-time feedback on the download progress of each video and the overall download progress.

## Features

- **Read Excel File**: Reads video names and links from an Excel file.
- **Download Videos**: Downloads the videos from YouTube using `pytube`.
- **Progress Feedback**: Provides real-time feedback on the download progress of each video and the overall download progress.
- **GUI**: Simple graphical user interface (GUI) using `tkinter`.

## Requirements

- Python 3.x
- `tkinter` (comes with Python)
- `pandas`
- `openpyxl` (to read Excel files)
- `pytube`

## Installation

1. Clone the repository or download the source code.

2. Install the required Python packages:
    ```bash
    pip install pandas openpyxl pytube
    ```

## File Structure

- `pytube_services.py`: Contains the logic for reading the Excel file and downloading the videos.
- `main_app.py`: Contains the `tkinter` GUI code and uses the services from `pytube_services.py`.

## Excel File Format

The Excel file should have two columns: one for the video names and one for the YouTube links.

### Example

| Name            | Link                                          |
|-----------------|-----------------------------------------------|
| Python Tutorial | https://www.youtube.com/watch?v=rfscVS0vtbw   |
| Python Tutorial 2 | https://www.youtube.com/watch?v=N4mEzFDjqtA |
| Python Tutorial 3 | https://www.youtube.com/watch?v=HGOBQPFzWKo |

## Usage

1. Save the Excel file with video names and links (e.g., `video_links.xlsx`).

2. Run the `main_app.py` script:
    ```bash
    python main_app.py
    ```

3. Use the GUI to select the Excel file and download the videos.

### `pytube_services.py`

```python
import pandas as pd
from pytube import YouTube
import threading

class VideoDownloader:
    def __init__(self):
        self.current_video = ""
        self.current_video_progress = 0
        self.overall_progress = 0
        self.total_videos = 0
        self.downloaded_videos = 0
        self.lock = threading.Lock()

    def progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = int((bytes_downloaded / total_size) * 100)
        with self.lock:
            self.current_video_progress = progress

    def complete_callback(self, stream, file_path):
        with self.lock:
            self.downloaded_videos += 1
            self.overall_progress = int((self.downloaded_videos / self.total_videos) * 100)
        print(f"Downloaded: {self.current_video}")

    def read_excel(self, filepath):
        try:
            df = pd.read_excel(filepath)
            if not all(col in df.columns for col in ["Name", "Link"]):
                raise ValueError("Excel file must contain 'Name' and 'Link' columns")
            return df
        except Exception as e:
            raise ValueError(f"Could not read the file: {e}")

    def download_video(self, name, link, output_path="downloads"):
        try:
            self.current_video = name
            yt = YouTube(link, on_progress_callback=self.progress_callback, on_complete_callback=self.complete_callback)
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=output_path, filename=name)
        except Exception as e:
            print(f"Failed to download {name}: {e}")
            raise e

    def download_videos_from_excel(self, filepath, output_path="downloads"):
        df = self.read_excel(filepath)
        self.total_videos = len(df)
        self.downloaded_videos = 0
        for index, row in df.iterrows():
            self.download_video(row["Name"], row["Link"], output_path)

    def start_download(self, filepath, output_path="downloads"):
        thread = threading.Thread(target=self.download_videos_from_excel, args=(filepath, output_path))
        thread.start()
        return thread
