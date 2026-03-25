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
