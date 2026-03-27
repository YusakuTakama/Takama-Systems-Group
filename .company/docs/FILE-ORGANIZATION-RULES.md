# ファイル保存ルール一覧

> **最終更新**: 2026-03-27
> **目的**: どのファイルをどこに保存するかの判断基準を明確にする

---

## 📋 クイックリファレンス

| 何を保存するか | 保存先 | 例 |
|--------------|--------|-----|
| 日々のTODO | `secretary/todos/YYYY-MM-DD.md` | 今日やること・期限付きタスク |
| クイックメモ・アイデア | `secretary/inbox/` | 「後で整理する」メモ |
| 意思決定ログ | `secretary/notes/YYYY-MM-DD-decisions.md` | 「〇〇を△△にすることに決めた」 |
| 学び・気づき | `secretary/notes/YYYY-MM-DD-learnings.md` | 「〇〇を試したら△△だった」 |
| 壁打ち（一時） | `secretary/notes/brainstorm/YYYY-MM-DD-topic.md` | 要件を考え中、相談中 |
| 研究の要件定義 | `lab/projects/<project>/specs/<topic>-spec.md` | ヒートマップ可視化の仕様 |
| 実験ログ | `lab/projects/<project>/experiments/<experiment>.md` | Dual Optimizer実験の記録 |
| MTG記録 | `lab/projects/<project>/meetings/YYYY-MM-DD-mtg.md` | 教授MTGの議事録 |
| 実装完了報告 | `lab/projects/<project>/implementation/<feature>-report.md` | LoRA可視化v2.0完成報告 |
| 個人開発の要件定義 | `engineering/projects/<project>/specs/<feature>-spec.md` | Workout Trackerの仕様 |
| デバッグログ | `engineering/projects/<project>/debug-log/YYYY-MM-DD-issue.md` | バグ調査の記録 |
| 組織全体のドキュメント | `.company/docs/` | 移行レポート、セットアップガイド |

---

## 🗂 フォルダ別詳細ルール

### 1. Secretary（秘書室）

#### `secretary/todos/`
**いつ使う**: 日々のタスク管理

**ルール**:
- ファイル名: `YYYY-MM-DD.md`（1日1ファイル）
- 同じ日付のファイルがあれば追記、なければ新規作成
- TODO形式: `- [ ] タスク内容 | 優先度: 高/通常/低 | 期限: YYYY-MM-DD`
- 完了時: `- [x] タスク内容 | 完了: YYYY-MM-DD`

**例**:
```markdown
## 最優先
- [ ] 評価指標のベクトル化 | 優先度: 最優先 | 期限: 2026-03-30

## 通常
- [ ] 可視化システムの運用テスト | 優先度: 通常

## 完了
- [x] LoRA可視化v2.0の実装 | 完了: 2026-03-27
```

---

#### `secretary/inbox/`
**いつ使う**: 迷ったらここ。クイックキャプチャ。

**ルール**:
- 未整理のメモ・アイデア・リンク・スクラップ
- 後で整理する前提の一時置き場
- タイムスタンプ付きで追記

**例**:
```markdown
## 2026-03-27 15:30
- 〇〇という論文を見つけた。後で読む。
- △△のアイデアを思いついた。

## 2026-03-27 20:00
- □□の調査結果をメモ。
```

---

#### `secretary/notes/`

##### サブフォルダ: `brainstorm/`
**いつ使う**: 研究相談・要件定義の壁打ち中

**ルール**:
- ファイル名: `YYYY-MM-DD-topic.md`
- 一時的なドキュメント
- 固まったら `lab/projects/<project>/specs/` に昇格
- 昇格後、元ファイルに「✅ Lab に昇格」のリンクを追記

**例**:
```markdown
# ヒートマップ可視化 要件定義（壁打ち中）

## 背景
- 加重コーダル距離では個別成分が見えない

（... 対話を続ける ...）

---

**✅ 2026-03-26: Lab に昇格**
→ [lab/projects/lora-dynamic-separation/specs/heatmap-visualization-spec.md]
```

##### その他のファイル
**いつ使う**: 意思決定・学びを記録

**ルール**:
- **意思決定**: `YYYY-MM-DD-decisions.md`
  - 「〇〇を△△にすることに決めた」
  - 判断理由も記録
- **学び**: `YYYY-MM-DD-learnings.md`
  - 「〇〇を試したら△△だった」
  - 気づき・教訓
- 同じ日付のファイルがあれば追記

**例（decisions）**:
```markdown
# 2026-03-27 意思決定ログ

## PM部署を廃止して Lab に統合
- **理由**: 研究プロジェクトの情報が3箇所に分散していた
- **効果**: Single Source of Truth を実現
```

---

### 2. Lab（研究所）

#### `lab/projects/<project-name>/`
**いつ使う**: 研究プロジェクトごとに1フォルダ

**ルール**:
- プロジェクト名: kebab-case（例: `lora-dynamic-separation`）
- 必須ファイル: `README.md`（プロジェクト概要 + frontmatter）

---

#### `lab/projects/<project>/README.md`
**いつ使う**: プロジェクトの概要・進捗を管理

**必須 frontmatter**:
```yaml
---
project: project-name
status: planning | in-progress | review | completed | archived
department: lab
summary: ダッシュボードに表示する1行の現在状況（日本語）
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

**含めるべき内容**:
- プロジェクト概要
- ゴール
- マイルストーン（チェックリスト形式）
- 実験結果サマリー
- 関連リンク

---

#### `lab/projects/<project>/specs/`
**いつ使う**: 要件定義書を保存

**ルール**:
- ファイル名: `<topic>-spec.md`（例: `heatmap-visualization-spec.md`）
- **企業レベルのテンプレート**（`.company/templates/requirements-spec-template.md`）を使用
- 壁打ち（`secretary/notes/brainstorm/`）から昇格したもの

**14セクション**:
1. Executive Summary
2. Background & Motivation
3. Requirements (FR/NFR)
4. Technical Specification
5. Design Decisions
6. Implementation Plan
7. Success Criteria
8. Dependencies & Prerequisites
9. Risks & Mitigation
10. Validation & Testing
11. Future Enhancements
12. References
13. Change Log
14. Approval

---

#### `lab/projects/<project>/experiments/`
**いつ使う**: 実験ログを記録

**ルール**:
- ファイル名: `<experiment-name>-log.md`（例: `dual-optimizer-log.md`）
- 実験の目的、手法、結果、考察を記録
- 再現可能な形で記述（ハイパーパラメータ、コマンド等）

**例**:
```markdown
# Dual Optimizer 実験ログ

## 目的
L_ce と L_orth を別々の Optimizer で更新する効果を検証

## 手法
- η_ce = 0.0005
- η_orth = 0.001
- ...

## 結果
- 直交性指標: 0.9999（1.0に届かず）
- ...

## 考察
...
```

---

#### `lab/projects/<project>/meetings/`
**いつ使う**: MTG記録を保存

**ルール**:
- ファイル名: `YYYY-MM-DD-mtg.md`
- 生データ + サマリーを1ファイルに統合
- 専用スキル `/meeting-minutes` で自動生成

**含めるべき内容**:
- 日時・参加者
- ディスカッション内容
- 決定事項
- アクションアイテム（TODO）

---

#### `lab/projects/<project>/implementation/`
**いつ使う**: 実装完了報告を保存

**ルール**:
- ファイル名: `<feature>-report.md`（例: `lora-viz-v2-report.md`）
- 実装した機能、技術的改善、次のステップを記録

**例**:
```markdown
# LoRA可視化ツールキット v2.0 実装完了報告

## 実装概要
- マルチビューヒートマップ生成
- トグル機能
- バッチ処理システム

## 技術的改善点
...

## 次のステップ
...
```

---

### 3. Engineering（個人開発）

#### `engineering/projects/<project-name>/`
**いつ使う**: 個人開発プロジェクトごとに1フォルダ

**構造は Lab と同じ**:
- `README.md`: プロジェクト概要（frontmatter含む）
- `specs/`: 要件定義書
- `implementation/`: 実装報告
- `debug-log/`: デバッグログ（Engineering 特有）

---

#### `engineering/projects/<project>/debug-log/`
**いつ使う**: バグ調査・デバッグ記録

**ルール**:
- ファイル名: `YYYY-MM-DD-issue.md`
- フォーマット:
  - 症状
  - 期待する動作
  - 再現手順
  - 仮説
  - 解決方法（解決後に追記）
  - 再発防止策（解決後に追記）

**例**:
```markdown
# ログイン機能のバグ調査

## 症状
- ユーザーがログインできない

## 期待する動作
- 正しいパスワードでログインできる

## 再現手順
1. ...

## 仮説
- セッション管理の問題？

## 解決方法（2026-03-27追記）
- Cookie の SameSite 属性を Lax に変更

## 再発防止策
- E2E テストを追加
```

---

### 4. その他のフォルダ

#### `.company/docs/`
**いつ使う**: 組織全体のドキュメント

**保存するもの**:
- 移行レポート
- セットアップガイド
- このファイル（FILE-ORGANIZATION-RULES.md）

---

#### `.company/templates/`
**いつ使う**: テンプレート集

**保存するもの**:
- `requirements-spec-template.md`: 要件定義のテンプレート
- 今後追加されるテンプレート

---

## 🔄 判断フロー

### 「これどこに保存する？」と迷ったら

```
START
  ↓
┌─────────────────────┐
│ 研究関連？          │ YES → lab/projects/<project>/
└─────────────────────┘
  ↓ NO
┌─────────────────────┐
│ 個人開発関連？      │ YES → engineering/projects/<project>/
└─────────────────────┘
  ↓ NO
┌─────────────────────┐
│ TODO・タスク？      │ YES → secretary/todos/YYYY-MM-DD.md
└─────────────────────┘
  ↓ NO
┌─────────────────────┐
│ 意思決定・学び？    │ YES → secretary/notes/YYYY-MM-DD-decisions.md
│                     │       または YYYY-MM-DD-learnings.md
└─────────────────────┘
  ↓ NO
┌─────────────────────┐
│ 迷ったら            │ → secretary/inbox/
└─────────────────────┘
```

---

## 🚫 やってはいけないこと

1. **同じ情報を複数箇所に書かない**
   - ❌ PM と Lab と Secretary に同じタスクを書く
   - ✅ Single Source of Truth（1箇所に集約）

2. **同じ日付のファイルを複数作らない**
   - ❌ `2026-03-27.md` を新規作成
   - ✅ 既存の `2026-03-27.md` に追記

3. **古い日付のファイルに書き込まない**
   - ❌ 今日は3月27日なのに `2026-03-26.md` に書く
   - ✅ 必ず今日の日付を確認してから書き込む

4. **既存ファイルを上書きしない**
   - ❌ 既存ファイルの内容を削除して新しく書く
   - ✅ 追記する（タイムスタンプ付き）

---

## 📌 まとめ

| フォルダ | 用途 | 一時的 or 永続的 |
|---------|------|-----------------|
| `secretary/todos/` | 日々のタスク | 一時的（完了したら過去のもの） |
| `secretary/inbox/` | クイックメモ | 一時的（後で整理する） |
| `secretary/notes/brainstorm/` | 壁打ち | 一時的（Labに昇格する） |
| `secretary/notes/` (その他) | 意思決定・学び | 永続的（記録として残す） |
| `lab/projects/*/specs/` | 要件定義 | 永続的（正式ドキュメント） |
| `lab/projects/*/experiments/` | 実験ログ | 永続的（研究記録） |
| `lab/projects/*/meetings/` | MTG記録 | 永続的（議事録） |
| `lab/projects/*/implementation/` | 実装報告 | 永続的（完成記録） |
| `engineering/projects/*/debug-log/` | デバッグログ | 永続的（再発防止のため） |

---

**原則**: 迷ったら `secretary/inbox/`。後で秘書が整理します。