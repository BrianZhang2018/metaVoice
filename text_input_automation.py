#!/usr/bin/env python3
"""
Text Input Automation for macOS
Automatically inputs transcribed text into Cursor or any input box
"""

import subprocess
import time
import json
import os
from typing import Optional, Dict, Any

class TextInputAutomation:
    def __init__(self):
        """Initialize text input automation"""
        self.clipboard_methods = ["applescript", "pbcopy", "pyautogui"]
        self.input_methods = ["applescript", "pyautogui", "keyboard"]
        
    def copy_to_clipboard(self, text: str, method: str = "applescript") -> bool:
        """
        Copy text to clipboard using various methods
        
        Args:
            text: Text to copy
            method: Method to use ("applescript", "pbcopy", "pyautogui")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if method == "applescript":
                return self._copy_to_clipboard_applescript(text)
            elif method == "pbcopy":
                return self._copy_to_clipboard_pbcopy(text)
            elif method == "pyautogui":
                return self._copy_to_clipboard_pyautogui(text)
            else:
                print(f"Unknown clipboard method: {method}")
                return False
        except Exception as e:
            print(f"Error copying to clipboard with {method}: {e}")
            return False
    
    def _copy_to_clipboard_applescript(self, text: str) -> bool:
        """Copy text to clipboard using AppleScript"""
        try:
            # Escape quotes in text
            escaped_text = text.replace('"', '\\"')
            
            script = f'''
            set the clipboard to "{escaped_text}"
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Copied to clipboard via AppleScript: '{text[:50]}...'")
                return True
            else:
                print(f"❌ AppleScript clipboard error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ AppleScript clipboard error: {e}")
            return False
    
    def _copy_to_clipboard_pbcopy(self, text: str) -> bool:
        """Copy text to clipboard using pbcopy command"""
        try:
            result = subprocess.run(['pbcopy'], input=text, text=True, 
                                  capture_output=True)
            
            if result.returncode == 0:
                print(f"✅ Copied to clipboard via pbcopy: '{text[:50]}...'")
                return True
            else:
                print(f"❌ pbcopy error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ pbcopy error: {e}")
            return False
    
    def _copy_to_clipboard_pyautogui(self, text: str) -> bool:
        """Copy text to clipboard using PyAutoGUI"""
        try:
            import pyautogui
            pyautogui.write(text)
            print(f"✅ Copied to clipboard via PyAutoGUI: '{text[:50]}...'")
            return True
        except ImportError:
            print("❌ PyAutoGUI not installed")
            return False
        except Exception as e:
            print(f"❌ PyAutoGUI clipboard error: {e}")
            return False
    
    def paste_from_clipboard(self, method: str = "applescript") -> bool:
        """
        Paste text from clipboard using various methods
        
        Args:
            method: Method to use ("applescript", "pyautogui", "keyboard")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if method == "applescript":
                return self._paste_from_clipboard_applescript()
            elif method == "pyautogui":
                return self._paste_from_clipboard_pyautogui()
            elif method == "keyboard":
                return self._paste_from_clipboard_keyboard()
            else:
                print(f"Unknown paste method: {method}")
                return False
        except Exception as e:
            print(f"Error pasting from clipboard with {method}: {e}")
            return False
    
    def _paste_from_clipboard_applescript(self) -> bool:
        """Paste text from clipboard using AppleScript"""
        try:
            script = '''
            tell application "System Events"
                keystroke "v" using command down
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Pasted from clipboard via AppleScript")
                return True
            else:
                print(f"❌ AppleScript paste error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ AppleScript paste error: {e}")
            return False
    
    def _paste_from_clipboard_pyautogui(self) -> bool:
        """Paste text from clipboard using PyAutoGUI"""
        try:
            import pyautogui
            pyautogui.hotkey('cmd', 'v')
            print("✅ Pasted from clipboard via PyAutoGUI")
            return True
        except ImportError:
            print("❌ PyAutoGUI not installed")
            return False
        except Exception as e:
            print(f"❌ PyAutoGUI paste error: {e}")
            return False
    
    def _paste_from_clipboard_keyboard(self) -> bool:
        """Paste text from clipboard using keyboard module"""
        try:
            import keyboard
            keyboard.press_and_release('cmd+v')
            print("✅ Pasted from clipboard via keyboard")
            return True
        except ImportError:
            print("❌ keyboard module not installed")
            return False
        except Exception as e:
            print(f"❌ keyboard paste error: {e}")
            return False
    
    def input_text_direct(self, text: str, method: str = "applescript") -> bool:
        """
        Input text directly without using clipboard
        
        Args:
            text: Text to input
            method: Method to use ("applescript", "pyautogui", "keyboard")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if method == "applescript":
                return self._input_text_applescript(text)
            elif method == "pyautogui":
                return self._input_text_pyautogui(text)
            elif method == "keyboard":
                return self._input_text_keyboard(text)
            else:
                print(f"Unknown input method: {method}")
                return False
        except Exception as e:
            print(f"Error inputting text with {method}: {e}")
            return False
    
    def _input_text_applescript(self, text: str) -> bool:
        """Input text using AppleScript"""
        try:
            # Escape quotes and special characters
            escaped_text = text.replace('"', '\\"').replace("'", "\\'")
            
            script = f'''
            tell application "System Events"
                keystroke "{escaped_text}"
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Input text via AppleScript: '{text[:50]}...'")
                return True
            else:
                print(f"❌ AppleScript input error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ AppleScript input error: {e}")
            return False
    
    def _input_text_pyautogui(self, text: str) -> bool:
        """Input text using PyAutoGUI"""
        try:
            import pyautogui
            pyautogui.write(text)
            print(f"✅ Input text via PyAutoGUI: '{text[:50]}...'")
            return True
        except ImportError:
            print("❌ PyAutoGUI not installed")
            return False
        except Exception as e:
            print(f"❌ PyAutoGUI input error: {e}")
            return False
    
    def _input_text_keyboard(self, text: str) -> bool:
        """Input text using keyboard module"""
        try:
            import keyboard
            keyboard.write(text)
            print(f"✅ Input text via keyboard: '{text[:50]}...'")
            return True
        except ImportError:
            print("❌ keyboard module not installed")
            return False
        except Exception as e:
            print(f"❌ keyboard input error: {e}")
            return False
    
    def focus_cursor(self) -> bool:
        """
        Focus on Cursor application
        
        Returns:
            True if successful, False otherwise
        """
        try:
            script = '''
            tell application "Cursor"
                activate
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Focused on Cursor")
                return True
            else:
                print(f"❌ Error focusing Cursor: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error focusing Cursor: {e}")
            return False
    
    def focus_qoder(self) -> bool:
        """
        Focus on Qoder IDE application
        
        Returns:
            True if successful, False otherwise
        """
        try:
            script = '''
            tell application "Qoder"
                activate
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Focused on Qoder")
                return True
            else:
                print(f"❌ Error focusing Qoder: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error focusing Qoder: {e}")
            return False
    
    def get_frontmost_app(self) -> str:
        """
        Get the name of the frontmost (active) application
        
        Returns:
            Name of frontmost application, or 'unknown' if unable to determine
        """
        try:
            script = '''
            tell application "System Events"
                name of first application process whose frontmost is true
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                app_name = result.stdout.strip()
                print(f"🎯 Frontmost app: {app_name}")
                return app_name.lower()
            else:
                print(f"❌ Error getting frontmost app: {result.stderr}")
                return "unknown"
                
        except Exception as e:
            print(f"❌ Error getting frontmost app: {e}")
            return "unknown"
    
    def auto_detect_target(self) -> str:
        """
        Automatically detect the best target application based on frontmost app
        
        Returns:
            Suggested target app name
        """
        frontmost = self.get_frontmost_app()
        
        # Map common application names to our target names
        app_mapping = {
            "cursor": "cursor",
            "qoder": "qoder", 
            "qoder ide": "qoder",
            "electron": "qoder",  # Qoder runs on Electron
            "visual studio code": "vscode",
            "code": "vscode",
            "pycharm": "pycharm",
            "safari": "safari",
            "google chrome": "chrome",
            "chrome": "chrome",
            "terminal": "terminal",
            "iterm2": "terminal",
            "notes": "notes",
            "textedit": "notes"
        }
        
        for app_key, target_name in app_mapping.items():
            if app_key in frontmost:
                print(f"✅ Auto-detected target: {target_name}")
                return target_name
        
        print(f"⚠️ Unknown app '{frontmost}', using 'active'")
        return "active"
    
    def focus_active_app(self) -> bool:
        """
        Focus on the currently active application (bring to front)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            script = '''
            tell application "System Events"
                set frontApp to first application process whose frontmost is true
                set frontmost of frontApp to true
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Focused on active app")
                return True
            else:
                print(f"❌ Error focusing active app: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error focusing active app: {e}")
            return False
        """
        Focus on the currently active application
        
        Returns:
            True if successful, False otherwise
        """
        try:
            script = '''
            tell application "System Events"
                set frontmost to true
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Focused on active application")
                return True
            else:
                print(f"❌ Error focusing active app: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error focusing active app: {e}")
            return False
    
    def auto_input_text(self, text: str, target_app: str = "cursor", 
                       method: str = "clipboard") -> bool:
        """
        Automatically input text into the target application
        
        Args:
            text: Text to input
            target_app: Target application ("auto-detect", "cursor", "qoder", "active", or app name)
            method: Input method ("clipboard", "direct")
            
        Returns:
            True if successful, False otherwise
        """
        print(f"🎯 Auto-inputting text: '{text[:50]}...'")
        
        try:
            # Handle auto-detection
            if target_app.lower() == "auto-detect":
                target_app = self.auto_detect_target()
                print(f"🤖 Auto-detected target: {target_app}")
            
            # Focus on target application
            if target_app.lower() == "cursor":
                if not self.focus_cursor():
                    print("⚠️ Could not focus Cursor, trying active app")
                    self.focus_active_app()
            elif target_app.lower() == "qoder":
                if not self.focus_qoder():
                    print("⚠️ Could not focus Qoder, trying active app")
                    self.focus_active_app()
            elif target_app.lower() == "active":
                self.focus_active_app()
            else:
                # Focus specific application
                script = f'''
                tell application "{target_app}"
                    activate
                end tell
                '''
                subprocess.run(['osascript', '-e', script])
            
            # Wait a moment for app to focus
            time.sleep(0.3)  # Increased wait time for Electron apps
            
            # Input the text using specified method
            if method.lower() == "clipboard":
                # Copy to clipboard first
                if not self.copy_to_clipboard(text):
                    print("❌ Failed to copy to clipboard")
                    return False
                
                # Wait for clipboard to update
                time.sleep(0.2)
                
                # Paste with improved method
                return self.paste_with_retry()
                
            elif method.lower() == "direct":
                # Direct keyboard input
                return self._input_text_keyboard(text)
            else:
                print(f"Unknown input method: {method}")
                return False
                
        except Exception as e:
            print(f"❌ Error in auto_input_text: {e}")
            return False
            
    def paste_with_retry(self, retries=3) -> bool:
        """
        Paste from clipboard with retry logic for better reliability
        
        Args:
            retries: Number of retry attempts
            
        Returns:
            True if successful, False otherwise
        """
        for attempt in range(retries):
            try:
                # Method 1: AppleScript paste (most reliable)
                script = '''
                tell application "System Events"
                    keystroke "v" using command down
                end tell
                '''
                
                result = subprocess.run(['osascript', '-e', script], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Pasted from clipboard (attempt {attempt + 1})")
                    return True
                else:
                    print(f"⚠️ Paste attempt {attempt + 1} failed: {result.stderr}")
                    
            except Exception as e:
                print(f"⚠️ Paste attempt {attempt + 1} error: {e}")
            
            # Wait before retry
            if attempt < retries - 1:
                time.sleep(0.5)
        
        # If all AppleScript attempts fail, try direct keyboard input
        try:
            import pyautogui
            pyautogui.hotkey('cmd', 'v')
            print("✅ Pasted using pyautogui fallback")
            return True
        except Exception as e:
            print(f"❌ All paste methods failed: {e}")
            return False
    
    def test_automation(self) -> bool:
        """
        Test the automation system
        
        Returns:
            True if successful, False otherwise
        """
        print("🧪 Testing Text Input Automation")
        print("=" * 40)
        
        test_text = "Hello from voice automation! This is a test."
        
        # Test clipboard methods
        print("\n📋 Testing clipboard methods:")
        for method in self.clipboard_methods:
            print(f"Testing {method}...")
            success = self.copy_to_clipboard(test_text, method)
            if success:
                print(f"✅ {method} clipboard method works")
                break
        
        # Test input methods
        print("\n⌨️ Testing input methods:")
        for method in self.input_methods:
            print(f"Testing {method}...")
            success = self.input_text_direct("Test input", method)
            if success:
                print(f"✅ {method} input method works")
                break
        
        # Test auto input
        print("\n🎯 Testing auto input:")
        success = self.auto_input_text("Auto input test", "active", "clipboard")
        
        return success

def main():
    """Main function for testing"""
    automation = TextInputAutomation()
    automation.test_automation()

if __name__ == "__main__":
    main() 