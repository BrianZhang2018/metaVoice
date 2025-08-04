#!/usr/bin/env python3
"""
Runtime hook to fix path issues when metaVoice app is moved to Applications
"""

import os
import sys
from pathlib import Path

def fix_paths():
    """Fix paths for bundled app when moved to Applications"""
    
    # Get the app bundle path
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        app_path = Path(sys._MEIPASS)
        bundle_path = Path(sys.executable).parent.parent.parent
        
        # Set environment variables for the app
        os.environ['META_VOICE_APP_PATH'] = str(bundle_path)
        os.environ['META_VOICE_RESOURCE_PATH'] = str(app_path)
        
        # Add the resource path to sys.path
        if str(app_path) not in sys.path:
            sys.path.insert(0, str(app_path))
        
        print(f"✅ App bundle path: {bundle_path}")
        print(f"✅ Resource path: {app_path}")
    else:
        # Running in development
        print("🔧 Running in development mode")

# Run the path fix
fix_paths() 