from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ScreenshotStore:
    output_dir: Path = Path("captures/screens")
    max_width: int = 960

    def capture_once(self) -> str | None:
        try:
            from PIL import ImageGrab
        except Exception:
            return None
        try:
            image = ImageGrab.grab()
            if self.max_width > 0 and image.width > self.max_width:
                ratio = self.max_width / image.width
                image = image.resize((self.max_width, int(image.height * ratio)))
            self.output_dir.mkdir(parents=True, exist_ok=True)
            path = self.output_dir / f"screen_{int(time.time() * 1000)}.jpg"
            image.convert("RGB").save(path, "JPEG", quality=75)
            return path.as_posix()
        except Exception:
            return None
