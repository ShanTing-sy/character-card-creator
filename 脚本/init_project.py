#!/usr/bin/env python3
"""
初始化角色卡 / 世界书项目目录。

角色卡和世界书是两个独立的产出：
  --mode chara     仅创建角色卡目录和模板
  --mode worldbook 仅创建世界书目录和模板
  --mode both      同时创建角色卡和世界书

用法:
    python init_project.py --name "角色名" --mode chara
    python init_project.py --name "世界观名" --mode worldbook
    python init_project.py --name "项目名" --mode both
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


# ── YAML 角色卡模板（Tavern/SillyTavern） ──
CHARA_YAML_TEMPLATE = """# ============================================================
# 角色卡 · {name}
# 平台：TavernAI / SillyTavern
# 创建时间：{timestamp}
# ============================================================
character:
  basic_info:
    name: "{name}"
    alias: ["暂无"]
    gender: ""
    age:
    birthday: ""
    birthday_note: ""
    zodiac: ""
    mbti: ""
    blood_type: ""
    nationality: ""

  identity:
    occupation: ""
    organization: ""
    status_in_field: ""
    social_class: ""
    reputation_note: ""

  appearance:
    height: ""
    weight: ""
    build: ""
    hair: ""
    eyes: ""
    skin: ""
    face: ""
    distinctive_features:
      - feature: ""
        origin: ""
    voice: ""
    scent: ""

  style:
    daily: ""
    formal: ""
    preference_note: ""
    taboo: ""

  food:
    likes:
      - ""
    dislikes:
      - ""

  personality:
    keywords: ["", "", "", ""]
    core_traits:
      - trait: ""
        detail: ""
    contradictions:
      - ""
    flaws:
      - ""
    fears:
      - ""

  hobbies:
    - hobby: ""
      detail: ""

  emotional_expression:
    when_happy:
      expression: ""
      verbal: ""
      physical: ""
    when_sad:
      expression: ""
      verbal: ""
      physical: ""
      note: ""
    when_angry:
      expression: ""
      verbal: ""
      physical: ""
      note: ""
    when_embarrassed:
      expression: ""
      verbal: ""
      physical: ""

  behavior_with_user:
    note: "以下为与 {{{{user}}}} 建立亲密关系后的相处模式"
    behaviors:
      - ""

  background:
    childhood: ""
    key_turning_points:
      - age:
        event: ""
    personality_origin_analysis: ""

  relationships:
    friends: []
    rivals: []
    family:
      father:
        personality: ""
        current_relation: ""
      mother:
        personality: ""
        current_relation: ""
      family_atmosphere: ""

  roleplay_guidance:
    language_style:
      overall: ""
      examples:
        casual: ""
        caring: ""
        cold: ""
        angry: ""
        soft: ""
    attitude_toward_user:
      default: ""
      after_bonding: ""
      core_tension: ""
    forbidden_behaviors:
      - ""
"""

# ── tavo JSON 角色卡模板 ──
def make_tavo_template(name: str, timestamp: int) -> dict:
    return {
        "spec": "chara_card_v3",
        "spec_version": "3.0",
        "data": {
            "avatar": "charaCard/xxx.png",
            "name": name,
            "description": "",
            "first_mes": "",
            "personality": "",
            "scenario": "",
            "mes_example": "",
            "creator_notes": "",
            "system_prompt": "",
            "post_history_instructions": "",
            "alternate_greetings": None,
            "character_book": None,  # 世界书独立存放，此处不内嵌
            "tags": [],
            "creator": "",
            "character_version": "1.0",
            "nickname": None,
            "creation_date": timestamp,
            "modification_date": timestamp,
            "extensions": {}
        }
    }


# ── 世界书模板 ──
def make_worldbook_template(name: str) -> dict:
    return {
        "name": f"{name}世界观",
        "description": "",
        "entries": []
    }


def make_worldbook_entry_template(entry_id: int, insertion_order: int) -> dict:
    return {
        "keys": [],
        "content": "",
        "extensions": {
            "selectiveLogic": 0,
            "position": 0,
            "depth": 4,
            "role": 0,
            "match_whole_words": True,
            "probability": 100,
            "useProbability": True,
            "sticky": 0,
            "cooldown": 0,
            "delay": 0,
            "exclude_recursion": False,
            "prevent_recursion": False,
            "delay_until_recursion": False,
            "group": "",
            "group_override": False,
            "group_weight": 100,
            "use_group_scoring": False,
            "scan_depth": 2,
            "case_sensitive": False,
            "automation_id": "",
            "vectorized": False
        },
        "enabled": True,
        "use_regex": False,
        "insertion_order": insertion_order,
        "id": entry_id,
        "name": "",
        "comment": "",
        "selective": False,
        "case_sensitive": False,
        "constant": False,
        "position": "before_char",
        "display_index": entry_id + 1
    }


def create_chara_project(name: str, output_base: str) -> dict:
    """创建角色卡项目"""
    project_dir = Path(output_base) / name
    project_dir.mkdir(parents=True, exist_ok=True)
    created = []
    timestamp = int(datetime.now().timestamp())

    # YAML 角色卡（SillyTavern/TavernAI）
    yaml_path = project_dir / f"{name}_角色卡.yaml"
    yaml_content = CHARA_YAML_TEMPLATE.format(
        name=name,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    created.append(str(yaml_path))

    # JSON 角色卡（tavo）
    json_path = project_dir / f"{name}_角色卡.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(make_tavo_template(name, timestamp), f, ensure_ascii=False, indent=2)
    created.append(str(json_path))

    return {"project_dir": str(project_dir), "files": created}


def create_worldbook_project(name: str, output_base: str) -> dict:
    """创建世界书项目"""
    project_dir = Path(output_base) / name
    project_dir.mkdir(parents=True, exist_ok=True)
    created = []

    # 世界书 JSON
    wb_path = project_dir / f"{name}_世界书.json"
    with open(wb_path, 'w', encoding='utf-8') as f:
        json.dump(make_worldbook_template(name), f, ensure_ascii=False, indent=2)
    created.append(str(wb_path))

    return {"project_dir": str(project_dir), "files": created}


def create_both_project(name: str, output_base: str) -> dict:
    """同时创建角色卡和世界书"""
    project_dir = Path(output_base) / name
    project_dir.mkdir(parents=True, exist_ok=True)
    created = []
    timestamp = int(datetime.now().timestamp())

    # YAML 角色卡
    yaml_path = project_dir / f"{name}_角色卡.yaml"
    yaml_content = CHARA_YAML_TEMPLATE.format(
        name=name,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    created.append(str(yaml_path))

    # JSON 角色卡（tavo）
    json_path = project_dir / f"{name}_角色卡.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(make_tavo_template(name, timestamp), f, ensure_ascii=False, indent=2)
    created.append(str(json_path))

    # 世界书
    wb_path = project_dir / f"{name}_世界书.json"
    with open(wb_path, 'w', encoding='utf-8') as f:
        json.dump(make_worldbook_template(name), f, ensure_ascii=False, indent=2)
    created.append(str(wb_path))

    return {"project_dir": str(project_dir), "files": created}


def main():
    parser = argparse.ArgumentParser(
        description="初始化角色卡 / 世界书项目目录"
    )
    parser.add_argument('--name', required=True, help='角色名或世界观名')
    parser.add_argument(
        '--mode', choices=['chara', 'worldbook', 'both'], default='chara',
        help='chara=仅角色卡, worldbook=仅世界书, both=两者 (默认: chara)'
    )
    parser.add_argument(
        '--output', default=r'D:\cc 与 ST\角色卡',
        help='输出基础路径'
    )

    args = parser.parse_args()

    try:
        if args.mode == 'chara':
            result = create_chara_project(args.name, args.output)
            print(f"角色卡项目已创建: {result['project_dir']}")
            print("文件:")
            for f in result['files']:
                print(f"  → {f}")
            print(f"\n下一步: 编辑 {args.name}_角色卡.yaml 填写13个模块")

        elif args.mode == 'worldbook':
            result = create_worldbook_project(args.name, args.output)
            print(f"世界书项目已创建: {result['project_dir']}")
            print("文件:")
            for f in result['files']:
                print(f"  → {f}")
            print(f"\n下一步: 编辑 {args.name}_世界书.json 添加世界法则条目")

        elif args.mode == 'both':
            result = create_both_project(args.name, args.output)
            print(f"完整项目已创建: {result['project_dir']}")
            print("文件:")
            for f in result['files']:
                print(f"  → {f}")
            print(f"\n下一步:")
            print(f"  1. 编辑 {args.name}_角色卡.yaml 填写角色设定")
            print(f"  2. 编辑 {args.name}_世界书.json 添加世界观条目")

    except (ValueError, OSError) as e:
        print(json.dumps({
            "error": str(e),
            "error_type": "validation" if isinstance(e, ValueError) else "runtime",
            "hint": "请检查参数并重试"
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
