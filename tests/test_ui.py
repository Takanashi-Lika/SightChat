from sightchat.ui_tk import SightChatApp, run_ui


def test_ui_exports_app_and_runner() -> None:
    assert SightChatApp is not None
    assert callable(run_ui)


def test_ui_class_has_monitoring_controls() -> None:
    assert hasattr(SightChatApp, "_start_monitoring")
    assert hasattr(SightChatApp, "_stop_monitoring")
