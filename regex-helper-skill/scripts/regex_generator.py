#!/usr/bin/env python3
"""
SillyTavern 正则条目生成器
根据需求描述和标签体系，生成符合格式的正则 JSON 条目。
"""

import json
import uuid
import os
import sys
from datetime import datetime


# 七大正则类别定义
CATEGORIES = {
    1: {
        'name': '内容清除',
        'description': '删除不需要的标签及其全部内容',
        'placement': [2],
        'promptOnly': True,
        'markdownOnly': True,
        'minDepth': None,
        'maxDepth': None,
        'regex_template': '/{patterns}/gi',
        'replaceString': '',
        'flags': 'gi',
    },
    2: {
        'name': '深度过滤',
        'description': '在特定消息深度后过滤指定内容',
        'placement': [2],
        'promptOnly': True,
        'markdownOnly': False,
        'minDepth': 6,  # 用户可指定
        'maxDepth': None,
        'regex_template': '/(?<=<{frame_tag}>[\\s\\S]*?){pattern}[\\s\\S]*?(?=<\\/{frame_tag}>)/i',
        'replaceString': '',
        'flags': 'i',
    },
    3: {
        'name': '内容隐藏',
        'description': '在渲染前隐藏指定标签内容',
        'placement': [2],
        'promptOnly': True,
        'markdownOnly': True,
        'minDepth': None,
        'maxDepth': None,
        'regex_template': '/<{tag}>[\\s\\S]*?<\\/{tag}>/g',
        'replaceString': '',
        'flags': 'g',
    },
    4: {
        'name': '用户输入处理',
        'description': '捕获、格式化或清除用户输入',
        'placement': [1],
        'promptOnly': True,
        'markdownOnly': False,
        'minDepth': None,
        'maxDepth': None,
        'regex_template': '^([\\s\\S]*)$',
        'replaceString': '',  # 用户提供包装内容
        'flags': '',
    },
    5: {
        'name': '美化注入',
        'description': '解析标签内容并替换为美化的HTML+CSS',
        'placement': [2],
        'promptOnly': False,
        'markdownOnly': True,
        'minDepth': None,
        'maxDepth': None,
        'regex_template': '',  # 完全由用户定制
        'replaceString': '',   # 包含完整HTML+CSS
        'flags': 's',
    },
    6: {
        'name': '样式统一',
        'description': '统一某个标签的内联样式属性',
        'placement': [2],
        'promptOnly': False,
        'markdownOnly': True,
        'minDepth': None,
        'maxDepth': None,
        'regex_template': '/<{tag}>/g',
        'replaceString': '<{tag} style="{styles}">',
        'flags': 'g',
    },
    7: {
        'name': '关键词过滤',
        'description': '移除输出中的特定关键词',
        'placement': [1, 2],
        'promptOnly': True,
        'markdownOnly': True,
        'minDepth': None,
        'maxDepth': None,
        'regex_template': '/{keywords}/g',
        'replaceString': '',
        'flags': 'g',
    },
}


def generate_uuid_str() -> str:
    """生成合法的 UUID v4 字符串。"""
    return str(uuid.uuid4())


def escape_regex(s: str) -> str:
    """转义正则表达式中的特殊字符。"""
    special_chars = r'\.+*?[^]$(){}=!<>|:-/'
    result = ''
    for c in s:
        if c in special_chars:
            result += '\\' + c
        else:
            result += c
    return result


def build_cleanup_regex(tags: list[str], extra_patterns: list[str] = None) -> str:
    """
    构建类别1（内容清除）的正则表达式。
    tags: 要清除的标签名列表，如 ['finish', 'disclaimer']
    extra_patterns: 额外的正则片段，如 ['<!--[\\s\\S]*?-->', '<@>']
    """
    parts = []
    for tag in tags:
        parts.append(f'<{tag}>[\\\\s\\\\S]*?<\\\\/{tag}>')

    if extra_patterns:
        parts.extend(extra_patterns)

    return '/\\s?' + '|\\s?'.join(parts) + '/gi'


def build_depth_filter_regex(keyword: str, frame_tag: str = 'frame') -> str:
    """
    构建类别2（深度过滤）的正则表达式。
    keyword: 要过滤的关键词/内容标识
    frame_tag: 框架标签名
    """
    return f'/(?<=<{frame_tag}>[\\\\s\\\\S]*?){keyword}[\\\\s\\\\S]*?(?=<\\\\/{frame_tag}>)/i'


def build_hide_regex(tag: str, global_flag: bool = True) -> str:
    """构建类别3（内容隐藏）的正则表达式。"""
    flag = 'g' if global_flag else ''
    return f'/<{tag}>[\\\\s\\\\S]*?<\\\\/{tag}>/{flag}'


def build_keyword_filter_regex(keywords: list[str]) -> str:
    """构建类别7（关键词过滤）的正则表达式。"""
    escaped = [escape_regex(k) for k in keywords]
    return '/' + '|'.join(escaped) + '/g'


def generate_regex_entry(
    category: int,
    script_name: str,
    find_regex: str,
    replace_string: str,
    disabled: bool = False,
    min_depth: int | None = None,
    max_depth: int | None = None,
    placement: list[int] | None = None,
    markdown_only: bool | None = None,
    prompt_only: bool | None = None,
) -> dict:
    """生成一个完整的正则 JSON 条目。"""
    cat = CATEGORIES.get(category, CATEGORIES[1])

    entry = {
        'id': generate_uuid_str(),
        'scriptName': script_name,
        'findRegex': find_regex,
        'replaceString': replace_string,
        'trimStrings': [],
        'placement': placement if placement is not None else cat['placement'],
        'disabled': disabled,
        'markdownOnly': markdown_only if markdown_only is not None else cat['markdownOnly'],
        'promptOnly': prompt_only if prompt_only is not None else cat['promptOnly'],
        'runOnEdit': False,
        'substituteRegex': 0,
        'minDepth': min_depth if min_depth is not None else cat['minDepth'],
        'maxDepth': max_depth if max_depth is not None else cat['maxDepth'],
    }
    return entry


def save_entry(entry: dict, filename: str, output_dir: str = None) -> str:
    """保存正则条目为 JSON 文件。"""
    if output_dir is None:
        output_dir = r'D:\cc 与 ST\预设\正则助手输出'

    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)

    return filepath


def suggest_category(user_request: str) -> tuple[int, str]:
    """
    根据用户需求文本，推荐最匹配的类别。
    返回 (类别ID, 匹配理由)
    """
    request_lower = user_request.lower()

    rules = [
        (1, ['清除', '删除', '去掉', '移除', 'clean', 'remove', '多余', '清理',
             'finish', 'disclaimer', '注释', 'comment', 'html标签']),
        (2, ['深度', '楼层', '楼外', '不发送', '过滤', 'depth', 'floor',
             '摘要', '角色关系', '绝密', '伏笔', '档案']),
        (3, ['隐藏', 'hide', 'thinking', '思维链', '推理']),
        (4, ['用户输入', '捕获', '输入捕获', 'user_input', 'user input',
             '包裹', '格式化输入', '以前的用户']),
        (5, ['美化', '标题', '样式', '卡片', 'style', 'css', 'html',
             '现代', '古风', '设计', '装饰', '排版']),
        (6, ['统一', '折叠', '样式统一', '标签属性', 'summary样式']),
        (7, ['关键词', '敏感词', '触发词', '过滤词', '屏蔽词']),
    ]

    scores = {}
    for cat_id, keywords in rules:
        score = sum(1 for kw in keywords if kw in request_lower)
        if score > 0:
            scores[cat_id] = score

    if not scores:
        return (1, '未识别到明确的类别特征，默认使用类别1（内容清除）')

    best_cat = max(scores, key=scores.get)
    reasons = {
        1: '检测到"清除/删除"语义，匹配类别1（内容清除）',
        2: '检测到"深度/楼层过滤"语义，匹配类别2（深度过滤）',
        3: '检测到"隐藏/thinking"语义，匹配类别3（内容隐藏）',
        4: '检测到"用户输入/捕获"语义，匹配类别4（用户输入处理）',
        5: '检测到"美化/标题/样式"语义，匹配类别5（美化注入）',
        6: '检测到"统一/样式统一"语义，匹配类别6（样式统一）',
        7: '检测到"关键词过滤"语义，匹配类别7（关键词过滤）',
    }
    return (best_cat, reasons.get(best_cat, ''))


# 美化模板库
BEAUTIFY_TEMPLATES = {
    'modern_title': {
        'name': '现代文字标题',
        'regex': '/<title>\\s*时间：\\s*(.*?)\\s*\\|\\s*(.*?)\\s*地点：\\s*(.*?)\\s*天气：\\s*(.*?)\\s*序号：\\s*(.*?)\\s*标题：\\s*(.*?)\\s*题记：\\s*(.*?)\\s*<\\/title>/s',
        'description': '将标准title标签解析为现代风格的存档卡片，适合科技/现代题材',
    },
    'classic_title': {
        'name': '古风文字标题',
        'regex': '/<title>\\s*时间：\\s*(.*?)\\s*\\|\\s*(.*?)\\s*地点：\\s*(.*?)\\s*天气：\\s*(.*?)\\s*序号：\\s*(.*?)\\s*标题：\\s*(.*?)\\s*题记：\\s*(.*?)\\s*<\\/title>/s',
        'description': '将标准title标签解析为古风排版，适合古风/武侠/仙侠题材',
    },
}


if __name__ == '__main__':
    print("正则条目生成器")
    print("用法: from regex_generator import generate_regex_entry, build_cleanup_regex, ...")
    print()
    print("支持的类别:")
    for cid, cinfo in CATEGORIES.items():
        print(f"  类别{cid}: {cinfo['name']} — {cinfo['description']}")
