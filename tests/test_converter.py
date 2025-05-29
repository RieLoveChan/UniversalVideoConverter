import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import subprocess # Required for CalledProcessError
from argparse import Namespace

# Adjust the import path if your project structure is different
# This assumes 'converter.py' is in the parent directory of 'tests'
# and the root directory has an __init__.py to make 'converter' a package.
from converter import get_video_info, convert_video, load_presets, main

class TestGetVideoInfo(unittest.TestCase):

    sample_ffprobe_output_valid = {
        "streams": [
            {
                "codec_type": "video",
                "codec_name": "h264",
                "width": 1920,
                "height": 1080,
                "avg_frame_rate": "30/1"
            },
            {
                "codec_type": "audio",
                "codec_name": "aac",
                "sample_rate": "48000",
                "channels": 2
            }
        ],
        "format": {
            "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
            "duration": "120.500000",
            "size": "5000000",
            "bit_rate": "332000"
        }
    }

    sample_ffprobe_output_no_audio = {
        "streams": [
            {
                "codec_type": "video",
                "codec_name": "vp9",
                "width": 1280,
                "height": 720,
                "avg_frame_rate": "25/1"
            }
        ],
        "format": {
            "format_name": "webm",
            "duration": "60.000000",
            "size": "2500000",
            "bit_rate": "100000"
        }
    }

    @patch('converter.subprocess.run')
    def test_successful_parsing(self, mock_run):
        mock_process = MagicMock()
        mock_process.stdout = json.dumps(self.sample_ffprobe_output_valid)
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        expected_info = {
            'format_name': 'mov,mp4,m4a,3gp,3g2,mj2',
            'duration': 120.5,
            'size': 5000000,
            'bit_rate': 332000,
            'video_codec_name': 'h264',
            'width': 1920,
            'height': 1080,
            'avg_frame_rate': '30/1',
            'audio_codec_name': 'aac',
            'sample_rate': 48000,
            'channels': 2
        }
        self.assertEqual(get_video_info("dummy.mp4"), expected_info)

    @patch('converter.subprocess.run')
    def test_missing_audio_stream(self, mock_run):
        mock_process = MagicMock()
        mock_process.stdout = json.dumps(self.sample_ffprobe_output_no_audio)
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        expected_info = {
            'format_name': 'webm',
            'duration': 60.0,
            'size': 2500000,
            'bit_rate': 100000,
            'video_codec_name': 'vp9',
            'width': 1280,
            'height': 720,
            'avg_frame_rate': '25/1',
            'audio_codec_name': None,
            'sample_rate': None,
            'channels': None
        }
        self.assertEqual(get_video_info("dummy.webm"), expected_info)

    @patch('converter.subprocess.run')
    def test_ffprobe_called_process_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd", stderr="ffprobe error")
        # Suppress print output during this test
        with patch('builtins.print') as mock_print:
            self.assertIsNone(get_video_info("dummy.mp4"))
            mock_print.assert_any_call("Error during ffprobe execution. FFPROBE stderr:\nffprobe error")


    @patch('converter.subprocess.run')
    def test_json_decode_error(self, mock_run):
        mock_process = MagicMock()
        mock_process.stdout = "this is not json"
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        with patch('builtins.print') as mock_print:
            self.assertIsNone(get_video_info("dummy.mp4"))
            mock_print.assert_any_call("Error: Could not parse ffprobe output.")

    @patch('converter.subprocess.run')
    def test_file_not_found_error(self, mock_run):
        mock_run.side_effect = FileNotFoundError("ffprobe not found")
        with patch('builtins.print') as mock_print:
            self.assertIsNone(get_video_info("dummy.mp4"))
            mock_print.assert_any_call("Error: ffprobe command not found. Please ensure FFMPEG (which includes ffprobe) is installed and in your PATH.")


class TestConvertVideoCommand(unittest.TestCase):

    @patch('converter.subprocess.run')
    def test_default_codecs(self, mock_run):
        convert_video("input.mp4", "output.mp4", None, "libx264", "aac", None)
        expected_command = ["ffmpeg", "-i", "input.mp4", "-c:v", "libx264", "-c:a", "aac", "-y", "output.mp4"]
        mock_run.assert_called_once()
        self.assertEqual(mock_run.call_args[0][0], expected_command)

    @patch('converter.subprocess.run')
    def test_all_options(self, mock_run):
        convert_video("input.avi", "output.mkv", "1280x720", "libvpx-vp9", "libopus", "1500k")
        expected_command = [
            "ffmpeg", "-i", "input.avi",
            "-s", "1280x720",
            "-c:v", "libvpx-vp9",
            "-c:a", "libopus",
            "-b:v", "1500k",
            "-y", "output.mkv"
        ]
        mock_run.assert_called_once()
        self.assertEqual(mock_run.call_args[0][0], expected_command)

    @patch('converter.subprocess.run')
    def test_only_resolution_and_bitrate(self, mock_run):
        convert_video("input.mp4", "output.mp4", "1920x1080", "libx264", "aac", "2M")
        expected_command = [
            "ffmpeg", "-i", "input.mp4",
            "-s", "1920x1080",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:v", "2M",
            "-y", "output.mp4"
        ]
        mock_run.assert_called_once()
        self.assertEqual(mock_run.call_args[0][0], expected_command)


class TestLoadPresets(unittest.TestCase):
    sample_presets_content = """
{
  "test1": {"video_codec": "libx264"},
  "test2": {"resolution": "1024x768"}
}
"""
    invalid_json_content = "this is not json"

    @patch("builtins.open", new_callable=mock_open, read_data=sample_presets_content)
    def test_load_valid_presets(self, mock_file):
        expected = {"test1": {"video_codec": "libx264"}, "test2": {"resolution": "1024x768"}}
        self.assertEqual(load_presets("dummy_presets.json"), expected)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_presets_file_not_found(self, mock_file):
        with patch('builtins.print') as mock_print:
            self.assertEqual(load_presets("nonexistent.json"), {})
            mock_print.assert_any_call("Warning: Preset file 'nonexistent.json' not found.")


    @patch("builtins.open", new_callable=mock_open, read_data=invalid_json_content)
    def test_load_presets_invalid_json(self, mock_file):
        with patch('builtins.print') as mock_print:
            self.assertEqual(load_presets("invalid_presets.json"), {})
            mock_print.assert_any_call("Error: Could not decode preset file 'invalid_presets.json'. Make sure it's valid JSON.")

# For testing option precedence, we need to mock argparse and parts of main.
# This is more of an integration test for the argument parsing and option merging logic.
class TestOptionPrecedence(unittest.TestCase):

    # Mock 'get_video_info' and 'print_video_info' as they are not relevant to option testing and require file access.
    # Also mock 'convert_video' to just capture the options passed to it.
    @patch('converter.get_video_info', return_value={"format_name": "dummy_format"}) # Needs to return non-None to proceed
    @patch('converter.print_video_info')
    @patch('converter.convert_video')
    @patch('converter.load_presets') # We'll provide presets directly
    @patch('argparse.ArgumentParser.parse_args')
    def run_main_with_args(self, cli_args, presets_data, mock_parse_args, mock_load_presets, mock_convert_video, mock_print_info, mock_get_info):
        # Configure mocks
        mock_parse_args.return_value = Namespace(**cli_args)
        mock_load_presets.return_value = presets_data
        
        # Call main, which contains the option precedence logic
        # We need to catch SystemExit because main calls sys.exit() on preset not found.
        try:
            main()
        except SystemExit: 
            pass # Expected if preset not found and test is designed for it
            
        # Return the arguments passed to convert_video
        if mock_convert_video.called:
            return mock_convert_video.call_args[0] # Returns a tuple of args
        return None


    def test_cli_only_no_defaults_changed(self):
        cli_args = {
            "input_file": "in.mp4", "output_file": "out.mp4",
            "resolution": None, "video_codec": None, "audio_codec": None, "bitrate": None, "preset": None
        }
        args_passed = self.run_main_with_args(cli_args, {})
        self.assertIsNotNone(args_passed)
        self.assertEqual(args_passed[0], "in.mp4")          # input_file
        self.assertEqual(args_passed[1], "out.mp4")         # output_file
        self.assertIsNone(args_passed[2])                   # resolution
        self.assertEqual(args_passed[3], "libx264")         # video_codec (default)
        self.assertEqual(args_passed[4], "aac")             # audio_codec (default)
        self.assertIsNone(args_passed[5])                   # bitrate

    def test_cli_overrides_defaults(self):
        cli_args = {
            "input_file": "in.mp4", "output_file": "out.mp4",
            "resolution": "1920x1080", "video_codec": "libvpx-vp9", "audio_codec": "libopus", "bitrate": "2M", "preset": None
        }
        args_passed = self.run_main_with_args(cli_args, {})
        self.assertIsNotNone(args_passed)
        self.assertEqual(args_passed[2], "1920x1080")
        self.assertEqual(args_passed[3], "libvpx-vp9")
        self.assertEqual(args_passed[4], "libopus")
        self.assertEqual(args_passed[5], "2M")

    def test_preset_only(self):
        cli_args = {
            "input_file": "in.mp4", "output_file": "out.mp4",
            "resolution": None, "video_codec": None, "audio_codec": None, "bitrate": None, "preset": "p1"
        }
        presets_data = {
            "p1": {"resolution": "1280x720", "video_codec": "preset_vc", "audio_codec": "preset_ac", "bitrate": "1M"}
        }
        args_passed = self.run_main_with_args(cli_args, presets_data)
        self.assertIsNotNone(args_passed)
        self.assertEqual(args_passed[2], "1280x720")
        self.assertEqual(args_passed[3], "preset_vc")
        self.assertEqual(args_passed[4], "preset_ac")
        self.assertEqual(args_passed[5], "1M")

    def test_cli_overrides_preset(self):
        cli_args = {
            "input_file": "in.mp4", "output_file": "out.mp4",
            "resolution": "1920x1080", "video_codec": "cli_vc", 
            "audio_codec": None, "bitrate": None, "preset": "p1" # audio_codec and bitrate from preset
        }
        presets_data = {
            "p1": {"resolution": "1280x720", "video_codec": "preset_vc", "audio_codec": "preset_ac", "bitrate": "1M"}
        }
        args_passed = self.run_main_with_args(cli_args, presets_data)
        self.assertIsNotNone(args_passed)
        self.assertEqual(args_passed[2], "1920x1080") # CLI resolution
        self.assertEqual(args_passed[3], "cli_vc")       # CLI video_codec
        self.assertEqual(args_passed[4], "preset_ac") # Preset audio_codec
        self.assertEqual(args_passed[5], "1M")          # Preset bitrate
        
    def test_preset_fills_unspecified_cli_options(self):
        cli_args = {
            "input_file": "in.mp4", "output_file": "out.mp4",
            "resolution": "1920x1080", # CLI specified
            "video_codec": None,        # To be filled by preset
            "audio_codec": "cli_ac",    # CLI specified
            "bitrate": None,            # To be filled by preset
            "preset": "p1"
        }
        presets_data = {
            "p1": {"video_codec": "preset_vc", "audio_codec": "preset_ac_ignored", "bitrate": "1M"}
        }
        args_passed = self.run_main_with_args(cli_args, presets_data)
        self.assertIsNotNone(args_passed)
        self.assertEqual(args_passed[2], "1920x1080") # CLI
        self.assertEqual(args_passed[3], "preset_vc") # Preset
        self.assertEqual(args_passed[4], "cli_ac")    # CLI
        self.assertEqual(args_passed[5], "1M")       # Preset

    def test_preset_not_found(self):
         cli_args = {
            "input_file": "in.mp4", "output_file": "out.mp4",
            "preset": "unknown_preset"
        }
         # Expect sys.exit to be called, so convert_video should not be called
         # The run_main_with_args helper catches SystemExit
         with patch('builtins.print') as mock_print: # To check error message
            args_passed = self.run_main_with_args(cli_args, {"p1": {}},) # Empty presets data
            self.assertIsNone(args_passed) # convert_video should not be called
            mock_print.assert_any_call("Error: Preset 'unknown_preset' not found in presets.json. Available presets: p1")


if __name__ == '__main__':
    unittest.main()
