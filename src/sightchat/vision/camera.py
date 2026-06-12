from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import cv2


@dataclass
class CameraService:
    camera_index: int = 0

    def open(self) -> Any:
        backend = os.environ.get("CV_CAMERA_BACKEND", "DSHOW" if os.name == "nt" else "").upper()
        if backend == "DSHOW" and hasattr(cv2, "CAP_DSHOW"):
            return cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        if backend == "MSMF" and hasattr(cv2, "CAP_MSMF"):
            return cv2.VideoCapture(self.camera_index, cv2.CAP_MSMF)
        return cv2.VideoCapture(self.camera_index)

    def read_once(self) -> Any:
        cap = self.open()
        try:
            if not cap.isOpened():
                raise RuntimeError("摄像头打开失败，请检查权限、占用或设备编号")
            ok, frame = cap.read()
            if not ok or frame is None:
                raise RuntimeError("摄像头读取失败")
            return frame
        finally:
            cap.release()
