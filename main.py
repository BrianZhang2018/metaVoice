#!/usr/bin/env python3
"""
metaVoice - Main Entry Point
Starts both the dashboard and floating recorder together
"""

import threading
import time
from auto_input_voice_gui import MetaVoiceApp
from floating_recorder import FloatingRecorder

def main():
    """Main function that starts both components"""
    print("🚀 Starting metaVoice...")
    print("📊 Initializing dashboard (hidden by default)...")
    print("🎤 Initializing floating recorder (visible by default)...")
    
    # Create dashboard instance (will be hidden by default)
    dashboard = MetaVoiceApp()
    
    # Create floating recorder instance (will be visible by default)
    floating_recorder = FloatingRecorder()
    
    # Set up cross-references between components
    print("🔗 Setting up component communication...")
    dashboard.set_floating_recorder(floating_recorder)
    floating_recorder.set_dashboard(dashboard)
    
    # Start dashboard in hidden mode
    print("📊 Starting dashboard in hidden mode...")
    dashboard.hide_window()
    
    # Start floating recorder in visible mode
    print("🎤 Starting floating recorder in visible mode...")
    floating_recorder.show_window()
    
    print("✅ metaVoice started successfully!")
    print("💡 Use the ⚙️ button on the floating recorder to open the dashboard")
    print("💡 Use Cmd+Shift+R to show/hide the floating recorder")
    print("💡 Use Cmd (Command key) to start/stop recording")
    
    # Run floating recorder in main thread (this will show the floating window)
    print("🎤 Starting floating recorder main loop...")
    floating_recorder.run()

if __name__ == "__main__":
    main()
