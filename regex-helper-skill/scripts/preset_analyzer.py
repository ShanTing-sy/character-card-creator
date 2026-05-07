#!/usr/bin/env python3
"""
SillyTavern 预设标签分析器
读取预设 JSON 文件，提取所有自定义 XML 标签及其上下文。
"""

import json
import re
import os
import sys
from collections import Counter


def analyze_preset(filepath: str) -> dict:
    """分析预设文件，返回标签体系分析结果。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    prompts = data.get('prompts', [])

    # 收集所有 content 文本
    all_text = ''
    content_map = {}  # identifier/name -> content 片段
    for p in prompts:
        name = p.get('name', 'unnamed')
        identifier = p.get('identifier', 'unknown')
        content = p.get('content', '')
        enabled = p.get('enabled', False)
        role = p.get('role', 'system')

        if content:
            all_text += content + '\n'
            content_map[name] = {
                'identifier': identifier,
                'enabled': enabled,
                'role': role,
                'length': len(content),
                'preview': content[:150]
            }

    # 提取所有 XML 风格标签
    tag_pattern = re.compile(r'</?([a-zA-Z_][a-zA-Z_0-9]*(?:\s+[^>]*)?)>')
    tag_matches = tag_pattern.findall(all_text)
    tag_names = [t.split()[0] if ' ' in t else t for t in tag_matches]

    # 提取中文标签
    cn_tag_pattern = re.compile(r'</?([一-鿿][一-鿿\w]*)>')
    cn_tag_matches = cn_tag_pattern.findall(all_text)

    all_tags = tag_names + cn_tag_matches
    tag_counts = Counter(all_tags)

    # 识别配对标签（有开有闭的）
    open_tags = set(re.findall(r'<([a-zA-Z_][a-zA-Z_0-9]*(?![\s/>]))', all_text))
    close_tags = set(re.findall(r'</([a-zA-Z_][a-zA-Z_0-9]*)>', all_text))
    paired_tags = open_tags & close_tags

    # 搜索标签内容示例
    tag_examples = {}
    for tag in list(paired_tags)[:20]:
        pattern = re.compile(rf'<{tag}>(.*?)</{tag}>', re.DOTALL)
        matches = pattern.findall(all_text)
        if matches:
            sample = matches[0][:200].strip()
            tag_examples[tag] = sample

    return {
        'file': filepath,
        'total_prompts': len(prompts),
        'enabled_prompts': sum(1 for p in prompts if p.get('enabled')),
        'total_tags': len(tag_matches) + len(cn_tag_matches),
        'unique_tags': len(tag_counts),
        'top_tags': tag_counts.most_common(30),
        'paired_tags': sorted(paired_tags),
        'tag_examples': {k: v for k, v in list(tag_examples.items())[:10]},
        'content_count': len(content_map),
    }


def print_report(result: dict):
    """打印人类可读的分析报告。"""
    print(f"\n{'='*60}")
    print(f"  预设标签分析报告")
    print(f"  文件: {os.path.basename(result['file'])}")
    print(f"{'='*60}")
    print(f"\n  总提示词数: {result['total_prompts']}")
    print(f"  已启用: {result['enabled_prompts']}")
    print(f"  检测到标签总数: {result['total_tags']}")
    print(f"  唯一标签类型: {result['unique_tags']}")

    print(f"\n  [高频标签 Top 20]")
    for tag, count in result['top_tags'][:20]:
        bar = '█' * min(count, 40)
        print(f"  {tag:20s} {count:4d}  {bar}")

    print(f"\n  [成对标签] ({len(result['paired_tags'])}个)")
    for tag in result['paired_tags']:
        print(f"  <{tag}>...</{tag}>")

    if result['tag_examples']:
        print(f"\n  [标签内容示例]")
        for tag, sample in result['tag_examples'].items():
            print(f"  <{tag}>: {sample[:120]}...")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        # 默认路径
        preset_dir = r'D:\cc 与 ST\预设\预设'
        files = [f for f in os.listdir(preset_dir) if f.endswith('.json')]
        if not files:
            print("错误：预设目录中没有找到 JSON 文件")
            sys.exit(1)
        path = os.path.join(preset_dir, files[0])
        print(f"未指定文件，默认使用: {files[0]}")

    if not os.path.exists(path):
        print(f"错误：文件不存在 - {path}")
        sys.exit(1)

    result = analyze_preset(path)
    print_report(result)
