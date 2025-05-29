#!/usr/bin/env python3

import subprocess
import json
import argparse


def get_video_info(file_path: str):
    """
    Retrieves video information using ffprobe.
    Returns a dictionary with extracted info, or None on failure.
    """
    ffprobe_command = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]
    try:
        process = subprocess.run(ffprobe_command, capture_output=True, text=True, check=True)
        data = json.loads(process.stdout)
        
        info = {}
        
        # Extract format information
        if 'format' in data:
            format_data = data['format']
            info['format_name'] = format_data.get('format_name')
            info['duration'] = float(format_data.get('duration', 0))
            info['size'] = int(format_data.get('size', 0))
            info['bit_rate'] = int(format_data.get('bit_rate', 0))
            
        # Extract video stream information
        video_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'video'), None)
        if video_stream:
            info['video_codec_name'] = video_stream.get('codec_name')
            info['width'] = int(video_stream.get('width', 0))
            info['height'] = int(video_stream.get('height', 0))
            info['avg_frame_rate'] = video_stream.get('avg_frame_rate')
        else:
            info['video_codec_name'] = None
            info['width'] = None
            info['height'] = None
            info['avg_frame_rate'] = None

        # Extract audio stream information
        audio_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'audio'), None)
        if audio_stream:
            info['audio_codec_name'] = audio_stream.get('codec_name')
            info['sample_rate'] = int(audio_stream.get('sample_rate', 0))
            info['channels'] = int(audio_stream.get('channels', 0))
        else:
            info['audio_codec_name'] = None
            info['sample_rate'] = None
            info['channels'] = None
            
        return info
        
    except FileNotFoundError:
        print("Error: ffprobe command not found. Please ensure FFMPEG (which includes ffprobe) is installed and in your PATH.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error during ffprobe execution. FFPROBE stderr:\n{e.stderr}")
        return None
    except json.JSONDecodeError:
        print("Error: Could not parse ffprobe output.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while getting video info: {e}")
        return None

def print_video_info(info: dict):
    """Prints video information in a human-readable format."""
    print("\n--- Video Information ---")
    if info.get('format_name'):
        print(f"Format: {info['format_name']}")
    if info.get('duration') is not None:
        print(f"Duration: {info['duration']:.2f} s")
    if info.get('size') is not None:
        print(f"Size: {info['size'] / (1024*1024):.2f} MB") # More readable size
    if info.get('bit_rate') is not None:
        print(f"Overall Bit Rate: {info['bit_rate'] // 1000} kbps") # More readable bit_rate

    if info.get('video_codec_name'):
        print(f"Video Codec: {info['video_codec_name']}")
    if info.get('width') and info.get('height'):
        print(f"Resolution: {info['width']}x{info['height']}")
    if info.get('avg_frame_rate'):
        # Evaluate avg_frame_rate if it's a fraction (e.g., "30000/1001")
        try:
            num, den = map(int, info['avg_frame_rate'].split('/'))
            fps = num / den
            print(f"Frame Rate: {fps:.2f} fps ({info['avg_frame_rate']})")
        except (ValueError, ZeroDivisionError, AttributeError):
             print(f"Frame Rate: {info['avg_frame_rate']}") # Print as is if not a simple fraction

    if info.get('audio_codec_name'):
        print(f"Audio Codec: {info['audio_codec_name']}")
    if info.get('sample_rate') is not None:
        print(f"Sample Rate: {info['sample_rate'] // 1000} kHz") # More readable sample_rate
    if info.get('channels') is not None:
        print(f"Channels: {info['channels']}")
    print("-----------------------\n")

def convert_video(input_file: str, output_file: str, resolution: str | None, video_codec: str, audio_codec: str, bitrate: str | None):
    """Converts video using FFMPEG with specified options."""
    ffmpeg_command = ["ffmpeg", "-i", input_file]

    if resolution:
        ffmpeg_command.extend(["-s", resolution])
    
    ffmpeg_command.extend(["-c:v", video_codec])
    ffmpeg_command.extend(["-c:a", audio_codec])

    if bitrate:
        ffmpeg_command.extend(["-b:v", bitrate])
    
    ffmpeg_command.extend(["-y", output_file]) # -y to overwrite output

    print(f"Executing FFMPEG command: {' '.join(ffmpeg_command)}")

    try:
        process = subprocess.run(ffmpeg_command, capture_output=True, text=True, check=True)
        print(f"Successfully converted '{input_file}' to '{output_file}'")
        if process.stdout:
            print(f"FFMPEG stdout:\n{process.stdout}")
        if process.stderr: # Should be empty on success with check=True, but good practice
            print(f"FFMPEG stderr:\n{process.stderr}")
            
    except FileNotFoundError:
        print("Error: ffmpeg command not found. Please ensure FFMPEG is installed and in your PATH.")
        sys.exit(1) # Consider re-raising or returning status
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion. FFMPEG command: '{' '.join(e.cmd)}'")
        print(f"FFMPEG stderr:\n{e.stderr}")
        sys.exit(1) # Consider re-raising or returning status
    except Exception as e:
        print(f"An unexpected error occurred during conversion: {e}")
        sys.exit(1) # Consider re-raising or returning status

def load_presets(filename: str = "presets.json") -> dict:
    """Loads presets from a JSON file."""
    try:
        with open(filename, 'r') as f:
            presets = json.load(f)
        return presets
    except FileNotFoundError:
        print(f"Warning: Preset file '{filename}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode preset file '{filename}'. Make sure it's valid JSON.")
        return {} # Or sys.exit(1) if presets are critical
    except Exception as e:
        print(f"An unexpected error occurred while loading presets: {e}")
        return {}


def main():
    parser = argparse.ArgumentParser(description="Convert video files using FFMPEG with customizable options. CLI options override presets.")
    parser.add_argument("input_file", help="Path to the input video file.")
    parser.add_argument("output_file", help="Path for the output converted video file.")
    
    # Conversion options
    parser.add_argument("--resolution", "-r", type=str, default=None, help="Output resolution, e.g., '1280x720'. Overrides preset.")
    parser.add_argument("--video-codec", "-vc", type=str, default=None, help="Video codec, e.g., 'libx264', 'libvpx-vp9'. Overrides preset.")
    parser.add_argument("--audio-codec", "-ac", type=str, default=None, help="Audio codec, e.g., 'aac', 'libopus'. Overrides preset.")
    parser.add_argument("--bitrate", "-b", type=str, default=None, help="Video bitrate, e.g., '1M', '2000k'. Overrides preset.")
    
    parser.add_argument("--preset", "-p", type=str, help="Name of the preset to use from presets.json.")
    
    args = parser.parse_args()

    # Determine effective conversion options
    effective_resolution = args.resolution
    effective_video_codec = args.video_codec
    effective_audio_codec = args.audio_codec
    effective_bitrate = args.bitrate

    # Argparse defaults for codecs if not specified by CLI or preset
    default_video_codec_argparse = "libx264"
    default_audio_codec_argparse = "aac"

    if args.preset:
        presets = load_presets()
        if not presets:
            print(f"Could not load presets. If you specified a preset '{args.preset}', it cannot be applied.")
            # Depending on desired strictness, could exit here. For now, will proceed without preset.
        elif args.preset in presets:
            print(f"Applying preset: {args.preset}")
            preset_values = presets[args.preset]
            
            # Preset values are applied first if the corresponding CLI arg was not set
            if effective_resolution is None:
                effective_resolution = preset_values.get("resolution")
            if effective_video_codec is None:
                effective_video_codec = preset_values.get("video_codec")
            if effective_audio_codec is None:
                effective_audio_codec = preset_values.get("audio_codec")
            if effective_bitrate is None:
                effective_bitrate = preset_values.get("bitrate")
        else:
            print(f"Error: Preset '{args.preset}' not found in presets.json. Available presets: {', '.join(presets.keys())}")
            sys.exit(1)

    # Apply argparse defaults if no CLI or preset value was found
    if effective_video_codec is None:
        effective_video_codec = default_video_codec_argparse
    if effective_audio_codec is None:
        effective_audio_codec = default_audio_codec_argparse
    
    # Get and print video information before conversion
    video_info = get_video_info(args.input_file)
    if video_info:
        print_video_info(video_info)
    else:
        print("Could not retrieve video information. Exiting without conversion.")
        sys.exit(1)

    print(f"Proceeding with conversion of '{args.input_file}' to '{args.output_file}' with specified options...\n")
    
    convert_video(
        args.input_file,
        args.output_file,
        effective_resolution,
        effective_video_codec,
        effective_audio_codec,
        effective_bitrate
    )

if __name__ == "__main__":
    main()
