# TuxGuitar AI MCP (Model Context Protocol)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![TuxGuitar](https://img.shields.io/badge/TuxGuitar-2.1.1-orange.svg)](http://www.tuxguitar.com.ar/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**TuxGuitar AI MCP** 是专为 **TuxGuitar** 打造的大语言模型上下文协议（Model Context Protocol）工具集。支持与 AI Agent（如 Antigravity、Claude、Cursor 等）无缝协作，实现专业级吉他谱读写、编配、和弦伴奏生成、指弹独奏改编、移调以及与 TuxGuitar 桌面客户端的联动播放。

---

## 🌟 核心特性

- **多格式全兼容**：
  - 原生支持 TuxGuitar 原生格式（`.tg`，XML Zip）。
  - 原生支持 Guitar Pro 标准格式（`.gp5`、`.gp4`、`.gp3`）。
  - 支持两种格式间无损双向转换。
- **全方位乐谱编辑**：
  - **乐谱概览**：读取曲名、作者、调号、速度、拍号、总小节数、各音轨详细配置。
  - **小节与音符读写**：精确读取/修改任意小节、拍子、弦（1~6弦/贝斯4弦/7弦等）、品位（Fret）、时值与三连音。
  - **吉他演奏技巧**：推弦（Bend）、击勾弦（Hammer-on / Pull-off）、滑音（Slide）、揉弦（Vibrato）、掌心闷音（Palm Mute）、自然/人工泛音（Harmonics）、重音、跳音。
- **智能吉他理论与和弦库**：
  - 内置吉他和弦词典（大三、小三、七和弦、大七、小七、挂留和弦等）。
  - 自动扫弦节奏型（经典下下上下上、连续四分音符、八分音符扫弦、金属闷音、分解和弦琶音）。
- **极速旋律与 SOLO 创作**：
  - 输入音符序列即可自动计算节拍刻度并填充小节。
- **ASCII 制表谱渲染**：
  - 实时渲染标准 ASCII 六线谱，在终端或 AI 对话框中直观呈现。
- **TuxGuitar 桌面无缝联动**：
  - 检测客户端状态并一键调用 TuxGuitar 桌面应用打开乐谱播放试听。

---

## 📂 项目结构

```text
.
├── tuxguitar_mcp/                     # 核心 FastMCP 服务与乐谱处理引擎
│   ├── server.py                      # 18 项核心 MCP 工具实现
│   ├── models.py                      # 乐谱音轨/小节/音符/技巧数据结构
│   ├── song_editor.py                 # 高层乐谱编辑引擎 (增删改查、算拍、移调)
│   ├── tg_parser.py                   # TuxGuitar 原生 .tg (XML Zip) 读写器
│   ├── gp_adapter.py                  # Guitar Pro (.gp5/.gp4/.gp3) 读写适配器
│   ├── ascii_tab.py                   # ASCII 六线谱可视化生成器
│   ├── chords.py                      # 吉他和弦字典与扫弦节奏型库
│   ├── app_launcher.py                # TuxGuitar 桌面应用进程管理
│   └── tests/                         # 自动化测试套件
├── requirements.txt                   # 依赖清单
└── .gitignore                         # 忽略安装包、二进制与本地乐谱
```

---

## 🛠️ MCP 工具清单 (18 Tools)

| 工具名称 | 功能描述 | 关键参数 |
| :--- | :--- | :--- |
| `tuxguitar_get_score_summary` | 读取乐谱全局摘要（曲名、作者、调号、速度、拍号、音轨） | `file_path` |
| `tuxguitar_read_measures` | 结构化读取指定音轨的小节音符、时值与技巧 | `file_path`, `track_number`, `start_measure`, `end_measure` |
| `tuxguitar_get_ascii_tab` | 将乐谱渲染为直观的 ASCII 六线谱 | `file_path`, `track_number`, `start_measure`, `end_measure` |
| `tuxguitar_create_score` | 从零创建全新乐谱（支持多音轨与调弦预设） | `file_path`, `title`, `artist`, `tempo`, `time_signature`, `tracks` |
| `tuxguitar_add_track` | 向现有乐谱追加新乐器音轨（电吉他、民谣吉他、贝斯等） | `file_path`, `name`, `tuning`, `instrument` |
| `tuxguitar_remove_track` | 移除指定音轨 | `file_path`, `track_number` |
| `tuxguitar_write_measures` | 批量写入/替换小节的拍子、音符、技巧与和弦 | `file_path`, `track_number`, `start_measure`, `measures_data` |
| `tuxguitar_add_riff` | 便捷写入旋律、Riff 或吉他 Solo（自动算拍与跨小节） | `file_path`, `track_number`, `start_measure`, `notes_list` |
| `tuxguitar_add_chord_progression` | 写入和弦进行与扫弦节奏型（如 C-G-Am-F） | `file_path`, `track_number`, `start_measure`, `progression`, `strum_pattern` |
| `tuxguitar_transpose` | 音轨或全曲半音移调 | `file_path`, `track_number`, `semitones` |
| `tuxguitar_add_marker` | 添加曲式段落标记（Intro, Verse, Chorus, Solo, Outro） | `file_path`, `measure_number`, `title` |
| `tuxguitar_set_tempo` | 在指定小节修改速度（BPM） | `file_path`, `measure_number`, `tempo` |
| `tuxguitar_set_time_signature` | 在指定小节修改拍号（4/4, 3/4, 6/8, 2/4 等） | `file_path`, `measure_number`, `numerator`, `denominator` |
| `tuxguitar_get_chord_info` | 查询吉他和弦指法（品位、组成音、第一品位） | `chord_name` |
| `tuxguitar_list_chords` | 列出内置和弦库中支持的所有和弦名称 | - |
| `tuxguitar_convert_format` | 在 `.tg` 与 `.gp5` 间双向无损转换 | `input_path`, `output_path` |
| `tuxguitar_open_in_app` | 调用 TuxGuitar 桌面客户端打开乐谱播放试听 | `file_path` |
| `tuxguitar_app_status` | 检测 TuxGuitar 桌面端安装路径与运行状态 | - |

---

## 🚀 安装与快速开始

### 1. 安装依赖

```bash
git clone https://github.com/xjtu-tanLHY/TuxGuitar-mcp.git
cd TuxGuitar-mcp
pip install -r requirements.txt
```

### 2. 运行单元与集成测试

```bash
python -m unittest discover -s tuxguitar_mcp/tests
```

### 3. 作为 MCP 服务运行

```bash
python -m tuxguitar_mcp serve
```

在全局 MCP 配置文件（如 `mcp_config.json`）中接入：

```json
{
  "mcpServers": {
    "tuxguitar": {
      "command": "python",
      "args": ["-m", "tuxguitar_mcp", "serve"],
      "cwd": "/path/to/TuxGuitar-mcp"
    }
  }
}
```

---

## 📄 开源许可证

本项目基于 [MIT License](LICENSE) 开源。
