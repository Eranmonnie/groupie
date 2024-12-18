import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import time

class FileOrganizerHandler(FileSystemEventHandler):
    def __init__(self, watch_folder):
        self.watch_folder = watch_folder
        self.document_types = {'.pdf': 'PDFs', '.docx': 'WordDocs', '.txt': 'TextFiles'}
        self.video_types = {'.mp4', '.mkv', '.avi'}
    
    def on_modified(self, event):
        """
        Handles modified events in the watched folder.
        Organizes files when a new file is added or modified.
        """
        for filename in os.listdir(self.watch_folder):
            filepath = os.path.join(self.watch_folder, filename)
            if os.path.isfile(filepath):
                self.organize_file(filepath)
    
    def organize_file(self, filepath):
        """
        Organizes files into respective folders (Documents or Videos) based on file type.
        """
        file_name, file_ext = os.path.splitext(filepath)
        if file_ext in self.document_types:
            # Organize documents
            self.move_file(filepath, 'Documents', self.document_types[file_ext])
        elif file_ext in self.video_types:
            # Organize videos
            self.organize_videos(filepath)
    
    def move_file(self, filepath, main_folder, sub_folder=None):
        """
        Moves the file to the specified main folder and sub-folder.
        Handles duplicates by renaming the file if needed.
        """
        # Create destination path
        base_folder = os.path.join(self.watch_folder, main_folder)
        if sub_folder:
            base_folder = os.path.join(base_folder, sub_folder)
        
        # Create folder if it doesn't exist
        os.makedirs(base_folder, exist_ok=True)

        # Destination file path
        target_path = os.path.join(base_folder, os.path.basename(filepath))

        # Handle duplicate files
        if os.path.exists(target_path):
            target_path = self.resolve_duplicate(target_path)

        # Move file
        shutil.move(filepath, target_path)
        print(f"Moved: {filepath} to {target_path}")

    def organize_videos(self, filepath):
        """
        Organizes video files into subfolders based on the video series.
        If a series already exists, it groups the video into that series folder.
        """
        filename = os.path.basename(filepath)
        match = re.match(r"(.+?) - Episode (\d+)", filename)
        
        if match:
            # Extract series name and create folder if not exists
            series_name = match.group(1).strip()
            series_folder = os.path.join(self.watch_folder, 'Videos', series_name)
            
            # Check if the folder exists, create if not
            if not os.path.exists(series_folder):
                os.makedirs(series_folder)  # Create only if it doesn't exist
            
            target_path = os.path.join(series_folder, filename)
            
            # Handle duplicate file names in the series folder
            if os.path.exists(target_path):
                target_path = self.resolve_duplicate(target_path)
            
            shutil.move(filepath, target_path)
            print(f"Grouped video: {filepath} into {series_folder}")
        else:
            # If the file does not match the episode pattern, just move it to Videos
            self.move_file(filepath, 'Videos')

    def resolve_duplicate(self, target_path):
        """
        Resolves file name duplication by appending a counter to the file name.
        """
        base, ext = os.path.splitext(target_path)
        counter = 1
        
        # Increment counter until a unique file name is found
        while os.path.exists(target_path):
            target_path = f"{base} ({counter}){ext}"
            counter += 1
        
        return target_path

def get_downloads_folder():
    """
    Returns the path to the user's Downloads folder.
    This is platform-independent and works on Windows, macOS, and Linux.
    """
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    elif os.name == 'posix':  # macOS or Linux
        return os.path.join(os.environ['HOME'], 'Downloads')
    else:
        raise Exception("Unsupported operating system")

def start_organizer(folder_to_watch):
    """
    Starts the file organizer and monitors the specified folder for new or modified files.
    """
    event_handler = FileOrganizerHandler(folder_to_watch)
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()
    print(f"Monitoring folder: {folder_to_watch}")
    
    try:
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_watch = get_downloads_folder()  # Automatically get Downloads folder path
    start_organizer(folder_to_watch)
