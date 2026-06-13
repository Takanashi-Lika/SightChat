from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class VisionContext:
    max_items: int = 8
    ttl_seconds: float = 60.0
    items: list[dict[str, Any]] = field(default_factory=list)

    def update(self, summary: dict[str, Any]) -> None:
        item = dict(summary)
        item.setdefault("timestamp", time.time())
        if self.items and self._signature(self.items[-1]) == self._signature(item):
            self.items[-1] = item
        else:
            self.items.append(item)
        self.items = self.items[-self.max_items :]
        self.prune()

    def latest(self) -> dict[str, Any] | None:
        self.prune()
        if not self.items:
            return None
        return self.items[-1]

    def compact(self) -> dict[str, Any]:
        latest = self.latest()
        if latest is None:
            return {"available": False, "description": "暂无摄像头视觉上下文"}
        labels = latest.get("labels") if isinstance(latest.get("labels"), list) else []
        return {
            "available": True,
            "description": "，".join(str(x) for x in labels) if labels else "已有画面摘要，但没有明确标签",
            "latest": latest,
            "history_count": len(self.items),
        }

    def prune(self) -> None:
        now = time.time()
        self.items = [item for item in self.items if now - float(item.get("timestamp", 0.0)) <= self.ttl_seconds]

    def _signature(self, item: dict[str, Any]) -> str:
        labels = item.get("labels") if isinstance(item.get("labels"), list) else []
        return "|".join(str(x) for x in labels)
