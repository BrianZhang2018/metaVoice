#!/usr/bin/env python3
"""
Test Auto-Input Functionality
Simple test to demonstrate voice-to-text auto-input
"""

from whisper_wrapper import WhisperWrapper
from text_input_automation import TextInputAutomation
import time

def test_auto_input():
    """Test auto-input functionality"""
    print("🎤 Auto-Input Voice Test")
    print("=" * 40)
    print()
    print("This test will:")
    print("1. Record your voice")
    print("2. Transcribe what you say")
    print("3. Automatically type it into the active application")
    print()
    print("IMPORTANT: Make sure you have an input box ready (like Cursor, Notes, etc.)")
    print()
    
    # Initialize components
    whisper = WhisperWrapper()
    automation = TextInputAutomation()
    
    # Countdown
    print("Starting in 5 seconds...")
    print("Switch to your target application (Cursor, Notes, etc.)")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print()
    print("🎤 SPEAK NOW!")
    print("Say something you want typed automatically")
    print("Recording for 5 seconds...")
    
    # Record and transcribe
    text = whisper.transcribe_microphone(duration=5)
    
    print()
    print("🎯 Results:")
    print(f"Transcribed: '{text}'")
    
    if text and text.strip() and text.strip() != "[BLANK_AUDIO]":
        print("✅ SUCCESS! Speech detected!")
        
        # Auto-input the text
        print("🎯 Auto-inputting text...")
        success = automation.auto_input_text(text, "active", "clipboard")
        
        if success:
            print("✅ Text successfully input!")
            print("🎉 Check your active application - the text should be there!")
        else:
            print("❌ Failed to input text")
            print("🔧 This might be due to accessibility permissions")
            print("   Try enabling accessibility for Terminal in System Preferences")
    else:
        print("❌ No speech detected.")
        print("Did you speak during the recording?")

def test_clipboard_only():
    """Test clipboard functionality only"""
    print("\n📋 Clipboard Test")
    print("=" * 20)
    
    test_text = "This is a test from voice automation!"
    automation = TextInputAutomation()
    
    print(f"Copying to clipboard: '{test_text}'")
    success = automation.copy_to_clipboard(test_text)
    
    if success:
        print("✅ Text copied to clipboard!")
        print("🎯 Now manually paste (Cmd+V) in any application")
    else:
        print("❌ Failed to copy to clipboard")

def main():
    """Main function"""
    print("🧪 Auto-Input Voice Recognition Test")
    print("=" * 50)
    
    # Test 1: Full auto-input
    test_auto_input()
    
    # Test 2: Clipboard only
    print("\n" + "=" * 50)
    response = input("Test clipboard only? (y/n): ").lower().strip()
    if response == 'y':
        test_clipboard_only()
    
    print("\n🎯 Test completed!")

if __name__ == "__main__":
    main() 