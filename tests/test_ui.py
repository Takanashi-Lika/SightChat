from sightchat.ui_tk import SightChatApp, run_ui


def test_ui_exports_app_and_runner() -> None:
    assert SightChatApp is not None
    assert callable(run_ui)
