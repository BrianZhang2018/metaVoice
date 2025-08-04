#!/usr/bin/env python3
"""
Setup script to help configure macOS permissions for hotkeys
"""

import os
import sys
import subprocess

def check_accessibility_permissions():
    """Check if accessibility permissions are granted"""
    try:
        # Try to register a test hotkey
        import keyboard
        keyboard.add_hotkey('cmd+shift+test', lambda: None)
        keyboard.remove_hotkey('cmd+shift+test')
        return True
    except Exception as e:
        return False

def show_permission_instructions():
    """Show instructions for setting up permissions"""
    print("🔧 macOS Permission Setup for metaVoice Hotkeys")
    print("=" * 50)
    print()
    print("The hotkeys require accessibility permissions on macOS.")
    print()
    print("📋 Setup Steps:")
    print("1. Open System Preferences")
    print("2. Go to Security & Privacy")
    print("3. Click the Privacy tab")
    print("4. Select 'Accessibility' from the left sidebar")
    print("5. Click the lock icon to make changes (enter your password)")
    print("6. Add your terminal application:")
    print("   - Terminal.app")
    print("   - iTerm2.app")
    print("   - VS Code.app")
    print("   - Cursor.app")
    print("   - Or your current IDE")
    print("7. Check the box next to the application")
    print("8. Restart your terminal/IDE")
    print()
    print("💡 Alternative: Use the floating window buttons instead of hotkeys")
    print()

def open_system_preferences():
    """Open System Preferences to the Accessibility section"""
    try:
        subprocess.run([
            'open', 
            'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'
        ])
        print("✅ Opened System Preferences to Accessibility settings")
    except Exception as e:
        print(f"❌ Could not open System Preferences: {e}")
        print("💡 Please open manually: System Preferences → Security & Privacy → Privacy → Accessibility")

def main():
    print("🎤 metaVoice Permission Setup")
    print("=" * 30)
    print()
    
    # Check current permissions
    if check_accessibility_permissions():
        print("✅ Accessibility permissions are already granted!")
        print("🎉 Hotkeys should work correctly.")
        return
    
    print("❌ Accessibility permissions not granted")
    print()
    
    # Show instructions
    show_permission_instructions()
    
    # Ask if user wants to open System Preferences
    try:
        response = input("Would you like to open System Preferences now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            open_system_preferences()
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled")
        return
    
    print()
    print("🔧 After setting up permissions:")
    print("1. Restart your terminal/IDE")
    print("2. Run: python test_hotkeys.py")
    print("3. Test the hotkeys: Cmd+Shift+Space and Cmd+Shift+R")
    print()
    print("💡 The floating recorder will work with button clicks even without hotkeys!")

if __name__ == "__main__":
    main() 