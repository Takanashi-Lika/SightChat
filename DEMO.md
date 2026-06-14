# SightChat Demo 指南

## 演示目标

展示 SightChat 如何通过摄像头视觉摘要、屏幕活动感知、文本/语音输出和桌面 UI 辅助学习专注。

## 演示准备

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q
```

如需云端模型，复制 `.env.example` 为 `.env`，填入本地 API Key。不要提交 `.env`。

## 建议录屏流程

1. 展示 README、PR 记录和测试通过结果。
2. 运行 `python -m sightchat.app --text "你是谁"`，展示本地回复。
3. 运行 `python -m sightchat.app --camera --text "你看到什么"`，展示摄像头上下文。
4. 如果屏幕感知 PR 已合并，运行 `python -m sightchat.app --screen --text "我在做什么"`。
5. 如果 UI PR 已合并，运行 `python -m sightchat.app --ui`，展示窗口输入、回复和摄像头采集。
6. 说明云端模型通过 `.env` 配置，密钥不入库。

## 视频链接

提交前将 demo 视频上传到可访问平台，并把链接填入 README 的 Demo 视频部分。
