# TuxGuitar AI MCP 工具 (TuxGuitar Model Context Protocol)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![TuxGuitar](https://img.shields.io/badge/TuxGuitar-2.1.1-orange.svg)](http://www.tuxguitar.com.ar/)

专为 **TuxGuitar** 打造的 AI MCP (Model Context Protocol) 工具集。让大语言模型（AI Agent，如 Antigravity、Claude、Cursor 等）具备专业级吉他谱读写、编辑、移调、和弦伴奏生成、独奏创作及与 TuxGuitar 桌面应用联动的能力。

---

## 🌟 核心特性

- **多格式全兼容**：
  - 原生支持 TuxGuitar 原生格式（`.tg`，XML Zip）。
  - 原生支持 Guitar Pro 标准格式（`.gp5`、`.gp4`、`.gp3`）。
  - 支持格式间无损双向转换。
- **全方位乐谱编辑**：
  - **乐谱概览**：快速获取曲名、作者、调号、速度、拍号、总小节数、各音轨配置。
  - **小节与音符读写**：精确读取/修改任意小节、拍子、弦（1~6弦/贝斯4弦/7弦）、品位（Fret）、时值。
  - **吉他专业演奏技巧**：推弦（Bend）、击勾弦（Hammer-on / Pull-off）、滑音（Slide）、揉弦（Vibrato）、掌心闷音（Palm Mute）、泛音（Harmonics）、重音、跳音、幽灵音。
- **智能吉他理论与和弦库**：
  - 内置丰富和弦词典（大三和弦、小三和弦、七和弦、大七、小七、挂留和弦、五力和弦等）。
  - 自动扫弦节奏型（经典下下上下上、下弹连续四分音符、八分音符扫弦、金属闷音冲锋、分解和弦指弹琶音）。
- **极速旋律与 SOLO 助手**：
  - 只要输入音符序列，工具自动计算节拍刻度并填充小节。
- **ASCII 制表谱渲染**：
  - 任何修改都能即时渲染出格式工整的 ASCII 六线谱，直接在 AI 对话和 Markdown 中直观展现。
- **TuxGuitar 桌面无缝联动**：
  - 检测应用运行状态。
  - 一键在 TuxGuitar 桌面端（`tuxguitar.exe`）中打开乐谱，实时试听与播放。

---

## 🛠️ MCP 工具清单 (Tool Reference)

| 工具名称 | 功能描述 | 关键参数 |
| :--- | :--- | :--- |
| `tuxguitar_get_score_summary` | 读取乐谱摘要（标题、速度、调号、小节数、音轨详情） | `file_path` |
| `tuxguitar_read_measures` | 读取指定音轨详细小节音符、技巧与时值数据 | `file_path`, `track_number`, `start_measure`, `end_measure` |
| `tuxguitar_get_ascii_tab` | 将乐谱片段渲染为可视化 ASCII 六线谱 | `file_path`, `track_number`, `start_measure`, `end_measure` |
| `tuxguitar_create_score` | 从零创建全新乐谱（支持多音轨配置与调弦预设） | `file_path`, `title`, `artist`, `tempo`, `time_signature`, `tracks` |
| `tuxguitar_add_track` | 向现有乐谱添加新乐器音轨（电吉他、木吉他、贝斯等） | `file_path`, `name`, `tuning`, `instrument` |
| `tuxguitar_remove_track` | 移除指定音轨 | `file_path`, `track_number` |
| `tuxguitar_write_measures` | 批量写入/替换小节的完整拍子与音符数据 | `file_path`, `track_number`, `start_measure`, `measures_data` |
| `tuxguitar_add_riff` | 便捷写入旋律、Riff 或吉他 Solo（自动算拍） | `file_path`, `track_number`, `start_measure`, `notes_list` |
| `tuxguitar_add_chord_progression` | 写入和弦进行与扫弦节奏型（如 C-G-Am-F） | `file_path`, `track_number`, `start_measure`, `progression`, `strum_pattern` |
| `tuxguitar_transpose` | 音轨或全曲半音移调（支持向上/向下移调） | `file_path`, `track_number`, `semitones` |
| `tuxguitar_add_marker` | 在指定小节添加曲式段落标记（Intro, Verse, Chorus, Solo, Outro） | `file_path`, `measure_number`, `title` |
| `tuxguitar_set_tempo` | 在指定小节修改速度（BPM） | `file_path`, `measure_number`, `tempo` |
| `tuxguitar_set_time_signature` | 在指定小节修改拍号（4/4, 3/4, 6/8 等） | `file_path`, `measure_number`, `numerator`, `denominator` |
| `tuxguitar_get_chord_info` | 查询吉他和弦指法（品位、组成音、第一品位） | `chord_name` |
| `tuxguitar_list_chords` | 列出内置和弦库中支持的所有和弦名称 | - |
| `tuxguitar_convert_format` | 在 `.tg` 与 `.gp5` 间双向转换 | `input_path`, `output_path` |
| `tuxguitar_open_in_app` | 在 TuxGuitar 桌面客户端中打开乐谱 | `file_path` |
| `tuxguitar_app_status` | 检测 TuxGuitar 是否安装、进程 PID 与运行状态 | - |

---

## ⚙️ 客户端接入配置 (Client Setup)

### 1. Google Antigravity / Gemini
已为您自动注册至全局配置 `~/.gemini/config/mcp_config.json`：
```json
{
  "mcpServers": {
    "tuxguitar": {
      "command": "C:\\Users\\30907\\Miniconda3\\python.exe",
      "args": [
        "-m",
        "tuxguitar_mcp",
        "serve"
      ],
      "cwd": "D:\\Program Files\\tuxguitar",
      "env": {
        "PYTHONPATH": "D:\\Program Files\\tuxguitar",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

### 2. Claude Desktop (`claude_desktop_config.json`)
在 `%APPDATA%\Claude\claude_desktop_config.json` 中添加：
```json
{
  "mcpServers": {
    "tuxguitar": {
      "command": "C:\\Users\\30907\\Miniconda3\\python.exe",
      "args": [
        "-m",
        "tuxguitar_mcp",
        "serve"
      ],
      "cwd": "D:\\Program Files\\tuxguitar",
      "env": {
        "PYTHONPATH": "D:\\Program Files\\tuxguitar",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

### 3. Cursor / Windsurf / VS Code (`mcp.json`)
```json
{
  "mcpServers": {
    "tuxguitar": {
      "command": "C:\\Users\\30907\\Miniconda3\\python.exe",
      "args": [
        "-m",
        "tuxguitar_mcp",
        "serve"
      ],
      "cwd": "D:\\Program Files\\tuxguitar",
      "env": {
        "PYTHONPATH": "D:\\Program Files\\tuxguitar",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

## 💻 命令行用法 (CLI)

除了作为 MCP Server 运行外，还提供了独立的命令行工具：

```bash
# 1. 检查 TuxGuitar 运行状态
python -m tuxguitar_mcp status

# 2. 查看乐谱摘要
python -m tuxguitar_mcp summary demo_song.gp5

# 3. 渲染 ASCII 制表谱
python -m tuxguitar_mcp tab demo_song.gp5 --track 1 --start 1 --end 4

# 4. 转换乐谱格式 (GP5 -> TG 或 TG -> GP5)
python -m tuxguitar_mcp convert song.tg song.gp5

# 5. 在桌面软件中打开
python -m tuxguitar_mcp open demo_song.gp5
```

---

## 🎸 常见 AI 对话场景示例

在与 AI Agent 对话时，你可以直接提出如下需求：

1. **创作新歌伴奏**：
   > *"帮我新建一个乐谱 `my_song.gp5`，速度 120，包含主音吉他和扫弦节奏吉他，在节奏吉他前 4 小节写入 C - G - Am - Em 的扫弦伴奏。"*

2. **编写吉他独奏 (Solo)**：
   > *"在第 5 小节为主音吉他写一段 A 小调五声音阶 Solo，加入 3 弦 7 品击音到 9 品、2 弦 10 品全音推弦，并在 Markdown 中用 ASCII 制表谱展示给我看。"*

3. **乐谱移调**：
   > *"把 `demo_song.gp5` 的主音吉他音轨向上移调 2 个半音（一个全音），保存并展示移调后的第 5~8 小节。"*

4. **打开试听**：
   > *"在 TuxGuitar 软件中打开刚才修改好的乐谱。"*
