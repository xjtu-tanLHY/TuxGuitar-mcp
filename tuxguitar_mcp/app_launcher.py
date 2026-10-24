from __future__ import annotations
import os
import subprocess
import sys
from typing import Dict, Any, Optional

DEFAULT_TG_DIR = r"D:\Program Files\tuxguitar"


def find_tuxguitar_executable() -> Optional[str]:
    # Check directory of this package or DEFAULT_TG_DIR
    candidates = [
        os.path.join(DEFAULT_TG_DIR, "tuxguitar.exe"),
        os.path.join(DEFAULT_TG_DIR, "tuxguitar.bat"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tuxguitar.exe")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tuxguitar.bat")),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c

    # Check PATH
    try:
        import shutil
        found = shutil.which("tuxguitar")
        if found:
            return found
    except Exception:
        pass
    return None


def get_tuxguitar_status() -> Dict[str, Any]:
    exe = find_tuxguitar_executable()
    is_running = False
    pids = []

    # Check running processes using powershell Get-Process or tasklist
    try:
        if sys.platform == "win32":
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Get-Process -Name tuxguitar -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"],
                capture_output=True,
                text=True,
                timeout=5
            )
            out = res.stdout.strip()
            if out:
                is_running = True
                pids = [int(p) for p in out.splitlines() if p.strip().isdigit()]
    except Exception:
        pass

    return {
        "installed": exe is not None,
        "executable_path": exe,
        "is_running": is_running,
        "pids": pids,
        "version": "2.1.1",
    }


def open_in_tuxguitar(file_path: str) -> Dict[str, Any]:
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        return {"error": f"File not found: {abs_path}"}

    exe = find_tuxguitar_executable()
    if not exe:
        return {"error": "TuxGuitar executable (tuxguitar.exe or tuxguitar.bat) not found."}

    # Launch asynchronously
    try:
        working_dir = os.path.dirname(exe)
        if exe.endswith(".bat"):
            proc = subprocess.Popen(
                ["cmd.exe", "/c", exe, abs_path],
                cwd=working_dir,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
            )
        else:
            proc = subprocess.Popen(
                [exe, abs_path],
                cwd=working_dir,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
            )
        return {
            "success": True,
            "message": f"Opened '{os.path.basename(abs_path)}' in TuxGuitar.",
            "file_path": abs_path,
            "launcher": exe,
            "pid": proc.pid
        }
    except Exception as e:
        return {"error": f"Failed to launch TuxGuitar: {str(e)}"}
