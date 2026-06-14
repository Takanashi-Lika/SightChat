from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk

from sightchat.app import build_service, capture_context
from sightchat.audio import TextToSpeech


class SightChatApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("SightChat")
        self.geometry("760x560")
        self.minsize(680, 480)
        self.service = build_service()
        self.tts_enabled = tk.BooleanVar(value=False)
        self.input_text = tk.StringVar(value="你现在看到了什么？")
        self.focus_minutes = tk.IntVar(value=25)
        self.monitor_interval = tk.IntVar(value=10)
        self.status_text = tk.StringVar(value="已启动。可以输入问题，或先采集一次摄像头上下文。")
        self.tts = TextToSpeech(enabled=False)
        self.monitoring = False
        self.monitor_job: str | None = None
        self._build_layout()

    def _build_layout(self) -> None:
        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)
        header = ttk.Frame(root)
        header.pack(fill="x")
        ttk.Label(header, text="SightChat AI 视觉对话助手", font=("Microsoft YaHei UI", 16, "bold")).pack(side="left")
        ttk.Checkbutton(header, text="语音播报", variable=self.tts_enabled, command=self._toggle_tts).pack(side="right")

        monitor_bar = ttk.Frame(root)
        monitor_bar.pack(fill="x", pady=(16, 0))
        ttk.Label(monitor_bar, text="专注分钟").pack(side="left")
        ttk.Spinbox(monitor_bar, from_=5, to=120, textvariable=self.focus_minutes, width=6).pack(side="left", padx=(6, 16))
        ttk.Label(monitor_bar, text="检测间隔秒").pack(side="left")
        ttk.Spinbox(monitor_bar, from_=5, to=60, textvariable=self.monitor_interval, width=6).pack(side="left", padx=(6, 16))
        self.start_button = ttk.Button(monitor_bar, text="开始自动监控", command=self._start_monitoring)
        self.start_button.pack(side="left")
        self.stop_button = ttk.Button(monitor_bar, text="停止", command=self._stop_monitoring, state="disabled")
        self.stop_button.pack(side="left", padx=(8, 0))

        self.log = tk.Text(root, height=18, wrap="word")
        self.log.pack(fill="both", expand=True, pady=16)
        self.log.configure(state="disabled")

        input_bar = ttk.Frame(root)
        input_bar.pack(fill="x")
        ttk.Entry(input_bar, textvariable=self.input_text).pack(side="left", fill="x", expand=True)
        ttk.Button(input_bar, text="发送", command=self._send).pack(side="left", padx=(8, 0))
        ttk.Button(input_bar, text="采集摄像头", command=self._capture_camera).pack(side="left", padx=(8, 0))

        ttk.Label(root, textvariable=self.status_text).pack(anchor="w", pady=(12, 0))
        self._append("系统", self.status_text.get())

    def _toggle_tts(self) -> None:
        self.tts.enabled = self.tts_enabled.get()

    def _send(self) -> None:
        text = self.input_text.get().strip()
        if not text:
            return
        self._append("你", text)
        threading.Thread(target=self._reply_worker, args=(text,), daemon=True).start()

    def _reply_worker(self, text: str) -> None:
        answer = self.service.reply(text)
        self.after(0, lambda: self._show_answer(answer))

    def _show_answer(self, answer: str) -> None:
        self._append("AI", answer)
        self.tts.speak(answer)

    def _capture_camera(self) -> None:
        threading.Thread(target=self._capture_camera_worker, daemon=True).start()
        self.status_text.set("正在采集摄像头上下文……")

    def _capture_camera_worker(self) -> None:
        try:
            capture_context(self.service)
            self.after(0, lambda: self.status_text.set("摄像头上下文已更新。"))
            self.after(0, lambda: self._append("系统", "摄像头上下文已更新。"))
        except Exception as exc:
            self.after(0, lambda: self.status_text.set(f"摄像头采集失败：{exc}"))
            self.after(0, lambda: self._append("系统", f"摄像头采集失败：{exc}"))

    def _start_monitoring(self) -> None:
        if self.monitoring:
            return
        self.monitoring = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self._append("系统", f"已开始 {self.focus_minutes.get()} 分钟专注自动监控。")
        self._schedule_monitor_tick(immediate=True)

    def _stop_monitoring(self) -> None:
        self.monitoring = False
        if self.monitor_job is not None:
            self.after_cancel(self.monitor_job)
            self.monitor_job = None
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_text.set("自动监控已停止。")
        self._append("系统", "自动监控已停止。")

    def _schedule_monitor_tick(self, immediate: bool = False) -> None:
        if not self.monitoring:
            return
        delay = 0 if immediate else max(5, int(self.monitor_interval.get())) * 1000
        self.monitor_job = self.after(delay, self._monitor_tick)

    def _monitor_tick(self) -> None:
        if not self.monitoring:
            return
        self._capture_camera()
        self._schedule_monitor_tick()

    def _append(self, role: str, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", f"[{role}] {text}\n\n")
        self.log.see("end")
        self.log.configure(state="disabled")


def run_ui() -> None:
    SightChatApp().mainloop()
