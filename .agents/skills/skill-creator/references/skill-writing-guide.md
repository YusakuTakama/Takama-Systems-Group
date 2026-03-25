# Skill Writing Guide — Detailed Reference

This document provides in-depth guidance for writing and improving Antigravity skills. Read this when you need more detail beyond what's in SKILL.md.

## Table of Contents

1. [Anatomy of a Skill](#anatomy-of-a-skill)
2. [Progressive Disclosure in Detail](#progressive-disclosure-in-detail)
3. [Writing Style](#writing-style)
4. [Description Optimization](#description-optimization)
5. [Improvement Patterns](#improvement-patterns)
6. [Domain Organization](#domain-organization)
7. [Examples](#examples)

---

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

### Frontmatter Fields

| Field | Required | Purpose |
|---|---|---|
| `description` | ✅ | Triggering mechanism. Always in context. Should describe what the skill does AND when to use it. |

### SKILL.md Body

The body contains the actual instructions. Target < 500 lines. If approaching this limit, move detailed content to `references/` with clear pointers about when to read them.

---

## Progressive Disclosure in Detail

The three-level system optimizes context usage:

### Level 1: Metadata (~100 words, always loaded)
The `description` field. This is the only part the agent always sees. It must contain enough information to decide whether to read the full skill.

### Level 2: SKILL.md Body (loaded on trigger, < 500 lines)
The main instructions. Loaded when the agent decides the skill is relevant. Should be self-contained for the common case.

### Level 3: Bundled Resources (loaded on demand, unlimited)
Reference docs, scripts, templates. Only loaded when the SKILL.md body explicitly directs the agent to read them. Use clear directives:

```markdown
For AWS deployments, read `references/aws.md` before proceeding.
```

---

## Writing Style

### Use Imperative Form
```markdown
# Good
Read the input file. Extract the headers. Generate the summary.

# Avoid
You should read the input file. Then you should extract the headers.
```

### Explain the Why
Today's LLMs are smart. They have good theory of mind and when given good reasoning, they go beyond rote instructions.

```markdown
# Good
Keep summaries under 3 sentences — longer summaries lose the reader's
attention and defeat the purpose of summarizing.

# Avoid
ALWAYS keep summaries under 3 sentences. NEVER exceed this limit.
```

### Define Output Formats with Templates
```markdown
## Report Structure
Use this template:

# [Title]
## Executive Summary
## Key Findings
## Recommendations
```

### Include Concrete Examples
```markdown
## Commit Message Format

**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication

**Example 2:**
Input: Fixed crash when opening empty files
Output: fix(editor): handle empty file edge case
```

---

## Description Optimization

The `description` frontmatter determines when the skill triggers. The agent sees all skill descriptions and decides which ones to consult.

### Key Insights

- Skills only trigger for tasks the agent can't easily handle on its own
- Simple, one-step queries may not trigger even with perfect descriptions
- Complex, multi-step, or specialized queries reliably trigger when descriptions match

### Writing Effective Descriptions

**Be pushy.** Include both what the skill does AND specific contexts where it should activate:

```yaml
# Good — covers multiple trigger scenarios
description: How to build and analyze dashboards for company data.
  Use this whenever the user mentions dashboards, data visualization,
  status overviews, or asks to see project/task summaries, even if 
  they don't explicitly ask for a "dashboard."

# Bad — too narrow
description: Dashboard creation tool.
```

### Manual Optimization Checklist

1. List 3-5 typical user phrases that should trigger the skill
2. List 2-3 near-miss phrases that should NOT trigger it
3. Check that description naturally covers all trigger phrases
4. Verify near-misses wouldn't accidentally match
5. Confirm with the user

---

## Improvement Patterns

### 1. Generalize from Feedback

A skill that only works for test cases is useless. Rather than adding fiddly, overfitting changes or oppressively constrictive MUSTs, try:

- Using different metaphors or framings
- Recommending different patterns of working
- Broadening scope slightly to handle variations

### 2. Keep the Skill Lean

Remove instructions that aren't pulling their weight. If you observe (from conversation context) that the agent is spending time on unproductive steps, remove the parts causing it.

### 3. Explain the Why

Every instruction should have a reason. If you find yourself writing `ALWAYS` or `NEVER` in all caps, that's a yellow flag. Reframe as reasoning:

```markdown
# Before (rigid)
ALWAYS check for null values before processing.

# After (reasoning)
Check for null values before processing — null inputs cause
silent data corruption that's extremely hard to debug later.
```

### 4. Spot Repeated Work

If you notice the same boilerplate being written every time the skill is used, bundle it:

- **Template files** → `assets/`
- **Helper scripts** → `scripts/`
- **Reference docs** → `references/`

This saves every future invocation from reinventing the wheel.

---

## Domain Organization

When a skill supports multiple domains or frameworks, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + selection logic)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

The agent reads only the relevant reference file, keeping context lean.

---

## Examples

### Minimal Skill (single file)

```
quick-commit/
└── SKILL.md
```

```yaml
---
description: Generate conventional commit messages from staged changes.
  Use when the user asks to commit, wants a commit message, or says
  "save my changes" or similar.
---

# Quick Commit

Generate a conventional commit message from the current staged changes.

## Steps
1. Run `git diff --staged` to see what changed
2. Analyze the changes and categorize (feat/fix/refactor/docs/etc.)
3. Write a concise commit message following conventional format
4. Present to user for confirmation before committing

## Format
```
<type>(<scope>): <description>
```

**Example:**
Changes: Added error handling to the login API endpoint
Message: `fix(api): add error handling for login endpoint`
```

### Multi-file Skill

```
data-pipeline/
├── SKILL.md
├── scripts/
│   └── validate_schema.py
├── references/
│   ├── csv-patterns.md
│   └── json-patterns.md
└── assets/
    └── report-template.md
```
