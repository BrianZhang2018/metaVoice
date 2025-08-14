#!/usr/bin/env python3
"""
Setup Permissions for metaVoice
Helps users grant necessary permissions for text input automation
"""

import subprocess
import sys
import os
import time

def check_permissions():
    """Check current permissions status"""
    print("🔍 Checking current permissions...")
    
    # Test AppleScript automation
    test_script = '''
    tell application "System Events"
        return "AppleScript automation is working"
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', test_script], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ AppleScript automation permissions: OK")
            return True
        else:
            print("❌ AppleScript automation permissions: BLOCKED")
            return False
    except subprocess.TimeoutExpired:
        print("❌ AppleScript automation permissions: TIMEOUT (likely blocked)")
        return False
    except Exception as e:
        print(f"❌ AppleScript automation permissions: ERROR - {e}")
        return False

def test_keystroke_permissions():
    """Test if keystroke automation is allowed"""
    print("\n🔍 Testing keystroke permissions...")
    
    test_script = '''
    tell application "System Events"
        keystroke "a" using command down
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', test_script], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Keystroke automation permissions: OK")
            return True
        else:
            print("❌ Keystroke automation permissions: BLOCKED")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Keystroke automation permissions: TIMEOUT (likely blocked)")
        return False
    except Exception as e:
        print(f"❌ Keystroke automation permissions: ERROR - {e}")
        return False

def open_system_preferences():
    """Open System Preferences to help user grant permissions"""
    print("\n🔧 Opening System Preferences...")
    
    # Open System Preferences > Security & Privacy > Privacy > Accessibility
    script = '''
    tell application "System Preferences"
        activate
        set current pane to pane id "com.apple.preference.security"
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', script])
        print("✅ System Preferences opened")
        print("\n📋 Please follow these steps:")
        print("1. Click on 'Privacy' tab")
        print("2. Select 'Accessibility' from the left sidebar")
        print("3. Click the lock icon and enter your password")
        print("4. Find 'Python' or 'Terminal' in the list")
        print("5. Check the box next to it to grant permission")
        print("6. Also check 'System Events' if it appears")
        print("7. Close System Preferences")
        return True
    except Exception as e:
        print(f"❌ Could not open System Preferences: {e}")
        return False

def test_text_input_automation():
    """Test the text input automation system"""
    print("\n🧪 Testing text input automation...")
    
    try:
        from text_input_automation import TextInputAutomation
        automation = TextInputAutomation()
        
        # Test clipboard functionality
        print("Testing clipboard functionality...")
        success = automation.copy_to_clipboard("Test from metaVoice")
        if success:
            print("✅ Clipboard functionality works")
        else:
            print("❌ Clipboard functionality failed")
            return False
        
        # Test auto input (this will likely fail without permissions)
        print("Testing auto input (this may fail without permissions)...")
        success = automation.auto_input_text("Test input", "active", "clipboard")
        if success:
            print("✅ Auto input works!")
            return True
        else:
            print("❌ Auto input failed - permissions needed")
            return False
            
    except ImportError:
        print("❌ Could not import text_input_automation module")
        return False
    except Exception as e:
        print(f"❌ Error testing automation: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 metaVoice Permission Setup")
    print("=" * 40)
    
    # Check current permissions
    apple_script_ok = check_permissions()
    keystroke_ok = test_keystroke_permissions()
    
    if apple_script_ok and keystroke_ok:
        print("\n✅ All permissions are already granted!")
        print("Testing text input automation...")
        if test_text_input_automation():
            print("\n🎉 Everything is working perfectly!")
            return
        else:
            print("\n⚠️ Permissions seem OK but automation still failing")
            print("This might be a different issue.")
            return
    
    # If permissions are not granted, help user set them up
    print("\n❌ Permissions need to be granted for text input automation to work")
    print("\nThis is required for metaVoice to automatically type your voice input into applications.")
    
    response = input("\nWould you like to open System Preferences to grant permissions? (y/n): ")
    if response.lower() in ['y', 'yes']:
        open_system_preferences()
        
        print("\n⏳ Waiting for you to grant permissions...")
        input("Press Enter when you've finished granting permissions...")
        
        print("\n🔍 Re-checking permissions...")
        time.sleep(2)
        
        apple_script_ok = check_permissions()
        keystroke_ok = test_keystroke_permissions()
        
        if apple_script_ok and keystroke_ok:
            print("\n✅ Permissions granted successfully!")
            print("Testing text input automation...")
            if test_text_input_automation():
                print("\n🎉 Everything is working perfectly!")
            else:
                print("\n⚠️ Permissions granted but automation still failing")
                print("Please try restarting metaVoice and test again.")
        else:
            print("\n❌ Permissions still not granted")
            print("Please make sure to:")
            print("- Grant Accessibility permission to Python/Terminal")
            print("- Grant permission to System Events")
            print("- Restart metaVoice after granting permissions")
    else:
        print("\n⚠️ Without these permissions, text input automation will not work.")
        print("You can run this setup script again later if you change your mind.")

if __name__ == "__main__":
    main() 