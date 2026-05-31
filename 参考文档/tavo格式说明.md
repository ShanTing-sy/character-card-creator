# tavo / silly stave 角色卡格式完整规范

## 概述

tavo 和 silly stave 平台使用 `chara_card_v3` 规范。角色卡是一个 JSON 文件，包含角色定义、开场白、世界书、主题配置等完整信息。

## 顶层结构

```json
{
  "spec": "chara_card_v3",
  "spec_version": "3.0",
  "data": {
    "avatar": "charaCard/xxx.png",
    "name": "角色卡名称",
    "description": "角色描述（群像时包含所有角色YAML）",
    "first_mes": "开场白内容",
    "personality": "",
    "scenario": "",
    "mes_example": "",
    "creator_notes": "创作者备注",
    "system_prompt": "",
    "post_history_instructions": "",
    "alternate_greetings": null,
    "character_book": { ... },
    "tags": ["标签1", "标签2"],
    "creator": "创作者名",
    "character_version": "版本名",
    "nickname": null,
    "extensions": {
      "tavo": {
        "theme": { ... }
      }
    }
  }
}
```

## data 字段详解

### 基础字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| avatar | string | 否 | 头像路径，格式 `charaCard/xxx.png` |
| name | string | 是 | 角色卡名称，群像时可为世界观名 |
| description | string | 是 | 角色描述，单角色用 YAML 格式，群像包含所有角色 |
| first_mes | string | 是 | 首次消息/开场白 |
| personality | string | 否 | 性格标签补充 |
| scenario | string | 否 | 场景描述补充 |
| mes_example | string | 否 | 对话示例 |
| creator_notes | string | 否 | 创作者备注说明 |
| system_prompt | string | 否 | 系统级提示词 |
| post_history_instructions | string | 否 | 历史后处理指令 |
| alternate_greetings | null/array | 否 | 备用开场白列表 |
| character_book | object | 否 | 世界书定义 |
| tags | array | 否 | 标签列表，如 `["无限流/群像/全性向"]` |
| creator | string | 否 | 创作者名称 |
| character_version | string | 否 | 版本标识 |
| nickname | null | 否 | 昵称 |
| extensions | object | 否 | 扩展配置（含 tavo 主题） |

### description 字段格式

单角色时使用 YAML 格式（多行字符串）：

```yaml
# ──────────
# No.1 角色名（原名）
# ──────────
- id: "pinyin_id"
  name: "角色名"
  original_name: "原名"
  gender: "男/女/未知"
  race: "种族名"
  age: 数字或字符串
  level: "Lv.数字"
  appearance: "外貌描写，50-150字"
  alignment: "守序·善良/混乱·中立/...（可选）"
  weapons:
    - "武器1"
    - "武器2"
  ability:
    name: "能力名称"
    description: "能力效果描述"
  personality: "性格特征描述"
  preferences: "喜好描述"
  background: >
    背景故事，100-300字。
    可分多行。
  speech_style: >
    说话风格描述。
  combat_notes: "战斗风格备注"
  personal_assets: "个人资产/身份"
  public_persona: "公众形象（可选）"
  rank: 数字排名
```

群像时的 description 字段包含按顺序排列的所有角色，用 `# ──────────` 分隔。

### first_mes 开场白设计

开场白应包含以下要素：

**1. 状态栏区块**（如适用）：
```html
<时间地点状态栏>
纪元名称:星辉纪元
年份:1247
时间细节:黄昏时分
安全等级:安全区
世界名称:艾尔德兰
世界状态:正常运转
当前区域:「中枢」—— 中转空间
区域描述:浅金色空间内，悬浮的符文石板缓慢自转，散发出柔和的微光。
当前状态:探索中
保护状态:受保护
</时间地点状态栏>
```

**2. 场景描写**：用五感细节铺设当前环境

**3. NPC 导入**：通过对话/动作引入引导角色

**4. 系统信息**：个人面板、任务列表、弹幕等

**5. 互动钩子**：明确的下一步行动提示

## character_book 世界书结构

```json
{
  "name": "世界书名",
  "entries": [
    {
      "keys": ["触发词1", "触发词2"],
      "content": "条目正文",
      "extensions": {
        "selectiveLogic": 0,
        "position": 0,
        "depth": 4,
        "role": 0,
        "match_whole_words": true,
        "probability": 100,
        "useProbability": true,
        "sticky": 0,
        "cooldown": 0,
        "delay": 0,
        "exclude_recursion": false,
        "prevent_recursion": false,
        "delay_until_recursion": false,
        "group": "",
        "group_override": false,
        "group_weight": 100,
        "use_group_scoring": false,
        "scan_depth": 2,
        "case_sensitive": false,
        "automation_id": "",
        "vectorized": false
      },
      "enabled": true,
      "use_regex": false,
      "insertion_order": 0,
      "id": 0,
      "name": "条目名称",
      "comment": "条目注释",
      "selective": false,
      "case_sensitive": false,
      "constant": false,
      "position": "before_char",
      "display_index": 1
    }
  ]
}
```

### extensions 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| selectiveLogic | 0/1 | 是否使用选择性逻辑 |
| position | 0/1 | 条目位置权重 |
| depth | 2-4 | 触发深度（2=表层，4=深层） |
| role | 0-2 | 角色锚定（0=全局） |
| match_whole_words | bool | 是否整词匹配 |
| probability | 0-100 | 触发概率 |
| useProbability | bool | 是否启用概率 |
| sticky | 0-5 | 黏性值（越高越持久） |
| cooldown | 0-N | 冷却时间 |
| delay | 0-N | 延迟触发 |
| scan_depth | 0-4 | 扫描深度 |

### 条目类型与优先级

**类型一：常驻铁则（constant: true）**
- 文风指南、视角限制、描写原则
- position: "before_char"，确保始终在上下文中
- sticky: 3-5，高持久性

**类型二：系统规则**
- 经济系统、等级经验、能力体系
- selective: true，由触发词激活
- scan_depth: 3，相关对话时触发

**类型三：场景地点**
- 各区域的描写与氛围
- position: "after_char"，需要时补充
- depth: 4，深入对话时触发

**类型四：势力组织**
- 工会、商会等机构详情
- sticky: 1-2，适度持久

**类型五：特殊指令**
- `$进入副本`、`$激活馈赠` 等命令
- useProbability: true, probability: 100
- match_whole_words: true，精确匹配

## tavo 主题配置

角色卡可通过 `extensions.tavo.theme` 配置聊天气泡、字体、背景等 UI 样式：

```json
{
  "extensions": {
    "tavo": {
      "theme": {
        "spec": "tavo_theme_v1",
        "name": "主题名",
        "display_mode": "message",
        "bubble_display_type": "flat",
        "user_bubble": {
          "color": 3428210263,
          "blur": 0.0,
          "radius": 13.3,
          "alignment": "right"
        },
        "character_bubble": {
          "color": 589267493,
          "blur": 0.0,
          "radius": 13.3,
          "alignment": "left"
        },
        "background": {
          "charAvatar": true,
          "image": null,
          "color": 3529401186,
          "imageOpacity": 0.3
        }
      }
    }
  }
}
```

## JSON 生成注意事项

1. **编码**：UTF-8 without BOM
2. **缩进**：2 空格
3. **字符串转义**：description 和 first_mes 中的引号需转义
4. **空值**：字符串空值用 `""`，数组空值用 `[]`，对象空值用 `null`
5. **文件大小**：单个 JSON 建议不超过 500KB
6. **头像路径**：如无实际图片，可填写占位路径 `charaCard/xxx.png`
