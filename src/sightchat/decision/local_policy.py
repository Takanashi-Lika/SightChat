from __future__ import annotations

from typing import Any


class LocalPolicy:
    def answer(self, text: str, context: dict[str, Any]) -> str | None:
        question = text.strip().lower()
        if not question:
            return "我没有听清你的问题，可以再说一遍吗？"
        visual_words = ("看到", "看见", "画面", "摄像头", "眼前", "there", "see", "camera")
        if not any(word in question for word in visual_words):
            return None
        if not context.get("available"):
            return "我暂时还没有获取到摄像头画面，请先打开摄像头后再问我。"
        latest = context.get("latest") if isinstance(context.get("latest"), dict) else {}
        labels = latest.get("labels") if isinstance(latest.get("labels"), list) else []
        brightness = latest.get("brightness")
        edges = latest.get("edges")
        parts = []
        if labels:
            parts.append("我根据本地视觉摘要判断：" + "，".join(str(x) for x in labels))
        if isinstance(brightness, (int, float)):
            parts.append(f"画面亮度约为 {brightness:.2f}")
        if isinstance(edges, (int, float)):
            parts.append(f"细节密度约为 {edges:.2f}")
        if not parts:
            return "我已经获取到画面，但当前摘要信息还不够明确。"
        return "；".join(parts) + "。"
