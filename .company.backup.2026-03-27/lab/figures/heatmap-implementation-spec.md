# ヒートマップ可視化実装の詳細仕様書

> 作成日: 2026-03-26
> 目的: 実装したヒートマップ可視化ノートブックの詳細仕様を記録
> ノートブック: `/mnt/HDD18TB/takama/2025_10_takama_Proj_CL/analysis/lora_heatmap_visualization.ipynb`

---

## 1. 実装の概要

### 1.1 目的

複数LoRAの部分空間における基底ベクトル間の角度をヒートマップで可視化する。

### 1.2 重要な前提理解（2026-03-26判明）

- **チェックポイント構造**: `task_19.pth` という1つのファイルに、task 0〜19の**全20個のLoRA**が含まれている
- **比較対象**: 異なるチェックポイント間ではなく、**同じチェックポイント内の異なるタスク**を比較する
- **キー形式**: `image_encoder.blocks.0.attn.lora_B_k.0.weight` のような構造

### 1.3 出力

- **ヒートマップ**: k×k の角度行列
  - 対角成分（同順位）が赤（大きい角度）→ 重要成分が分離できている ✅
  - 非対角成分（異順位）が青（小さい角度）→ 期待通りの挙動 ✅

---

## 2. 実装した関数の詳細

### 2.1 基本関数

#### `extract_basis_vectors(B, rank=None)`

**目的**: LoRA重み行列の列空間の基底ベクトルを特異値の大きい順に抽出

**入力**:
- `B`: LoRA重み行列 (n × d) の numpy array
- `rank`: 抽出する基底の数（Noneの場合は全て）

**処理**:
```python
U, S, Vt = np.linalg.svd(B, full_matrices=True)
U_basis = U[:, :rank]
singular_values = S[:rank]
```

**出力**:
- `U_basis`: 左特異ベクトル（列空間の正規直交基底） (n × rank)
- `singular_values`: 特異値 (rank,)

**重要な点**:
- SVDの**左特異ベクトル** (U) を使用
- 特異値の大きい順に並んでいる

---

#### `compute_angle_matrix(U1, U2, return_degrees=True)`

**目的**: 2つの基底ベクトル集合の全ペアの角度を計算

**入力**:
- `U1`: タスク1の基底ベクトル (n × k)
- `U2`: タスク2の基底ベクトル (n × k)
- `return_degrees`: True=度数法, False=ラジアン

**処理**:
```python
for i in range(k1):
    for j in range(k2):
        dot_product = np.abs(np.dot(U1[:, i], U2[:, j]))
        dot_product = np.clip(dot_product, 0.0, 1.0)  # 数値誤差対策
        angle_rad = np.arccos(dot_product)
        angle_matrix[i, j] = np.rad2deg(angle_rad) if return_degrees else angle_rad
```

**出力**:
- `angle_matrix`: 角度行列 (k × k)
  - `angle_matrix[i, j]` = U1の第i基底 と U2の第j基底 の角度

**重要な点**:
- 内積の**絶対値**を取る（ベクトルの符号は角度に無関係）
- `np.clip`で数値誤差を防ぐ

---

#### `plot_heatmap(...)`

**目的**: 角度行列をヒートマップとして可視化

**主要パラメータ**:
- `angle_matrix`: 角度行列 (k × k)
- `task1_name`, `task2_name`: 軸ラベル
- `cmap`: カラーマップ（デフォルト: `"RdYlBu_r"`）
  - 赤=90°（垂直）、青=0°（平行）
- `vmin=0, vmax=90`: カラーバーの範囲

**処理**:
```python
sns.heatmap(angle_matrix,
            annot=True,      # 数値を表示
            fmt=".1f",       # 小数点1桁
            cmap="RdYlBu_r", # カラーマップ
            vmin=0, vmax=90,
            xticklabels=[f"{task2_name}_σ{i+1}" for i in range(k2)],
            yticklabels=[f"{task1_name}_σ{i+1}" for i in range(k1)],
            square=True)     # 正方形
```

---

#### `save_figure_both_locations(fig, filename)`

**目的**: 図を2箇所に同時保存

**保存先**:
1. 研究プロジェクト: `../figures/heatmaps/{filename}`
2. .company: `/mnt/HDD18TB/takama/Takama-Systems-Group/.company/lab/figures/heatmaps/{filename}`

**処理**:
- ディレクトリを自動作成 (`mkdir -p` 相当)
- dpi=300で高解像度保存
- `bbox_inches='tight'` で余白削除

---

### 2.2 チェックポイント読み込み関数

#### `load_checkpoint(experiment_name, seed, task_id, dataset, method)`

**目的**: チェックポイントを読み込む

**入力例**:
- `experiment_name`: `"wcd_vanilla_reg1000.0"`
- `seed`: `0`
- `task_id`: `19`（task_19.pth）
- `dataset`: `"ImageNet_R"`
- `method`: `"InfLoRA"`

**処理**:
```python
ckpt_path = f"../logs/{dataset}/{method}/{experiment_name}/seed_{seed}/task_{task_id}.pth"
checkpoint = torch.load(ckpt_path, map_location='cpu')
```

**出力**:
- `checkpoint`: state_dict（辞書形式）
- `ckpt_path`: チェックポイントのパス

**重要な注意**:
- `task_19.pth` には task 0〜19 の**全20個のLoRA**が含まれる

---

#### `extract_lora_weights_for_task(checkpoint, layer_name, task_idx, lora_type)`

**目的**: チェックポイントから特定タスクのLoRA重みを抽出

**入力例**:
- `checkpoint`: 読み込んだstate_dict
- `layer_name`: `"image_encoder.blocks.0.attn"`
- `task_idx`: `0`（Task 0）
- `lora_type`: `"lora_B_k"` または `"lora_B_v"`

**処理**:
```python
key = f"{layer_name}.{lora_type}.{task_idx}.weight"
# 例: "image_encoder.blocks.0.attn.lora_B_k.0.weight"

if key not in checkpoint:
    raise KeyError(f"Key not found: {key}")

lora_weight = checkpoint[key].numpy()
```

**出力**:
- `lora_weight`: LoRA重み行列（numpy array）
  - `lora_B_k` shape: `(768, 10)` = (dim, rank)
  - `lora_A_k` shape: `(10, 768)` = (rank, dim)

**重要な点**:
- キー形式: `{layer_name}.{lora_type}.{task_idx}.weight`
- `image_encoder.` というプレフィックスが必要

---

#### `visualize_two_tasks_in_checkpoint(...)`

**目的**: 同じチェックポイント内の2つのタスクのLoRAを比較可視化

**主要パラメータ**:
- `checkpoint_task_id`: チェックポイントのID（例: 19 → task_19.pth）
- `task1_idx`: 比較するタスク1のID（例: 0）
- `task2_idx`: 比較するタスク2のID（例: 19）
- `layer_name`: 層の名前（例: `"image_encoder.blocks.0.attn"`）
- `lora_type`: `"lora_B_k"` または `"lora_B_v"`
- `rank`: 可視化する基底の数（例: 8）

**処理フロー**:
1. チェックポイント読み込み
2. 各タスクのLoRA重み抽出
3. B行列の列空間から基底ベクトル抽出
4. 角度行列計算
5. ヒートマップ描画と保存

**重要な処理**:
```python
# LoRA重み抽出
lora_B1 = extract_lora_weights_for_task(ckpt, layer_name, task1_idx, lora_type)
lora_B2 = extract_lora_weights_for_task(ckpt, layer_name, task2_idx, lora_type)

# lora_B_k は (dim, rank) = (768, 10)
# 列空間を比較するため、そのままextract_basis_vectorsに渡す
U1, S1 = extract_basis_vectors(lora_B1, rank=rank)
U2, S2 = extract_basis_vectors(lora_B2, rank=rank)

# 角度行列計算
angles = compute_angle_matrix(U1, U2)
```

**出力**:
- `fig`: matplotlib figure
- `angles`: 角度行列
- `(S1, S2)`: 各タスクの特異値

---

## 3. 使用方法

### 3.1 デフォルト設定（セクション4）

```python
EXPERIMENT_NAME = "wcd_vanilla_reg1000.0"
SEED = 0
CHECKPOINT_TASK_ID = 19  # task_19.pth を読み込む
TASK1_IDX = 0   # Task 0（最初のタスク）
TASK2_IDX = 19  # Task 19（最後のタスク）
LAYER_NAME = "image_encoder.blocks.0.attn"
LORA_TYPE = "lora_B_k"
RANK = 8
```

### 3.2 実行

```python
fig, angles, (S1, S2) = visualize_two_tasks_in_checkpoint(
    CHECKPOINT_TASK_ID,
    TASK1_IDX, TASK2_IDX,
    LAYER_NAME,
    EXPERIMENT_NAME,
    SEED,
    LORA_TYPE,
    RANK
)

plt.show()
```

---

## 4. 期待される挙動

### 4.1 正常動作時の出力

```
✅ Loaded: ../logs/ImageNet_R/InfLoRA/wcd_vanilla_reg1000.0/seed_0/task_19.pth
   Total keys: 1194

📊 Task 0 lora_B_k shape: (768, 10)
📊 Task 19 lora_B_k shape: (768, 10)

特異値:
  Task 0: [s1, s2, s3, s4, s5, s6, s7, s8]
  Task 19: [s1, s2, s3, s4, s5, s6, s7, s8]

角度行列の対角成分（同順位ペア）: [θ1, θ2, θ3, θ4, θ5, θ6, θ7, θ8]
対角成分の平均: XX.XX°

✅ 図を保存しました: 2026-03-26-wcd_vanilla_reg1000.0-ckpt19-task0vs19-blocks_0_attn-lora_B_k.png
   📁 研究プロジェクト: .../figures/heatmaps/...
   📁 .company: .../lab/figures/heatmaps/...
```

### 4.2 ヒートマップの見方

**理想的なケース（分離が良い）**:
- 対角成分: 赤色（70°〜90°）→ 同順位の重要成分が離れている
- 非対角成分: 青色（0°〜30°）→ 異なる順位間が近い

**問題のあるケース（分離不十分）**:
- 対角成分: 黄色〜オレンジ（30°〜60°）→ 同順位でも近い
- 非対角成分: 黄色（30°〜60°）→ 対角との差が小さい

---

## 5. テストデータでの動作確認（セクション3）

### 5.1 テストケース

```python
theta_angles = [70, 65, 60, 55]  # 主角度（度）
```

### 5.2 期待される結果

```
角度行列 (度):
[[70. 90. 90. 90.]
 [90. 65. 90. 90.]
 [90. 90. 60. 90.]
 [90. 90. 90. 55.]]

対角成分（期待: 70, 65, 60, 55度）: [70. 65. 60. 55.]
```

- 対角成分が正確に期待値と一致
- 非対角成分が90°（直交）

---

## 6. 実装上の重要な判断

### 6.1 LoRA_B行列の扱い

**形状**: `lora_B_k` は `(768, 10)` = (dim, rank)

**列空間の扱い**:
- `lora_B_k` の列空間 = dimからrankへの射影
- `extract_basis_vectors(lora_B, rank)` でそのまま列空間の基底を抽出

**なぜ転置しないのか？**
- `lora_B` は (dim, rank) だが、これは「rankの各基底がdim次元のベクトル」という意味
- SVD: `U @ diag(S) @ Vt = lora_B`
  - U: (dim, dim) の左特異ベクトル
  - S: (rank,) の特異値
  - Vt: (rank, rank) の右特異ベクトル
- Uの最初のrank列が列空間の基底

### 6.2 角度計算

**内積の絶対値を取る理由**:
- ベクトルの符号（+/-）は角度に無関係
- `arccos(|dot|)` で0°〜90°の範囲に収める

### 6.3 チェックポイント構造の理解

**誤った理解**（最初の勘違い）:
- ~~task_0.pth と task_1.pth という別々のファイルを比較する~~

**正しい理解**:
- task_19.pth という1つのファイルに全タスクのLoRAが含まれる
- `state_dict["blocks.0.attn.lora_B_k.0.weight"]` でTask 0
- `state_dict["blocks.0.attn.lora_B_k.19.weight"]` でTask 19

---

## 7. トラブルシューティング

### 7.1 KeyError: キーが見つからない

**原因**:
- レイヤー名が間違っている
- タスクIDが範囲外

**確認方法**:
```python
# チェックポイント内のキーを確認
lora_keys = [k for k in checkpoint.keys() if 'lora' in k.lower()]
print(lora_keys[:20])
```

### 7.2 形状が違う

**原因**:
- `lora_A` と `lora_B` を間違えている
- `lora_B_k` shape: (768, 10)
- `lora_A_k` shape: (10, 768)

### 7.3 角度が期待と違う

**確認ポイント**:
1. 特異値を確認（どの基底が重要か）
2. 対角成分の平均を確認
3. ヒートマップのカラースケールを確認

---

## 8. 環境設定

### 8.1 Python環境

```bash
source ~/.MTLoRA/bin/activate
```

**必要なパッケージ**:
- torch 2.6.0+cu124
- numpy
- matplotlib
- seaborn

### 8.2 Jupyter Lab起動

```bash
cd /mnt/HDD18TB/takama/2025_10_takama_Proj_CL/analysis
jupyter lab lora_heatmap_visualization.ipynb
```

---

## 9. 今後の拡張予定

- [ ] 継続学習の時系列変化プロット（task_0.pth, task_5.pth, task_10.pth...で推移を見る）
- [ ] 3個以上のLoRAの全組み合わせ可視化
- [ ] 加重コーダル距離との対応確認
- [ ] 異なる実験（Dual Optimizer vs λブースト）の比較
- [ ] 高次元（128次元）での累積寄与率ベースの次元選択

---

## 10. 関連ファイル

- ノートブック本体: `/mnt/HDD18TB/takama/2025_10_takama_Proj_CL/analysis/lora_heatmap_visualization.ipynb`
- 壁打ちメモ: `.company/secretary/notes/2026-03-26-heatmap-brainstorm.md`
- 研究ノート: `.company/lab/notes/lora-dynamic-separation.md`
- 意思決定ログ: `.company/secretary/notes/2026-03-26-decisions.md`

---

## 11. 改良版の追加機能（2026-03-26）

### 11.1 問題点

- 角度が 89.902度、89.845度など微妙に異なるのに、すべて「90.0」と表示される
- カラーマップ範囲が 0〜90度なので、89度台の微細な違いが色で判別できない

### 11.2 追加機能

#### 機能1: カラーマップ範囲の動的調整

```python
plot_heatmap(angle_matrix, auto_range=True)
```

- 角度の実際の範囲に応じて `vmin`, `vmax` を自動計算
- 範囲が5度未満の場合は拡大表示（例: 88〜90度）
- 範囲が広い場合は従来通り 0〜90度

#### 機能2: 小数点桁数の動的調整

- 範囲 < 1度 → `fmt=".3f"`（小数点3桁）
- 範囲 < 5度 → `fmt=".2f"`（小数点2桁）
- それ以外 → `fmt=".1f"`

#### 機能3: 統計情報の自動出力

```
📊 角度統計:
  最小値: 89.712°
  最大値: 89.998°
  範囲: 0.286°
  対角成分の平均: 89.845° (std: 0.082°)
  非対角成分の平均: 89.920° (std: 0.065°)
🎨 カラーマップ範囲を自動調整: 88.7° 〜 90.0°
```

#### 機能4: 相対角度ヒートマップ

```python
plot_relative_heatmap(angle_matrix, ...)
```

- 最小値を0として差分を可視化
- 微細な違いを強調
- カラーマップ: `viridis`（0からの差分用）

#### 機能5: 角度分布のヒストグラム

```python
plot_angle_distribution(angle_matrix, ...)
```

- 対角成分 vs 非対角成分の分布を並べて表示
- ヒストグラムと箱ひげ図の両方
- 分離の程度を視覚的に確認

### 11.3 使用方法

```python
# 1. 通常のヒートマップ（自動範囲調整）
fig, angles, (S1, S2) = visualize_two_tasks_in_checkpoint(
    ...,
    auto_range=True  # デフォルト: True
)

# 2. 相対角度ヒートマップ
plot_relative_heatmap(angles, task1_name="Task0", task2_name="Task19")

# 3. 角度分布のヒストグラム
plot_angle_distribution(angles, task1_name="Task0", task2_name="Task19")
```

---

## フィードバック用チェックリスト

実際に実行して確認した内容を記載してください：

- [ ] チェックポイントは正しく読み込めたか？
- [ ] LoRA重みの形状は期待通りか？
- [ ] 特異値は妥当な値か？
- [ ] 角度行列の対角成分は期待通りか？
- [ ] ヒートマップは表示されたか？
- [ ] 図は2箇所に保存されたか？
- [ ] **統計情報は出力されたか？**（2026-03-26追加）
- [ ] **カラーマップ範囲は自動調整されたか？**（2026-03-26追加）
- [ ] **微細な違いが色で判別可能か？**（2026-03-26追加）
- [ ] エラーメッセージは何か？
- [ ] 期待と違う挙動は何か？
