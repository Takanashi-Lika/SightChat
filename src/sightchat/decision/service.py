from __future__ import annotations

from dataclasses import dataclass

from sightchat.cost import CostPolicy
from sightchat.decision.cloud_llm import CloudLLMClient
from sightchat.decision.context import VisionContext
from sightchat.decision.local_policy import LocalPolicy


@dataclass
class DecisionService:
    context: VisionContext
    local_policy: LocalPolicy
    cloud_client: CloudLLMClient
    cost_policy: CostPolicy

    def observe(self, summary: dict) -> None:
        self.context.update(summary)

    def reply(self, user_text: str) -> str:
        compact_context = self.context.compact()
        local_answer = self.local_policy.answer(user_text, compact_context)
        if local_answer is not None:
            return local_answer
        if self.cost_policy.allow_cloud():
            self.cost_policy.record_cloud_call()
            return self.cloud_client.complete(user_text, compact_context)
        return "我可以先基于本地视觉上下文回答画面相关问题；当前云端模型未启用或已达到调用限制。"
