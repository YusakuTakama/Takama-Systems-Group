---
name: engineering-task
description: 個人開発プロジェクト（Workout Trackerなど）および研究プロジェクトへのコード修正・機能追加・UI調整・実験スクリプト作成をプロ品質で管理するスキル。「実装して」「バグ直して」「〜を追加したい」「UIを直して」「スクリプト作って」「可視化して」「実験コード書いて」と言われたとき、またはコードの変更を伴う依頼全般に使う。要件定義書の作成→実装→ユーザーレビュー→ドキュメント更新→Gitプッシュのフルライフサイクルを管理する。Engineering（個人開発）とLab（研究）の両部署で使用可能。コードを書く・修正する・追加するという文脈を検出したら、必ずこのスキルを使用すること。小さな変更から大規模なリファクタリングまで、すべてのコード変更タスクに対応する。
---

# Engineering Task Skill（エンジニアリング・タスクスキル）

個人開発プロジェクトおよび研究プロジェクトへのコード改修・機能追加・UI調整・実験スクリプト作成をプロ品質で管理するエンドツーエンドのワークフロー。

---

## 部署による動作の違い

このスキルは Engineering（個人開発）と Lab（研究）の両方で使用可能。
スキルは自動的にプロジェクトパスまたは `README.md` の `department` フィールドから部署を判定し、適切な動作を選択する。

### Engineering（個人開発）の場合

**プロジェクトパス**: `.company/engineering/projects/<project>/`

**重視する点**:
- ユーザビリティ・UX
- パフォーマンス
- エラーハンドリング

**特有の動作**:
- `debug-log/` へのバグ記録（バグ修正の場合）
- ブラウザ検証（オプション、ユーザー要求時）
- E2E テストの推奨

### Lab（研究）の場合

**プロジェクトパス**: `.company/lab/projects/<project>/`

**重視する点**:
- 実験の再現性
- 結果の正確性
- ドキュメンテーション

**特有の動作**:
- `experiments/` への実験ログ記録（実験の場合）
- ハイパーパラメータ・乱数シードの明記
- 可視化スクリプトの充実
- 計算量分析の推奨

---

## Phase 1: 要件定義と承認

ユーザーの依頼を受けたら、まず実装プランを作成し、**合意を得ることを最優先**にする。

### 1.1 プロジェクト情報の確認

ユーザーが「実装して」「バグ直して」などと言ったら、以下を確認する：

```markdown
承知しました！まず、以下の情報を教えてください：

1. **プロジェクト名**: どのプロジェクトに関する作業ですか？（例: workout-tracker, lora-dynamic-separation）
2. **実装内容**: 何を実装・修正しますか？（簡単な説明で OK）
3. **対象ファイル**: 変更が必要なファイルがわかれば教えてください（不明な場合は「わからない」で OK）
```

### 1.2 コンテキスト自動読み込み（内部処理）

プロジェクト名が確定したら、**自動的に以下を読み込む**（ユーザーに見せない内部処理）：

**必須読み込み**:
- `<department>/projects/<project>/README.md` - プロジェクト概要・現在の状況

**オプション（存在すれば）**:
- `<department>/projects/<project>/specs/*.md` - 最新1件（既存要件定義）
- `<department>/projects/<project>/implementation/*.md` - 最新2件（実装履歴）
- `engineering/projects/<project>/debug-log/*.md` - 最新1件（バグ情報、Engineering のみ）
- `lab/projects/<project>/experiments/*.md` - 最新1件（実験結果、Lab のみ）

これらの情報は実装プラン作成時に文脈を理解するために使用する。

### 1.3 タスクの複雑度判定

タスクの規模に応じて、要件定義の詳細度を調整する：

#### 軽量タスク（以下のいずれか）

- UI の微調整（色、サイズ、配置）
- 既存機能の小さなバグ修正
- 既存コードのリファクタリング（機能変更なし）
- 1-2ファイルの変更のみ

→ **簡易プラン**のみ（チャットで確認、ファイル作成なし）

**簡易プランの内容**:
```markdown
## 実装プラン

### ゴール
- [実装のゴール]

### 変更内容
- `file1.ts`: [変更内容]
- `file2.tsx`: [変更内容]

### 影響範囲
- [他機能への影響の有無]

このプランで進めてよろしいですか？
問題なければ「よし、いこう」「実装開始して」などとお知らせください。
```

#### 中規模タスク

- 新機能追加（既存の枠組み内）
- 複数ファイルにまたがる変更（3-5ファイル）
- データ構造の変更

→ **簡易版要件定義書**（5セクション）

**ファイルパス**: `<department>/projects/<project>/specs/<feature>-spec.md`

**フォーマット**:
```markdown
---
feature: <feature-name>
project: <project-name>
department: engineering | lab
created: YYYY-MM-DD
status: planning
---

# <機能名> 要件定義書

## 1. Summary
- 実装のゴール（1-2行）
- 期待される効果

## 2. Requirements
### Functional Requirements (FR)
- [ ] FR1: ...
- [ ] FR2: ...

### Non-Functional Requirements (NFR)
- パフォーマンス要件
- ユーザビリティ要件

## 3. Technical Specification
### 変更対象ファイル
- `src/file1.ts`: 変更内容の説明
- `src/file2.tsx`: 変更内容の説明

### データ構造
- 新規 interface/type の定義

## 4. Implementation Plan
### 実装順序
1. Phase 1: ...
2. Phase 2: ...

### 依存関係
- 前提となる実装
- 他機能への影響

## 5. Success Criteria
- [ ] 完了条件1
- [ ] 完了条件2
```

#### 大規模タスク

- 新しいサブシステムの追加
- アーキテクチャの大幅変更
- 複数のマイルストーンにまたがる実装（6ファイル以上）

→ **完全版要件定義書**（9セクション）

上記の5セクションに加えて：

```markdown
## 6. Background & Motivation
- なぜこの機能が必要か
- 現状の問題点

## 7. Test Strategy
- ユニットテスト
- 統合テスト
- 手動テスト項目

## 8. Risks & Mitigation
- リスク1: 対策
- リスク2: 対策

## 9. Future Enhancements
- 今回は含めないが、将来検討すべき拡張
```

### 1.4 実装プラン/要件定義書の提示と壁打ち

**ユーザーと対話しながらプランを洗練**:
1. 現状調査結果を共有
2. 実装プラン/要件定義書の提示
3. フィードバックとブラッシュアップ
4. ユーザーが「よし、いこう」「実装開始して」など**明示的に許可したときのみ** Phase 2 へ進む

**要件定義書を作成した場合**:
- 要件定義書の `status` を `planning` → `in-progress` に更新してから Phase 2 へ進む

> **Why**: 認識の相違をコードレベルで検証する前に解消することで、手戻りをゼロにする。

---

## Phase 2: 実装

ユーザーの許可を得た後、プランに基づいて実装する。

### 2.1 実装の原則

**Why**: 大きな変更を一度に行うと、問題の切り分けが困難になる。1ファイルずつ、動作確認しながら進めることで、エラーの原因を即座に特定できる。

**実装順序**:
1. 型定義・interface（他ファイルから参照される）
2. ユーティリティ関数・ヘルパー
3. コアロジック
4. UI コンポーネント
5. 統合・エントリーポイント

### 2.2 実装ループ

各ファイルについて、以下を繰り返す：

1. **編集前の確認**: `Read` で現在の内容を把握
2. **編集**: `Edit` ツールで変更を適用
3. **編集後の確認**: `Read` で意図通りに変更されたか確認
4. **TypeScript チェック**（TypeScript プロジェクトの場合）:
   ```bash
   npm run type-check || tsc --noEmit
   ```
   - エラーがあれば即座に修正
   - 修正できない場合は「エラーハンドリング戦略」を参照

5. **開発サーバー確認**（該当する場合）:
   ```bash
   cd "<project_root>" && npm run dev
   ```
   - ターミナルログにエラーがないか確認

### 2.3 研究コード特有の考慮事項（Lab のみ）

**再現性の確保**:
- 乱数シード: `np.random.seed(42)`, `torch.manual_seed(42)`
- ハイパーパラメータ: スクリプトの先頭に明記
- 依存ライブラリ: バージョンをコメントで記録

**ログ出力**:
- 実験の進捗（epoch, loss, metrics）
- 中間結果の保存（チェックポイント）
- 可視化の自動生成

**例**:
```python
# Hyperparameters
LEARNING_RATE = 0.001  # 学習率
BATCH_SIZE = 32        # バッチサイズ
NUM_EPOCHS = 100       # エポック数
SEED = 42              # 乱数シード

# Set random seed for reproducibility
np.random.seed(SEED)
torch.manual_seed(SEED)

# Log experimental settings
print(f"Experiment: {datetime.now()}")
print(f"LR={LEARNING_RATE}, BS={BATCH_SIZE}, EPOCHS={NUM_EPOCHS}")
```

---

## Phase 3: ユーザー確認と修正

実装完了後、**まずユーザーに結果を報告し、動作確認を依頼する**。

### 3.1 実装完了の報告

実装完了後、以下の形式で報告:

```markdown
実装が完了しました！

### 変更内容
- `file1.ts`: 変更内容の説明
- `file2.tsx`: 変更内容の説明

### 動作確認のお願い

（要件定義書がある場合）
以下の Success Criteria を確認してください：

- [ ] 完了条件1
- [ ] 完了条件2
- [ ] 完了条件3

動作確認後、フィードバックをお願いします：
- 問題なければ「OK」「完璧」など
- 修正が必要なら具体的な指摘をお願いします
```

### 3.2 フィードバックへの対応

- 「ここが動かない」「ここをもう少し直して」などのフィードバックを受ける
- 指摘がある場合は Phase 2 に戻り修正する
- **「OK」「これで大丈夫」「完璧」など、明示的な承認を得るまで Phase 4 以降へ進まない**

> 一度の実装で完璧に仕上がることは稀という前提で、対話を通じてクオリティを磨き上げるフェーズ。

### 3.3 Success Criteria の最終確認（要件定義書がある場合）

ユーザー承認後、Success Criteria を再確認:

```markdown
以下の Success Criteria をすべて達成しましたか？

- [ ] 完了条件1
- [ ] 完了条件2
- [ ] 完了条件3

達成していない項目がある場合は、追加実装が必要かもしれません。
すべて達成している場合は「はい」とお知らせください。
```

**Why**: 要件定義書で定義した Success Criteria との乖離を防ぐため、実装完了前に明示的に確認する。

---

## Phase 4: ブラウザ検証（原則スキップ）

**このフェーズは原則スキップ。** ユーザーから「ブラウザで確認して」「動作させてみて」と明示的な指示があった場合のみ、`Agent` (Playwright) を起動する。

実行する場合のチェックリスト:

```
[ ] 実装した機能が期待通りに動作するか
[ ] スタイルが他の要素と視覚的に調和しているか
[ ] スマートフォンサイズ（375x667）で表示が崩れていないか
[ ] エッジケース（リストの端、空の状態）で問題がないか
```

---

## Phase 5: ドキュメント更新

**ユーザーの承認（Phase 3）を得た後**、以下を順番に実行する：

### 5.1 要件定義書の完了マーク（要件定義書がある場合）

**ファイル**: `<department>/projects/<project>/specs/<feature>-spec.md`

**更新内容**:
- `status: in-progress` → `status: completed`
- Success Criteria の各項目を `[x]` にマーク

### 5.2 実装完了報告の作成（必須）

**ファイル**: `<department>/projects/<project>/implementation/<feature>-report.md`

**フォーマット**:
```markdown
# <機能名> 実装完了報告

## 実装概要
- 実装した機能の説明
- 要件定義書へのリンク（ある場合）: [<feature>-spec.md](../specs/<feature>-spec.md)

## 技術的改善点
- 使用した技術・ライブラリ
- 設計の意図
- パフォーマンス最適化

## 実装の詳細
### 変更ファイル一覧
- `src/file1.ts`: 変更内容
- `src/file2.tsx`: 変更内容

### 技術的な課題と解決策
- 課題1: 解決方法
- 課題2: 解決方法

## テスト結果
- 実施したテスト
- 結果

## 次のステップ
- 残タスク
- 今後の改善案
```

### 5.3 デバッグログ（条件付き: バグ修正の場合のみ、Engineering のみ）

**条件**: タスクが「バグ修正」の場合のみ実行

**ファイル**: `engineering/projects/<project>/debug-log/YYYY-MM-DD-issue.md`

**フォーマット**:
```markdown
# <バグタイトル>

## 症状
- バグの説明

## 期待する動作
- 正しい動作

## 再現手順
1. ...

## 仮説
- 原因の推測

## 解決方法（YYYY-MM-DD 追記）
- 実施した修正内容

## 再発防止策
- テストの追加
- コードレビューポイント
```

### 5.4 プロジェクト管理の更新（必須）

**README.md frontmatter 更新**:

ファイル: `<department>/projects/<project>/README.md`

```yaml
---
project: project-name
status: in-progress
department: engineering | lab
summary: 現在の状況を1行で更新（実装した機能を反映）
created: YYYY-MM-DD
last_updated: YYYY-MM-DD  # 今日の日付に更新
---
```

**マイルストーンの更新**:

README.md の「## マイルストーン」セクション:
- 該当タスクを `[x]` にマーク
- 新しいタスクが発生した場合は追加

**注意**: 既存のマイルストーンを上書きせず、新しいタスクを追加する形で更新する。

### 5.5 秘書室への記録（推奨、ユーザー確認）

**ユーザーに確認してから実行**:

```markdown
秘書室への記録を行いますか？

**意思決定ログ** (`secretary/notes/YYYY-MM-DD-decisions.md`):
- 今回の実装で選択した技術・設計の意図

**学びの記録** (`secretary/notes/YYYY-MM-DD-learnings.md`):
- 実装中に得た知見・ハマりどころ

記録する場合は「はい」、スキップする場合は「いいえ」とお知らせください。
```

ユーザーが「はい」と答えた場合のみ、以下を記録:

**意思決定ログ**: `secretary/notes/YYYY-MM-DD-decisions.md`
```markdown
## <機能名> 実装の意思決定（YYYY-MM-DD）

- 技術選択: [使用した技術・ライブラリとその理由]
- 設計の意図: [なぜこの設計にしたか]
- トレードオフ: [選択しなかった代替案と理由]
```

**学びの記録**: `secretary/notes/YYYY-MM-DD-learnings.md`
```markdown
## <機能名> 実装から得た学び（YYYY-MM-DD）

- ハマったポイント: [問題の説明]
- 解決方法: [どうやって解決したか]
- 今後に活かせる知見: [次回以降に役立つこと]
```

---

## Phase 6: Git Push

ユーザーから「push して」という指示を受けた場合のみ実行する:

```bash
git -C "<absolute_project_root>" add .
git -C "<absolute_project_root>" commit -m "<type>: <summary of changes>"
git -C "<absolute_project_root>" push
```

> ワークスペース外（OneDrive等）で絶対パスが拒否される場合は相対パス（`../〜`）で迂回する。

---

## エラーハンドリング戦略

### TypeScript エラーの対処

**レベル1: 自動修正可能**
- 型アノテーションの追加
- import 文の修正
- 簡単な型キャストの追加

→ 即座に修正して進行

**レベル2: ユーザー判断が必要**
- 型定義の変更が必要
- リファクタリングが必要
- 外部ライブラリの型定義が不足

→ ユーザーに報告し、以下を選択してもらう:
```markdown
TypeScript エラーが発生しました：

[エラーの内容]

以下の選択肢があります：
1. 一旦 `@ts-ignore` でスキップして先に進む
2. 今すぐ修正する（Phase 2 に戻る）
3. 実装を中断して要件を見直す（Phase 1 に戻る）

どうしますか？
```

**レベル3: 致命的エラー**
- ビルドが完全に失敗
- 開発サーバーが起動しない

→ **実装を停止**し、Phase 1 に戻って要件を再検討

### 実装中の問題発覚

実装中に「要件定義書に書かれていない問題」が発覚した場合:

1. **実装を一旦停止**
2. **問題を報告**:
   ```markdown
   実装中に以下の問題が発覚しました：

   [問題の説明]

   以下の選択肢があります：
   1. 要件定義書を更新して実装を続ける
   2. 今回は対処せず、Future Enhancements に記録
   3. 実装アプローチを変更する

   どうしますか？
   ```
3. **ユーザーの指示を待つ**

---

## ベストプラクティス

### Single Source of Truth の維持

- README.md の frontmatter が進捗管理の SSOT
- 要件定義書が技術仕様の SSOT
- 同じ情報を複数箇所に書かない

### コンテキスト読み込みの重要性

- 既存の specs/ や README.md を必ず参照
- 過去の実装履歴から学ぶ
- 同じ過ちを繰り返さない

### 研究と開発の違い

**Lab（研究）**:
- 実験の再現性を重視
- experiments/ に実験ログを記録
- ハイパーパラメータ・乱数シードを明記
- 可視化スクリプトの充実

**Engineering（開発）**:
- ユーザビリティを重視
- debug-log/ にバグ記録
- E2E テストの充実
- パフォーマンス最適化

---

## 参照ファイル

プロジェクト固有の詳細は以下を参照:

**Engineering（個人開発）**:
- プロジェクト概要: `.company/engineering/projects/<project>/README.md`
- 要件定義書: `.company/engineering/projects/<project>/specs/`
- 実装報告: `.company/engineering/projects/<project>/implementation/`
- デバッグログ: `.company/engineering/projects/<project>/debug-log/`

**Lab（研究）**:
- プロジェクト概要: `.company/lab/projects/<project>/README.md`
- 要件定義書: `.company/lab/projects/<project>/specs/`
- 実装報告: `.company/lab/projects/<project>/implementation/`
- 実験ログ: `.company/lab/projects/<project>/experiments/`
