from __future__ import annotations

import argparse

from sightchat.audio import TextToSpeech
from sightchat.config import settings
from sightchat.cost import CostPolicy
from sightchat.decision import DecisionService, VisionContext
from sightchat.decision.cloud_llm import CloudLLMClient
from sightchat.decision.local_policy import LocalPolicy


def build_service() -> DecisionService:
    return DecisionService(
        context=VisionContext(),
        local_policy=LocalPolicy(),
        cloud_client=CloudLLMClient(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            provider=settings.llm_provider,
        ),
        cost_policy=CostPolicy(
            enable_cloud=settings.enable_cloud,
            max_calls_per_minute=settings.max_cloud_calls_per_minute,
        ),
    )


def capture_context(service: DecisionService) -> None:
    from sightchat.vision import CameraService, VisionAnalyzer

    camera = CameraService(settings.camera_index)
    analyzer = VisionAnalyzer()
    frame = camera.read_once()
    summary = analyzer.analyze(frame)
    service.observe(summary.to_dict())


def capture_screen_context(service: DecisionService, include_screenshot: bool = False) -> None:
    from sightchat.screen import ScreenEventAdapter

    observation = ScreenEventAdapter().capture_once(include_screenshot=include_screenshot)
    service.observe(observation.to_dict())
    print(observation.to_dict())


def main() -> None:
    parser = argparse.ArgumentParser(prog="sightchat")
    parser.add_argument("--text", default="你现在看到了什么？")
    parser.add_argument("--camera", action="store_true")
    parser.add_argument("--screen", action="store_true")
    parser.add_argument("--screen-screenshot", action="store_true")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--speak", action="store_true")
    args = parser.parse_args()

    service = build_service()
    if args.camera:
        capture_context(service)
    if args.screen:
        capture_screen_context(service, include_screenshot=args.screen_screenshot)
    tts = TextToSpeech(enabled=args.speak)

    if args.interactive:
        while True:
            text = input("你：").strip()
            if text in {"exit", "quit", "退出"}:
                break
            answer = service.reply(text)
            print(f"AI：{answer}")
            tts.speak(answer)
        return

    answer = service.reply(args.text)
    print(answer)
    tts.speak(answer)


if __name__ == "__main__":
    main()
