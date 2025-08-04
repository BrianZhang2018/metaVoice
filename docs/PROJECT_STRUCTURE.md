# Project Structure

## Overview
This document describes the cleaned and organized project structure for metaVoice.

## Directory Structure

### Core Application (Root Directory)
- **auto_input_voice_gui.py**: Main GUI application with modern interface
- **whisper_wrapper.py**: Voice recognition wrapper for Whisper.cpp
- **text_input_automation.py**: Desktop automation functionality
- **floating_recorder.py**: Compact floating recorder window

### App Bundle Files
- **metaVoice.spec**: PyInstaller configuration for macOS app bundle
- **runtime_hook.py**: Path resolution for bundled applications
- **install_metaVoice.sh**: Installation script for macOS app bundle

### Testing (`tests/`)
- **test_auto_input.py**: Tests for auto-input functionality
- **test_whisper.py**: Tests for voice recognition

### Documentation (`docs/`)
- **features/**: Feature-specific documentation
- **GUI_GUIDE.md**: How to use the GUI interface
- **HOW_TO_RUN.md**: Detailed running instructions
- **README.md**: Comprehensive documentation
- **PROJECT_STRUCTURE.md**: This file

### Examples (`examples/`)
- **example_usage.py**: Basic usage examples
- **run_voice_commands.py**: Voice command examples

### External Dependencies
- **whisper.cpp/**: Whisper.cpp installation for voice recognition

### Configuration Files
- **requirements.txt**: Python dependencies
- **setup_permissions.py**: Permission setup utility

### Documentation (Root Directory)
- **INSTALLATION_GUIDE.md**: User-friendly installation guide
- **README.md**: Main project overview
- **GUI_GUIDE.md**: Interface documentation
- **HOW_TO_RUN.md**: Development setup guide
- **HOTKEY_GUIDE.md**: Hotkey configuration

## Cleanup Summary

### Removed Files
- **.history/**: 100+ backup files from development
- **build/**: PyInstaller build artifacts (regeneratable)
- **dist/**: PyInstaller output (regeneratable)
- **__pycache__/**: Python cache files
- **src/**: Redundant source files (moved to root)
- **backup_before_cleanup/**: Old backup directory
- **auto_input_voice_gui_backup.py**: Backup file
- ***.tmp**: Temporary files

### Consolidated Structure
- Core application files moved to root directory
- App bundle files organized together
- Documentation consolidated and updated
- Maintained essential functionality

### Preserved Files
- All core application files
- All test files
- All example files
- All essential documentation
- Configuration files
- External dependencies
- App bundle configuration

## Benefits of Cleanup

1. **Reduced Complexity**: Removed deprecated and unused files
2. **Better Organization**: Clear separation of concerns
3. **Easier Maintenance**: Simplified project structure
4. **Improved Documentation**: Consolidated and updated docs
5. **Cleaner Repository**: No cache or temporary files
6. **App Bundle Ready**: Optimized for macOS app distribution
7. **User-Friendly**: Easy installation and setup process

## Current Project Size
- **Total Size**: 294MB (mostly whisper.cpp models)
- **Core Application**: ~100KB
- **Documentation**: ~50KB
- **Dependencies**: ~294MB (whisper.cpp)

## Ready For
- ✅ Development and testing
- ✅ macOS app bundle distribution
- ✅ Easy user onboarding
- ✅ Documentation and tutorials
