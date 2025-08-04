#!/usr/bin/env python3
"""
Interactive Voice Command Runner
Run this script to test voice commands locally
"""

import time
from whisper_wrapper import WhisperWrapper

def main():
    print("🎤 Voice Command System - Local Mode")
    print("=" * 40)
    print("This script will let you test voice commands locally.")
    print("Commands will be transcribed and parsed automatically.")
    print()
    
    # Initialize Whisper
    try:
        whisper = WhisperWrapper()
        print("✅ Whisper.cpp initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Whisper: {e}")
        return
    
    print("\nAvailable commands to try:")
    print("- 'build app type react name my-app'")
    print("- 'record meeting duration 30 minutes'")
    print("- 'analyze meeting file zoom-recording.mp4'")
    print("- 'create component type button'")
    print()
    
    while True:
        try:
            # Get user choice
            choice = input("Choose an option:\n1. Record voice command (3 seconds)\n2. Record voice command (5 seconds)\n3. Test with sample audio file\n4. Exit\n\nEnter choice (1-4): ").strip()
            
            if choice == "1":
                print("\n🎤 Recording for 3 seconds... Speak now!")
                text = whisper.transcribe_microphone(duration=3)
                print(f"🎯 You said: '{text}'")
                
                # Parse command
                command = whisper.parse_command(text)
                print(f"📝 Parsed command: {command}")
                
            elif choice == "2":
                print("\n🎤 Recording for 5 seconds... Speak now!")
                text = whisper.transcribe_microphone(duration=5)
                print(f"🎯 You said: '{text}'")
                
                # Parse command
                command = whisper.parse_command(text)
                print(f"📝 Parsed command: {command}")
                
            elif choice == "3":
                print("\n📁 Testing with sample audio file...")
                sample_file = "./whisper.cpp/samples/jfk.wav"
                
                if whisper.whisper_path and os.path.exists(sample_file):
                    result = whisper.transcribe_audio_file(sample_file, "json")
                    print(f"🎯 Transcribed: '{result.get('text', 'No text found')}'")
                    
                    # Parse command
                    command = whisper.parse_command(result.get('text', ''))
                    print(f"📝 Parsed command: {command}")
                else:
                    print("❌ Sample file not found")
                    
            elif choice == "4":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.")
        
        print("\n" + "-" * 40 + "\n")

if __name__ == "__main__":
    import os
    main() 