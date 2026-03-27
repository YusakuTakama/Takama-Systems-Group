# 2026-03-26 意思決定ログ

## Claude Code スキル整備

### 決定事項

1. **`.claude/skills/` を Single Source of Truth にする**
   - `meeting-minutes` と `engineering-task` の本体を `.claude/skills/` に配置
   - Antigravity側（`.agents/skills/`）はdescription + `Read .claude/skills/<name>/SKILL.md` の1行のみ
   - 今後スキルを更新・追加するときは `.claude/skills/` だけ編集すればよい

2. **skill-creator は `example-skills:skill-creator` を使い続ける**
   - Antigravity用の skill-creator スキルは作らない

3. **新スキル作成時のルール**
   - `.claude/skills/<name>/SKILL.md` に本体を書く（Claude Code ツール名: Read, Edit, Bash等）
   - `.agents/skills/<name>/SKILL.md` にはdescription + インクルード1行だけ
   - Claude Code専用機能（Agentサブエージェント等）を使う場合のみ例外扱い

### 背景・理由

- AntigravityとClaude Codeでツール名が異なる（`view_file` → `Read` 等）
- `.company/CLAUDE.md` はClaude Code起動時に自動ロードされないため、`/company` を毎会話最初に呼ぶことで解消
- プロジェクトスコープのスキルは `.claude/skills/` に置くと `/plugin install` 不要で自動認識される

### 作成・変更したファイル

- `.claude/skills/meeting-minutes/SKILL.md` （新規作成）
- `.claude/skills/engineering-task/SKILL.md` （新規作成）
- `.agents/skills/meeting-minutes/SKILL.md` （インクルード方式に変更）
- `.agents/skills/engineering-task/SKILL.md` （インクルード方式に変更）

---

## LoRA研究: ヒートマップ可視化の実装方針

### 背景
- TODO 1番目のタスク「ヒートマップ可視化の実装」に着手
- 壁打ちで実装方針を固め、ユーザーと対話しながら仕様を確定

### 決定事項

#### 1. ディレクトリ構造
- **研究プロジェクト側**: `analyze_weighted_chordal/` → `analysis/` にリネーム
  - 理由: 加重コーダル距離以外の分析（ヒートマップ等）も含むため、より汎用的な名前に
- **画像保存先**: 2箇所管理方式を採用
  - `/mnt/HDD18TB/takama/2025_10_takama_Proj_CL/figures/heatmaps/`
  - `/mnt/HDD18TB/takama/Takama-Systems-Group/.company/lab/figures/heatmaps/`
  - 理由: `notion-imports/` と同様の構造。研究プロジェクトで独立管理しつつ、`.company/` でも参照可能

#### 2. ヒートマップの仕様確認
- **入力**: B_1, B_2（2つのタスクのLoRA重み行列）
- **処理**: SVDで列空間の基底ベクトルを抽出 → 全ペアの角度を計算
- **出力**: k×k のヒートマップ
  - 軸ラベル: 「Task1_σ1」= タスク1の第1特異値に対応する基底ベクトル
  - 対角（同順位）が赤 → 重要成分が分離 ✅
  - 非対角（異順位）が青 → 期待通り ✅

#### 3. 実装内容
- **新規ノートブック**: `analysis/lora_heatmap_visualization.ipynb`
  - 基本関数: `extract_basis_vectors()`, `compute_angle_matrix()`, `plot_heatmap()`
  - 両方の場所に保存する関数: `save_figure_both_locations()`
  - テストデータでの動作確認セクション付き
- **ドキュメント更新**: `.company/lab/CLAUDE.md` にフォルダ構成を追記

### 次のステップ
1. ノートブックを実行してテストデータで動作確認
2. チェックポイントの保存場所を特定
3. 実験データ（Dual Optimizer / λブースト）で可視化

### 参考資料
- 壁打ちメモ: `secretary/notes/2026-03-26-heatmap-brainstorm.md`
- 実装ノートブック: `/mnt/HDD18TB/takama/2025_10_takama_Proj_CL/analysis/lora_heatmap_visualization.ipynb`

---

## LoRA研究: ヒートマップ可視化の改良（微細な違いの可視化）

### 背景
- 初回実装後、実験データで実行したところ、すべて「90.0度」と表示される
- 実際には 89.902度、89.845度など微妙に異なるが、カラーマップ範囲（0〜90度）と小数点1桁表示により違いが見えない

### 問題点
1. **カラーマップ範囲が広すぎる**
   - 0〜90度の全範囲を表示
   - 89度台の微細な違い（0.1〜0.3度）が色で判別できない

2. **小数点桁数が固定**
   - `fmt=".1f"` により、すべて「90.0」と表示される
   - 89.902度 → 90.0度、89.712度 → 89.7度 のように丸められる

3. **統計情報が不足**
   - 対角成分と非対角成分の違いが数値で分からない
   - 分離の程度を定量的に評価できない

### 決定事項

#### 1. カラーマップ範囲の動的調整
- 角度の実際の範囲に応じて `vmin`, `vmax` を自動計算
- **範囲 < 5度の場合**: 拡大表示（例: 88.7度〜90.0度）
- **範囲 ≥ 5度の場合**: 従来通り 0〜90度
- `auto_range=True` パラメータで制御（デフォルト: True）

#### 2. 小数点桁数の動的調整
- **範囲 < 1度**: `fmt=".3f"`（小数点3桁）
- **範囲 < 5度**: `fmt=".2f"`（小数点2桁）
- **それ以外**: `fmt=".1f"`（従来通り）

#### 3. 統計情報の自動出力
`plot_heatmap()` 実行時に自動で以下を出力：
```
📊 角度統計:
  最小値: XX.XXX°
  最大値: XX.XXX°
  範囲: X.XXX°
  対角成分の平均: XX.XXX° (std: X.XXX°)
  非対角成分の平均: XX.XXX° (std: X.XXX°)
🎨 カラーマップ範囲を自動調整: XX.X° 〜 XX.X°
```

#### 4. 追加の可視化機能
**相対角度ヒートマップ** (`plot_relative_heatmap()`):
- 最小値を0として差分を可視化
- カラーマップ: `viridis`（0からの差分用）
- 微細な違いを強調

**角度分布のヒストグラム** (`plot_angle_distribution()`):
- 対角成分 vs 非対角成分の分布を並べて表示
- ヒストグラムと箱ひげ図の両方
- 分離の程度を視覚的に確認

### 実装内容

#### 変更したファイル
- `analysis/lora_heatmap_visualization.ipynb`
  - セル7: `plot_heatmap()` を改良版に置き換え
  - セル15: `visualize_two_tasks_in_checkpoint()` に `auto_range` パラメータを追加
  - セル19: テストケースで `auto_range=True` を使用
  - セル25〜29: 追加の可視化関数（相対角度、ヒストグラム）を挿入
  - セル30: メモセクションを更新

#### 新規追加したファイル
- `.company/lab/figures/heatmap-implementation-spec.md` に改良版の仕様を追記

### 期待される効果

1. **微細な違いが可視化可能**
   - 89.7度 vs 89.9度 の違いが色と数値で判別できる
   - 対角成分が非対角成分より小さい（近い）かどうかが一目瞭然

2. **実験間の比較が容易**
   - `reg100.0` vs `reg1000.0` など、異なる正則化係数の効果を比較しやすい
   - 統計情報により定量的な評価が可能

3. **分離の程度を多角的に評価**
   - 絶対角度ヒートマップ: 全体像
   - 相対角度ヒートマップ: 微細な違いを強調
   - ヒストグラム: 分布の傾向
   - 箱ひげ図: 外れ値の確認

### 次のステップ
1. 改良版ノートブックを実行して動作確認
2. 実験データ（`cd_vanilla_reg100.0`, Task 18 vs 19）で可視化
3. 異なる実験（`reg1000.0`, `wcd_vanilla` 等）と比較
4. 結果を `.company/lab/notes/lora-dynamic-separation.md` に記録

### 参考資料
- 実装ノートブック: `/mnt/HDD18TB/takama/2025_10_takama_Proj_CL/analysis/lora_heatmap_visualization.ipynb`
- 実装仕様書: `.company/lab/figures/heatmap-implementation-spec.md`

---

## LoRA研究: ヒートマップ可視化ノートブックのシンプル化

### 背景
- ユーザー要望: テストデータ削除、ヒートマップ表示以外の不要な機能を削除
- パス指定方式への変更

### 決定事項

#### 1. ノートブック構成の簡素化
**削除したセクション**:
- セクション3: テストデータでの動作確認（不要）
- セクション5: 複数層の比較（オプション機能）
- セクション5.5: 追加の可視化オプション（相対角度、ヒストグラム）の使用例

**残したセクション**:
- セクション1: 基本関数（`extract_basis_vectors`, `compute_angle_matrix`, `plot_heatmap`, `save_figure_both_locations`）
- セクション2: `visualize_lora_heatmap` 関数（統合関数）
- セクション3: 実行例
- セクション4: 追加の可視化（`plot_relative_heatmap`, `plot_angle_distribution`）の関数定義のみ

#### 2. パス指定方式への変更
**変更前**:
```python
EXPERIMENT_NAME = "cd_vanilla_reg100.0"
SEED = 0
CHECKPOINT_TASK_ID = 19  # task_19.pth
```
→ `../logs/{dataset}/{method}/{experiment_name}/seed_{seed}/task_{task_id}.pth` をプログラム内で構築

**変更後**:
```python
CHECKPOINT_PATH = "../logs/ImageNet_R/inflora_split/split_cd_orth_lr0.001/seed_0/task_19.pth"
```
→ **チェックポイントの絶対パスを直接指定**

#### 3. 関数の統合・簡素化
**削除した関数**:
- `load_checkpoint()`: 不要（`visualize_lora_heatmap` に統合）
- `extract_lora_weights_for_task()`: 不要（`visualize_lora_heatmap` に統合）
- `visualize_two_tasks_in_checkpoint()`: 削除

**新規統合関数**:
```python
visualize_lora_heatmap(
    checkpoint_path,      # 絶対パス
    task1_idx,
    task2_idx,
    layer_name,
    lora_type="lora_B_k",
    rank=8,
    auto_range=True,
    save_filename=None
)
```
- チェックポイント読み込み、LoRA重み抽出、角度計算、ヒートマップ描画をすべて統合
- パス指定がシンプル

### 実装内容

#### 変更したファイル
- `analysis/lora_heatmap_visualization.ipynb`
  - テストセクション（セル16-19）を削除
  - 複数層比較セクション（セル23-24）を削除
  - 追加可視化の使用例セクション（セル25-29）を削除
  - セクション2の関数を `visualize_lora_heatmap` に統合
  - セクション3を実行例に変更（パス指定方式）

### 期待される効果

1. **使いやすさの向上**
   - チェックポイントの絶対パスを指定するだけで実行可能
   - テンプレート的なコードが不要

2. **ノートブックの見通しが良くなる**
   - セクション数が減少（6 → 4）
   - ヒートマップ表示に集中

3. **柔軟性の維持**
   - 追加の可視化関数（`plot_relative_heatmap`, `plot_angle_distribution`）は残してある
   - 必要に応じて手動で呼び出し可能

### 使用方法（変更後）

```python
# チェックポイントの絶対パス
CHECKPOINT_PATH = "../logs/ImageNet_R/inflora_split/split_cd_orth_lr0.001/seed_0/task_19.pth"

# 比較するタスク
TASK1_IDX = 18
TASK2_IDX = 19

# 層とLoRAタイプ
LAYER_NAME = "image_encoder.blocks.0.attn"
LORA_TYPE = "lora_B_k"

# 可視化
fig, angles, (S1, S2) = visualize_lora_heatmap(
    CHECKPOINT_PATH,
    TASK1_IDX,
    TASK2_IDX,
    LAYER_NAME,
    LORA_TYPE,
    RANK
)
```

### 参考資料
- 実装ノートブック: `/mnt/HDD18TB/takama/2025_10_takama_Proj_CL/analysis/lora_heatmap_visualization.ipynb`
## 2026-03-26 意思決定: ヒートマップ可視化コードのモジュール化（リファクタリング）

### 内容
ヒートマップ可視化に関連する共通ロジックを外部モジュール `lora_viz_utils.py` に抽出し、Jupyter Notebook側ではこれらをインポートして使用する構成に変更した。

- **新規ファイル**: `analysis/lora_viz_utils.py`
    - `load_checkpoint`: チェックポイントのロード
    - `extract_lora_weights_for_task`: 特定タスクの重み抽出
    - `extract_basis_vectors`: SVDによる基底抽出
    - `compute_angle_matrix`: 角度行列計算
    - `plot_heatmap`: 改良型ヒートマップ描画
    - `save_figure_both_locations`: 2箇所への図の保存
- **ノートブックの簡易化**: `lora_heatmap_visualization.ipynb`
    - 冗長な関数定義を削除し、インポート形式に変更。
    - 実験設定（パスやタスク定数）と実行部分を明確に分離し、扱いやすくした。

### 背景
現状のコードが1つの巨大な関数に依存しており、他の可視化タスク（重みの抽出など）への再利用が困難であったため。ユーザーからの「重みの取り出しなどは他でも使えそう」という指摘に基づき、拡張性と保守性を向上させるための措置。

### タイムスタンプ
2026-03-26 11:15 (JST)

## 2026-03-26 意思決定: ヒートマップの生存期間管理とデフォルト保存設定の変更

### 内容
1. **既存ヒートマップの削除**: これまで生成されたすべてのヒートマップ画像（13枚）を研究ディレクトリおよび `.company` ディレクトリから完全に削除した。
2. **デフォルト保存の無効化**: ノートブックの `visualize_lora_heatmap` 関数の `do_save` 引数のデフォルト値を `False` に設定。デフォルトでは描画のみを行い、明示的な要求がある場合のみファイル保存するように変更した。

### 背景
大量の画像ファイルが各所に散在することを防ぎ、必要な解析結果のみを管理しやすくするため。

### タイムスタンプ
2026-03-26 11:20 (JST)

## 2026-03-26 意思決定: LoRA可視化システムの高度化と完全モジュール化

### 内容
ダッシュボード生成機能の強化に伴い、システム構成を「コア解析」と「レポート生成」に完全に分離する大規模なリファクタリングを実施した。

1. **ダッシュボードの2フェーズ化**:
   - 処理を `Phase 1 (画像プロット)` と `Phase 2 (HTML構築)` に分離。
   - デザイン修正時に重い計算をスキップしてHTMLのみを即座に更新可能にした。

2. **モジュールの専門化**:
   - **新規**: `lora_matrix_report.py` (バッチ・HTML担当)
   - **継続**: `lora_viz_utils.py` (基礎ロジック担当)

3. **ノートブックの役割分離**:
   - **新規**: `lora_matrix_report_batch.ipynb` (全タスク一括処理用)
   - **継続**: `lora_heatmap_visualization.ipynb` (個別深掘り解析用)

4. **UI/UXの向上**:
   - HTMLダッシュボードに **Lightbox (クリック拡大) 機能を実装**。
   - 大量の画像を `plots/` サブフォルダへ集約し、ディレクトリの見通しを改善。

### 背景
400枚規模のヒートマップ生成において、計算コストとファイル管理の煩雑さが課題となったため。研究者が「試行錯誤」と「レポート出力」をストレスなく並行できる環境を構築した。

### タイムスタンプ
2026-03-26 13:00 (JST)

### 参照
- 技術構成メモ: `.company/secretary/notes/2026-03-26-lora-viz-architecture.md`

## 2026-03-26 意思決定: 個別解析ヒートマップの保存先ディレクトリの統一

### 内容
`lora_heatmap_visualization.ipynb` で生成される単発のヒートマップ画像についても、一括レポートと同様に「レイヤー名＋LoRAタイプ」の専用サブフォルダに保存するように仕様を変更した。

### 理由
個別の試行錯誤の結果と一括レポートの結果が同じ構造で管理されることで、ディレクトリの散らかりを防止し、後からの参照を容易にするため。

### タイムスタンプ
2026-03-26 13:03 (JST)

## 2026-03-26 意思決定: .company 側の画像保存の廃止と研究DIRへの一本化

### 内容
ディスク容量の節約と管理の簡素化のため、これまで行っていた `.company/lab/figures/heatmaps/` への画像・HTMLの自動複製をすべて廃止した。

1. **保存機能の刷新**: `save_figure_both_locations` を `save_figure_to_project` に変更・簡素化。
2. **完全削除**: 既存の `.company` 側のヒートマップディレクトリをすべて削除。
3. **一本化**: すべての解析結果は、研究プロジェクト側の `{Layer}_{Type}/` フォルダのみで管理する。

### タイムスタンプ
2026-03-26 13:15 (JST)
