# HTML5 FFMPEG Script Generator

## Overview

This is a client-side HTML, CSS, and JavaScript application that helps users generate FFMPEG (FFmpeg) command scripts. It produces script text suitable for Windows Batch (`.bat`) files and Linux/macOS Shell (`.sh`) files.

The tool runs entirely in your web browser. No data is sent to any server, and no backend is required. You simply open the `index.html` file, input your desired video conversion parameters, and the tool generates the script text for you to copy and save.

## How to Use

This tool is provided as a single `index.html` file that includes all necessary styles and scripts.

1.  **Open the Tool:**
    *   Download the `index.html` file.
    *   Open the downloaded `index.html` file in a modern web browser (e.g., Chrome, Firefox, Edge, Safari).

2.  **Fill in Parameters:**
    *   In the "Input Parameters" section, fill in the fields:
        *   **Input Video File (Placeholder Name):** The name you want to use as a placeholder for your input file in the script (e.g., `my_video.mp4`).
        *   **Output Video File (Placeholder Name):** The name for the output file placeholder (e.g., `converted_video.mkv`).
        *   **Resolution (Optional):** Desired output resolution like `1280x720`. Leave blank to use the original.
        *   **Video Codec (Optional):** Specify a video codec (e.g., `libx264`, `libvpx-vp9`). Defaults to `libx264`.
        *   **Audio Codec (Optional):** Specify an audio codec (e.g., `aac`, `libopus`). Defaults to `aac`.
        *   **Video Bitrate (Optional):** Set a video bitrate like `1M` (1 Mbps) or `2000k` (2000 Kbps). Leave blank for FFMPEG's default.

3.  **Generate Scripts:**
    *   Click the "Generate Scripts" button.

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
        Detailed instructions for macOS users, including Terminal commands and notes on installing FFMPEG via Homebrew, are available in the collapsible "▶ Instructions for macOS Users" section directly within the application.

8.  **Prepare Files & Run:**
    *   The generated scripts use the placeholder filenames you entered in the form.
    *   **Option 1 (Recommended):** Rename your actual input video file to match the "Input Video File (Placeholder Name)" you used in the form (e.g., rename your video to `my_video.mp4` if that was your placeholder).
    *   **Option 2:** Alternatively, edit the script file you saved and replace the placeholder names directly within the script with your actual filenames.
    *   Place the script in the same directory as your input video file. If your video file is elsewhere, you'll need to adjust the paths in the script.
    *   Run the script from your command line or terminal:
        *   Windows: `convert_video.bat` (or double-click it)
        *   Linux/macOS: `./convert_video.sh`

## Prerequisites (for the generated scripts to work)

*   **FFMPEG Installation:** This is crucial. The generated scripts **will not work** unless FFMPEG is installed on your system and its executable is accessible in your system's PATH environment variable.
*   Download FFMPEG from the official website: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html). Follow the installation instructions specific to your operating system.

## Features

*   Generates FFMPEG command scripts for Windows Batch (`.bat`) and Linux/macOS Shell (`.sh`) environments.
*   Customizable FFMPEG parameters: input/output file placeholders, resolution, video codec, audio codec, and video bitrate.
*   Applies default video (`libx264`) and audio (`aac`) codecs if not specified by the user.
*   Automatically includes `-y` in the FFMPEG command to overwrite output files without prompting.
*   Quotes filenames in the FFMPEG command to handle spaces.
*   "Copy to Clipboard" functionality for easy retrieval of the generated scripts.
*   Responsive user interface design for usability on different screen sizes.
*   Includes a collapsible section with specific instructions for macOS users (Terminal usage, Homebrew for FFMPEG).
*   Fully client-side: operates entirely within the browser, ensuring privacy as no data is sent to any server.

## Notes & Limitations

*   **Script Generator, Not a Converter:** This tool *generates script text*. It does not execute FFMPEG or perform any video conversion itself. You need to run the generated script on your local machine.
*   **FFMPEG Dependency:** The functionality of the generated scripts is entirely dependent on a correct FFMPEG installation on the user's system.
*   **Parameter Accuracy:** The success of the FFMPEG conversion depends on the validity and compatibility of the parameters chosen by the user.
*   **File Placeholders:** The script uses the exact placeholder names you provide in the form. You must ensure these align with your actual file names when you run the script, or modify the script manually.
*   **Error Handling in Scripts:** The generated scripts are basic and include simple `echo` statements. FFMPEG itself will output detailed error messages to the console if it encounters issues during conversion.

---
*This README replaces information about any previous Python CLI tool that might have existed in this repository.*
