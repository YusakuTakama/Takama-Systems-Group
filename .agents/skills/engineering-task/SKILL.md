---
description: Handles engineering tasks for personal development projects (e.g., Workout Tracker). Coordinates the full lifecycle: requirement clarification → implementation → user review → documentation update → Git push. Use this skill for any code fixes, feature additions, or UI tweaks.
---

# Engineering Task Skill（エンジニアリング・タスクスキル）

個人開発プロジェクトへのコード改修・機能追加・UIの微調整をプロ品質で管理するための、エンドツーエンドのワークフロー。

---

## Workflow

### Phase 1: Requirement Definition & Approval（要件定義と承認）

ユーザーの依頼を受けたら、まず「実装要件定義書（または実装プラン）」を作成し、**ユーザーの合意を得ることを最優先**する。

1. **現状調査**: 対象ファイルを `view_file` で読み込み、現在の実装と矛盾がないか把握する。
2. **要件定義書の作成**: 以下を含む定義書を作成し、チャットで提示する。
   - 実装のゴールと期待される挙動
   - 変更対象ファイルと具体的な変更内容（Tailwindクラスやロジックの変更点）
   - 懸念点やトレードオフ（あれば）
3. **フィードバックとブラッシュアップ**: ユーザーからの質問や指摘に対して回答・改善を行い、定義書を洗練させる。
4. **実装移行のトリガー**: **ユーザーが「よし、いこう」「実装開始して」など、実装への移行を明示的に許可したときのみ** Phase 2（実装）へ進む。勝手に実装を開始してはならない。

> **Why**: 認識の相違をコードレベルで検証する前に解消することで、手戻りをゼロにする。

---

### Phase 2: Implementation（実装）

ユーザーの許可を得た後、定義書の内容に基づき実装を行う。

- **1ファイルずつ、論理的な順番で変更する**。依存するファイルから順に変更する。
- `replace_file_content` または `multi_replace_file_content` を使い、的なターゲット行指定で編集する。
- 変更後は `view_file` で実際のコードを再確認し、意図通りに適用されたか必ずチェックする。

#### 開発サーバーの確認

```bash
# サーバーが起動していない場合は起動する
cd "<project_root>" && npm run dev
```

- TypeScriptエラーがないか、ターミナルのログだけでサッと確認する。

---

### Phase 3: User Review & Refinement（ユーザー確認と修正）

実装完了後、**まずはユーザーに結果を報告し、ユーザー自身による動作チェックを依頼する。**

1. **完了報告**: 実装が完了したことをユーザーに伝え、確認を促す。
2. **フィードバックの受領**: ユーザーから「ここが動かない」「ここをもう少し直して」などの指摘を受ける。
3. **再実装のループ**: 指摘事項がある場合は Phase 2 に戻り、修正を行う。
4. **通過条件**: **ユーザーから「OK」「これで大丈夫」「完璧」などの承認を得るまで、Phase 4 以降（ドキュメント更新・Push）に進んではならない。**

> [!IMPORTANT]
> 「一度の実装で完璧に仕上がることは稀である」という前提に立ち、ユーザーとの対話を通じてクオリティを磨き上げるフェーズ。

---

### Phase 4: Browser Verification（ブラウザ検証 - 原則スキップ）

**本フェーズは原則としてスキップする。** ユーザーから「ブラウザで確認して」「動作させてみて」と明示的な指示があった場合のみ、`browser_subagent` を起動する。

#### 実行する場合のチェックリスト

```
[ ] 実装した機能が期待通りに動作するか
[ ] スタイルが他の要素と視覚的に調和しているか
[ ] スマートフォンサイズ（375x667）で表示が崩れていないか
[ ] エッジケース（リストの端、空の状態）で問題がないか
```

スクリーンショットを撮影し、ユーザーに確かなエビデンスとして提示する。

---

### Phase 5: Documentation Update（ドキュメント更新）

**ユーザーの承認（Phase 3）を得た後**、以下のファイルを更新する。

| ファイル | 更新内容 |
|---|---|
| `spec.md` | 新機能の仕様・変更点を正確に反映。 |
| `engineering/docs/<project>.md` | 実装した内容の技術概要を追記。 |
| `pm/projects/<project>.md` | 該当タスクを `[x]` にマーク。 |
| `secretary/notes/YYYY-MM-DD-decisions.md` | 使用した技術や設計の意図を記録。 |
| `secretary/notes/YYYY-MM-DD-learnings.md` | 実装中に得た知見やハマりどころを記録。 |

---

### Phase 6: Git Push（バージョン管理）

ユーザーから「push して」という指示を受けた場合のみ実行する。

```bash
# プロジェクトルートの【絶対パス】を明示的に指定して実行することを基本とする。
# ※ワークスペース外（OneDrive等）で絶対パスが拒否される場合は、相対パス（../～）による迂回を検討する。
git -C "<absolute_project_root>" add .
git -C "<absolute_project_root>" commit -m "<type>: <summary of changes>"
git -C "<absolute_project_root>" push
```

> [!IMPORTANT]
> ユーザーの承認（Phase 3）を得た時点で、自律的に Phase 5（ドキュメント更新）を開始すること。

---

## References

プロジェクト固有の詳細情報は以下を参照する。

- **Workout Tracker 仕様**: `.company/engineering/docs/spec.md`  
- **Workout Tracker 技術概要**: `.company/engineering/docs/workout-tracker.md`  
- **PM管理**: `.company/pm/projects/workout-tracker.md`
