# .company/ フォルダ構造再編成 - 移行完了報告

**実施日**: 2026-03-27
**バックアップ**: `.company.backup.2026-03-27/`

---

## 🎯 移行の目的

1. **情報の一元化**: 研究プロジェクトの情報が PM/Lab/Secretary の3箇所に分散していた問題を解消
2. **要件定義の正式な置き場を確立**: specs/ フォルダを新設
3. **企業レベルの要件定義テンプレートを導入**: 14セクションの本格的なテンプレート
4. **秘書が研究コンテキストを活用できるルールを追加**: 研究相談時のワークフロー確立

---

## 📂 新しいフォルダ構造

### Before（問題のあった構造）
```
.company/
├── pm/                    ← プロジェクト管理
│   └── projects/
├── lab/                   ← 研究ノート・実験
│   ├── notes/
│   ├── experiments/
│   └── meeting-logs/
├── secretary/             ← 壁打ち・TODO
│   └── notes/
├── engineering/
│   └── docs/
└── research/              ← ほぼ未使用
```

**問題点**:
- 同じプロジェクトの情報が3箇所（PM/Lab/Secretary）に分散
- 要件定義の置き場が不明確
- MTGの生データとサマリーが別フォルダ
- 秘書が研究コンテキストを活用できない

### After（新しい構造）
```
.company/
├── CLAUDE.md              ← 組織全体のルール（更新済み）
├── templates/             ← テンプレート集（新設）
│   └── requirements-spec-template.md
├── secretary/
│   ├── CLAUDE.md          ← 研究相談ワークフロー追加
│   ├── inbox/
│   ├── todos/
│   └── notes/
│       └── brainstorm/    ← 壁打ち専用（新設）
├── lab/
│   ├── CLAUDE.md          ← プロジェクト管理ルール追加
│   ├── figures/
│   └── projects/          ← プロジェクトごとに1フォルダ（新設）
│       └── lora-dynamic-separation/
│           ├── README.md        # PM情報を統合
│           ├── specs/           # 要件定義書
│           ├── experiments/     # 実験ログ
│           ├── meetings/        # MTG記録（統合）
│           └── implementation/  # 実装報告
└── engineering/
    └── projects/          ← プロジェクトごとに1フォルダ（新設）
        └── workout-tracker/
            ├── README.md
            ├── specs/
            ├── implementation/
            └── debug-log/
```

---

## ✅ 実施した作業

### 1. バックアップ
- `.company/` 全体を `.company.backup.2026-03-27/` にコピー

### 2. Lab の再構築
- `lab/projects/lora-dynamic-separation/` フォルダ作成
- PM の frontmatter + Lab notes を統合した `README.md` を作成
- 既存ファイルを新構造に移動:
  - `experiments/` → `projects/lora-dynamic-separation/experiments/`
  - `meeting-logs/` → `projects/lora-dynamic-separation/meetings/`
  - `lab/figures/heatmap-implementation-spec.md` → `projects/lora-dynamic-separation/specs/`
  - `secretary/notes/*lora-viz*.md` → `projects/lora-dynamic-separation/specs/` または `implementation/`

### 3. Secretary の整理
- `secretary/notes/brainstorm/` フォルダ作成
- 研究相談時のワークフロー（コンテキスト読み込み → 壁打ち → 昇格確認）を CLAUDE.md に追加

### 4. Engineering の整備
- `engineering/projects/workout-tracker/` フォルダ作成
- `docs/` の内容を `projects/workout-tracker/` に移動

### 5. 企業レベルテンプレート作成
- `.company/templates/requirements-spec-template.md` を作成
- 14セクション（Executive Summary、Background、Requirements、Technical Spec、Design Decisions、Implementation Plan、Success Criteria、Risks、Validation、Future Enhancements、References、Change Log、Approval）

### 6. CLAUDE.md の更新
- `.company/CLAUDE.md`: PM削除、Research削除、プロジェクト粒度ルール追加
- `lab/CLAUDE.md`: 新構造の説明、プロジェクト管理ルール
- `secretary/CLAUDE.md`: 研究相談ワークフロー
- `engineering/CLAUDE.md`: 新構造に対応

### 7. PM/Research 部署の削除
- `pm/` → `.company/_archive/pm/` に移動
- `research/` → 削除（CLAUDE.mdのみだったため）

### 8. 古いフォルダをアーカイブ
- `lab/notes/` → `lab/_archive/notes/`
- `lab/experiments/` → `lab/_archive/experiments/`
- `lab/meeting-logs/` → `lab/_archive/meeting-logs/`
- `engineering/docs/` → `engineering/_archive/docs/`

---

## 🎉 期待される効果

### 1. 情報の一元化
- 研究プロジェクトの情報が1箇所（`lab/projects/lora-dynamic-separation/`）に集約
- 「どこを見ればいいか」が明確

### 2. 要件定義が正式なドキュメントに
- `specs/` フォルダで企業レベルの品質管理
- 壁打ち（一時）→ specs（永続）の明確な昇格フロー

### 3. 秘書の活用強化
- 研究相談時に既存研究を自動的に読み込む
- 既存のMTG・実験を踏まえた提案が可能

### 4. 検索性の向上
- プロジェクトフォルダ内で完結
- 関連ドキュメント（MTG、実験、要件定義）が同じ場所

### 5. スケーラビリティ
- 新しいプロジェクトを追加しやすい
- Lab も Engineering も同じプロジェクト管理方式

---

## 📋 プロジェクトの粒度（新ルール）

### プロジェクトとして独立させる条件（いずれか1つ以上）
- 単体で論文1本書けるレベルの独立性がある
- 他の研究でも再利用される汎用ツール/ライブラリになる
- 別ドメイン（RL、NLPなど）への応用研究になる
- 期間が2ヶ月以上、独立した進捗管理が必要

### サブタスク/マイルストーンとして管理する条件
- 親プロジェクトのゴール達成のための手段・実験・分析
- 同じMTGから派生した関連タスク
- 親プロジェクトと成果を共有する（例: 同じ論文に含まれる）

### 運用方針
- 最初は親プロジェクト内で管理（`specs/`, `experiments/`, `implementation/`）
- 独立性が明確になったら、その時点で切り出す

**例**: ヒートマップ可視化、ベクトル化指標、非直交分離手法の調査は、すべて「LoRA動的分離」プロジェクトのサブタスクとして管理。汎用ツール化や別論文テーマになったら独立。

---

## 🔧 秘書の新しいワークフロー

### 研究相談時の動作

#### 1. コンテキスト読み込み
- `lab/projects/` 配下の関連プロジェクトの `README.md`
- 最新の `meetings/*.md`（直近2件）
- 最新の `experiments/*.md`（直近1件）
- 既存の `specs/*.md`（重複チェック）

#### 2. 壁打ち（一時保存）
- 場所: `secretary/notes/brainstorm/YYYY-MM-DD-topic.md`
- テンプレートに沿って対話的に情報収集

#### 3. 昇格確認
```
「要件定義が固まりましたね。
 Lab に正式な要件定義書として保存しますか？

 保存先: lab/projects/<project>/specs/<topic>-spec.md

 - 「保存して」→ テンプレートで整形して保存
 - 「もう少し詰める」→ 壁打ち継続
 - 「いらない」→ Secretary に残すのみ」
```

#### 4. テンプレート整形
企業レベルの要件定義テンプレートに自動整形

#### 5. 昇格リンク追記
壁打ちメモに「✅ Lab に昇格」のリンクを追記

---

## 🗂 アーカイブされたファイル

### `.company/_archive/pm/`
- プロジェクト管理ファイル（Lab の README.md に統合済み）
- チケット（Workout Tracker 用、参照可能）

### `lab/_archive/`
- 旧 `notes/`（プロジェクトに統合済み）
- 旧 `experiments/`（プロジェクトに統合済み）
- 旧 `meeting-logs/`（プロジェクトに統合済み）

### `engineering/_archive/`
- 旧 `docs/`（プロジェクトに統合済み）

---

## ⚠️ 注意事項

### バックアップからの復元方法
問題があった場合:
```bash
cd /mnt/HDD18TB/takama/Takama-Systems-Group
rm -rf .company
cp -r .company.backup.2026-03-27 .company
```

### 既存のリンク
- 一部のファイルで古いパス（`pm/projects/`, `lab/notes/`）を参照している可能性がある
- 発見次第、新しいパス（`lab/projects/*/README.md`, `lab/projects/*/specs/`）に更新

---

## 📊 統計

| 項目 | Before | After |
|------|--------|-------|
| 部署数 | 5（Lab, Engineering, PM, Research, Secretary） | 3（Lab, Engineering, Secretary） |
| プロジェクト管理方式 | 分散（PM/Lab/Secretary） | 統一（projects/ 配下） |
| 要件定義の場所 | 不明確 | specs/ フォルダ |
| テンプレート | なし | 企業レベル（14セクション） |
| 秘書の研究理解 | 記憶頼り | 自動的にコンテキスト読み込み |

---

## ✅ 次のステップ

1. **新しい構造での運用開始**
   - 次の研究相談から新しいワークフローを試す
   - 要件定義を `specs/` に保存してみる

2. **ダッシュボードの動作確認**
   - `lab/projects/*/README.md` の frontmatter が正しく読み込まれるか確認

3. **フィードバック収集**
   - 使いにくい点があれば随時改善

4. **アーカイブの整理**
   - 数週間後、問題がなければ `_archive/` を削除検討

---

## 🎓 学んだこと

1. **Single Source of Truth の重要性**
   - 同じ情報を複数箇所に書くと必ず同期漏れが起きる

2. **壁打ち（一時）と正式ドキュメント（永続）の分離**
   - 考えながら書く場所と、後で読む場所は分けるべき

3. **プロジェクト粒度の基準**
   - 最初から分けすぎない。必要になったら切り出す

4. **テンプレートの威力**
   - 企業レベルのテンプレートがあれば、品質が自然に保たれる

---

**移行実施者**: ユーザー + 秘書
**所要時間**: 約1時間
**状態**: ✅ 完了
