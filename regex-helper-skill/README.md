# regex-helper-skill

SillyTavern 正则助手 —— 根据预设内容和需求描述，自动生成正确的正则 JSON 条目。

## 功能

- 分析 SillyTavern 预设文件中的 XML 标签体系
- 根据需求描述自动匹配七种正则类别
- 生成符合 SillyTavern 格式的正则 JSON 条目
- 支持内容清除、深度过滤、内容隐藏、用户输入处理、美化注入、样式统一、关键词过滤

## 安装

### Claude Code
```bash
git clone <repo-url> ~/.claude/skills/regex-helper-skill
```

### 自动安装
```bash
./install.sh
```

### 指定平台
```bash
./install.sh --platform cursor
./install.sh --platform windsurf
./install.sh --all
```

## 使用

在 Claude Code（或支持的其他平台）中输入：

```
/regex-helper-skill 帮我分析预设文件
/regex-helper-skill 生成一个清除多余内容的正则
/regex-helper-skill 我想在10楼后隐藏角色关系
/regex-helper-skill 将标题美化输出为现代卡片风格
```

## 文件结构

```
regex-helper-skill/
├── SKILL.md                  # 技能主文件
├── scripts/
│   ├── preset_analyzer.py    # 预设标签分析器
│   └── regex_generator.py    # 正则条目生成器
├── references/
│   ├── preset-tags.md        # 标签模式参考
│   └── regex-patterns.md     # 正则模式目录
├── assets/
│   └── regex-template.json   # JSON 模板
├── install.sh                # 跨平台安装脚本
└── README.md                 # 本文件
```

## 要求

- Python 3.8+
- 无额外 Python 依赖（仅使用标准库）

## 许可

MIT
