from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class CostPolicy:
    enable_cloud: bool = False
    max_calls_per_minute: int = 6
    call_timestamps: list[float] = field(default_factory=list)

    def allow_cloud(self) -> bool:
        if not self.enable_cloud:
            return False
        now = time.time()
        self.call_timestamps = [ts for ts in self.call_timestamps if now - ts < 60.0]
        return len(self.call_timestamps) < self.max_calls_per_minute

    def record_cloud_call(self) -> None:
        self.call_timestamps.append(time.time())
