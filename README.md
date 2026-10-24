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
