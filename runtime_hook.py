#!/usr/bin/env python3
"""
Runtime Hook for metaVoice App
Handles macOS-specific threading and compatibility issues
"""

import sys
import os

def setup_macos_compatibility():
    """Setup macOS compatibility fixes"""
    try:
        # Fix for Input Source Manager threading issues
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
        
        # Ensure we're running on the main thread for UI operations
        if AppKit.NSThread.isMainThread():
            print("✅ Running on main thread")
        else:
            print("⚠️ Warning: Not running on main thread")
        
        # Initialize Application Services properly
        app = AppKit.NSApplication.sharedApplication()
        app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
        
        # Set up input source handling
        if hasattr(Foundation, 'NSRunLoop'):
            runloop = Foundation.NSRunLoop.currentRunLoop()
            print("✅ NSRunLoop initialized")
            
    except ImportError as e:
        print(f"⚠️ macOS compatibility setup skipped: {e}")
    except Exception as e:
        print(f"⚠️ macOS compatibility warning: {e}")

def setup_environment():
    """Setup environment variables for the packaged app"""
    # Set up paths for bundled resources
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        bundle_dir = sys._MEIPASS
        
        # Add whisper models path
        whisper_models_path = os.path.join(bundle_dir, 'whisper_models')
        if os.path.exists(whisper_models_path):
            os.environ['WHISPER_MODELS_PATH'] = whisper_models_path
            print(f"✅ Whisper models path: {whisper_models_path}")
        
        # Add customtkinter assets path
        ctk_assets_path = os.path.join(bundle_dir, 'customtkinter', 'assets')
        if os.path.exists(ctk_assets_path):
            os.environ['CUSTOMTKINTER_ASSETS_PATH'] = ctk_assets_path
            print(f"✅ CustomTkinter assets path: {ctk_assets_path}")
            
        print(f"✅ Bundle directory: {bundle_dir}")
    else:
        print("✅ Running in development mode")

def main():
    """Main runtime hook execution"""
    print("🔧 Running metaVoice runtime hook...")
    
    # Setup environment
    setup_environment()
    
    # Setup macOS compatibility
    setup_macos_compatibility()
    
    print("✅ Runtime hook completed")

if __name__ == "__main__":
    main()