from __future__ import annotations

from typing import Any

import requests


class CloudLLMClient:
    def __init__(self, base_url: str, api_key: str, model: str, provider: str = "mock") -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.provider = provider

    def complete(self, user_text: str, visual_context: dict[str, Any]) -> str:
        if self.provider == "mock" or not self.api_key:
            return self._mock_reply(user_text, visual_context)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是 SightChat，一个简洁、可靠的 AI 视觉对话助手。请基于视觉摘要回答，不要编造未观察到的内容。"},
                {"role": "user", "content": f"用户问题：{user_text}\n视觉上下文：{visual_context}"},
            ],
            "temperature": 0.4,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        response = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        return str(data["choices"][0]["message"]["content"]).strip()

    def _mock_reply(self, user_text: str, visual_context: dict[str, Any]) -> str:
        description = visual_context.get("description", "暂无视觉摘要")
        return f"我已收到你的问题：{user_text}。当前视觉摘要是：{description}。云端模型未启用，所以这是本地模拟回复。"
