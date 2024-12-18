# Groupie

Groupie is a Python script that automatically organizes files in a specified folder (default: Downloads) based on their type. Documents are grouped by file type, and video files are grouped into series based on their names. It resolves duplicate files by renaming them.

## Features

- **Monitors a specified folder** (default is `Downloads`) for new or modified files.
- **Organizes documents** into subfolders based on file types such as PDFs, Word Documents, and Text Files.
- **Organizes videos** into folders based on their series, creating separate folders for each video series.
- **Handles duplicate files** by renaming them (e.g., `filename (1).ext`).
- **Cross-platform**: Works on Windows, macOS, and Linux.


## Requirements
- Python 3.6+  
- `watchdog` library for monitoring folder changes

## Installation
clone repo:
```bash
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer
```

### Install Dependencies

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

### Configure the folder to watch
By default, the script watches the Downloads folder. If you want to monitor a different folder, you can update the folder_to_watch variable in the __main__ section of the script.

If you want to monitor a custom folder, you can manually specify the path by modifying the script as follows:

```python
folder_to_watch = r"C:\Path\To\Your\Folder"
```
### Running the Script
Run the script with:

```bash
python file_organizer.py
```
Once started, the script will monitor the Downloads (or the specified folder) for any new files added or modified. When files are detected, they will be organized into appropriate folders (e.g., PDFs, WordDocs, Videos).

### Stopping the Script
To stop the script, simply interrupt it by pressing Ctrl + C.

## File Organization Details
Documents: Files with the extensions .pdf, .docx, and .txt will be moved to the Documents folder. Inside, they will be further grouped by their file type (e.g., PDFs, WordDocs, TextFiles).
Videos: Files with extensions .mp4, .mkv, and .avi will be moved to the Videos folder. Videos will be grouped by their series name if the file name follows the pattern Series Name - Episode X.
Example video filename format:

```
Series Name - Episode 1.mp4
Series Name - Episode 2.mkv
```
If a video file is detected that doesn't follow this format, it will be grouped under the Videos folder.

## Handling Duplicates
If a file with the same name already exists in the target folder, the script will rename the file by appending a number in parentheses to its name (e.g., filename (1).ext).

## Troubleshooting
Ensure that the folder to monitor exists and that the script has read and write permissions.
Make sure all dependencies are installed by running pip install -r requirements.txt.
