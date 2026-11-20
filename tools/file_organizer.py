#!/usr/bin/env python3
"""
File Organizer - Organizes files in a directory by their type
Usage: python file_organizer.py /path/to/directory
"""

import os
import shutil
from pathlib import Path
from typing import Dict

# File type categories
FILE_CATEGORIES: Dict[str, list] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".key"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c"],
    "Executables": [".exe", ".msi", ".deb", ".dmg"],
}


def get_category(file_extension: str) -> str:
    """Get the category for a file based on its extension."""
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category
    return "Others"


def organize_files(directory: str) -> None:
    """Organize files in the given directory."""
    path = Path(directory)

    if not path.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return

    # Create category folders
    for category in FILE_CATEGORIES.keys():
        (path / category).mkdir(exist_ok=True)
    (path / "Others").mkdir(exist_ok=True)

    # Move files
    moved_count = 0
    for file in path.iterdir():
        if file.is_file():
            category = get_category(file.suffix)
            destination = path / category / file.name

            # Handle duplicate filenames
            counter = 1
            while destination.exists():
                new_name = f"{file.stem}_{counter}{file.suffix}"
                destination = path / category / new_name
                counter += 1

            shutil.move(str(file), str(destination))
            moved_count += 1
            print(f"Moved: {file.name} → {category}/")

    print(f"\n✅ Organized {moved_count} files successfully!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python file_organizer.py /path/to/directory")
        sys.exit(1)

    organize_files(sys.argv[1])
