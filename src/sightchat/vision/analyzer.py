from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import cv2
import numpy as np


@dataclass
class VisionSummary:
    width: int
    height: int
    brightness: float
    edges: float
    motion: float | None = None
    labels: list[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "brightness": round(self.brightness, 3),
            "edges": round(self.edges, 3),
            "motion": None if self.motion is None else round(self.motion, 3),
            "labels": self.labels,
            "timestamp": self.timestamp,
        }


class VisionAnalyzer:
    def __init__(self) -> None:
        self._last_gray: np.ndarray | None = None

    def analyze(self, frame: np.ndarray) -> VisionSummary:
        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray) / 255.0)
        edges = float(np.mean(cv2.Canny(gray, 80, 160) > 0))
        motion = self._estimate_motion(gray)
        labels = self._labels_from_stats(brightness, edges, motion)
        self._last_gray = gray
        return VisionSummary(width=width, height=height, brightness=brightness, edges=edges, motion=motion, labels=labels)

    def _estimate_motion(self, gray: np.ndarray) -> float | None:
        if self._last_gray is None or self._last_gray.shape != gray.shape:
            return None
        diff = cv2.absdiff(gray, self._last_gray)
        return float(np.mean(diff) / 255.0)

    def _labels_from_stats(self, brightness: float, edges: float, motion: float | None) -> list[str]:
        labels: list[str] = []
        if brightness < 0.25:
            labels.append("光线较暗")
        elif brightness > 0.75:
            labels.append("光线充足")
        else:
            labels.append("室内常规光照")
        if edges > 0.08:
            labels.append("画面细节较多")
        else:
            labels.append("画面较简洁")
        if motion is not None and motion > 0.04:
            labels.append("画面有明显变化")
        return labels
