#!/usr/bin/env python3
"""
metaVoice Floating Recorder
Floating recording status window with global hotkey support
"""

import tkinter as tk
import customtkinter as ctk
import threading
import time
import queue
from pynput import keyboard
import pyaudio
import numpy as np
from whisper_wrapper import WhisperWrapper
from text_input_automation import TextInputAutomation

# Set appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class FloatingRecorder:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("metaVoice Recorder")
        self.root.geometry("300x100")  # Increased height to accommodate all buttons
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        # Set maximum window level to stay above all apps
        try:
            self.root.call('wm', 'attributes', '.', '-level', 'floating')
        except:
            pass
        
        # Try to remove window decorations, but handle potential errors
        try:
            self.root.overrideredirect(True)  # Remove window decorations
        except Exception as e:
            print(f"⚠️  Could not remove window decorations: {e}")
            # Fallback: try alternative method
            try:
                self.root.attributes('-type', 'dock')  # macOS dock-style window
            except:
                pass  # Continue without borderless window
        
        # Ensure window is properly initialized and clickable
        self.root.update_idletasks()
        self.root.lift()
        self.root.focus_force()
        
        # Position in top-right corner
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"300x100+{screen_width-320}+20")  # Updated height
        
        # Initialize components
        self.whisper = WhisperWrapper()
        self.automation = TextInputAutomation()
        self.is_recording = False
        self.is_visible = False
        self.should_stop_recording = False  # Flag to stop recording early
        
        # Hotkey listener
        self.hotkey_listener = None
        
        # Audio visualization
        self.audio_levels = [0] * 12
        self.audio_thread = None
        self.audio_running = False
        
        # Settings
        self.target_app = "cursor"
        self.input_method = "clipboard"
        self.auto_input_enabled = True
        
        # Dashboard reference (will be set later)
        self.dashboard = None
        
        # Thread-safe communication queue
        self.update_queue = queue.Queue()
        
        # Create a simple restore file to help users find the window
        self.create_restore_file()
        
        self.create_widgets()
        self.setup_hotkey()
        
        # Start checking for updates from background threads
        self.check_queue()
    
    def create_restore_file(self):
        """Create a simple restore file to help users find the window"""
        try:
            import os
            restore_file = os.path.join(os.path.dirname(__file__), '.floating_recorder_running')
            with open(restore_file, 'w') as f:
                f.write(f"metaVoice floating recorder is running\nPID: {os.getpid()}\n")
        except:
            pass
        
    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="#2a2a2a", corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Record button (left) - macOS style
        self.record_button = ctk.CTkButton(
            main_frame,
            text="●",  # Record symbol
            width=48,  # Slightly smaller for better proportion
            height=48,  # Slightly smaller for better proportion
            corner_radius=24,  # Perfect circle
            fg_color="#4CAF50",  # Green for recording
            hover_color="#45a049",  # Darker green on hover
            command=self.toggle_recording,
            font=ctk.CTkFont(size=18, weight="bold"),  # Slightly smaller font
            text_color="#ffffff"  # White text
        )
        self.record_button.pack(side="left", padx=15, pady=10)
        
        # Remove the separate icon label since we're using button text
        # self.record_icon = tk.Label(...) - REMOVED
        
        # Audio visualizer (middle)
        self.visualizer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.visualizer_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        # Create visualizer bars
        self.visualizer_bars = []
        for i in range(12):
            bar = ctk.CTkFrame(
                self.visualizer_frame,
                fg_color="#ffffff",
                width=3,
                height=20
            )
            bar.pack(side="left", padx=1, pady=10)
            self.visualizer_bars.append(bar)
        
        # Right side button frame
        right_button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_button_frame.pack(side="right", padx=5, pady=10)
        
        # Hide button - macOS style yellow (since minimize doesn't work with borderless windows)
        self.minimize_button = ctk.CTkButton(
            right_button_frame,
            text="−",
            width=28,
            height=28,
            corner_radius=14,
            fg_color="#FFBD2E",
            hover_color="#E6A825",
            command=self.minimize_window,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000"
        )
        self.minimize_button.pack(side="top", pady=3)
        
        # Close button - macOS style red
        self.close_button = ctk.CTkButton(
            right_button_frame,
            text="×",
            width=28,
            height=28,
            corner_radius=14,
            fg_color="#FF5F57",
            hover_color="#E64A47",
            command=self.close_window,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000"
        )
        self.close_button.pack(side="top", pady=3)
        
        # Settings label - clickable text
        self.settings_label = ctk.CTkLabel(
            right_button_frame,
            text="SETTINGS",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#FF6B35",  # Bright orange text
            cursor="hand2"  # Hand cursor on hover
        )
        self.settings_label.pack(side="top", pady=5)
        self.settings_label.bind("<Button-1>", lambda e: self.open_dashboard())
        print(f"✅ Settings label created: {self.settings_label is not None}")
        
        # Hotkey indicator (small label)
        self.hotkey_label = ctk.CTkLabel(
            main_frame,
            text="⌨️ ⌘+⌥",
            font=ctk.CTkFont(size=8),
            text_color="#888888"
        )
        self.hotkey_label.pack(side="bottom", pady=2)
        
        # Make window draggable
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.on_drag)
        
        # Hide window initially - will only show during recording
        self.root.withdraw()
        self.is_visible = False
        
    def setup_hotkey(self):
        """Setup global hotkeys for the floating window using pynput"""
        self.hotkeys_registered = False
        
        try:
            # Define hotkey mappings
            hotkey_map = {
                '<cmd>+<alt>': self.toggle_recording,  # Command+Alt for recording
                '<f2>': self.toggle_visibility,    # F2 for show/hide window
                '<cmd>+<shift>+d': self.open_dashboard,  # Command+Shift+D for dashboard
                '<cmd>+<shift>+z': self.open_dashboard,  # Command+Shift+Z for dashboard (alternative)
            }
            
            # Create and start the global hotkey listener
            self.hotkey_listener = keyboard.GlobalHotKeys(hotkey_map)
            self.hotkey_listener.start()
            
            print("✅ Recording hotkey registered: Command+Alt")
            print("✅ Window hotkey registered: F2")
            print("✅ Dashboard hotkey registered: Command+Shift+D")
            print("✅ Dashboard hotkey registered: Command+Shift+Z (alternative)")
            
            self.hotkeys_registered = True
            self.update_hotkey_label("⌨️ ⌘+⌥")
            
        except Exception as e:
            print(f"❌ Failed to register hotkeys: {e}")
            if "accessibility" in str(e).lower():
                print("💡 Accessibility permissions required for global hotkeys")
                print("💡 Go to System Preferences → Security & Privacy → Privacy → Accessibility")
                print("💡 Add your application to the list")
            else:
                print("💡 You may need to grant accessibility permissions")
                print("💡 Alternative: Use the floating window buttons instead")
            
            self.update_hotkey_label("⌨️ Use buttons")
    
    def update_hotkey_label(self, text):
        """Update the hotkey indicator label"""
        if hasattr(self, 'hotkey_label'):
            self.hotkey_label.configure(text=text)
    
    def show_hotkey_notification(self, message):
        """Show a brief notification for hotkey actions"""
        # Temporarily change the hotkey label to show the action
        original_text = self.hotkey_label.cget("text")
        self.hotkey_label.configure(text=message, text_color="#4CAF50")
        
        # Reset after 2 seconds
        self.root.after(2000, lambda: self.hotkey_label.configure(text=original_text, text_color="#888888"))
    
    def toggle_visibility(self):
        """Toggle floating window visibility (manual override)"""
        if self.is_visible:
            print("👁️ Hotkey: Hiding window...")
            self.hide_window()
        else:
            print("👁️ Hotkey: Showing window...")
            self.show_window()
            # If not recording, auto-hide after 3 seconds
            if not self.is_recording:
                def auto_hide():
                    time.sleep(3)
                    if not self.is_recording:  # Double check we're not recording
                        self.hide_window()
                        print("⏰ Auto-hiding window after 3 seconds")
                
                auto_hide_thread = threading.Thread(target=auto_hide)
                auto_hide_thread.daemon = True
                auto_hide_thread.start()
    
    def is_window_minimized(self):
        """Check if window is minimized"""
        try:
            # Try to get window state
            state = self.root.state()
            return state == 'iconic'
        except:
            return False
    
    def restore_window(self):
        """Restore window from minimized state"""
        if self.is_window_minimized():
            self.show_window()
            print("📱 Window restored from minimized state")
    
    def show_window(self):
        """Show the floating window"""
        # Handle both withdrawn and minimized states
        try:
            self.root.deiconify()
        except:
            # If deiconify fails, the window might be withdrawn
            self.root.withdraw()
            self.root.deiconify()
        
        self.is_visible = True
        self.root.lift()
        self.root.focus_force()
        # Ensure maximum priority
        self.root.attributes('-topmost', True)
        try:
            self.root.call('wm', 'attributes', '.', '-level', 'floating')
        except:
            pass
    
    def hide_window(self):
        """Hide the floating window"""
        self.root.withdraw()
        self.is_visible = False
    
    def minimize_window(self):
        """Hide the floating window (since minimize doesn't work with borderless windows)"""
        print("📱 Hiding floating window...")
        self.show_hotkey_notification("📱 Hidden")
        
        # Just hide the window since iconify doesn't work with overrideredirect
        self.hide_window()
        
        # Show a notification about how to restore
        print("💡 Window hidden! Use F2 to show it again")
        print("💡 Or run: python floating_recorder.py to restart")
        
        # Try to show a system notification
        try:
            import subprocess
            subprocess.run([
                'osascript', '-e', 
                'display notification "metaVoice is hidden. Use F2 to restore." with title "metaVoice"'
            ])
        except:
            pass
    
    def close_window(self):
        """Close the floating window and exit application"""
        print("❌ Closing floating window...")
        
        # Show confirmation dialog
        try:
            import tkinter.messagebox as messagebox
            result = messagebox.askyesno(
                "Close metaVoice", 
                "Are you sure you want to close metaVoice?\n\nThis will stop all recording and exit the application."
            )
            if not result:
                return
        except:
            # If messagebox fails, proceed anyway
            pass
        
        # Stop recording if active
        if self.is_recording:
            self.stop_recording()
        
        # Stop audio visualization
        self.stop_audio_visualization()
        
        # Stop hotkey listener
        if self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
                print("🔇 Hotkey listener stopped")
            except:
                pass
        
        # Clean up restore file
        try:
            import os
            restore_file = os.path.join(os.path.dirname(__file__), '.floating_recorder_running')
            if os.path.exists(restore_file):
                os.remove(restore_file)
        except:
            pass
        
        # Close the window
        self.root.destroy()
        
        # Exit the application
        import sys
        sys.exit(0)
    
    def start_drag(self, event):
        """Start dragging the window"""
        self.x = event.x
        self.y = event.y
    
    def on_drag(self, event):
        """Handle window dragging"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def update_record_button(self):
        """Update record button appearance"""
        if self.is_recording:
            self.record_button.configure(fg_color="#FF5F57", text="⏹")  # Red when recording
        else:
            self.record_button.configure(fg_color="#4CAF50", text="●")  # Green when ready
    
    def update_visualizer(self):
        """Update audio visualizer bars"""
        if not self.audio_running:
            return
        
        # Simulate audio levels (replace with real audio analysis)
        if self.is_recording:
            # Generate random levels for demo
            self.audio_levels = [np.random.randint(5, 25) for _ in range(12)]
        else:
            # Reset to low levels
            self.audio_levels = [2] * 12
        
        # Update bar heights
        for i, bar in enumerate(self.visualizer_bars):
            height = max(5, self.audio_levels[i])
            bar.configure(height=height)
        
        # Schedule next update
        self.root.after(100, self.update_visualizer)
    
    def start_audio_visualization(self):
        """Start audio visualization thread"""
        self.audio_running = True
        self.update_visualizer()
    
    def stop_audio_visualization(self):
        """Stop audio visualization"""
        self.audio_running = False
        # Reset bars
        for bar in self.visualizer_bars:
            bar.configure(height=5)
    
    def toggle_recording(self):
        """Toggle recording on/off"""
        if self.is_recording:
            print("⏹️ Hotkey: Stopping recording...")
            self.show_hotkey_notification("⏹️ Stopping...")
            self.stop_recording()
        else:
            print("🎤 Hotkey: Starting recording...")
            self.show_hotkey_notification("🎤 Recording...")
            self.start_recording()
    
    def start_recording(self):
        """Start recording"""
        self.is_recording = True
        self.update_record_button()
        self.start_audio_visualization()
        
        # Show window during recording
        self.show_window()
        
        print("🎤 Starting recording...")
        
        # Start recording in thread
        thread = threading.Thread(target=self.record_audio)
        thread.daemon = True
        thread.start()
    
    def stop_recording(self):
        """Stop recording"""
        self.should_stop_recording = True  # Set flag to stop recording
        self.is_recording = False
        self.update_record_button()
        self.stop_audio_visualization()
        
        # Hide window after recording
        self.hide_window()
        
        print("⏹️ Recording stopped")
    
    def record_audio(self):
        """Record audio with auto-input"""
        try:
            print("🎤 Recording for 20 seconds...")
            print("🎤 SPEAK NOW! Your words will be typed automatically!")
            print("🎤 Click the stop button to finish early!")
            print("🎯 Using ACCURATE mode for best transcription quality")
            
            # Reset stop flag
            self.should_stop_recording = False
            
            # Create stop flag function
            def should_stop():
                return self.should_stop_recording
            
            # Record audio with accurate mode and stop flag
            text = self.whisper.transcribe_microphone(
                duration=20, 
                speed_mode="accurate",
                stop_flag=should_stop
            )
            
            print("✅ Recording finished")
            print(f"🎯 Transcribed text: '{text}'")
            
            # Send update to main thread via queue
            self.update_queue.put(("transcription", text))
            
        except Exception as e:
            print(f"❌ Error: {e}")
            self.update_queue.put(("error", str(e)))
    
    def handle_transcription(self, text):
        """Handle transcription results"""
        self.stop_recording()
        
        if text and text.strip() and text.strip() != "[BLANK_AUDIO]":
            print("✅ SUCCESS! Speech detected!")
            
            # Parse command
            command = self.whisper.parse_command(text)
            print(f"🔍 Parsed command: {command}")
            
            if command["command"] != "unknown":
                print("🎉 Command recognized!")
                # Handle specific commands
                self.handle_command(command)
            else:
                print("⚠️ Command not recognized, treating as text input")
                # Auto-input the transcribed text
                if self.auto_input_enabled:
                    self.auto_input_text(text)
                else:
                    print("🤖 Auto-input disabled, text not sent")
        else:
            print("❌ No speech detected")
    
    def handle_command(self, command):
        """Handle recognized commands"""
        cmd = command["command"]
        params = command["parameters"]
        
        if cmd == "record-meeting":
            print("📹 Starting meeting recording...")
            # TODO: Implement meeting recording
            print("📹 Meeting recording started")
        elif cmd == "build-app":
            app_type = params.get("type", "react")
            app_name = params.get("name", "my-app")
            print(f"🚀 Building {app_type} app named '{app_name}'...")
            # TODO: Implement app building
            print(f"🚀 App building initiated")
        else:
            print(f"🔧 Command '{cmd}' not yet implemented")
    
    def auto_input_text(self, text):
        """Auto-input text into target application"""
        try:
            print(f"🎯 Auto-inputting text: '{text[:50]}...'")
            
            success = self.automation.auto_input_text(
                text, 
                self.target_app, 
                self.input_method
            )
            
            if success:
                print("✅ Text successfully input!")
            else:
                print("❌ Failed to input text")
                
        except Exception as e:
            print(f"❌ Error auto-inputting text: {e}")
    
    def handle_error(self, error_msg):
        """Handle errors"""
        print(f"❌ Error: {error_msg}")
        self.stop_recording()
    
    def open_dashboard(self):
        """Open the main dashboard window"""
        print("⚙️ Hotkey: Opening dashboard...")
        if self.dashboard:
            print("✅ Dashboard found, opening...")
            # Schedule dashboard opening on main thread to avoid threading issues
            self.root.after(0, self._open_dashboard_safe)
            print("✅ Dashboard opening scheduled")
        else:
            print("⚠️ Dashboard not available - reference not set")
            print("💡 This might be a connection issue between windows")
    
    def _open_dashboard_safe(self):
        """Safely open dashboard on main thread"""
        try:
            self.dashboard.show_window()
            print("✅ Dashboard opened successfully")
        except Exception as e:
            print(f"❌ Error opening dashboard: {e}")
    
    def set_dashboard(self, dashboard):
        """Set reference to main dashboard"""
        self.dashboard = dashboard
        print(f"✅ Dashboard reference set: {dashboard is not None}")
    
    def check_queue(self):
        """Check for updates from background threads"""
        try:
            while True:
                # Non-blocking check for queue items
                update_type, data = self.update_queue.get_nowait()
                
                if update_type == "transcription":
                    self.handle_transcription(data)
                elif update_type == "error":
                    self.handle_error(data)
                    
        except queue.Empty:
            # No updates in queue, continue
            pass
        
        # Schedule next check
        self.root.after(100, self.check_queue)
    
    def run(self):
        """Run the floating recorder"""
        self.root.mainloop()

def main():
    """Main function for testing the floating recorder"""
    recorder = FloatingRecorder()
    recorder.show_window()
    recorder.run()

if __name__ == "__main__":
    main() 