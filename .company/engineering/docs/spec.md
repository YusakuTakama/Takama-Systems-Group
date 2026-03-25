# Workout Tracker — Feature Specification

> **Version:** 2026-03 (Updated: 2026-03-25)
> **Platform:** Web App (Next.js / PWA)  
> **Data Storage:** `localStorage` (Keys: `workout_tracker_data`, `routinesData`, `workout_tracker_home_expanded`)

---

## 1. Data Model

### 1.1 Region (Master Data)
部位グループ（例: Chest, Back, Legs）。

| フィールド | 型 | 説明 |
|---|---|---|
| `id` | `string` | 一意ID (Date.now文字列) |
| `name` | `string` | 部位名 |
| `color` | `string?` | テーマカラーキー（gray / red / blue / green / yellow / purple / orange） |

### 1.2 Exercise (Master Data)
種目。必ずひとつの Region に属する。

| フィールド | 型 | 説明 |
|---|---|---|
| `id` | `string` | 一意ID |
| `name` | `string` | 種目名 |
| `regionId` | `string` | 所属 Region の ID |
| `memo` | `string?` | 自由記述メモ（種目に紐づく） |

### 1.3 Routine / Rest (User Plan)
ユーザーが作成するトレーニングメニューの構成要素。

| フィールド | 型 | 説明 |
|---|---|---|
| `id` | `string` | 一意ID |
| `type` | `'routine' \| 'rest'` | 種類（ルーティンまたは休憩日） |
| `name` | `string` | ルーティン名または休憩日の説明 |
| `exercises` | `string[]` | 種目IDの配列（`type: 'routine'` の場合のみ） |

### 1.4 WorkoutLog (History Data)
特定の日付×種目の記録。

| フィールド | 型 | 説明 |
|---|---|---|
| `id` | `string` | 一意ID |
| `date` | `string` | `YYYY-MM-DD` 形式 |
| `exerciseId` | `string` | 対象種目の ID |
| `sets` | `WorkoutSet[]` | セット一覧 |

### 1.5 WorkoutSet

| フィールド | 型 | 説明 |
|---|---|---|
| `setNumber` | `number` | セット番号（1始まり） |
| `weight` | `number` | 重量 (kg) |
| `reps` | `number` | レップ数 |

---

## 2. 画面構成 (4タブ・ボトムナビゲーション)

| 画面 | パス | アイコン | 概要 |
|---|---|---|---|
| ホーム | `/` | Dumbbell | ルーティンの構築・管理・実行 |
| 種目図録 | `/exercises` | BookOpen | 種目マスターデータ（部位・種目）の管理 |
| カレンダー | `/calendar` | Calendar | 月/週カレンダー＋日別詳細モーダル |
| 設定 | `/settings` | Settings | アプリ設定・Config管理 |

---

## 3. ホーム画面 (`/`) - ルーティン管理

### 3.1 ルーティン・レスト一覧
- ユーザーが作成した `Routine` および `Rest` カードをリスト表示。
- **Routineカード**: 展開可能。中に登録された種目がリスト表示される。
- **Restカード**: コンパクトなセパレーター形式。

### 3.2 ワークアウトの開始 (`▶ Start`)
- Routineカードの右上に `▶ Start` ボタンを表示（種目が1件以上ある場合のみ）。
- タップすると、そのルーティンの最初の種目の詳細画面へ「実行モード」で遷移する。

### 3.3 編集モード
- 右上の `Edit` ボタンで切り替え。
- **カードの追加**: `[＋ Add Routine or Rest]` ボタンからRoutineまたはRestを新規作成。
- **カードの管理**: ドラッグハンドルによる並び替え、および削除が可能。
- **種目の追加**: Routineカード展開時の `[＋ Add Exercise]` ボタンから専用の選択モーダルを開く。
- **種目の管理**: Routine内の種目の並び替え・削除（ルーティンからの除外）が可能。

### 3.4 種目選択モーダル (Add Exercise)
- 全種目マスターデータを部位アコーディオン形式で表示。
- タップした順に `1, 2, 3...` と番号が振られ、一括でルーティン末尾に追加可能。
- すでに当該ルーティンに含まれる種目は「Added」として選択不可。

---

## 4. 種目図録画面 (`/exercises`) - マスターデータ管理

### 4.1 種目リスト表示
- 部位 (`Region`) ごとに種目 (`Exercise`) をアコーディオン表示。
- 各部位・種目に「最終トレーニング日」バッジを表示。

### 4.2 編集モード
- 部位の追加・名称変更・カラーテーマ変更（7色）・削除が可能。
- 種目の追加・名称変更・削除が可能。
- **カスケード削除**: 部位や種目をここで削除すると、関連するルーティン内の項目や過去のログもすべて物理削除される。

---

## 5. カレンダー画面 (`/calendar`)

### 5.1 カレンダー表示
- 月表示 / 週表示を切り替え可能。
- トレーニング実施日は部位カラーのドット積み上げバーで視覚化。

### 5.2 日別詳細モーダル
- 日付タップでスライドアップ。実施種目一覧を表示。
- 種目名のタップで詳細画面へ、矢印のタップでセット内容（読み取り専用）を展開表示。

---

## 6. 種目詳細画面 (`/exercise/[id]`)

### 6.1 通常閲覧モード
- **Reps入力 (v2.5)**: `React Portal` を用いたカスタム・オーバーレイ・ピッカー。
  - **ページジャンプ防止**: `scrollIntoView` を廃止し、`.scrollTop` による直接制御に切り替えることで、メインページのスクロールが勝手に動く問題を解決。
  - **インテリジェント・スクロール**: `useLayoutEffect` により展開時に選択中の値を即時中央表示。
  - **サイレント・オートセーブ**: ステップごとの手動保存ボタンを廃止し、入力変更時にバックグラウンドで即時永続化。通知（トースト）を排したミニマルなUX。
- **スワイプ削除**: セット行を左スワイプして削除可能。
- **スマート入力**: 重量入力時に `kg` 単位が数値幅に合わせて動的に右隣へ追従。

### 6.2 ワークアウト実行モード (Wizard)
- ホームの `Start` ボタンや種目カードから遷移した場合に有効化。
- **ウィザードヘッダー**: 画面上部に固定される一体型ナビゲーション。
  - `＜ Prev` / `Next ＞` ボタンでルーティン内の種目を前後移動。
  - `1 / 4` のような進捗カウンターを表示。
- **Replace遷移**: 前後の移動は `router.replace` を使用し、ブラウザの戻る履歴を汚さない。
- **完了演出**: 最後の種目で `Complete` ボタンを押すとホームに戻り、「🎉 Workout Complete!」トーストを一定時間表示。

---

## 7. UI/UX 共通仕様

### 7.1 状態の保持 (Persistence)
- **アコーディオン**: `sessionStorage` を使用し、詳細画面から戻った際もホーム画面のルーティン展開状態などを完全に復元する。
- **ドラッグ＆ドロップ**: `@dnd-kit` を使用し、ホームのメニュー順および図録の表示順を永続化。

### 7.2 カラーシステム
- 部位ごとに定義された 7 色のテーマ（gray, red, blue, green, yellow, purple, orange）を、図録・ホーム内の種目カード・カレンダー上のドットに一貫して適用。

### 7.3 日付フォーマット
- 今年度: `M/D` (例: `3/22`)
- 過去・未来の別年: `YYYY/M/D` (例: `2023/3/22`)

---

## 8. 技術スタック

- **Framework**: Next.js (App Router)
- **Styling**: Tailwind CSS
- **State/Storage**: React Hooks + LocalStorage / SessionStorage
- **Icons**: Lucide React
- **DnD**: @dnd-kit
- **Charts**: Recharts
