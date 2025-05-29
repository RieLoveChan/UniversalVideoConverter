# HTML5 FFMPEG Script Generator

## Overview

This is a client-side HTML, CSS, and JavaScript application that helps users generate FFMPEG (FFmpeg) command scripts. It produces script text suitable for Windows Batch (`.bat`) files and Linux/macOS Shell (`.sh`) files.

The tool runs entirely in your web browser. No data is sent to any server, and no backend is required. You simply open the `index.html` file, input your desired video conversion parameters, and the tool generates the script text for you to copy and save.

## How to Use

This tool is provided as a single `index.html` file that includes all necessary styles and scripts.

1.  **Open the Tool:**
    *   Download the `index.html` file.
    *   Open the downloaded `index.html` file in a modern web browser (e.g., Chrome, Firefox, Edge, Safari).

2.  **Set Conversion Parameters:**
    *   In the "Input Parameters" section, configure the desired video conversion settings:
        *   **Resolution (Optional):** e.g., `1280x720`. Leave blank to use the original.
        *   **Video Codec (Optional):** e.g., `libx264`, `libvpx-vp9`. Defaults to `libx264`.
        *   **Audio Codec (Optional):** e.g., `aac`, `libopus`. Defaults to `aac`.
        *   **Video Bitrate (Optional):** e.g., `1M` (for 1 Mbps), `2000k` (for 2000 Kbps). Leave blank for FFMPEG's default.
    *   Note: Specific input and output filenames are not set here; the generated scripts are designed to process files provided at runtime.

3.  **Generate Scripts:**
    *   Click the "⚙️ Generate Scripts" button.

4.  **View Scripts:**
    *   The generated Windows Batch and Linux/macOS Shell script text will appear in their respective textareas.

5.  **Copy Script:**
    *   Click the "Copy Windows Script" or "Copy Linux Script" button to copy the desired script to your clipboard.

6.  **Save Script:**
    *   Open a plain text editor (like Notepad on Windows, TextEdit on Mac in plain text mode, or any code editor).
    *   Paste the copied script text.
    *   Save the file with the appropriate extension:
        *   For Windows: e.g., `convert_video.bat`
        *   For Linux/macOS: e.g., `convert_video.sh`

7.  **Make Executable (Linux/macOS):**
    *   For Linux/macOS, open your terminal, navigate to where you saved the script, and make it executable:
        ```bash
        chmod +x convert_video.sh
        ```
        Detailed instructions for macOS users, including Terminal commands and notes on installing FFMPEG via Homebrew, are available in the collapsible "ℹ️ Instructions for macOS Users" section directly within the application.

8.  **Prepare Files & Run:**
    *   Place the generated script (`.bat` or `.sh`) in a convenient directory.
    *   **For Windows (.bat script):**
        *   Drag and drop one or more video files directly onto the `.bat` script icon.
        *   The script will process each file, creating an output file with `_reencoded` appended to its original name in the same directory as the input file.
    *   **For Linux/macOS (.sh script):**
        *   Open your Terminal.
        *   Navigate to the directory containing the `.sh` script.
        *   Provide the video files you want to convert as command-line arguments to the script. For example:
            ```bash
            ./convert_video.sh /path/to/your/video1.mp4 /another/path/video2.mkv "video with spaces.avi"
            ```
        *   You can often drag files from Finder (macOS) or your file manager (Linux) directly into the Terminal window after typing the script name and a space, which will paste their full paths.
        *   The script will process each file, creating an output file with `_reencoded` appended to its original name in the same directory as its respective input file.

## Prerequisites (for the generated scripts to work)

*   **FFMPEG Installation:** This is crucial. The generated scripts **will not work** unless FFMPEG is installed on your system and its executable is accessible in your system's PATH environment variable.
*   Download FFMPEG from the official website: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html). Follow the installation instructions specific to your operating system.

## Features

*   Generates FFMPEG command scripts for Windows Batch (`.bat`) and Linux/macOS Shell (`.sh`) environments.
*   Batch processing: Handles multiple files via drag-and-drop (Windows) or command-line arguments (Linux/macOS).
*   Automatic output naming: Output files are automatically named by appending `_reencoded` to the original filename (e.g., `video.mp4` becomes `video_reencoded.mp4`).
*   Customizable FFMPEG conversion parameters: resolution, video codec, audio codec, and video bitrate.
*   Applies default video (`libx264`) and audio (`aac`) codecs if not specified by the user.
*   Automatically includes `-y` in the FFMPEG command to overwrite output files without prompting (if an output file with the `_reencoded` name already exists).
*   "Copy to Clipboard" functionality for easy retrieval of the generated scripts.
*   Enhanced iOS-inspired UI with refined text colors and descriptive icons.
*   Includes a collapsible section with specific instructions for macOS users (Terminal usage, Homebrew for FFMPEG).
*   Fully client-side: operates entirely within the browser, ensuring privacy as no data is sent to any server.

## Output Files and Naming

*   Output files are saved in the **same directory** as their respective original input files.
*   The script appends an `_reencoded` suffix to the original filename before the extension. For example, if you process `myVideo.mp4`, the output will be `myVideo_reencoded.mp4`.
*   If a file named `originalName_reencoded.extension` already exists in the source directory, FFMPEG (due to the `-y` flag in the command) will **overwrite it without prompting**. Be mindful of this if re-running scripts on files that have already been processed or if you have other files that coincidentally match this naming pattern.

## Notes & Limitations

*   **Script Generator, Not a Converter:** This tool *generates script text*. It does not execute FFMPEG or perform any video conversion itself. You need to run the generated script on your local machine.
*   **FFMPEG Dependency:** The functionality of the generated scripts is entirely dependent on a correct FFMPEG installation on the user's system.
*   **Parameter Accuracy:** The success of the FFMPEG conversion depends on the validity and compatibility of the parameters chosen by the user.
*   **Error Handling in Scripts:** The generated scripts are basic and include simple `echo` statements. FFMPEG itself will output detailed error messages to the console if it encounters issues during conversion.

---
*This README replaces information about any previous Python CLI tool that might have existed in this repository.*
