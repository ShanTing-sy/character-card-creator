# 角色卡与世界书工具集

角色卡格式转换器以及创作小助手，为 TavernAI / SillyTavern / tavo 等 AI 角色扮演平台打造的三个创作助手。

## 包含工具

| 工具 | 用途 | 触发方式 |
|------|------|---------|
| **chara-card-creator-skill** | 从零创作角色卡（13模块YAML模板）和世界书 | `/chara-card-creator-skill` |
| **正则与世界书小助手** | 生成驱动前端格式渲染的世界书条目（LoreForge） | `/loreforge-skill` |
| **regex-helper-skill** | 生成 SillyTavern 正则替换 JSON 条目 | `/regex-helper-skill` |

## 三者关系

```
chara-card-creator-skill（宏观：从零设计角色+世界观）
        ↓
正则与世界书小助手（微观：填充格式驱动条目）
        ↓
regex-helper-skill（底层：编写正则替换 JSON）
```

## 安装

每个工具目录下均有 `SKILL.md`，复制到对应平台的 skills 目录即可：

| 平台 | 路径 |
|------|------|
| Claude Code | `~/.claude/skills/<工具名>/` |
| 通用 | `~/.agents/skills/<工具名>/` |

也可运行各目录下的 `install.sh` 自动安装。

## 目录结构

```
角色卡世界书工具集/
├── chara-card-creator-skill/     # 角色卡与世界书创作 Agent
│   ├── SKILL.md
│   ├── 角色卡模板/               # YAML + JSON 模板
│   ├── 世界书模板/               # 世界书条目模板
│   ├── 参考文档/                 # 创作方法论、格式规范
│   └── 脚本/                     # init_project.py
├── 正则与世界书小助手/           # LoreForge / 铸典师
│   ├── SKILL.md
│   └── 知识库/                   # Agent 知识体系
└── regex-helper-skill/           # SillyTavern 正则助手
    ├── SKILL.md
    ├── assets/                   # 模板
    ├── references/               # 参考文档
    └── scripts/                  # 分析/生成脚本
```


