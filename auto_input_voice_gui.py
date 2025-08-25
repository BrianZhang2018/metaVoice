#!/usr/bin/env python3
"""
metaVoice - Voice-to-Text Desktop Automation
Voice recorder that automatically inputs transcribed text into Cursor or any input box
"""

import tkinter as tk
import customtkinter as ctk
import threading
import time
import queue
from whisper_wrapper import WhisperWrapper
from text_input_automation import TextInputAutomation

# Set appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MetaVoiceApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("metaVoice")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Initialize components
        self.whisper = WhisperWrapper()
        self.automation = TextInputAutomation()
        self.is_recording = False
        self.should_stop_recording = False  # Flag to stop recording early
        
        # Settings
        self.target_app = "auto-detect"  # Default to auto-detection
        self.input_method = "clipboard"  # Default method
        self.auto_input_enabled = True
        
        # Statistics tracking
        self.recording_sessions = 0
        self.words_captured = 0
        self.total_speaking_time = 0
        
        # Floating recorder reference
        self.floating_recorder = None
        
        # Thread-safe communication queue
        self.update_queue = queue.Queue()
        
        self.create_widgets()
        
        # Start checking for updates from background threads
        self.check_queue()
        
    def create_widgets(self):
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Left Navigation Sidebar
        self.create_sidebar(main_container)
        
        # Main Content Area
        self.create_main_content(main_container)
        
    def create_sidebar(self, parent):
        # Sidebar frame
        sidebar = ctk.CTkFrame(parent, width=250, fg_color="#1a1a1a")
        sidebar.pack(side="left", fill="y", padx=0, pady=0)
        sidebar.pack_propagate(False)
        
        # metaVoice Logo/Title
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(20, 30))
        
        logo_label = ctk.CTkLabel(
            logo_frame, 
            text="metaVoice", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4CAF50"
        )
        logo_label.pack()
        
        # Navigation Menu
        nav_items = [
            ("Dashboard", "📊"),
            ("Settings", "⚙️"),
            ("History", "📝"),
            ("About", "ℹ️")
        ]
        
        self.nav_buttons = {}
        for text, icon in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"{icon} {text}",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                text_color="#ffffff",
                hover_color="#2a2a2a",
                anchor="w",
                height=40
            )
            btn.pack(fill="x", padx=15, pady=2)
            self.nav_buttons[text] = btn
            
            # Bind click events
            if text == "Dashboard":
                btn.configure(command=lambda: self.show_dashboard())
                btn.configure(fg_color="#3B8ED0")
            elif text == "Settings":
                btn.configure(command=lambda: self.show_settings())
            elif text == "History":
                btn.configure(command=lambda: self.show_history())
            elif text == "About":
                btn.configure(command=lambda: self.show_about())
    
    def create_main_content(self, parent):
        # Main content frame
        self.main_content = ctk.CTkFrame(parent, fg_color="transparent")
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Create different content areas
        self.create_dashboard()
        self.create_settings_panel()
        self.create_history_panel()
        self.create_about_panel()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_dashboard(self):
        # Dashboard frame
        self.dashboard_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        
        # Trial banner
        trial_banner = ctk.CTkFrame(self.dashboard_frame, fg_color="#2196F3", height=50)
        trial_banner.pack(fill="x", pady=(0, 20))
        trial_banner.pack_propagate(False)
        
        trial_label = ctk.CTkLabel(
            trial_banner,
            text="Trial Active • You have 7 days left in your trial",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        trial_label.pack(expand=True)
        
        # Main headline
        headline = ctk.CTkLabel(
            self.dashboard_frame,
            text="You are 4.4x Faster with metaVoice",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ffffff"
        )
        headline.pack(pady=(0, 30))
        
        # Highlight "4.4x Faster" in green
        headline.configure(text="You are ")
        faster_label = ctk.CTkLabel(
            self.dashboard_frame,
            text="4.4x Faster",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#4CAF50"
        )
        faster_label.pack(pady=(0, 30))
        meta_label = ctk.CTkLabel(
            self.dashboard_frame,
            text=" with metaVoice",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ffffff"
        )
        meta_label.pack(pady=(0, 30))
        
        # Time comparison cards
        time_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        time_frame.pack(fill="x", pady=(0, 20))
        
        # Speaking time card
        speaking_card = ctk.CTkFrame(time_frame, fg_color="#2E7D32", height=80)
        speaking_card.pack(side="left", fill="x", expand=True, padx=(0, 10))
        speaking_card.pack_propagate(False)
        
        speaking_content = ctk.CTkFrame(speaking_card, fg_color="transparent")
        speaking_content.pack(expand=True, padx=20, pady=10)
        
        speaking_icon = ctk.CTkLabel(speaking_content, text="🎤", font=ctk.CTkFont(size=20))
        speaking_icon.pack()
        speaking_label = ctk.CTkLabel(
            speaking_content,
            text="20s SPEAKING TIME",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffffff"
        )
        speaking_label.pack()
        
        # Typing time card
        typing_card = ctk.CTkFrame(time_frame, fg_color="#FF9800", height=80)
        typing_card.pack(side="right", fill="x", expand=True, padx=(10, 0))
        typing_card.pack_propagate(False)
        
        typing_content = ctk.CTkFrame(typing_card, fg_color="transparent")
        typing_content.pack(expand=True, padx=20, pady=10)
        
        typing_icon = ctk.CTkLabel(typing_content, text="⌨️", font=ctk.CTkFont(size=20))
        typing_icon.pack()
        typing_label = ctk.CTkLabel(
            typing_content,
            text="80s TYPING TIME",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffffff"
        )
        typing_label.pack()
        
        # Time saved section
        time_saved_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        time_saved_frame.pack(fill="x", pady=(0, 20))
        
        time_saved_label = ctk.CTkLabel(
            time_saved_frame,
            text="TIME SAVED",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        time_saved_label.pack(side="left")
        
        time_saved_value = ctk.CTkLabel(
            time_saved_frame,
            text="60s",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#2196F3"
        )
        time_saved_value.pack(side="left", padx=(10, 0))
        
        # Support section
        support_frame = ctk.CTkFrame(time_saved_frame, fg_color="transparent")
        support_frame.pack(side="right")
        
        support_icon = ctk.CTkLabel(support_frame, text="💬", font=ctk.CTkFont(size=16))
        support_icon.pack(side="left")
        support_text = ctk.CTkLabel(
            support_frame,
            text="Need Support? Got Feature Ideas? We're Listening!",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        support_text.pack(side="left", padx=(5, 10))
        
        discord_btn = ctk.CTkButton(
            support_frame,
            text="JOIN DISCORD →",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2196F3",
            height=30,
            width=120
        )
        discord_btn.pack(side="left")
        
        # Statistics grid
        stats_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Create 4 stat cards
        stats_data = [
            ("Words Captured", "0", "📋"),
            ("Voice-to-Text Sessions", "0", "🎤"),
            ("Average Words/Minute", "0", "⏱️"),
            ("Words/Session", "0", "📊")
        ]
        
        for i, (title, value, icon) in enumerate(stats_data):
            stat_card = ctk.CTkFrame(stats_frame, fg_color="#1a1a1a", height=100)
            stat_card.pack(side="left", fill="x", expand=True, padx=(0 if i == 0 else 10, 0))
            stat_card.pack_propagate(False)
            
            stat_content = ctk.CTkFrame(stat_card, fg_color="transparent")
            stat_content.pack(expand=True, padx=15, pady=15)
            
            stat_icon = ctk.CTkLabel(stat_content, text=icon, font=ctk.CTkFont(size=16))
            stat_icon.pack()
            stat_value = ctk.CTkLabel(
                stat_content,
                text=value,
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#ffffff"
            )
            stat_value.pack()
            stat_title = ctk.CTkLabel(
                stat_content,
                text=title,
                font=ctk.CTkFont(size=10),
                text_color="#888888"
            )
            stat_title.pack()
        
        # Main recording section
        recording_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="#1a1a1a")
        recording_frame.pack(fill="x", pady=(20, 0))
        
        recording_title = ctk.CTkLabel(
            recording_frame,
            text="Voice Recording",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        recording_title.pack(pady=(20, 10))
        
        # Record button
        self.record_button = ctk.CTkButton(
            recording_frame,
            text="🎤 Start Recording",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=200,
            height=60,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=self.toggle_recording
        )
        self.record_button.pack(pady=(0, 20))
        
        # Status text
        self.status_text = ctk.CTkTextbox(
            recording_frame, 
            width=800, 
            height=150,
            fg_color="#0a0a0a",
            text_color="#ffffff"
        )
        self.status_text.pack(pady=(0, 20))
        
        # Control buttons
        button_frame = ctk.CTkFrame(recording_frame, fg_color="transparent")
        button_frame.pack(pady=(0, 20))
        
        clear_button = ctk.CTkButton(
            button_frame, 
            text="Clear Log", 
            command=self.clear_log,
            fg_color="#666666",
            hover_color="#555555"
        )
        clear_button.pack(side="left", padx=5)
        
        test_button = ctk.CTkButton(
            button_frame, 
            text="Test Automation", 
            command=self.test_automation,
            fg_color="#666666",
            hover_color="#555555"
        )
        test_button.pack(side="left", padx=5)
        
        # Minimize to floating recorder button
        minimize_button = ctk.CTkButton(
            button_frame,
            text="Minimize to Floating Recorder",
            command=self.minimize_to_floating,
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        minimize_button.pack(side="left", padx=5)
    
    def create_settings_panel(self):
        self.settings_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        
        settings_title = ctk.CTkLabel(
            self.settings_frame,
            text="Settings",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ffffff"
        )
        settings_title.pack(pady=(0, 30))
        
        # Settings cards
        settings_container = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        settings_container.pack(fill="x")
        
        # Target app selection
        target_card = ctk.CTkFrame(settings_container, fg_color="#1a1a1a")
        target_card.pack(fill="x", pady=10)
        
        target_title = ctk.CTkLabel(
            target_card,
            text="Target Application",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        target_title.pack(pady=(15, 10))
        
        target_frame = ctk.CTkFrame(target_card, fg_color="transparent")
        target_frame.pack(pady=(0, 15))
        
        target_label = ctk.CTkLabel(target_frame, text="Target App:", font=ctk.CTkFont(size=12))
        target_label.pack(side="left", padx=10, pady=5)
        
        self.target_var = ctk.StringVar(value="auto-detect")
        target_options = ["auto-detect", "cursor", "qoder", "active", "safari", "chrome", "terminal", "notes", "vscode", "pycharm"]
        target_menu = ctk.CTkOptionMenu(target_frame, values=target_options, variable=self.target_var)
        target_menu.pack(side="left", padx=10, pady=5)
        
        # Input method selection
        method_card = ctk.CTkFrame(settings_container, fg_color="#1a1a1a")
        method_card.pack(fill="x", pady=10)
        
        method_title = ctk.CTkLabel(
            method_card,
            text="Input Method",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        method_title.pack(pady=(15, 10))
        
        method_frame = ctk.CTkFrame(method_card, fg_color="transparent")
        method_frame.pack(pady=(0, 15))
        
        method_label = ctk.CTkLabel(method_frame, text="Input Method:", font=ctk.CTkFont(size=12))
        method_label.pack(side="left", padx=10, pady=5)
        
        self.method_var = ctk.StringVar(value="clipboard")
        method_options = ["clipboard", "direct"]
        method_menu = ctk.CTkOptionMenu(method_frame, values=method_options, variable=self.method_var)
        method_menu.pack(side="left", padx=10, pady=5)
        
        # Auto-input toggle
        auto_card = ctk.CTkFrame(settings_container, fg_color="#1a1a1a")
        auto_card.pack(fill="x", pady=10)
        
        auto_title = ctk.CTkLabel(
            auto_card,
            text="Automation Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        auto_title.pack(pady=(15, 10))
        
        auto_frame = ctk.CTkFrame(auto_card, fg_color="transparent")
        auto_frame.pack(pady=(0, 15))
        
        self.auto_var = ctk.BooleanVar(value=True)
        auto_checkbox = ctk.CTkCheckBox(auto_frame, text="Auto-input enabled", variable=self.auto_var)
        auto_checkbox.pack(side="left", padx=10, pady=5)
        
    def create_history_panel(self):
        self.history_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        
        history_title = ctk.CTkLabel(
            self.history_frame,
            text="History & Logs",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ffffff"
        )
        history_title.pack(pady=(0, 30))
        
        # History text area
        self.history_text = ctk.CTkTextbox(
            self.history_frame,
            width=800,
            height=500,
            fg_color="#1a1a1a",
            text_color="#ffffff"
        )
        self.history_text.pack(pady=(0, 20))
        
        # History controls
        history_controls = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        history_controls.pack()
        
        clear_history_btn = ctk.CTkButton(
            history_controls,
            text="Clear History",
            command=self.clear_history,
            fg_color="#666666",
            hover_color="#555555"
        )
        clear_history_btn.pack(side="left", padx=5)
    
    def create_about_panel(self):
        self.about_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        
        about_title = ctk.CTkLabel(
            self.about_frame,
            text="About metaVoice",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ffffff"
        )
        about_title.pack(pady=(0, 30))
        
        about_content = ctk.CTkFrame(self.about_frame, fg_color="#1a1a1a")
        about_content.pack(fill="x", pady=10)
        
        about_text = ctk.CTkLabel(
            about_content,
            text="metaVoice is a desktop automation system that uses voice commands to control your computer, record and analyze meetings, and learn from your work patterns.\n\nFeatures:\n• Voice Command Recognition\n• Desktop Automation\n• Meeting Recording & Analysis\n• Local Learning\n• Privacy-First\n\nHotkey: Cmd+Shift+R to show/hide floating recorder",
            font=ctk.CTkFont(size=14),
            text_color="#ffffff",
            justify="left"
        )
        about_text.pack(pady=20, padx=20)
    
    def show_dashboard(self):
        self.hide_all_panels()
        self.dashboard_frame.pack(fill="both", expand=True)
        self.update_nav_selection("Dashboard")
    
    def show_settings(self):
        self.hide_all_panels()
        self.settings_frame.pack(fill="both", expand=True)
        self.update_nav_selection("Settings")
    
    def show_history(self):
        self.hide_all_panels()
        self.history_frame.pack(fill="both", expand=True)
        self.update_nav_selection("History")
    
    def show_about(self):
        self.hide_all_panels()
        self.about_frame.pack(fill="both", expand=True)
        self.update_nav_selection("About")
    
    def hide_all_panels(self):
        self.dashboard_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.history_frame.pack_forget()
        self.about_frame.pack_forget()
    
    def update_nav_selection(self, selected):
        for name, btn in self.nav_buttons.items():
            if name == selected:
                btn.configure(fg_color="#3B8ED0")
            else:
                btn.configure(fg_color="transparent")
    
    def clear_history(self):
        self.history_text.delete("1.0", "end")
    
    def minimize_to_floating(self):
        """Minimize dashboard and show floating recorder"""
        self.hide_window()
        if self.floating_recorder:
            self.floating_recorder.show_window()
    
    def show_window(self):
        """Show the dashboard window"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def hide_window(self):
        """Hide the dashboard window"""
        self.root.withdraw()
    
    def set_floating_recorder(self, floating_recorder):
        """Set reference to floating recorder"""
        self.floating_recorder = floating_recorder
        print(f"✅ Floating recorder reference set: {floating_recorder is not None}")
    
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
        
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.status_text.insert("end", log_message)
        self.status_text.see("end")
        self.history_text.insert("end", log_message)
        self.history_text.see("end")
        print(message)
    
    def clear_log(self):
        """Clear the log"""
        self.status_text.delete("1.0", "end")
    
    def toggle_recording(self):
        """Toggle recording on/off"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start recording"""
        self.is_recording = True
        self.record_button.configure(text="⏹️ Stop Recording", fg_color="#ff6666")
        
        # Get current settings
        self.target_app = self.target_var.get()
        self.input_method = self.method_var.get()
        self.auto_input_enabled = self.auto_var.get()
        
        self.log("🎤 Starting recording...")
        self.log(f"📱 Target app: {self.target_app}")
        self.log(f"⌨️ Input method: {self.input_method}")
        self.log(f"🤖 Auto-input: {'Enabled' if self.auto_input_enabled else 'Disabled'}")
        
        # Start recording in thread
        thread = threading.Thread(target=self.record_audio)
        thread.daemon = True
        thread.start()
    
    def stop_recording(self):
        """Stop recording"""
        self.should_stop_recording = True  # Set flag to stop recording
        self.is_recording = False
        self.record_button.configure(text="🎤 Start Recording", fg_color="#4CAF50")
        self.log("⏹️ Recording stopped by user")
    
    def record_audio(self):
        """Record audio with auto-input"""
        try:
            self.log("🎤 Recording for 20 seconds...")
            self.log("🎤 SPEAK NOW! Your words will be typed automatically!")
            self.log("🎤 Click the stop button to finish early!")
            self.log("🎯 Using ACCURATE mode for best transcription quality")
            
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
            
            self.log("✅ Recording finished")
            self.log(f"🎯 Transcribed text: '{text}'")
            
            # Update statistics
            self.recording_sessions += 1
            if text and text.strip() and text.strip() != "[BLANK_AUDIO]":
                words = len(text.split())
                self.words_captured += words
                self.total_speaking_time += 20
            
            # Send update to main thread via queue
            self.update_queue.put(("transcription", text))
            
        except Exception as e:
            self.log(f"❌ Error: {e}")
            self.update_queue.put(("error", str(e)))
    
    def handle_transcription(self, text):
        """Handle transcription results"""
        if text and text.strip() and text.strip() != "[BLANK_AUDIO]":
            self.log("✅ SUCCESS! Speech detected!")
            
            # Parse command
            command = self.whisper.parse_command(text)
            self.log(f"🔍 Parsed command: {command}")
            
            if command["command"] != "unknown":
                self.log("🎉 Command recognized!")
                # Handle specific commands
                self.handle_command(command)
            else:
                self.log("⚠️ Command not recognized, treating as text input")
                # Auto-input the transcribed text
                if self.auto_input_enabled:
                    self.auto_input_text(text)
                else:
                    self.log("🤖 Auto-input disabled, text not sent")
        else:
            self.log("❌ No speech detected")
            self.log("🔧 Troubleshooting:")
            self.log("  - Did you speak during the recording?")
            self.log("  - Was your speech loud enough?")
            self.log("  - Try speaking louder and more clearly")
        
        self.is_recording = False
        self.record_button.configure(text="🎤 Start Recording", fg_color="#4CAF50")
    
    def handle_command(self, command):
        """Handle recognized commands"""
        cmd = command["command"]
        params = command["parameters"]
        
        if cmd == "record-meeting":
            self.log("📹 Starting meeting recording...")
            # TODO: Implement meeting recording
            self.log("📹 Meeting recording started")
        elif cmd == "build-app":
            app_type = params.get("type", "react")
            app_name = params.get("name", "my-app")
            self.log(f"🚀 Building {app_type} app named '{app_name}'...")
            # TODO: Implement app building
            self.log(f"🚀 App building initiated")
        else:
            self.log(f"🔧 Command '{cmd}' not yet implemented")
    
    def auto_input_text(self, text):
        """Auto-input text into target application"""
        try:
            self.log(f"🎯 Auto-inputting text: '{text[:50]}...'")
            
            success = self.automation.auto_input_text(
                text, 
                self.target_app, 
                self.input_method
            )
            
            if success:
                self.log("✅ Text successfully input!")
            else:
                self.log("❌ Failed to input text")
                
        except Exception as e:
            self.log(f"❌ Error auto-inputting text: {e}")
    
    def test_automation(self):
        """Test the automation system"""
        self.log("🧪 Testing automation system...")
        
        try:
            success = self.automation.test_automation()
            if success:
                self.log("✅ Automation test successful!")
            else:
                self.log("❌ Automation test failed")
        except Exception as e:
            self.log(f"❌ Automation test error: {e}")
    
    def handle_error(self, error_msg):
        """Handle errors"""
        self.log(f"❌ Error: {error_msg}")
        self.is_recording = False
        self.record_button.configure(text="🎤 Start Recording", fg_color="#4CAF50")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    app = MetaVoiceApp()
    app.run()

if __name__ == "__main__":
    main() 