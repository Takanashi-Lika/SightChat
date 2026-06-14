# SightChat

SightChat 是一款精简版 AI 视觉对话助手，目标是让 AI 通过摄像头理解当前画面，通过麦克风听到用户问题，并以文字和语音给出回应。


## 功能

- 打开本机摄像头并读取当前画面。
- 生成轻量视觉摘要，包括亮度、主体区域、运动变化和可选快照。
- 支持文本输入，预留麦克风语音输入接口。
- 使用本地规则优先回答常见视觉问题。
- 在允许云端调用时，将用户问题和视觉上下文发送给云端 LLM。
- 使用成本策略限制云端调用频率、上下文长度和快照尺寸。

## 快速开始

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m sightchat.app --text "你现在看到了什么？"
```

如需启用云端模型，请复制 `.env.example` 为 `.env`，填入本机密钥。项目支持 OpenAI-compatible API，例如 DeepSeek：

```text
SIGHTCHAT_ENABLE_CLOUD=true
SIGHTCHAT_LLM_PROVIDER=deepseek
SIGHTCHAT_OPENAI_BASE_URL=https://api.deepseek.com/v1
SIGHTCHAT_OPENAI_API_KEY=你的本地密钥
SIGHTCHAT_OPENAI_MODEL=deepseek-chat
```

不要把 `.env` 或 API Key 提交到仓库；`.env` 已在 `.gitignore` 中忽略。

## 运行模式

```bash
python -m sightchat.app --text "画面里有什么？"
python -m sightchat.app --interactive
python -m sightchat.app --camera
```

## 依赖说明

- `opencv-python`：摄像头采集和基础图像分析。
- `numpy`：图像统计计算。
- `requests`：调用 OpenAI-compatible 云端模型。
- `pyttsx3`：本地语音播报。
- `SpeechRecognition`：语音识别接口预留。
- `pytest`：核心策略测试。

## 复用说明

本项目复用了本人旧项目中的部分设计思想，并进行了精简重构：

- 摄像头打开方式参考旧项目中的 OpenCV 摄像头后端选择逻辑。
- 本地/云端双架构参考旧项目的世界状态聚合、规则回退、云端 LLM 调用思想。

## 设计文档

请见 [DESIGN.md](DESIGN.md)。

## Demo 视频

待录制后补充可访问链接。

## 合规说明

- 本仓库只提交与 AI 视觉对话助手相关的精简代码。
- 第三方依赖已在 README 和 `requirements.txt` 中列明。
- 复用本人旧代码的来源和重构范围已在 README 中说明。
- 不提交 API Key、token、模型密钥和本地运行数据。
