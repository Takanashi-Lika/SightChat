from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class ActiveWindowInfo:
    title: str = ""
    app: str = "unknown"


def get_active_window_info() -> ActiveWindowInfo:
    if os.name != "nt":
        return ActiveWindowInfo()
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return ActiveWindowInfo(title=buffer.value, app=_process_name(pid.value))
    except Exception:
        return ActiveWindowInfo()


def _process_name(pid: int) -> str:
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32
        psapi = ctypes.windll.psapi
        handle = kernel32.OpenProcess(0x1000, False, pid)
        if not handle:
            return "unknown"
        try:
            buffer = ctypes.create_unicode_buffer(260)
            size = wintypes.DWORD(len(buffer))
            if psapi.GetModuleBaseNameW(handle, None, buffer, size.value):
                return buffer.value
            return "unknown"
        finally:
            kernel32.CloseHandle(handle)
    except Exception:
        return "unknown"
