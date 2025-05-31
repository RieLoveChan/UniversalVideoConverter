# FFMPEG Script Generator

## Overview

This is a client-side HTML, CSS, and JavaScript application that helps users generate FFMPEG (FFmpeg) command scripts. It produces script text suitable for Windows Batch (`.bat`) files and Linux/macOS Shell (`.sh`) files.

The tool runs entirely in your web browser. No data is sent to any server, and no backend is required. You simply open the `index.html` file, input your desired video conversion parameters, and the tool generates the script text for you to copy and save.

## Features

- **Batch Processing**: Handles multiple files via drag-and-drop (Windows) or command-line arguments (Linux/macOS).
- **Customizable Output Suffix**: Output files can have custom suffixes (default: `_reencoded`).
- **Video Parameters**:
  - Resolution
  - Video Codec (`libx264`, `libx265`, `mpeg2video`, `vp9`, etc.)
  - Video Bitrate
  - Frame Rate
  - Video Filters (`-vf`)
  - Aspect Ratio
  - Preset (`ultrafast`, `medium`, etc.)
  - Profile and Level
  - CRF Value (`-crf`)
  - Pixel Format (`-pix_fmt`)
  - Hardware Acceleration (`-hwaccel`)
- **Audio Parameters**:
  - Audio Codec (`aac`, `libmp3lame`, `opus`, `flac`)
  - Audio Bitrate
  - Sampling Rate
  - Audio Channels
  - Volume Adjustment
  - Audio Filters (`-af`)
  - Advanced Filters (`-filter_complex`)
- **Cross-Platform**: Generates scripts for Windows Batch (`.bat`) and Linux/macOS Shell (`.sh`).
- **Configuration Management**:
  - Save your settings locally.
  - Load previously saved settings.
- **Fully Client-Side**: Operates entirely within the browser—no data is sent to any server.

## How to Use

1. **Open the Tool**:
   - Download the `index.html` file.
   - Open the downloaded `index.html` file in a modern web browser (e.g., Chrome, Firefox, Edge, Safari).

2. **Set Conversion Parameters**:
   - Configure your desired video and audio settings in the input fields/dropdowns.
   - Specify additional features such as CRF value, hardware acceleration, pixel format, advanced filters, and more.

3. **Set Output File Suffix**:
   - Use the "Output File Suffix" field to customize the suffix for the output filenames (default: `_reencoded`).

4. **Generate Scripts**:
   - Click the "Generate Scripts" button.

5. **View Scripts**:
   - The generated Windows Batch and Linux/macOS Shell script text will appear in their respective text areas.

6. **Copy Script**:
   - Click the "Copy Windows Script" or "Copy Linux Script" button to copy the desired script to your clipboard.

7. **Save Script**:
   - Open a plain text editor (like Notepad on Windows, TextEdit on Mac in plain text mode, or any code editor).
   - Paste the copied script text.
   - Save the file with the appropriate extension:
     - For Windows: e.g., `convert_video.bat`
     - For Linux/macOS: e.g., `convert_video.sh`

8. **Make Executable (Linux/macOS)**:
   - Open your terminal, navigate to where you saved the script, and make it executable:
     ```bash
     chmod +x convert_video.sh
     ```

9. **Prepare Files & Run**:
   - **Windows (.bat script)**:
     - Drag and drop one or more video files directly onto the `.bat` script icon.
     - The script will process each file, creating an output file with the specified suffix.
   - **Linux/macOS (.sh script)**:
     - Open your terminal.
     - Navigate to the directory containing the `.sh` script.
     - Provide the video files you want to convert as command-line arguments to the script. For example:
       ```bash
       ./convert_video.sh /path/to/your/video1.mp4 /another/path/video2.mkv "video with spaces.avi"
       ```

## Prerequisites

- **FFMPEG Installation**:
  - Ensure FFMPEG is installed on your system and its executable is accessible in your system's PATH environment variable.
  - Download FFMPEG from the official website: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
  - Follow the installation instructions specific to your operating system.

## Notes & Limitations

- **Script Generator, Not a Converter**:
  - This tool *generates script text*. It does not execute FFMPEG or perform any video conversion itself. You need to run the generated script on your local machine.

- **Parameter Accuracy**:
  - The success of the FFMPEG conversion depends on the validity and compatibility of the parameters chosen by the user.

- **Error Handling in Scripts**:
  - The generated scripts are basic and include simple `echo` statements. FFMPEG itself will output detailed error messages to the console if it encounters issues during conversion.

## Output Files and Naming

- Output files are saved in the **same directory** as their respective original input files.
- The script appends the custom suffix to the original filename before the extension. For example, if you process `myVideo.mp4` with `_customSuffix`, the output will be `myVideo_customSuffix.mp4`.
- If a file with the same name already exists in the source directory, FFMPEG (due to the `-y` flag in the command) will **overwrite it without prompting**.

## License

This project is open-source and licensed under the MIT License. Feel free to modify and use it for your own projects!
