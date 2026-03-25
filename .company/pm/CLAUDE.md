# PM（プロジェクト管理）

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

## プロジェクトファイルの必須frontmatter
全プロジェクトファイルの先頭に以下のYAML frontmatterを必ず付けること:
```yaml
---
project: project-name
status: planning | in-progress | review | completed | archived
department: lab | engineering | secretary | research | ...
summary: ダッシュボードに表示する1行の現在状況（日本語）
created: YYYY-MM-DD
---
```
- **`summary` は進捗が変わるたびに必ず更新すること**（ダッシュボードのSingle Source of Truth）
- `department` はどの部署が主担当かを示す


## フォルダ構成
- `projects/` - プロジェクト管理（1プロジェクト1ファイル）
- `tickets/` - タスクチケット（1チケット1ファイル）
