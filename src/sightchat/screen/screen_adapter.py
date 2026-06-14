from __future__ import annotations

from dataclasses import dataclass

from sightchat.screen.screenshot import ScreenshotStore
from sightchat.screen.window import ActiveWindowInfo, get_active_window_info


STUDY_KEYWORDS = {"考研", "高等数学", "线性代数", "概率论", "论文", "pdf", "word", "vscode", "pycharm", "notion", "知网", "arxiv", "leetcode", "github", "course", "lecture", "study"}
ENTERTAINMENT_KEYWORDS = {"搞笑", "鬼畜", "游戏", "直播", "番剧", "电影", "短视频", "抖音", "快手", "bilibili", "哔哩哔哩", "youtube", "netflix"}
GAME_KEYWORDS = {"steam", "wegame", "epic", "valorant", "league of legends", "原神", "崩坏", "minecraft"}
COMMUNICATION_KEYWORDS = {"微信", "wechat", "qq", "telegram", "discord", "slack", "飞书"}


@dataclass
class ScreenObservation:
    active_app: str = "unknown"
    window_title: str = ""
    content_category: str = "unknown"
    study_signal: float = 0.0
    distraction_signal: float = 0.0
    keywords: list[str] | None = None
    duration_seconds: float = 0.0
    confidence: float = 0.0
    screenshot_ref: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "source": "screen",
            "active_app": self.active_app,
            "window_title": self.window_title,
            "content_category": self.content_category,
            "study_signal": self.study_signal,
            "distraction_signal": self.distraction_signal,
            "keywords": self.keywords or [],
            "duration_seconds": self.duration_seconds,
            "confidence": self.confidence,
            "screenshot_ref": self.screenshot_ref,
            "labels": self._labels(),
        }

    def _labels(self) -> list[str]:
        labels = [f"屏幕分类:{self.content_category}"]
        if self.active_app != "unknown":
            labels.append(f"活动应用:{self.active_app}")
        if self.window_title:
            labels.append(f"窗口:{self.window_title}")
        return labels


@dataclass
class ScreenEventAdapter:
    screenshot_store: ScreenshotStore | None = None

    def capture_once(self, include_screenshot: bool = False) -> ScreenObservation:
        screenshot_ref = self._capture_screenshot() if include_screenshot else None
        return self.from_window_info(get_active_window_info(), screenshot_ref=screenshot_ref)

    def from_window_info(self, info: ActiveWindowInfo, screenshot_ref: str | None = None) -> ScreenObservation:
        title = info.title or ""
        app = info.app or "unknown"
        text = f"{app} {title}".lower()
        study_score = self._score(text, STUDY_KEYWORDS)
        entertainment_score = self._score(text, ENTERTAINMENT_KEYWORDS)
        game_score = self._score(text, GAME_KEYWORDS)
        communication_score = self._score(text, COMMUNICATION_KEYWORDS)
        category = "unknown"
        distraction_signal = max(entertainment_score, game_score, communication_score * 0.65)
        if game_score >= 0.4:
            category = "game"
        elif entertainment_score > study_score and entertainment_score >= 0.25:
            category = "entertainment"
        elif communication_score >= 0.35:
            category = "communication"
        elif study_score >= 0.25:
            category = "study"
        confidence = round(min(1.0, max(study_score, distraction_signal, 0.2)), 3)
        return ScreenObservation(
            active_app=app,
            window_title=title,
            content_category=category,
            study_signal=round(study_score, 3),
            distraction_signal=round(distraction_signal, 3),
            keywords=self._matched_keywords(text),
            duration_seconds=0.0,
            confidence=confidence,
            screenshot_ref=screenshot_ref,
        )

    def _capture_screenshot(self) -> str | None:
        store = self.screenshot_store or ScreenshotStore()
        return store.capture_once()

    def _score(self, text: str, keywords: set[str]) -> float:
        if not text.strip():
            return 0.0
        matches = sum(1 for keyword in keywords if keyword.lower() in text)
        return min(1.0, matches / 3.0)

    def _matched_keywords(self, text: str) -> list[str]:
        keywords = STUDY_KEYWORDS | ENTERTAINMENT_KEYWORDS | GAME_KEYWORDS | COMMUNICATION_KEYWORDS
        return sorted(keyword for keyword in keywords if keyword.lower() in text)
