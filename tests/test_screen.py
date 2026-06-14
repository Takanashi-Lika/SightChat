from sightchat.screen import ActiveWindowInfo, ScreenEventAdapter, ScreenObservation


def test_screen_observation_to_dict_has_labels() -> None:
    observation = ScreenObservation(active_app="Code.exe", window_title="README.md - VSCode", content_category="study")

    data = observation.to_dict()

    assert data["source"] == "screen"
    assert "屏幕分类:study" in data["labels"]


def test_screen_adapter_classifies_study_window() -> None:
    observation = ScreenEventAdapter().from_window_info(ActiveWindowInfo(title="论文 pdf", app="Code.exe"))

    assert observation.content_category == "study"
    assert observation.study_signal > 0
