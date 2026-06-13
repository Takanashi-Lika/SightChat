from sightchat.decision.context import VisionContext


def test_context_compact_empty():
    context = VisionContext()
    assert context.compact()["available"] is False


def test_context_update_latest():
    context = VisionContext()
    context.update({"labels": ["室内常规光照"]})
    compact = context.compact()
    assert compact["available"] is True
    assert "室内常规光照" in compact["description"]
