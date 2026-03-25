---
description: How to create, improve, and manage Antigravity skills. Use this skill whenever the user asks to create a new skill, turn a workflow into a skill, improve an existing skill, or asks about skill structure and best practices. Also use it when you notice a repeated workflow that could benefit from being captured as a skill.
---

# Skill Creator

A skill for creating new Antigravity skills and iteratively improving them.

## Overview

Skills are folders of instructions that extend your capabilities for specialized tasks. Each skill folder lives in `.agents/skills/<skill-name>/` and contains at minimum a `SKILL.md` file with YAML frontmatter and markdown instructions.

```
skill-name/
├── SKILL.md          (required) Main instructions
├── scripts/          (optional) Helper scripts
├── references/       (optional) Docs loaded as needed
└── assets/           (optional) Templates, icons, etc.
```

## Pre-requisite: Design & Consultation（設計・相談フェーズ）

新しいスキルを作成、あるいは既存のスキルに大幅な変更を加える前に、必ず以下の手順を踏むこと。

1. **スキルの構想提案**: どのような自動化が必要か、なぜスキル化すべきかをユーザーに提案する。
2. **設計案の提示**: スキルの構成（SKILL.md の骨子、必要なスクリプトなど）をドラフトとして提示し、ユーザーと内容を揉む。
3. **作成許可の取得**: ユーザーから「その内容で作って」という明確な合意を得てから、実際のファイル作成に着手する。

> **Why**: スキルはエージェントの振る舞いを不可逆的に規定する強力なツールであるため、ユーザーの意図との完全な一致が不可欠である。

---

## Skill Creation Flow

### Step 1: Capture Intent

Understand what the user wants. The conversation might already contain a workflow to capture (e.g., "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made.

Clarify these points:
1. What should this skill enable the agent to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Are there edge cases or important constraints?

### Step 2: Interview and Research

Proactively ask about:
- Edge cases and error handling
- Input/output formats
- Example files or data
- Success criteria
- Dependencies (MCPs, tools, file access)

Check the existing `.agents/skills/` directory for similar skills to avoid duplication or to build upon existing patterns. Also check `.agents/rules/` for any relevant rules that might interact.

### Step 3: Write the SKILL.md

Based on the interview, create the skill. Follow the structure below.

#### Frontmatter

```yaml
---
description: What the skill does and when to trigger it. Be specific and slightly "pushy" — include both the purpose AND the contexts where it should activate.
---
```

The `description` is the primary triggering mechanism. It is always loaded into context (~100 words). Make it comprehensive enough that the agent knows when to use the skill without reading the full body.

**Good example:**
```yaml
description: How to analyze meeting transcripts and extract action items. Use this skill whenever the user mentions meetings, MTGs, transcripts, action items, or says they finished a meeting, even if they don't explicitly ask for analysis.
```

**Bad example:**
```yaml
description: Meeting analysis tool.
```

#### Body Structure

Keep the body under 500 lines. Use imperative form. Explain **why** things are important rather than heavy-handed MUSTs.

Key patterns:
- Define output formats with templates
- Include 1-2 concrete examples
- Reference additional files clearly: "Read `references/foo.md` when you need to handle X"
- For large reference files (>300 lines), include a table of contents

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (description) — Always in context (~100 words)
2. **SKILL.md body** — Loaded when the skill triggers (<500 lines ideal)
3. **Bundled resources** — Loaded as needed (unlimited size)

Heavy content goes in `references/` or `scripts/`, not in the SKILL.md body.

### Step 4: Test the Skill

Since Antigravity doesn't have subagents, test manually in the conversation:

1. Come up with 2-3 realistic test prompts — the kind of thing a user would actually say
2. Share them with the user: "Here are a few test cases I'd like to try. Do these look right?"
3. For each test case, read the new SKILL.md, then follow its instructions to accomplish the task
4. Present results to the user and ask for feedback

#### Test Case Checklist Template

```markdown
## Test Cases for <skill-name>

### Test 1: <descriptive name>
- **Prompt**: "<realistic user input>"
- **Expected**: <what should happen>
- **Result**: ✅/❌ <what actually happened>
- **Feedback**: <user comments>

### Test 2: ...
```

Save test results in the skill's workspace or in conversation notes for reference.

### Step 5: Improve the Skill

Based on feedback, improve the skill. Key principles:

1. **Generalize from feedback** — Don't overfit to specific test cases. If there's a stubborn issue, try different metaphors or patterns rather than adding rigid constraints.
2. **Keep it lean** — Remove instructions that aren't pulling their weight.
3. **Explain the why** — If you find yourself writing ALWAYS or NEVER in all caps, reframe and explain the reasoning instead.
4. **Spot repeated work** — If every test run required the same boilerplate, bundle it as a script or template.

Iterate: improve → re-test → get feedback → repeat until the user is satisfied.

### Step 6: Optimize the Description

After the skill body is finalized, refine the `description` for better triggering:

1. List 3-5 phrases a user might say that should trigger this skill
2. List 2-3 phrases that are similar but should NOT trigger it
3. Ensure the description covers the trigger phrases naturally
4. Confirm with the user

## Updating an Existing Skill

When improving an existing skill:
- Preserve the original directory name
- Read the current SKILL.md fully before making changes
- Make targeted improvements rather than rewriting from scratch
- Test the updated version against the same scenarios that motivated the change

## Reference Files

For detailed guidance on writing style, improvement patterns, and advanced techniques, read `references/skill-writing-guide.md`.
