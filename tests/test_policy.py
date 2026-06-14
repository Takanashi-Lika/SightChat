from sightchat.cost import CostPolicy
from sightchat.decision.local_policy import LocalPolicy


def test_local_policy_answers_visual_question_without_context():
    answer = LocalPolicy().answer("你看到了什么？", {"available": False})
    assert answer is not None
    assert "摄像头" in answer


def test_cost_policy_disabled_cloud():
    policy = CostPolicy(enable_cloud=False)
    assert policy.allow_cloud() is False


def test_cost_policy_rate_limit():
    policy = CostPolicy(enable_cloud=True, max_calls_per_minute=1)
    assert policy.allow_cloud() is True
    policy.record_cloud_call()
    assert policy.allow_cloud() is False
