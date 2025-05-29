# Command-Line Video Converter

## Introduction

This script provides a command-line interface for converting video files using FFMPEG. It allows for customizable conversion options including resolution, video/audio codecs, and bitrate. Additionally, it supports presets defined in a JSON file for common conversion settings and uses FFPROBE to display information about the input video before processing.

## Prerequisites/Setup

1.  **FFMPEG and FFPROBE:**
    *   This script relies on FFMPEG (for conversion) and FFPROBE (for video information). You **must** have them installed and accessible in your system's PATH.
    *   Download FFMPEG (which includes FFPROBE) from the official website: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
    *   Follow the installation instructions for your operating system.

2.  **Python 3:**
    *   The script is written for Python 3. Ensure you have Python 3 installed. You can check by running `python3 --version`.

3.  **Making the Script Executable (Optional but Recommended):**
    *   To run the script directly (e.g., `./converter.py` instead of `python3 converter.py`), make it executable:
        ```bash
        chmod +x converter.py
        ```

## Usage

The script is run from the command line.

**Basic Syntax:**

```bash
python3 converter.py [OPTIONS] <input_file> <output_file>
```

Or, if you've made it executable:

```bash
./converter.py [OPTIONS] <input_file> <output_file>
```

For a full list of up-to-date options and their descriptions, run:
```bash
python3 converter.py --help
```

### Command-Line Arguments:

*   **`input_file`**: (Positional) The path to the video file you want to convert.
*   **`output_file`**: (Positional) The desired path and filename for the converted video.
*   **`--resolution FORMAT`, `-r FORMAT`**:
    *   Set the output video resolution (e.g., "1280x720", "1920x1080").
*   **`--video-codec CODEC`, `-vc CODEC`**:
    *   Specify the video codec for the output file (e.g., "libx264", "libvpx-vp9").
    *   Defaults to "libx264" if not specified by a preset or this argument.
*   **`--audio-codec CODEC`, `-ac CODEC`**:
    *   Specify the audio codec for the output file (e.g., "aac", "libopus").
    *   Defaults to "aac" if not specified by a preset or this argument.
*   **`--bitrate RATE`, `-b RATE`**:
    *   Set the video bitrate (e.g., "1M", "2000k", "500K").
*   **`--preset NAME`, `-p NAME`**:
    *   Use a predefined set of options from the `presets.json` file. Command-line arguments can override preset values.

### Usage Examples:

1.  **Default Conversion (H.264 video, AAC audio):**
    ```bash
    python3 converter.py input.mov output.mp4
    ```

2.  **Convert to 720p with a specific video bitrate:**
    ```bash
    python3 converter.py input.avi -r 1280x720 -b 1500k output.mp4
    ```

3.  **Convert using VP9 video codec and Opus audio codec:**
    ```bash
    python3 converter.py input.webm -vc libvpx-vp9 -ac libopus output_vp9.mkv
    ```

4.  **Using a preset named `vp9_opus_720p` (defined in `presets.json`):**
    ```bash
    python3 converter.py input.mp4 -p vp9_opus_720p output_preset.mkv
    ```

5.  **Using a preset but overriding the bitrate:**
    ```bash
    python3 converter.py input.mp4 -p vp9_opus_720p -b 2M output_preset_custom_bitrate.mkv
    ```

## Presets

The script supports loading default conversion settings from a `presets.json` file located in the same directory as `converter.py`.

### `presets.json` Structure:

The file should contain a JSON object where each key is a preset name. The value for each preset name is another object that can define `resolution`, `video_codec`, `audio_codec`, and `bitrate`. An optional `description` field can be added for clarity; it is not used by FFMPEG.

**Example `presets.json`:**
```json
{
  "default_h264_aac": {
    "video_codec": "libx264",
    "audio_codec": "aac",
    "description": "Standard MP4 with H.264 video and AAC audio."
  },
  "vp9_opus_720p": {
    "resolution": "1280x720",
    "video_codec": "libvpx-vp9",
    "audio_codec": "libopus",
    "bitrate": "1M",
    "description": "VP9 video with Opus audio at 720p resolution and 1Mbps bitrate."
  },
  "low_res_test": {
    "resolution": "640x360",
    "video_codec": "libx264",
    "audio_codec": "aac",
    "bitrate": "500k",
    "description": "Low resolution for quick testing."
  }
}
```

### Order of Precedence for Options:
1.  **Hardcoded defaults in script** (for video/audio codec if not specified elsewhere).
2.  **Values from the loaded preset**, if `--preset` is used.
3.  **Explicitly provided command-line arguments** (these always override preset values or defaults).

## Video Information

Before starting the conversion, the script uses `ffprobe` to display key information about the input video, such as its format, duration, size, resolution, and codec details for video and audio streams.

## Error Handling

The script includes error handling for several common issues:
*   FFMPEG or FFPROBE not found in PATH.
*   Invalid input files or formats that FFMPEG cannot handle.
*   Errors during the conversion process (FFMPEG will usually output specific error messages).
*   Issues with loading or parsing the `presets.json` file.
*   Incorrect number of command-line arguments.

Please check the console output for error messages if a conversion fails.

## Running Tests

The project includes unit tests to verify the functionality of the script's logic (excluding actual FFMPEG/FFPROBE execution).

To run the tests:

1.  Ensure you are in the root directory of the project (the one containing `converter.py` and the `tests/` directory).
2.  Run the following command:

    ```bash
    python3 -m unittest discover tests
    ```

    Or, for a more verbose output:

    ```bash
    python3 -m unittest discover -v tests
    ```

This will automatically find and run all tests defined in `tests/test_converter.py`.
