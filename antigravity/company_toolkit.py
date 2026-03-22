#!/usr/bin/env python3
"""
Company Toolkit for Antigravity

This script provides CLI commands for the Antigravity agent to setup the virtual
company organization and add new departments.

Usage:
  python company_toolkit.py setup --business_type "..." --goals "..."
  python company_toolkit.py add_department <department_id>
"""

import os
import argparse
from datetime import datetime

# --- Templates ---

COMPANY_RULES_MD = """# Company - 仮想組織管理システム

## オーナープロフィール

- **事業・活動**: {business_type}
- **目標・課題**: {goals_and_challenges}
- **作成日**: {created_date}

## 組織構成

```
.company/
├── RULES.md
└── secretary/
    ├── RULES.md
    ├── inbox/
    ├── todos/
    └── notes/
```

{additional_departments_tree}

## 部署一覧

| 部署 | フォルダ | 役割 |
|------|---------|------|
| 秘書室 | secretary | 窓口・相談役。TODO管理、壁打ち、メモ。常設。 |
{department_table_rows}

## 運営ルール

### 秘書が窓口
- ユーザーとの対話は常に秘書が担当する
- 秘書は丁寧だが親しみやすい口調で話す
- 壁打ち、相談、雑談、何でも受け付ける
- 部署の作業が必要な場合、秘書が直接該当部署のフォルダに書き込む

### 自動記録
- 意思決定、学び、アイデアは言われなくても記録する
- 意思決定 → `secretary/notes/YYYY-MM-DD-decisions.md`
- 学び → `secretary/notes/YYYY-MM-DD-learnings.md`
- アイデア → `secretary/inbox/YYYY-MM-DD.md`

### 同日1ファイル
- 同じ日付のファイルがすでに存在する場合は追記する。新規作成しない

### 日付チェック
- ファイル操作の前に必ず今日の日付を確認する

### ファイル命名規則
- **日次ファイル**: `YYYY-MM-DD.md`
- **トピックファイル**: `kebab-case-title.md`

### TODO形式
```markdown
- [ ] タスク内容 | 優先度: 高/通常/低 | 期限: YYYY-MM-DD
- [x] 完了タスク | 完了: YYYY-MM-DD
```

### コンテンツルール
1. 迷ったら `secretary/inbox/` に入れる
2. 既存ファイルは上書きしない（追記のみ）
3. 追記時はタイムスタンプを付ける
"""

SECRETARY_RULES_MD = """# 秘書室

## 役割
オーナーの常駐窓口。何でも相談に乗り、タスク管理・壁打ち・メモを担当する。

## 口調・キャラクター
- 丁寧だが堅すぎない。「〜ですね！」「承知しました」「いいですね！」
- 主体的に提案する。「ついでにこれもやっておきましょうか？」
- 壁打ち時はカジュアルに寄り添う
- 過去のメモや決定事項を参照して文脈を持った対話をする

## ルール
- オーナーからの入力はまず秘書が受け取る
- 秘書で完結するもの（TODO、メモ、壁打ち、雑談）は直接対応
- 部署の作業が必要な場合は該当部署のフォルダに直接書き込む
- 該当部署が未作成の場合は secretary/notes/ に保存する
- TODO形式: `- [ ] タスク | 優先度: 高/通常/低 | 期限: YYYY-MM-DD`
- 日次ファイルは `todos/YYYY-MM-DD.md`
- Inboxは `inbox/YYYY-MM-DD.md`。迷ったらまずここ
- 壁打ちの結論が出たら `notes/` に保存を提案する
- 意思決定は `notes/YYYY-MM-DD-decisions.md` に記録する
- 同じ日付のファイルがすでにある場合は追記する。新規作成しない
- ファイル操作前に必ず今日の日付を確認する

## 部署追加の提案
- 同じ領域のタスクが2回以上繰り返されたら、部署作成を提案する
- ユーザーが明示的に依頼した場合は即座に作成する

## フォルダ構成
- `inbox/` - 未整理のクイックキャプチャ
- `todos/` - 日次タスク管理（1日1ファイル）
- `notes/` - 壁打ち・相談メモ・意思決定ログ（1トピック1ファイル）
"""

SECRETARY_TODOS_TEMPLATE = """---
date: "{date}"
type: daily
---

# {date}

## 最優先
- [ ]

## 通常
- [ ]

## 余裕があれば
- [ ]

## 完了
- [x]

## メモ・振り返り
-
"""

# Departments configuration definitions
DEPARTMENTS_CONFIG = {
    "pm": {
        "name": "PM",
        "role": "プロジェクト進捗・マイルストーン・チケット管理",
        "description": "プロジェクト進捗、マイルストーン、チケット管理。",
        "subfolders": ["projects", "tickets"],
        "rules_md": """# PM（プロジェクト管理）

## 役割
プロジェクトの立ち上げから完了まで進捗を管理する。

## ルール
- プロジェクトファイルは `projects/project-name.md`
- チケットは `tickets/YYYY-MM-DD-title.md`
- プロジェクトのステータス: planning → in-progress → review → completed → archived
- チケットのステータス: open → in-progress → done
- チケット優先度: high / normal / low
- 新規プロジェクト作成時は必ずゴールとマイルストーンを定義
- マイルストーン完了時は秘書のTODOに報告を追記

## フォルダ構成
- `projects/` - プロジェクト管理（1プロジェクト1ファイル）
- `tickets/` - タスクチケット（1チケット1ファイル）
"""
    },
    "research": {
        "name": "リサーチ",
        "role": "市場調査・競合分析・技術調査",
        "description": "市場調査、競合分析、技術調査。",
        "subfolders": ["topics"],
        "rules_md": """# リサーチ

## 役割
市場調査・競合分析・技術調査など、情報収集と分析を担当する。

## ルール
- 調査トピックごとに `topics/kebab-case-topic.md` を作成する
- 調査開始前に必ず「目的」を明確にする
- 情報源（URL）と要点をセットで記録する
- 調査完了時は「結論」と「ネクストアクション」をまとめる

## フォルダ構成
- `topics/` - 調査トピック（1トピック1ファイル）
"""
    },
    "marketing": {
        "name": "マーケティング",
        "role": "コンテンツ企画・SNS戦略・集客",
        "description": "コンテンツ企画、SNS戦略、キャンペーン管理。",
        "subfolders": ["content-plan", "campaigns"],
        "rules_md": """# マーケティング

## 役割
コンテンツ企画、SNS戦略、集客キャンペーンなどを担当する。

## ルール
- コンテンツ企画は `content-plan/YYYY-MM-DD-title.md`
- キャンペーン管理は `campaigns/YYYY-MM-DD-campaign.md`
- コンテンツ作成時は「プラットフォーム」「ターゲット」「キーメッセージ」を必ず定義する
- ステータス: draft → review → published

## フォルダ構成
- `content-plan/` - コンテンツ企画
- `campaigns/` - キャンペーン管理
"""
    },
    "engineering": {
        "name": "開発",
        "role": "技術ドキュメント・設計・デバッグ",
        "description": "技術ドキュメント、設計書、デバッグログ。",
        "subfolders": ["docs", "debug-log"],
        "rules_md": """# 開発

## 役割
技術的なドキュメント、アーキテクチャ設計、バグ調査の記録を担当する。

## ルール
- 技術ドキュメントは `docs/kebab-case-title.md`
- デバッグログは `debug-log/YYYY-MM-DD-issue.md`
- バグ調査時は「症状」「期待する動作」「再現手順」「仮説」をフォーマットに従って記述する
- 解決したデバッグログには「再発防止策」を追記する

## フォルダ構成
- `docs/` - 技術ドキュメント・設計書
- `debug-log/` - デバッグ・バグ調査ログ
"""
    }
}

GENERIC_DEPARTMENT_RULES_MD = """# {name}

## 役割
{role}

## ルール
- 依頼されたタスクや情報をこのフォルダ内で整理して管理する
- 日付やトピックごとにわかりやすいファイル名（`YYYY-MM-DD.md` や `kebab-case.md`）で記録する
"""

def setup_company(business_type: str, goals: str, base_dir: str = ".company"):
    """Initialize the .company directory structure."""
    if os.path.exists(base_dir):
        print(f"Error: Directory '{base_dir}' already exists.")
        return

    # Create directories
    os.makedirs(base_dir, exist_ok=True)
    secretary_dir = os.path.join(base_dir, "secretary")
    os.makedirs(os.path.join(secretary_dir, "inbox"), exist_ok=True)
    os.makedirs(os.path.join(secretary_dir, "todos"), exist_ok=True)
    os.makedirs(os.path.join(secretary_dir, "notes"), exist_ok=True)

    # Write root RULES.md
    today = datetime.now().strftime("%Y-%m-%d")
    root_content = COMPANY_RULES_MD.format(
        business_type=business_type,
        goals_and_challenges=goals,
        created_date=today,
        additional_departments_tree="",
        department_table_rows=""
    )
    with open(os.path.join(base_dir, "RULES.md"), "w", encoding="utf-8") as f:
        f.write(root_content)

    # Write secretary RULES.md
    with open(os.path.join(secretary_dir, "RULES.md"), "w", encoding="utf-8") as f:
        f.write(SECRETARY_RULES_MD)

    # Write today's TODO
    todo_content = SECRETARY_TODOS_TEMPLATE.format(date=today)
    with open(os.path.join(secretary_dir, "todos", f"{today}.md"), "w", encoding="utf-8") as f:
        f.write(todo_content)

    print(f"Successfully initialized company organization in '{base_dir}'.")
    print("Secretary is ready!")

def add_department(department_id: str, base_dir: str = ".company"):
    """Add a new department to the company organization."""
    if not os.path.exists(base_dir):
        print(f"Error: Directory '{base_dir}' does not exist. Run setup first.")
        return

    dept_dir = os.path.join(base_dir, department_id)
    if os.path.exists(dept_dir):
        print(f"Error: Department '{department_id}' already exists.")
        return

    # Get department config or fallback to generic
    dept_id_lower = department_id.lower()
    config = DEPARTMENTS_CONFIG.get(dept_id_lower)
    
    name = config["name"] if config else department_id.capitalize()
    role = config["role"] if config else "専門タスクの実行と管理"
    desc = config["description"] if config else "専門タスクの領域。"
    subfolders = config["subfolders"] if config else ["general"]
    rules_md_content = config["rules_md"] if config else GENERIC_DEPARTMENT_RULES_MD.format(name=name, role=role)

    # Create directories
    os.makedirs(dept_dir, exist_ok=True)
    for sub in subfolders:
        os.makedirs(os.path.join(dept_dir, sub), exist_ok=True)

    # Write department RULES.md
    with open(os.path.join(dept_dir, "RULES.md"), "w", encoding="utf-8") as f:
        f.write(rules_md_content)

    # Note: Modifying the existing root RULES.md to inject the new department
    root_md_path = os.path.join(base_dir, "RULES.md")
    if os.path.exists(root_md_path):
        with open(root_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Simple injection: append to the table
        table_row = f"| {name} | {department_id} | {desc} |\n"
        if "|------|---------|------|" in content:
            content = content.replace("|------|---------|------|", f"|------|---------|------|\n{table_row.strip()}")
            
        with open(root_md_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Successfully added department '{name}' ({department_id}).")

def main():
    parser = argparse.ArgumentParser(description="Company Toolkit for Antigravity")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: setup
    parser_setup = subparsers.add_parser("setup", help="Initialize the company organization")
    parser_setup.add_argument("--business_type", required=True, help="ユーザーの事業・活動の種類")
    parser_setup.add_argument("--goals", required=True, help="目標や課題")

    # Command: add_department
    parser_add = subparsers.add_parser("add_department", help="Add a new department")
    parser_add.add_argument("department_id", help="部署のID (例: pm, research, marketing, engineering)")

    args = parser.parse_args()

    if args.command == "setup":
        setup_company(args.business_type, args.goals)
    elif args.command == "add_department":
        add_department(args.department_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
