# LoRA部分空間のヒートマップ可視化手法 - 詳細レポート

> 作成日: 2026-03-26
> 目的: 複数LoRAの部分空間分離を定量的に評価するための可視化手法の確立
> 用途: 教授MTG報告資料

---

## 1. 概要

### 1.1 背景と目的

複数LoRAの動的分離研究において、従来のスカラ指標（直交性、コーダル距離、加重コーダル距離）では「どの主成分が分離されているか」という情報が失われる問題があった。本手法は、**2つのLoRA部分空間の基底ベクトル間の角度を行列形式で可視化**することで、以下を実現する：

1. **成分ごとの分離状態の可視化**: どの主成分ペアが分離され、どのペアが重なっているかを一目で把握
2. **非スカラ指標としての機能**: スカラ指標では捉えられない「空間的な関係性」の保存
3. **継続学習における時系列変化の追跡**: 各タスク学習後の空間変化を視覚的に比較

### 1.2 本手法の位置づけ

- **加重コーダル距離との関係**: 考え方は繋がるが、式としては直接繋がらない。別の観点として併用が妥当（教授評価）
- **空間版IoUのイメージ**: スカラに潰さず、空間ごとの関係を保存する指標
- **高次元への対応**: 128次元等の高次元でもメジャー・マイナー成分（10〜20個）の個別寄与を可視化可能

---

## 2. 数学的定式化

### 2.1 LoRAパラメータの構造

LoRAは低ランク分解により、事前学習済み重み $W_0 \in \mathbb{R}^{n \times d}$ に対して以下の更新を行う：

$$
W = W_0 + \Delta W = W_0 + BA
$$

ここで、
- $B \in \mathbb{R}^{n \times r}$: LoRA の「B行列」（出力側）
- $A \in \mathbb{R}^{r \times d}$: LoRA の「A行列」（入力側）
- $r$: LoRAのランク（$r \ll \min(n, d)$）

継続学習では、各タスク $t$ に対して独立したLoRAペア $(B_t, A_t)$ を追加する。本研究では特に **$B$ 行列の列空間**（column space）に着目する。

---

### 2.2 部分空間の抽出

タスク $t$ のLoRA $B_t$ 行列の列空間を表す正規直交基底を、特異値分解（SVD）により抽出する。

#### SVD による分解

$$
B_t = U_t \Sigma_t V_t^\top
$$

ここで、
- $U_t \in \mathbb{R}^{n \times r}$: 左特異ベクトル（**列空間の正規直交基底**）
- $\Sigma_t = \text{diag}(\sigma_{t,1}, \sigma_{t,2}, \ldots, \sigma_{t,r})$: 特異値（降順）
- $V_t \in \mathbb{R}^{r \times r}$: 右特異ベクトル

**重要な性質**:
- $U_t$ の各列 $\mathbf{u}_{t,i}$ ($i = 1, 2, \ldots, r$) は正規化されている：$\|\mathbf{u}_{t,i}\| = 1$
- $U_t$ の列同士は互いに直交している：$\mathbf{u}_{t,i}^\top \mathbf{u}_{t,j} = \delta_{ij}$
- 特異値 $\sigma_{t,i}$ が大きいほど、その方向の「重要度」が高い

#### ランクの選択

本実装では、ランク $k \leq r$ を指定することで、上位 $k$ 個の主成分のみを抽出可能：

$$
U_t^{(k)} = [\mathbf{u}_{t,1}, \mathbf{u}_{t,2}, \ldots, \mathbf{u}_{t,k}] \in \mathbb{R}^{n \times k}
$$

デフォルトでは $k = r$（全成分を使用）。

---

### 2.3 主角度行列（Principal Angle Matrix）の計算

2つのタスク $i, j$ の部分空間基底 $U_i, U_j$ について、**全ペアの主角度**を計算する。

#### 定義

タスク $i$ の第 $p$ 主成分ベクトル $\mathbf{u}_{i,p}$ とタスク $j$ の第 $q$ 主成分ベクトル $\mathbf{u}_{j,q}$ の間の**主角度** $\theta_{pq}$ を以下で定義する：

$$
\theta_{pq} = \arccos\left( \left| \mathbf{u}_{i,p}^\top \mathbf{u}_{j,q} \right| \right)
$$

ここで、
- $\mathbf{u}_{i,p}^\top \mathbf{u}_{j,q}$: 2つのベクトルの内積（コサイン類似度）
- 絶対値 $|\cdot|$ をとることで、方向の違いを無視し、**部分空間の重なり度合い**のみを評価
- $\theta_{pq} \in [0, \pi/2]$（度数法では $[0°, 90°]$）

#### 角度行列の構成

全ペアについて角度を計算し、行列 $\Theta \in \mathbb{R}^{k_i \times k_j}$ を構成する：

$$
\Theta = \begin{bmatrix}
\theta_{11} & \theta_{12} & \cdots & \theta_{1k_j} \\
\theta_{21} & \theta_{22} & \cdots & \theta_{2k_j} \\
\vdots & \vdots & \ddots & \vdots \\
\theta_{k_i1} & \theta_{k_i2} & \cdots & \theta_{k_ik_j}
\end{bmatrix}
$$

- **行**: タスク $i$ の主成分（$\sigma_{i,1}, \sigma_{i,2}, \ldots, \sigma_{i,k_i}$ の順）
- **列**: タスク $j$ の主成分（$\sigma_{j,1}, \sigma_{j,2}, \ldots, \sigma_{j,k_j}$ の順）
- $\Theta_{pq} = \theta_{pq}$: 第 $p$ 主成分と第 $q$ 主成分の角度

#### 実装（擬似コード）

```python
def compute_angle_matrix(U_i, U_j):
    k_i, k_j = U_i.shape[1], U_j.shape[1]
    Theta = zeros((k_i, k_j))

    for p in range(k_i):
        for q in range(k_j):
            dot_product = abs(dot(U_i[:, p], U_j[:, q]))
            dot_product = clip(dot_product, 0.0, 1.0)  # 数値誤差対策
            Theta[p, q] = arccos(dot_product) * (180 / pi)  # 度数法

    return Theta
```

---

### 2.4 期待される挙動

本手法では、損失関数の設計（コーダル距離 vs 加重コーダル距離）によってヒートマップに現れる**「法則性」**の違いを可視化できると期待される。

#### 1. コーダル距離（Chordal Distance）の場合
- **特徴**: 全ての基底ベクトルを一律に直交化するように学習。
- **期待されるヒートマップ**: 
  - 全てのペア（対角・非対角問わず）が $90^\circ$ に近づく。
  - 特定の成分に依存したパターンは見られず、全体的に均一に「赤い（離れている）」状態。

#### 2. 加重コーダル距離（Weighted Chordal Distance）の場合
- **特徴**: 特異値（$\sigma$）の大きい重要な基底ほど、優先的に直交化するように学習。
- **期待されるヒートマップ**: 
  - **重要な基底ペア（左上）**: 強烈な直交化圧力がかかるため、確実に $90^\circ$（赤）となる。
  - **重要でない基底ペア（右下）**: 反発力が弱いため、空間の競合がある場合は角度が小さくなる（青〜黄色）可能性がある。
  - **法則性**: 左上から右下にかけてのグラデーションや、特定の重要成分がどのマイナー成分のスペースを「逃げ道」として利用しているかといった**構造的なパターン**が可視化される。

---

## 3. 可視化の実装

### 3.1 ヒートマップの種類

本手法では、以下の3種類のヒートマップを生成する：

#### (A) 絶対角度ヒートマップ（Absolute Heatmap）

- **カラースケール**: デフォルトで $[0°, 90°]$
- **カラーマップ**: `RdYlBu_r`（赤=離れている、青=近い）
- **用途**: 部分空間の絶対的な分離状態を評価

**自動範囲調整**（`auto_range=True`）:
- 角度の範囲が $5°$ 未満の場合、自動的にスケールを調整
- 例: 最小値 $87°$, 最大値 $89°$ の場合 → スケールを $[86°, 90°]$ に設定

#### (B) 相対角度ヒートマップ（Relative Heatmap）

- **定義**: $\Theta_{\text{rel}} = \Theta - \min(\Theta)$
- **カラースケール**: $[0°, \max(\Theta) - \min(\Theta)]$
- **カラーマップ**: `viridis`
- **用途**: 微細な角度差を強調して可視化

#### (C) ツインビュー（Twin Heatmap）

- 絶対角度と相対角度を左右に並べて表示
- 両方の視点から同時に評価可能

---

### 3.2 統計情報の自動出力

ヒートマップ生成時、以下の統計情報を自動計算・出力する：

1. **全体統計**:
   - 最小角度: $\min(\Theta)$
   - 最大角度: $\max(\Theta)$
   - 角度範囲: $\max(\Theta) - \min(\Theta)$

2. **対角成分の統計**（$k_i = k_j$ の場合）:
   - 平均: $\frac{1}{k} \sum_{p=1}^{k} \theta_{pp}$
   - 標準偏差: $\sqrt{\frac{1}{k} \sum_{p=1}^{k} (\theta_{pp} - \bar{\theta}_{\text{diag}})^2}$

3. **非対角成分の統計**:
   - 平均: $\frac{1}{k^2 - k} \sum_{p \neq q} \theta_{pq}$
   - 標準偏差

4. **角度行列の詳細表示**:
   - 全要素を3桁精度で出力（ターミナル上で確認可能）

---

### 3.3 ディレクトリ構造と保存方式

実験結果は以下の階層構造で自動保存される：

```
figures/heatmaps/
└── {DATASET_NAME}/             # 例: ImageNet_R
    └── {MODEL_NAME}/           # 例: inflora_split
        └── {RUN_NAME}/         # 例: split_orth_orth_lr0.001
            └── {layer}_{lora_type}/  # 例: blocks_0_attn_lora_B_k
                ├── heatmap_task18vs19_*.png  # Twin view（デフォルト）
                ├── absolute/
                │   └── heatmap_task18vs19_*.png
                └── relative/
                    └── heatmap_task18vs19_*.png
```

**保存先の二重化**:
- **研究プロジェクトフォルダ**: `/mnt/HDD18TB/takama/2025_10_takama_Proj_CL/figures/heatmaps/`
- **Company管理フォルダ**: `.company/lab/figures/heatmaps/`

---

## 4. 使用方法

### 4.1 基本的な使い方

```python
from lora_viz_utils import visualize_lora_heatmap

# 実験設定
CHECKPOINT_PATH = "logs/ImageNet_R/inflora_split/split_orth_orth_lr0.001/seed_0/task_19.pth"
TASK1_IDX = 18
TASK2_IDX = 19
LAYER_NAME = "image_encoder.blocks.0.attn"
LORA_TYPE = "lora_B_k"

# 可視化実行
fig, angles, (S1, S2) = visualize_lora_heatmap(
    CHECKPOINT_PATH,
    TASK1_IDX,
    TASK2_IDX,
    LAYER_NAME,
    LORA_TYPE,
    rank=None,          # Noneで全成分を表示
    auto_range=True,    # 自動範囲調整
    do_save=True,       # 保存する
    dataset_name="ImageNet_R",
    model_name="inflora_split",
    run_name="split_orth_orth_lr0.001"
)
```

### 4.2 パラメータの説明

| パラメータ | 説明 | デフォルト |
|-----------|------|-----------|
| `checkpoint_path` | チェックポイントファイルのパス | 必須 |
| `task1_idx`, `task2_idx` | 比較するタスクのインデックス | 必須 |
| `layer_name` | LoRA層の名前 | 必須 |
| `lora_type` | LoRAのタイプ（`lora_B_k`, `lora_B_v`, `lora_A_k`, `lora_A_v`） | `"lora_B_k"` |
| `rank` | 使用する主成分の数（Noneで全成分） | `None` |
| `auto_range` | カラースケールの自動調整 | `False` |
| `do_save` | 図を保存するかどうか | `False` |

---

## 5. 実験結果の例

### 5.1 チェックポイントの構造（重要な発見）

**1つのチェックポイント**（例: `task_19.pth`）に、**全20タスクのLoRA**が含まれている：

```python
state_dict = {
    "image_encoder.blocks.0.attn.lora_B_k.0.weight": ...,  # Task 0
    "image_encoder.blocks.0.attn.lora_B_k.1.weight": ...,  # Task 1
    ...
    "image_encoder.blocks.0.attn.lora_B_k.19.weight": ..., # Task 19
}
```

これは、InfLoRAの実装が**ModuleList**を使用しているためである：

```python
class Attention_LoRA(nn.Module):
    def __init__(self, dim, num_heads=8, r=64, n_tasks=10):
        self.lora_B_k = nn.ModuleList([
            nn.Linear(r, dim, bias=False) for _ in range(n_tasks)
        ])
```

### 5.2 期待される可視化結果

#### (A) 理想的な全空間分離（Chordal Distance 等）
- **ヒートマップ**: 全域が赤色（$\approx 90^\circ$）
- **解釈**: 全ての主成分が互いに直交しており、干渉が最小化されている。

#### (B) 優先順位付き分離（Weighted Chordal Distance 等）
- **ヒートマップ**: 
  - 左上のメジャー成分同士：赤色（$\approx 90^\circ$）
  - 右下のマイナー成分同士：青〜黄色（角度が小さい）
- **解釈**: 重要な情報を含む主成分が優先的に分離されており、低ランクの制約下で賢く空間を使い分けている。

---

## 6. 今後の展開

### 6.1 継続学習での時系列変化プロット

各タスク学習後のチェックポイント（`task_0.pth`, `task_1.pth`, ..., `task_19.pth`）について、同一のタスクペア（例: Task 0 vs Task 1）のヒートマップを時系列で並べることで、**学習が進むにつれて空間の重なりがどう変化するか**を可視化できる。

**期待される成果**:
- 「0.9999」状態での干渉蓄積の様子を視覚的に捉える
- 臨界閾値に達するステップ数を特定

### 6.2 評価指標のベクトル化

加重コーダル距離の「和」を分解し、成分ごとの寄与を保持したベクトル指標を考案する：

$$
\text{WCD}_{\text{vector}} = [\sigma_{i,1} \cdot d_1, \sigma_{i,2} \cdot d_2, \ldots, \sigma_{i,k} \cdot d_k]
$$

ここで、$d_p$ は第 $p$ 主成分ペアの距離。

本ヒートマップ手法と組み合わせることで、**どの成分が分離に寄与しているか**を定量的に評価可能。

### 6.3 高次元（128次元等）での検証

ランク $r = 128$ の場合でも、上位10〜20個の主成分のヒートマップを表示することで、メジャー・マイナー成分の個別挙動を確認できる。

---

## 7. まとめ

### 7.1 本手法の貢献

1. **非スカラ指標の実現**: スカラ指標では失われる「どの成分が分離されているか」の情報を保存
2. **直感的な可視化**: 対角成分と非対角成分のパターンから、分離状態を一目で把握
3. **時系列解析への拡張性**: 継続学習における空間変化を追跡可能
4. **実装の完成度**: 自動統計出力、柔軟な保存方式、複数のビュー（絶対/相対/ツイン）

### 7.2 教授からのフィードバック（2026-03-25 MTG）

- ✅ 「ヒートマップ可視化の提案は非常に有意義」
- ✅ 「空間版IoUのイメージで、スカラに潰さず関係性を保存する」
- ✅ 「加重コーダル距離とは考え方が繋がるが、式としては直接繋がらない → 別観点として併用が妥当」
- ✅ 「継続学習でのヒートマップ時系列変化の観察は特に重要」

### 7.3 次のステップ

- [ ] 実験データ（Dual Optimizer / λブースト）でのヒートマップ生成
- [ ] 継続学習での時系列変化プロットの実装
- [ ] 評価指標のベクトル化との統合
- [ ] 高次元（128次元）での挙動確認

---

## 参考文献

- 実装ファイル: [`lora_viz_utils.py`](file:///mnt/HDD18TB/takama/2025_10_takama_Proj_CL/analysis/lora_viz_utils.py)
- ノートブック: [`lora_heatmap_visualization.ipynb`](file:///mnt/HDD18TB/takama/2025_10_takama_Proj_CL/analysis/lora_heatmap_visualization.ipynb)
- プロジェクト管理: [`.company/pm/projects/lora-dynamic-separation.md`](file:///mnt/HDD18TB/takama/Takama-Systems-Group/.company/pm/projects/lora-dynamic-separation.md)
