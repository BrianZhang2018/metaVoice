#!/usr/bin/env python3
"""
Example Usage of Whisper.cpp for Desktop Automation
Shows how to integrate voice commands into your applications
"""

from whisper_wrapper import WhisperWrapper
import time

class VoiceCommandHandler:
    def __init__(self):
        """Initialize the voice command handler"""
        self.whisper = WhisperWrapper()
        self.running = False
    
    def start_listening(self):
        """Start listening for voice commands"""
        self.running = True
        print("🎤 Voice command system started!")
        print("Say 'stop listening' to exit")
        print()
        
        while self.running:
            try:
                # Listen for command
                print("🎤 Listening... (3 seconds)")
                text = self.whisper.transcribe_microphone(duration=3)
                
                if text.strip():
                    print(f"🎯 Heard: '{text}'")
                    
                    # Parse command
                    command = self.whisper.parse_command(text)
                    print(f"📝 Parsed: {command}")
                    
                    # Handle command
                    self.handle_command(command)
                    
                else:
                    print("🔇 No speech detected")
                    
            except KeyboardInterrupt:
                print("\n👋 Stopping voice command system...")
                self.running = False
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def handle_command(self, command):
        """Handle parsed voice commands"""
        cmd_type = command.get("command", "unknown")
        params = command.get("parameters", {})
        
        print(f"🤖 Executing command: {cmd_type}")
        
        if cmd_type == "build-app":
            app_type = params.get("type", "unknown")
            app_name = params.get("name", "my-app")
            print(f"   Building {app_type} app named '{app_name}'")
            # Add your app building logic here
            
        elif cmd_type == "record-meeting":
            duration = params.get("duration", "30")
            print(f"   Recording meeting for {duration} minutes")
            # Add your meeting recording logic here
            
        elif cmd_type == "analyze-meeting":
            filename = params.get("file", "unknown")
            print(f"   Analyzing meeting file: {filename}")
            # Add your meeting analysis logic here
            
        elif cmd_type == "create-component":
            comp_type = params.get("type", "unknown")
            print(f"   Creating {comp_type} component")
            # Add your component creation logic here
            
        elif "stop" in command.get("original_text", "").lower():
            print("🛑 Stopping voice command system...")
            self.running = False
            
        else:
            print(f"   Unknown command: {cmd_type}")
            print("   Available commands: build-app, record-meeting, analyze-meeting, create-component")
        
        print()

def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    whisper = WhisperWrapper()
    
    # Transcribe from microphone
    print("🎤 Recording 3 seconds of speech...")
    text = whisper.transcribe_microphone(duration=3)
    print(f"Transcribed: '{text}'")
    
    # Parse as command
    command = whisper.parse_command(text)
    print(f"Command: {command}")

def example_file_transcription():
    """Example of transcribing audio files"""
    print("\n=== File Transcription Example ===")
    
    whisper = WhisperWrapper()
    
    # Transcribe audio file
    sample_file = "./whisper.cpp/samples/jfk.wav"
    try:
        result = whisper.transcribe_audio_file(sample_file, "json")
        print(f"File transcription: {result.get('text', 'No text found')}")
    except Exception as e:
        print(f"Error transcribing file: {e}")

def example_continuous_listening():
    """Example of continuous voice command listening"""
    print("\n=== Continuous Listening Example ===")
    
    handler = VoiceCommandHandler()
    handler.start_listening()

if __name__ == "__main__":
    print("🎤 Whisper.cpp Usage Examples")
    print("=" * 40)
    
    # Run examples
    example_basic_usage()
    example_file_transcription()
    
    # Uncomment to test continuous listening
    # example_continuous_listening() 