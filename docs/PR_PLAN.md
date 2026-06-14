# PR 拆分计划

本项目按“每个 PR 只做一件事”的原则持续交付。当前未提交功能应按以下顺序拆分到独立分支和独立 PR 中，每个 PR 合并后主分支都需保持可运行。

## 已有持续交付记录

- PR 1：初始化项目结构与视觉基础模块。
- PR 2：新增本地/云端决策服务。
- PR 3：新增语音辅助能力与 CLI Demo。
- 后续 PR 应继续基于 `main` 逐个小步提交。

## 后续 PR 队列

### PR 4：Add screen activity observation

- 功能描述：新增屏幕活动窗口检测、窗口分类和可选截图证据。
- 实现思路：封装屏幕事件适配器，把活动窗口转换为统一事件契约。
- 测试方式：`python -m pytest -q`，`python -m sightchat.app --screen-once`。

### PR 5：Add cloud scene judging configuration

- 功能描述：支持通过 `.env` 配置 OpenAI-compatible / DeepSeek 云端判定。
- 实现思路：配置层读取 base URL、模型和 API Key，云端判定只在不确定场景触发。
- 测试方式：`python -m pytest -q`，`python -m sightchat.app --demo cloud`。

### PR 6：Add desktop UI for focus sessions

- 功能描述：新增 tkinter 桌面 UI，支持开始/停止专注、状态展示和事件日志。
- 实现思路：复用现有 FridayGraph，UI 只负责事件输入和结果展示。
- 测试方式：`python -m pytest -q`，`python -m sightchat.app --ui`。

### PR 7：Add automatic focus monitoring loop

- 功能描述：开始专注后自动周期采集 timer/screen/camera 事件。
- 实现思路：后台线程执行检测，避免阻塞 tkinter 主线程。
- 测试方式：`python -m pytest -q`，UI 中点击“开始专注并自动监控”。

### PR 8：Add camera preview and object detection

- 功能描述：新增摄像头预览、检测框和 YOLO/MediaPipe 可选检测。
- 实现思路：优先使用 YOLOv8/MediaPipe，失败时回退启发式检测。
- 测试方式：`python -m pytest -q`，UI 勾选“自动检测摄像头”。

### PR 9：Add natural speech playback

- 功能描述：新增 Edge TTS 在线语音播报，失败时回退本地 TTS。
- 实现思路：使用队列化播报避免阻塞 UI 和语音重叠。
- 测试方式：`python -m pytest -q`，UI 勾选“语音播报”。

### PR 10：Add continuous voice input mode

- 功能描述：新增常态语音输入开关，用户无需打字即可交互。
- 实现思路：后台循环短句识别，识别结果进入意图解析或大模型聊天。
- 测试方式：`python -m pytest -q`，UI 点击“开启常态语音”。

### PR 11：Add behavior stability state machine

- 功能描述：手机/低头等提醒需要连续多次检测才触发，减少误报。
- 实现思路：新增行为状态机统计连续 tick，再放行稳定风险信号。
- 测试方式：`python -m pytest -q`。

### PR 12：Add local settings and feedback storage

- 功能描述：保存用户设置并记录“提醒有用/误报”反馈。
- 实现思路：本地 JSON 保存设置，JSONL 记录反馈，`data/` 不提交。
- 测试方式：`python -m pytest -q`，UI 点击“设置”和反馈按钮。

### PR 13：Add demo guide and review documentation

- 功能描述：补充 Demo 视频链接位置、演示脚本、依赖说明和评审运行命令。
- 实现思路：整理 README、DEMO 和 DESIGN，列明第三方依赖与原创部分。
- 测试方式：按 README 运行 `python -m pytest -q` 和核心 Demo 命令。

## PR 描述要求

每个 PR 描述必须包含：

- 标题：一句话说明新增或修改内容。
- 功能描述：说明功能作用与使用方式。
- 实现思路：说明技术选型或核心逻辑。
- 测试方式：说明如何验证功能正常运行。

## 合规注意事项

- 不提交 `.env`、`data/`、`captures/`、模型权重和 API Key。
- README 必须列明第三方依赖和原创功能范围。
- 每个 PR 合并后主分支必须能运行测试和 Demo。
- demo 视频链接应在最终 README 中补充。
