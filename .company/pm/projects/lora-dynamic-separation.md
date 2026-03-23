---
project: lora-dynamic-separation
status: review
department: lab
summary: 複数LoRA動的分離の研究（考察完了：既存の継続学習アプローチは中止、別タスク探索へ）
created: 2026-03-22
---

# 複数LoRA動的分離の研究

## 概要
事前学習済みモデルに複数のLoRAを追加し、損失関数で部分空間を動的直交化する研究。
継続学習の破滅的忘却防止 / マルチタスク学習での知識分離が主目的。

## 現在のフェーズ
**理論調査フェーズ**: 「0.9999」と「1.0」の性能差の理論的解明中

## ゴール
- 「ほぼ直交（0.9999）」の理論的解明
- マルチタスク学習等への応用可能性の探索
- 教授への進捗報告

## マイルストーン

- [x] 実験1: λブースト手法（単一Optimizer）
- [x] 実験2: Dual Optimizer導入
- [x] 実験3: cd/wcdアブレーション
- [ ] DeepResearch結果の分析
- [ ] Notionへの考察まとめ
- [ ] 教授への進捗報告

## 関連ドキュメント
- 研究ノート: `.company/lab/notes/lora-dynamic-separation.md`
- 実験ログ: `.company/lab/experiments/` 配下（随時追加）
