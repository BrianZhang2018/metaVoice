#!/usr/bin/env python3
"""
Test script for Whisper.cpp installation and Python wrapper
"""

import os
import sys
from whisper_wrapper import WhisperWrapper

def test_whisper_installation():
    """Test if Whisper.cpp is properly installed"""
    print("Testing Whisper.cpp installation...")
    
    # Check if whisper-cli exists
    whisper_cli_path = "./whisper.cpp/build/bin/whisper-cli"
    if not os.path.exists(whisper_cli_path):
        print("❌ Whisper CLI not found!")
        return False
    
    print("✅ Whisper CLI found")
    
    # Check if model exists
    model_path = "./whisper.cpp/models/ggml-base.en.bin"
    if not os.path.exists(model_path):
        print("❌ Whisper model not found!")
        return False
    
    print("✅ Whisper model found")
    
    return True

def test_wrapper_initialization():
    """Test if the Python wrapper can be initialized"""
    print("\nTesting Python wrapper initialization...")
    
    try:
        whisper = WhisperWrapper()
        print("✅ WhisperWrapper initialized successfully")
        return whisper
    except Exception as e:
        print(f"❌ Failed to initialize WhisperWrapper: {e}")
        return None

def test_audio_file_transcription():
    """Test transcription of the sample audio file"""
    print("\nTesting audio file transcription...")
    
    whisper = WhisperWrapper()
    sample_file = "./whisper.cpp/samples/jfk.wav"
    
    if not os.path.exists(sample_file):
        print("❌ Sample audio file not found!")
        return False
    
    try:
        result = whisper.transcribe_audio_file(sample_file, "json")
        print("✅ Audio file transcription successful")
        print(f"Transcribed text: {result.get('text', 'No text found')}")
        return True
    except Exception as e:
        print(f"❌ Audio file transcription failed: {e}")
        return False

def test_command_parsing():
    """Test command parsing functionality"""
    print("\nTesting command parsing...")
    
    whisper = WhisperWrapper()
    
    test_commands = [
        "build app type react name my-app",
        "record meeting duration 30 minutes",
        "analyze meeting file zoom-recording.mp4",
        "create component type button props onClick text"
    ]
    
    for cmd in test_commands:
        result = whisper.parse_command(cmd)
        print(f"Command: '{cmd}'")
        print(f"Parsed: {result}")
        print()

def main():
    """Run all tests"""
    print("🧪 Whisper.cpp Installation and Wrapper Tests")
    print("=" * 50)
    
    # Test 1: Installation
    if not test_whisper_installation():
        print("\n❌ Installation test failed. Please check your Whisper.cpp installation.")
        return
    
    # Test 2: Wrapper initialization
    whisper = test_wrapper_initialization()
    if whisper is None:
        print("\n❌ Wrapper initialization failed.")
        return
    
    # Test 3: Audio file transcription
    if not test_audio_file_transcription():
        print("\n❌ Audio file transcription test failed.")
        return
    
    # Test 4: Command parsing
    test_command_parsing()
    
    print("\n🎉 All tests passed! Whisper.cpp is ready for your desktop automation project.")
    print("\nNext steps:")
    print("1. Install Python dependencies: pip install -r requirements.txt")
    print("2. Test microphone recording (requires pyaudio)")
    print("3. Integrate with your desktop automation workflow")

if __name__ == "__main__":
    main() 