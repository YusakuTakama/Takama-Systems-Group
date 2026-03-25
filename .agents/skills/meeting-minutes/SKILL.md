---
description: Automates MTG summary creation, research note updates, and project task extraction. Triggered by "MTGが終わった", "打合せ完了", or raw transcripts. Ensures context parity by blocking on missing Notion imports and automatically syncs extracted tasks to secretary TODOs for seamless research workflow management.
---

# Meeting Minutes (議事録スキル)

This skill automates the organization of meeting results, ensuring coordination between project management, research notes, and task lists.

## Workflow

### 1. Request Inputs
When the user indicates a meeting has ended, ALWAYS ask for:
- **Raw Transcript (文字起こし)**
- **Session Notes (メモ)**
- **Notion URLs**

### How to provide inputs (Best Practice)
To keep the conversation clean and data organized, use these methods:

1. **Raw Transcript (文字起こし)**: 
   - Agent creates a file at `.company/lab/meeting-logs/YYYY-MM-DD-mtg-raw.md`.
   - User pastes the raw data into that file.
2. **Session Notes (メモ)**: 
   - User **pastes directly into the chat**. This serves as the primary context for the immediate processing and allows for quick clarification.
3. **Notion URLs & Content**:
   - User exports Notion content to Markdown.
   - User uploads/saves to `.company/lab/notes/notion-imports/`.
   - User provides the URL in chat so the agent can cross-check.

### Sample Response Template
Use a friendly but professional tone:
> お疲れ様でした！議事録の整理を開始しますね。
> 
> まず、以下の情報をいただけますか？
> 
> 1. **文字起こし**: 
>    [YYYY-MM-DD-mtg-raw.md](file:///absolute/path/to/log) を作成しました。こちらに内容を貼り付けて保存してください。
> 2. **当日メモ**: 
>    このチャットにそのまま貼り付けてください！
> 3. **Notion URL / インポート品**: 
>    Notion 側の更新があれば URL を教えてください。また、MDを `notion-imports/` に保存した場合はその旨教えてください。
> 
> 準備ができたら教えていただければ、すぐにサマリー作成と関連ファイルの更新を行います！

### 2. Process Notion Imports (Blocking Step)
If a Notion URL is provided:
1. Check if the corresponding `.md` file exists in `.company/lab/notes/notion-imports/`.
2. **IF MISSING**: STOP and request the user to upload/paste the content BEFORE proceeding to summary creation. 
   - *Reason*: Accurate summaries require full context from related Notion documents.

### 3. Generate MTG Summary (Mandatory Pro Model)
**IMPORTANT**: Before generating the summary, ALWAYS check if the current model is the "Pro" version (e.g., Gemini 1.5 Pro). 
- If uncertain or if the user is on a "Flash" or "Light" model, **warn the user** that for high-quality research synthesis, the Pro model is strongly recommended.

Create a file at `.company/lab/notes/YYYY-MM-DD-mtg-summary.md`.
... (existing logic) ...

### 4. Update Research & Project Files
... (existing logic) ...

### 5. Interactive Task Selection (User Decision Required)
1. **List all extracted NEXT ACTIONs** in the chat as a numbered or bulleted list.
2. **Propose Categorization**: Group them (e.g., Experimental, Theoretical, Strategy) to make it easier for the user to decide.
3. **MANDATORY PROMPT**: Ask the user: "**以上のタスクから、どれを本日のTODOリスト（最優先/通常）に反映しますか？**（追記・削除・調整も可能です）"
4. **Wait for user's selection.**
5. **Update TODO File**:
   - Open `.company/secretary/todos/YYYY-MM-DD.md`.
   - Append **ONLY** the tasks selected by the user.
   - **RULE**: **DO NOT** add deadlines (期限) unless explicitly asked.
   - Ensure they are clearly marked as derived from the MTG.

### 6. Update Project Management
Update the project management file at `.company/pm/projects/<project>.md`.
- **Frontmatter**: Update `summary` and `status` if they changed.
- **Milestones**: Mark completed tasks as `[x]` (after user confirmation) and add new NEXT ACTIONs.
- **Progress Tracking**: Ensure the milestone history makes the research progress visible.

### 6. Update TODOs
Update `.company/secretary/todos/YYYY-MM-DD.md`.
- Mark completed tasks.
- Add new tasks extracted from the MTG as "最優先" or "通常" based on context.

## Guiding Principles

- **Show, Don't Just Tell**: When updating `pm/projects/`, ensure the history of steps taken is clear.
- **Verifiable Completion**: Before marking a milestone as reached, ask the user: "◯◯も完了しましたか？"
- **Context Preservation**: Use information from the raw transcript to fill gaps in the user's brief notes, but ensure the user's intent remains primary.
- **Speaker Identification (1-on-1 MTG)**: 
  - Transcripts may have only one speaker label due to single-microphone setups.
  - ALWAYS treat the meeting as a **one-on-one session between the Professor and the User**.
  - Distinguish between "the Professor's advice/feedback" and "the User's reports/responses" based on conversational context.

## Reference Rules
- Refer to `.company/rules/RULES.md` for general organizational standards.
- Refer to `.company/lab/RULES.md` for specific research file roles.
