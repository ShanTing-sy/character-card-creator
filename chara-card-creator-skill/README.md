# chara-card-creator-skill — 角色卡与世界书创作助手

为 tavo 和 silly stave 平台创建角色卡（chara_card_v3 格式 JSON）与配套世界书。

## 功能

- 根据用户设定的角色，生成完整的 tavo/silly stave 格式角色卡 JSON
- 支持单角色和群像（多角色）角色卡
- 自动生成配套的世界书条目（触发词 + 内容）
- 输出到 `D:\cc 与 ST\角色卡\{角色名}\` 目录

## 安装

### 方法一：使用 install.sh（推荐）

```bash
chmod +x install.sh
./install.sh                          # 自动检测平台
./install.sh --platform claude-code   # 指定 Claude Code
./install.sh --all                    # 安装到所有检测到的平台
./install.sh --dry-run                # 预览安装效果
```

### 方法二：手动安装

| 平台 | 安装路径 |
|------|---------|
| Universal | `~/.agents/skills/chara-card-creator-skill/` |
| Claude Code | `~/.claude/skills/chara-card-creator-skill/` |
| GitHub Copilot | `.github/skills/chara-card-creator-skill/` |
| Cursor | `.cursor/rules/chara-card-creator-skill/` |
| Windsurf | `.windsurf/rules/chara-card-creator-skill/` |

### 方法三：npx

```bash
npx skills add <repo-url>
```

## 使用方法

### 创建单角色卡

```
/chara-card-creator-skill 帮我创建一个赛博朋克世界的黑客角色
```

### 创建群像角色卡

```
/chara-card-creator-skill 设计一个无限流群像，10个角色，各有各的能力体系
```

### 创建世界书

```
/chara-card-creator-skill 为这个修仙世界观写一套完整的世界书
```

### 初始化项目目录

```bash
python scripts/init_project.py --name "角色名" --type single
python scripts/init_project.py --name "世界观名" --type group
```

## 输出目录结构

```
D:\cc 与 ST\角色卡\{角色名}\
├── {角色名}.json          # 角色卡 JSON（含内嵌世界书）
└── {角色名}_世界书.json    # 独立世界书（可选）
```

## 前置条件

- Python 3.8+（仅 init_project.py 脚本需要）
- 无需其他外部依赖

## 参考文件

| 文件 | 内容 |
|------|------|
| `references/tavo-format.md` | tavo 角色卡 JSON 格式完整规范 |
| `references/worldbook-guide.md` | 世界书创作方法论与条目模板 |
| `references/writing-guide.md` | 角色与世界创作原则、文风指南 |

## 故障排除

### 安装后技能未激活

1. 确认 SKILL.md 包含有效的 frontmatter（name 和 description 字段）
2. 重启 AI 编程助手会话
3. 检查技能目录是否在正确的路径下

### Python 脚本错误

确保使用 Python 3.8 或更高版本：

```bash
python --version
```

## 许可

MIT License
