#!/usr/bin/env python3
"""
Whisper.cpp Python Wrapper for Desktop Automation
Provides easy-to-use functions for voice recognition in your desktop automation project.
"""

import subprocess
import json
import tempfile
import os
import sys
import wave
import pyaudio
from typing import Optional, Dict, Any

class WhisperWrapper:
    def __init__(self, whisper_path: str = None, model_path: str = None):
        """
        Initialize Whisper wrapper
        
        Args:
            whisper_path: Path to whisper-cli executable
            model_path: Path to the Whisper model
        """
        # Handle bundled app paths
        if whisper_path is None:
            if getattr(sys, 'frozen', False):
                # Running in a bundle
                base_path = os.path.dirname(sys.executable)
                # Check if whisper-cli is in MacOS directory
                macos_path = os.path.join(base_path, "whisper-cli")
                if os.path.exists(macos_path):
                    self.whisper_path = macos_path
                else:
                    # Check if it's in Frameworks directory
                    frameworks_path = os.path.join(base_path, "..", "Frameworks", "whisper-cli")
                    if os.path.exists(frameworks_path):
                        self.whisper_path = frameworks_path
                    else:
                        # Fallback to MacOS directory
                        self.whisper_path = macos_path
            else:
                # Running in development
                self.whisper_path = "./whisper.cpp/build/bin/whisper-cli"
        else:
            self.whisper_path = whisper_path
            
        if model_path is None:
            if getattr(sys, 'frozen', False):
                # Running in a bundle
                base_path = os.path.dirname(sys.executable)
                # Check if models are in MacOS directory
                macos_path = os.path.join(base_path, "whisper_models", "ggml-base.en.bin")
                if os.path.exists(macos_path):
                    self.model_path = macos_path
                else:
                    # Check if they're in Resources directory
                    resources_path = os.path.join(base_path, "..", "Resources", "whisper_models", "ggml-base.en.bin")
                    if os.path.exists(resources_path):
                        self.model_path = resources_path
                    else:
                        # Fallback to MacOS directory
                        self.model_path = macos_path
            else:
                # Running in development
                self.model_path = "./whisper.cpp/models/ggml-base.en.bin"
        else:
            self.model_path = model_path
        
        # Verify paths exist
        if not os.path.exists(self.whisper_path):
            raise FileNotFoundError(f"Whisper CLI not found at: {self.whisper_path}")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at: {self.model_path}")
    
    def transcribe_audio_file(self, audio_file: str, output_format: str = "json", speed_mode: str = "balanced") -> Dict[str, Any]:
        """
        Transcribe an audio file
        
        Args:
            audio_file: Path to audio file
            output_format: Output format (json, txt, srt, vtt)
            speed_mode: Speed mode ("fast", "balanced", "accurate")
            
        Returns:
            Dictionary containing transcription results
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        # Create temporary output file
        with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False) as tmp_file:
            output_file = tmp_file.name
        
        try:
            # Choose parameters based on speed mode
            if speed_mode == "fast":
                # Fastest settings - may reduce accuracy slightly
                nth, wt, et, nt = "0.5", "0.01", "2.0", "6"
            elif speed_mode == "accurate":
                # Most accurate settings - slower (original settings)
                nth, wt, et, nt = "0.1", "0.001", "1.0", "2"
            else:  # balanced (default)
                # Balanced settings - good speed and accuracy
                nth, wt, et, nt = "0.4", "0.005", "1.8", "4"
            
            # Build command with optimized settings for speed
            cmd = [
                self.whisper_path,
                "-m", self.model_path,
                "-f", audio_file,
                "-oj" if output_format == "json" else f"-o{output_format}",
                "-of", output_file.replace(f".{output_format}", ""),
                "-nth", nth,      # No-speech threshold
                "-wt", wt,        # Word timestamp threshold
                "-et", et,        # Entropy threshold
                "-lpt", "-1.0",   # Log probability threshold
                "-nt", nt         # Number of threads
            ]
            
            # Run transcription
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Read output
            if output_format == "json":
                with open(output_file, 'r') as f:
                    data = json.load(f)
                    # Extract text from the JSON structure
                    if isinstance(data, dict) and "transcription" in data:
                        # New format with transcription array
                        text_parts = []
                        for segment in data["transcription"]:
                            if "text" in segment:
                                text_parts.append(segment["text"].strip())
                        return {"text": " ".join(text_parts)}
                    elif isinstance(data, dict) and "text" in data:
                        # Direct text format
                        return data
                    else:
                        # Fallback
                        return {"text": str(data)}
            else:
                with open(output_file, 'r') as f:
                    return {"text": f.read().strip()}
                    
        finally:
            # Clean up temporary file
            if os.path.exists(output_file):
                os.unlink(output_file)
    
    def transcribe_microphone(self, duration: int = 5, sample_rate: int = 16000, speed_mode: str = "balanced", stop_flag=None) -> str:
        """
        Record from microphone and transcribe
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Audio sample rate
            speed_mode: Speed mode ("fast", "balanced", "accurate")
            stop_flag: Function that returns True if recording should stop
            
        Returns:
            Transcribed text
        """
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            audio_file = tmp_file.name
        
        try:
            # Record audio with stop flag
            self._record_audio(audio_file, duration, sample_rate, stop_flag)
            
            # Check if file was created and has content
            if not os.path.exists(audio_file) or os.path.getsize(audio_file) == 0:
                print("Warning: No audio was recorded")
                return ""
            
            # Transcribe with speed mode
            result = self.transcribe_audio_file(audio_file, speed_mode=speed_mode)
            
            if isinstance(result, dict) and "text" in result:
                return result["text"]
            elif isinstance(result, list) and len(result) > 0:
                return result[0].get("text", "")
            else:
                return str(result)
                
        except Exception as e:
            print(f"Error in transcribe_microphone: {e}")
            return ""
        finally:
            # Clean up temporary file
            if os.path.exists(audio_file):
                os.unlink(audio_file)
    
    def _record_audio(self, filename: str, duration: int, sample_rate: int, stop_flag=None):
        """Record audio from microphone"""
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        
        p = pyaudio.PyAudio()
        
        try:
            # Find the microphone device
            mic_device = None
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                if 'microphone' in device_info['name'].lower() or 'input' in device_info['name'].lower():
                    mic_device = i
                    break
            
            if mic_device is None:
                # Use default input device
                mic_device = p.get_default_input_device_info()['index']
            
            print(f"Using microphone device: {p.get_device_info_by_index(mic_device)['name']}")
            
            stream = p.open(format=format,
                           channels=channels,
                           rate=sample_rate,
                           input=True,
                           input_device_index=mic_device,
                           frames_per_buffer=chunk)
            
            print(f"Recording for {duration} seconds...")
            frames = []
            
            for i in range(0, int(sample_rate / chunk * duration)):
                # Check if we should stop recording early
                if stop_flag and stop_flag():
                    print("Recording stopped early by user.")
                    break
                    
                data = stream.read(chunk)
                frames.append(data)
            
            print("Recording finished.")
            
            stream.stop_stream()
            stream.close()
            
            # Save to WAV file
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(p.get_sample_size(format))
                wf.setframerate(sample_rate)
                wf.writeframes(b''.join(frames))
                
        except Exception as e:
            print(f"Error recording audio: {e}")
        finally:
            p.terminate()
    
    def parse_command(self, text: str) -> Dict[str, Any]:
        """
        Parse transcribed text as a structured command
        
        Args:
            text: Transcribed text
            
        Returns:
            Dictionary with parsed command structure
        """
        # Simple command parsing - can be enhanced with more sophisticated NLP
        text = text.lower().strip()
        
        # Define command patterns
        command_patterns = {
            "build-app": {
                "keywords": ["build", "create", "make", "new"],
                "app_keywords": ["app", "application", "project"]
            },
            "record-meeting": {
                "keywords": ["record", "start recording", "begin recording"],
                "meeting_keywords": ["meeting", "call", "zoom", "teams"]
            },
            "analyze-meeting": {
                "keywords": ["analyze", "transcribe", "summarize"],
                "meeting_keywords": ["meeting", "recording", "call"]
            },
            "create-component": {
                "keywords": ["create", "make", "build"],
                "component_keywords": ["component", "button", "input", "form"]
            }
        }
        
        # Try to match commands
        for command_type, patterns in command_patterns.items():
            if any(keyword in text for keyword in patterns["keywords"]):
                # Extract parameters (simple approach)
                params = {}
                
                # Extract type if present
                if "type:" in text:
                    type_start = text.find("type:") + 5
                    type_end = text.find(" ", type_start)
                    if type_end == -1:
                        type_end = len(text)
                    params["type"] = text[type_start:type_end].strip()
                
                # Extract name if present
                if "name:" in text:
                    name_start = text.find("name:") + 5
                    name_end = text.find(" ", name_start)
                    if name_end == -1:
                        name_end = len(text)
                    params["name"] = text[name_start:name_end].strip()
                
                return {
                    "command": command_type,
                    "parameters": params,
                    "original_text": text
                }
        
        return {
            "command": "unknown",
            "parameters": {},
            "original_text": text
        }

# Example usage
if __name__ == "__main__":
    # Initialize wrapper
    whisper = WhisperWrapper()
    
    # Example: Transcribe from microphone
    print("Testing microphone transcription...")
    try:
        text = whisper.transcribe_microphone(duration=3)
        print(f"Transcribed: {text}")
        
        # Parse as command
        command = whisper.parse_command(text)
        print(f"Parsed command: {command}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have pyaudio installed: pip install pyaudio") 