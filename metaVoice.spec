# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()

# Define paths for Whisper.cpp components
whisper_dir = current_dir / 'whisper.cpp'
whisper_bin = whisper_dir / 'build' / 'bin' / 'whisper-cli'
whisper_models = whisper_dir / 'models'

# Collect all model files
model_files = []
if whisper_models.exists():
    for model_file in whisper_models.glob('*.bin'):
        model_files.append((str(model_file), 'whisper_models'))

# Get CustomTkinter assets path
import customtkinter
ctk_path = os.path.dirname(customtkinter.__file__)

# Define data files to include
datas = [
    # Whisper.cpp binary
    (str(whisper_bin), '.'),
    # Whisper models
    *model_files,
    # CustomTkinter assets - include the entire package
    (ctk_path, 'customtkinter'),
    # Additional CustomTkinter assets
    (os.path.join(ctk_path, 'assets'), 'customtkinter/assets'),
    (os.path.join(ctk_path, 'assets', 'fonts'), 'customtkinter/assets/fonts'),
    (os.path.join(ctk_path, 'assets', 'icons'), 'customtkinter/assets/icons'),
    (os.path.join(ctk_path, 'assets', 'themes'), 'customtkinter/assets/themes'),
]

# Define hidden imports
hiddenimports = [
    'whisper_wrapper',
    'text_input_automation',
    'floating_recorder',
    'auto_input_voice_gui',
    'customtkinter',
    'customtkinter.windows.widgets',
    'customtkinter.windows.widgets.core_rendering',
    'customtkinter.windows.widgets.font',
    'customtkinter.windows.widgets.image',
    'customtkinter.windows.widgets.scaling',
    'customtkinter.windows.widgets.theme',
    'customtkinter.windows.widgets.appearance_mode',
    'customtkinter.windows.widgets.color',
    'customtkinter.windows.widgets.corner_radius',
    'customtkinter.windows.widgets.hover',
    'customtkinter.windows.widgets.border',
    'customtkinter.windows.widgets.entry',
    'customtkinter.windows.widgets.button',
    'customtkinter.windows.widgets.frame',
    'customtkinter.windows.widgets.label',
    'customtkinter.windows.widgets.textbox',
    'customtkinter.windows.widgets.checkbox',
    'customtkinter.windows.widgets.optionmenu',
    'customtkinter.windows.widgets.slider',
    'customtkinter.windows.widgets.progressbar',
    'customtkinter.windows.widgets.switch',
    'customtkinter.windows.widgets.tabview',
    'customtkinter.windows.widgets.scrollable_frame',
    'customtkinter.windows.widgets.toplevel',
    'customtkinter.windows.widgets.popup_menu',
    'customtkinter.windows.widgets.tooltip',
    'customtkinter.windows.widgets.segmented_button',
    'customtkinter.windows.widgets.selection',
    'customtkinter.windows.widgets.scaling',
    'customtkinter.windows.widgets.theme',
    'customtkinter.windows.widgets.appearance_mode',
    'customtkinter.windows.widgets.color',
    'customtkinter.windows.widgets.corner_radius',
    'customtkinter.windows.widgets.hover',
    'customtkinter.windows.widgets.border',
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'pyaudio',
    'numpy',
    'threading',
    'queue',
    'time',
    'wave',
    'subprocess',
    'os',
    'sys',
    'pathlib',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'pynput',
    'pynput.keyboard',
    'pynput.keyboard._base',
    'pynput.keyboard._darwin',
    'pyobjc',
    'pyobjc.ApplicationServices',
    'pyobjc.Quartz',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='metaVoice',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='metaVoice',
)

app = BUNDLE(
    coll,
    name='metaVoice.app',
    icon='metaVoice.icns',
    info_plist={
        'CFBundleName': 'metaVoice',
        'CFBundleDisplayName': 'metaVoice',
        'CFBundleIdentifier': 'com.metavoice.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleExecutable': 'metaVoice',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'LSMinimumSystemVersion': '10.15.0',
        'NSHighResolutionCapable': True,
        'NSMicrophoneUsageDescription': 'metaVoice needs microphone access to record voice commands.',
        'NSSystemAdministrationUsageDescription': 'metaVoice needs accessibility permissions to control other applications.',
    },
)
