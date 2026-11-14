# TikTok Case Video Skill

把人物、产品、委托或创作者案例素材，整理成适合 TikTok 的竖屏故事视频、剪辑脚本和逐秒旁白。

这套 Skill 来自多轮真实修改中反复出现的问题：视频像 PPT、素材重复、头像反复出现、不同画幅产生黑边、低清素材被强行放大、旁白太平、现有 TikTok 视频整段复用，以及事实素材被错误替代。

## 它能做什么

- 读取素材包和事实底稿，区分头像、作品、交付物、证明截图和参考素材
- 设计 12–25 秒的 TikTok 故事结构
- 输出逐秒分镜、屏幕文字、旁白和音乐方向
- 使用现有视频做有节奏的混剪
- 在素材有限时，用动态排版补足叙事，而不是重复同一张图
- 检查 9:16 比例、时长、帧率、音轨和导出规格
- 根据反馈修复黑边、模糊、重复、PPT 感和旁白节奏问题

## 安装

把仓库克隆到 Codex 的 skills 目录：

### Windows PowerShell

```powershell
git clone https://github.com/yutianai521-create/tiktok-case-video.git "$env:USERPROFILE\.codex\skills\tiktok-case-video"
```

### macOS / Linux

```bash
git clone https://github.com/yutianai521-create/tiktok-case-video.git ~/.codex/skills/tiktok-case-video
```

重新打开 Codex，或开始一个新任务。Skill 默认支持自动匹配，也可以显式调用：

```text
Use $tiktok-case-video to turn this material folder into a 15-second TikTok case video.
Give me the edited video, a no-voice master, and a timestamped English voiceover.
```

## 使用示例

### 只做方案

```text
使用 $tiktok-case-video 读取这个素材包，先给我一个 18 秒 TikTok 分镜。
不要生成视频。头像和最终作品各只出现一次，旁白单独给我。
```

### 直接剪辑

```text
使用 $tiktok-case-video 把这些原视频剪成 20 秒 9:16 混剪。
不要像 PPT，不要拉伸，不要整段复用已经发布过的视频。
配乐有节奏，但保留一段让最终作品完整展示。
```

### 修改现有成片

```text
使用 $tiktok-case-video 检查这个成片：现在有黑边、画面发糊，而且同一头像出现了三次。
请修复后导出 1080×1920 的无旁白版本。
```

### 只写旁白

```text
使用 $tiktok-case-video 按这个 15 秒视频的实际镜头节奏重写英文旁白。
开头更有 TikTok 感，结果画面处留 1.5 秒停顿。
```

## 推荐输入

最好同时提供：

- 原始视频和图片，不要只提供社媒截图
- 一份事实底稿：人物、行为、金额、时间、交付结果
- 哪些内容已公开、哪些只能用于核验
- 目标时长、语言、是否需要旁白和配乐
- 必须保留的水印、logo 或 CTA

素材不完整也可以使用，但 Skill 会明确标记缺失证据，不会用别的图片冒充。

## 输出建议

常用交付组合：

```text
final_music_no_voice.mp4    带配乐、不含旁白
final_silent.mp4            纯画面版本（可选）
voiceover_timeline.md       逐秒旁白与画面对照
edit_notes.md               素材来源和剪辑说明（可选）
preview.jpg                 抽帧预览（可选）
```

## 辅助脚本

需要系统安装 `ffprobe`（通常随 FFmpeg 一起安装）。

检查素材：

```bash
python scripts/inspect_media.py ./materials --json media-report.json
```

检查成片结构：

```bash
python scripts/validate_video.py final.mp4 \
  --width 1080 --height 1920 \
  --min-duration 12 --max-duration 20 \
  --require-audio
```

脚本只能检查规格，不能判断画面是否好看、是否重复或事实是否准确；这些仍需抽帧和人工观看。

## 目录

```text
tiktok-case-video/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── references/
│   ├── editing-playbook.md
│   ├── platform-copy.md
│   └── storyboard-template.md
└── scripts/
    ├── inspect_media.py
    └── validate_video.py
```

## 设计原则

这不是一个固定视觉模板。它优先让成片像素材本身的世界，而不是套上统一的“AI 风”。同一套方法可以服务动漫角色、音乐男团、TTRPG、设计委托或产品机制，但配色、字体、节奏和声音应跟着故事变化。

## License

当前仓库尚未附加开源许可证。仓库所有者可在确定允许的使用和再分发范围后补充许可证。


