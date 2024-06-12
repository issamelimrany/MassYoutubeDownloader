import tkinter as tk
from tkinter import filedialog, messagebox
import pytube_services

downloader = pytube_services.VideoDownloader()

def browse_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx *.xls")])
    if filepath:
        entry_filepath.delete(0, tk.END)
        entry_filepath.insert(0, filepath)

def download_videos():
    filepath = entry_filepath.get()
    if not filepath:
        messagebox.showerror("Error", "Please select an Excel file")
        return

    try:
        download_thread = downloader.start_download(filepath)
        update_progress(download_thread)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_progress(download_thread):
    current_video_progress.set(f"Current video ({downloader.current_video}): {downloader.current_video_progress}%")
    overall_progress.set(f"Overall progress: {downloader.overall_progress}%")
    if download_thread.is_alive():
        root.after(100, lambda: update_progress(download_thread))
    else:
        messagebox.showinfo("Success", "All videos have been downloaded")

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create and place the file selection widgets
label_filepath = tk.Label(root, text="Select Excel file:")
label_filepath.grid(row=0, column=0, padx=10, pady=10)

entry_filepath = tk.Entry(root, width=50)
entry_filepath.grid(row=0, column=1, padx=10, pady=10)

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2, padx=10, pady=10)

# Create and place the download button
button_download = tk.Button(root, text="Download Videos", command=download_videos)
button_download.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Create progress labels
current_video_progress = tk.StringVar()
label_current_progress = tk.Label(root, textvariable=current_video_progress)
label_current_progress.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

overall_progress = tk.StringVar()
label_overall_progress = tk.Label(root, textvariable=overall_progress)
label_overall_progress.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Initialize progress
current_video_progress.set("Current video: 0%")
overall_progress.set("Overall progress: 0%")

# Run the application
root.mainloop()
