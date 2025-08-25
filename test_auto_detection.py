#!/usr/bin/env python3
"""
Test Auto-Detection with Enhanced Logging
Quick test to see what app is currently detected and how the mapping works
"""

from text_input_automation import TextInputAutomation

def test_auto_detection():
    """Test the auto-detection with enhanced logging"""
    print("🎯 Testing Auto-Detection with Enhanced Logging")
    print("=" * 60)
    print()
    
    automation = TextInputAutomation()
    
    print("1. Testing frontmost app detection...")
    frontmost = automation.get_frontmost_app()
    print()
    
    print("2. Testing auto-detection logic...")
    target = automation.auto_detect_target()
    print()
    
    print("3. Testing auto-input text simulation...")
    print("📝 Simulating text input (no actual input will happen)")
    
    # Test with some sample text - this will show all the debug info
    result = automation.auto_input_text(
        "This is a test message to see auto-detection in action!",
        "auto-detect",  # Use auto-detect
        "clipboard"     # Use clipboard method
    )
    
    print()
    print(f"✅ Auto-input simulation result: {result}")
    print()
    print("🎯 Debug Summary:")
    print(f"   📱 Detected frontmost app: '{frontmost}'")
    print(f"   🎯 Mapped to target: '{target}'")
    print(f"   🔄 Auto-input completed: {result}")

if __name__ == "__main__":
    test_auto_detection()