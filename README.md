# TuxGuitar AI MCP & Guitar Arranger

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![TuxGuitar](https://img.shields.io/badge/TuxGuitar-2.1.1-orange.svg)](http://www.tuxguitar.com.ar/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**TuxGuitar AI MCP** 是专为 **TuxGuitar** 打造的大语言模型上下文协议（Model Context Protocol）工具集与智能吉他制谱套件。支持与 AI Agent（如 Antigravity、Claude、Cursor 等）无缝协作，实现专业级吉他谱读写、编配、和弦伴奏生成、指弹独奏改编、移调以及与 TuxGuitar 桌面客户端的联动播放。

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
├── build_yu_ai.py                     # 《雨爱 (司凤版)》三重奏生成脚本
├── build_yi_wu_suo_you.py             # 《一无所有》指弹独奏生成脚本
├── build_qu_nian_xia_tian_v2.py       # 《去年夏天》C调指弹独奏生成脚本
├── yu_ai_sifeng.tg / .gp5             # 《雨爱 (司凤版)》多声部总谱
├── yi_wu_suo_you_fingerstyle.tg/.gp5  # 《一无所有》指弹吉他谱 (全62小节)
├── qu_nian_xia_tian_fingerstyle.tg/.gp5 # 《去年夏天》指弹吉他谱 (Capo 2)
├── requirements.txt                   # 依赖清单
└── .gitignore                         # 忽略安装包与二进制文件
```

---

## 🎸 内置吉他乐谱作品

本项目内置了由 AI MCP 编配完成的多首经典曲目指弹与重奏乐谱，格式包含 `.tg`（TuxGuitar 原生工程）和 `.gp5`（Guitar Pro 5 标准格式）：

| 曲目名称 | 编配形式 | 调式与拍号 | 亮点特色 |
| :--- | :--- | :--- | :--- |
| **《雨爱 (司凤版)》** | 三声部重奏总谱<br>(主音+和弦+贝斯) | E 大调, 4/4 拍<br>Shuffle 162 BPM | 完整还原原曲 Shuffle 3:2 律动、三连暴重音断奏、弹舌音与高潮嗷大滑音。 |
| **《一无所有 (崔健)》** | 民谣摇滚指弹独奏 | C# 小调, 4/4 拍<br>169 BPM | 完整 62 小节，包含散板琶音、唢呐前奏、主歌低沉叙事、大副歌扫弦与 1 弦 9 品高音呼唤。 |
| **《去年夏天 (王大毛)》** | 抒情民谣指弹独奏 | C 调 (Capo 2 = D)<br>2/4 拍, 62 BPM | 4-5-3-6-2-5-1 经典走向，根音与每句末尾押韵词（在、待、哀、来）精准对齐，双音共鸣。 |

---

## 🛠️ 安装与快速开始

### 1. 环境依赖

```bash
git clone https://github.com/<your-username>/tuxguitar-mcp.git
cd tuxguitar-mcp
pip install -r requirements.txt
```

### 2. 运行自动化测试

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
      "cwd": "/path/to/tuxguitar-mcp"
    }
  }
}
```

---

## 📄 开源许可证

本项目基于 [MIT License](LICENSE) 开源。
