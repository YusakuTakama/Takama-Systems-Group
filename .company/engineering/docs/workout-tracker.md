# Workout Tracker — プロジェクト概要

> 記録日: 2026-03-22  
> ステータス: 一区切り完了・ブラッシュアップフェーズへ  
> 仕様書: `.company/engineering/docs/spec.md`

---

## 概要

筋トレ記録を管理するPWA（Progressive Web App）。  
スマートフォンを主なターゲットとして、快適なUXで日々のトレーニングログを手軽に残せるアプリ。

## 技術スタック

| 項目 | 内容 |
|------|------|
| フレームワーク | Next.js |
| スタイリング | Tailwind CSS |
| グラフ | Recharts |
| アイコン | lucide-react |
| DnD | @dnd-kit/core, @dnd-kit/sortable |
| データ永続化 | localStorage（キー: `workout_tracker_data`） |
| 対応 | PWA（manifest.json + Service Worker） |

## データモデル

```
Region（部位グループ）
 └── Exercise（種目）
      └── WorkoutLog（日付×種目の記録）
           └── WorkoutSet（セット番号・重量kg・レップ数）
```

- データはすべてlocalStorageにJSON保存
- 初回起動時に Chest / Back / Legs / Shoulders / Arms のプリセットあり
- カスケード削除: Region削除 → 傘下Exercise・WorkoutLog も全削除

## 画面構成

| 画面 | パス | 概要 |
|------|------|------|
| ホーム | `/` | 種目リスト・編集（Region別アコーディオン） |
| カレンダー | `/calendar` | 月/週カレンダー＋日別詳細モーダル |
| 種目詳細 | `/exercise/[id]` | セット入力・メモ・進捗グラフ |
| 設定 | `/settings` | アプリ設定 |

## 主な実装機能

### ホーム (`/`)
- Region別アコーディオン、最終トレーニング日バッジ
- 7色カラーテーマ（Region単位で設定）
- 編集モード（Region/Exercise の追加・名前変更・削除）
- @dnd-kit によるドラッグ＆ドロップ並び替え

### カレンダー (`/calendar`)
- 月表示 / 週表示の切り替え
- Region色のドット積み上げバーでトレーニング日を可視化（セット数比例）
- 今月・今週のトレーニング日数サマリーカード
- 日別詳細モーダル（種目カードの左半分→詳細画面遷移 / 右半分→セット展開）

### 種目詳細 (`/exercise/[id]`)
- 経過タイマー（リアルタイム mm:ss）
- 日付ピッカーで過去データ閲覧・編集
- 種目メモ（自動保存、高さ自動伸縮テキストエリア）
- Last Session カード（折りたたみ式、最大重量表示）
- セット入力行（スマートフォーカス、スワイプ削除、kg動的追従）
- **Reps入力 (v2.4)**: `createPortal` による見切れなしオーバーレイ、`useLayoutEffect` による即時中央配置、上下Paddingによる0/100中央化。
- 保存/削除アニメーション（Saved! / Deleted!）
- Rechartsによる進捗グラフ（1M/3M/ALL、タップで拡大モーダル）
- History ボタン → 過去セッション一覧モーダル（アコーディオン展開）

### 共通UI（読み取り専用セット表示）
- Last Sessionカード展開時・カレンダー詳細モーダルで共用
- 入力欄なし・完全読み取り専用のコンパクトグリッド

## 今後の方針

- ブラッシュアップフェーズ（改善点洗い出し中）
- 改善案は秘書に話して随時記録していく予定
- 2026-03-25: Reps入力UIの最終形態（Portal & Minimalist）を実装・Fix

---

*このドキュメントは随時追記していきます。*
