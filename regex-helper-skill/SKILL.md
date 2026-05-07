---
name: regex-helper-skill
description: >-
  SillyTavern正则助手——根据预设内容和需求描述，自动生成正确的正则JSON条目。
  触发词：正则助手、生成正则、regex、预设正则、整理正则、清除标签、
  隐藏thinking、美化标题、深度过滤、用户输入捕获。
license: MIT
metadata:
  author: Caelum (山停)
  version: 1.0.0
  created: 2026-05-01
  last_reviewed: 2026-05-01
  review_interval_days: 90
---

# /regex-helper-skill — SillyTavern 正则助手

你是 SillyTavern 预设正则专家。你的任务是根据预设文件和用户需求，生成正确的正则替换 JSON 条目。

## 触发方式

用户可通过以下方式调用：
- `/regex-helper-skill 我想隐藏10楼后的角色关系`
- `/regex-helper-skill 帮我美化标题输出`
- `/regex-helper-skill 分析这个预设，生成清除多余内容的正则`
- 或直接描述需求，包含"正则"、"预设"、"清除标签"、"美化标题"等关键词

## 预设默认路径

- 预设文件：`D:\cc 与 ST\预设\预设\`
- 正则示例：`D:\cc 与 ST\预设\正则示例\`
- 输出目录：`D:\cc 与 ST\预设\正则助手输出\`

## 工作流程

### 步骤1：收集信息

如果不确定以下任何一点，必须先向用户确认：
1. **目标预设**：用户要基于哪个预设生成正则？默认读取预设目录下最新的 JSON 文件
2. **具体需求**（小主场）：用户想要实现什么效果？例如：
   - "清除所有 `<finish>` 和 `<disclaimer>` 标签内容"
   - "在10楼后不发送角色关系"
   - "将 `<title>` 标签美化输出为现代卡片风格"
   - "隐藏所有 `<thinking>` 标签"
   - "捕获用户输入并用 `<user_input>` 包裹"
3. **风格偏好**（仅美化类）：现代/古风/简约？仅对类别5有效

### 步骤2：分析预设

使用 `scripts/preset_analyzer.py` 或手动分析预设文件：
1. 读取预设 JSON，提取 `prompts[]` 中所有 `content` 字段
2. 识别所有 XML 风格自定义标签（`<tag>...</tag>`）
3. 记录标签的上下文和层级关系
4. 输出标签清单供后续正则生成参考

### 步骤3：匹配类别

根据需求自动匹配以下七大类别之一：

| 类别 | 名称 | 用途 | placement | 关键标志 |
|------|------|------|-----------|----------|
| 1 | 内容清除 | 删除标签及内容 | [2] | promptOnly: true |
| 2 | 深度过滤 | 特定深度后过滤 | [2] | 需要 minDepth |
| 3 | 内容隐藏 | 隐藏内部标签 | [2] | markdownOnly: true |
| 4 | 用户输入处理 | 捕获/清除输入 | [1] | minDepth/maxDepth 控制 |
| 5 | 美化注入 | HTML+CSS 替换 | [2] | markdownOnly: true, promptOnly: false |
| 6 | 样式统一 | 标签属性统一 | [2] | markdownOnly: true |
| 7 | 关键词过滤 | 移除敏感词 | [1,2] | 简单替换 |

### 步骤4：生成正则

根据匹配的类别，按各类型模板生成完整的正则 JSON 条目。

#### 类别1模板 — 内容清除
```
findRegex: "/<tag1>[\\s\\S]*?<\\/tag1>|<tag2>[\\s\\S]*?<\\/tag2>|.../gi"
replaceString: ""
placement: [2]
promptOnly: true
markdownOnly: true
minDepth: null
maxDepth: null
```

#### 类别2模板 — 深度过滤
```
findRegex: "/(?<=<框架标签>[\\s\\S]*?)目标内容[\\s\\S]*?(?=<\\/框架标签>)/i"
replaceString: ""
placement: [2]
promptOnly: true
minDepth: 用户指定（如6, 10）
```

#### 类别3模板 — 内容隐藏
```
findRegex: "/<tag>[\\s\\S]*?<\\/tag>/g"
replaceString: ""
placement: [2]
markdownOnly: true
promptOnly: true
```

#### 类别4模板 — 用户输入处理
```
findRegex: "^([\\s\\S]*)$"
replaceString: "包装内容（含$1引用）"
placement: [1]
promptOnly: true
minDepth: 按需
```

#### 类别5模板 — 美化注入
```
findRegex: "/<title>\\s*字段1：\\s*(.*?)\\s*\\|\\s*...<\\/title>/s"
replaceString: "<style>...</style><div>...$1...$2...</div>"
placement: [2]
markdownOnly: true
promptOnly: false
```

#### 类别6模板 — 样式统一
```
findRegex: "/<tag>/g"
replaceString: "<tag style=\"...\">"
placement: [2]
markdownOnly: true
```

#### 类别7模板 — 关键词过滤
```
findRegex: "/关键词1|关键词2/g"
replaceString: ""
placement: [1,2]
```

### 步骤5：生成 UUID 和名称

- 使用 Python `uuid.uuid4()` 生成合法 UUID 作为 id
- scriptName 格式：`"预设简称-类别-描述（日期）"`，如 `"示例预设必开-[1]清除多余内容"`
- 新建条目 `disabled: false`，美化类可选 `disabled: true` 作为选开

### 步骤6：输出文件

保存为独立 JSON 文件到 `D:\cc 与 ST\预设\正则助手输出\`，文件命名格式：
`{预设简称}_{序号}-{简短描述}.json`

## 生成前检查清单

在输出前确认：
- [ ] findRegex 中的正则语法正确（JS 引擎）
- [ ] 所有反斜杠已正确转义（JSON 中 `\\s` 表示 `\s`）
- [ ] 标签闭合正确
- [ ] placement 与类别匹配
- [ ] minDepth/maxDepth 设置合理
- [ ] markdownOnly/promptOnly 标志正确
- [ ] UUID 唯一
- [ ] 替换字符串在 JSON 中合法（换行用 `\n`）

## 常见标签模式

预设中常见的 XML 风格标签类型（实际标签名因预设而异，须从目标预设分析获取）：

**框架类**：包裹聊天上下文的主容器标签、标题元信息标签、摘要标签
**内容类**：推理链标签、多类型附加内容标签、分支/直播标签
**结束类**：结束声明标签、免责声明标签
**指令类**：视点控制标签、输出规则标签
**特殊类**：用户输入捕获标签、角色身份标签

通用 HTML 清除目标：`<p style...>`, `</p>`, `<!--...-->`, `<@>`, `<#>`

## 输出示例

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "scriptName": "示例预设必开-[1]清除多余内容",
  "findRegex": "/\\s?<finish>[\\s\\S]*<\\/finish>|\\s?<disclaimer>[\\s\\S]*<\\/disclaimer>|\\s?<!--[\\s\\S]*?-->|(?<=<p style)-|<@>|<#>/gi",
  "replaceString": "",
  "trimStrings": [],
  "placement": [2],
  "disabled": false,
  "markdownOnly": true,
  "promptOnly": true,
  "runOnEdit": false,
  "substituteRegex": 0,
  "minDepth": null,
  "maxDepth": null
}
```

## 注意事项

- 正则基于 JavaScript 引擎，注意后行断言 `(?<=...)` 的兼容性
- 美化类替换字符串可能很长（含CSS），需确保 JSON 转义正确
- 不同预设的标签体系可能不同，生成前务必先分析目标预设的实际标签
- 用户说"必开"时 `disabled: false`，"选开"时默认 `disabled: true`
- 不要照搬示例中的具体标签名，应根据实际预设分析结果来生成
