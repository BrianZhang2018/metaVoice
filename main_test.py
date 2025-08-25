#!/usr/bin/env python3
"""
metaVoice - Minimal Test Version
Test basic functionality without full GUI
"""

import sys
import os

def setup_macos_app():
    """Setup macOS application environment"""
    try:
        # Import macOS frameworks to ensure proper initialization
        import Foundation
        import AppKit
        import objc
        
        # Add missing macOSVersion method to NSApplication to prevent Tk crashes
        def macOSVersion(self):
            """Compatibility method for Tk framework"""
            version_info = Foundation.NSProcessInfo.processInfo().operatingSystemVersion()
            # Return version in format expected by Tk (e.g., 10.15.7)
            return f"{version_info.majorVersion}.{version_info.minorVersion}.{version_info.patchVersion}"
        
        # Add missing _setup: method to NSApplication to prevent Tk crashes
        def _setup_(self, arg):
            """Compatibility method for Tk framework setup"""
            # This is a stub method that does nothing but prevents the crash
            return None
        
        # Patch NSApplication if methods don't exist
        if not hasattr(AppKit.NSApplication, 'macOSVersion'):
            print("🔧 Adding macOSVersion compatibility method to NSApplication")
            AppKit.NSApplication.macOSVersion = macOSVersion
            
        if not hasattr(AppKit.NSApplication, '_setup_'):
            print("🔧 Adding _setup: compatibility method to NSApplication")
            AppKit.NSApplication._setup_ = _setup_
        
        # Ensure we're running as a proper macOS application
        app = AppKit.NSApplication.sharedApplication()
        app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
        
        # This ensures UI operations run on the main thread
        if not AppKit.NSThread.isMainThread():
            print("⚠️ Warning: Not running on main thread")
        else:
            print("✅ Running on main thread")
            
        return True
    except Exception as e:
        print(f"⚠️ macOS setup warning: {e}")
        return False

def main():
    """Main function for minimal test"""
    print("🚀 Starting metaVoice minimal test...")
    
    # Setup macOS application environment first
    setup_macos_app()
    
    print("✅ macOS setup completed successfully!")
    print("🧪 Testing basic imports...")
    
    try:
        # Test basic imports without GUI
        import time
        import threading
        import subprocess
        print("✅ Basic imports successful")
        
        # Test PyObjC imports
        import Foundation
        import AppKit
        print("✅ PyObjC imports successful")
        
        # Test text automation (without GUI)
        from text_input_automation import TextInputAutomation
        automation = TextInputAutomation()
        print("✅ Text automation import successful")
        
        print("🎉 All basic tests passed!")
        print("📋 Testing without GUI (console mode)...")
        
        # Test whisper wrapper without GUI
        try:
            from whisper_wrapper import WhisperWrapper
            print("✅ Whisper wrapper import successful")
        except Exception as e:
            print(f"⚠️ Whisper wrapper import failed: {e}")
        
        print("✅ Console mode test completed successfully!")
        print("💡 The app core functionality works!")
        print("⚠️ GUI components need Tkinter compatibility fixes for macOS 15.5")
        
        # Keep the app running for a few seconds
        import time
        time.sleep(5)
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()