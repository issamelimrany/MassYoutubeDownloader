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
