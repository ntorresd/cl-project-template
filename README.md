# Project Template

Reusable template for starting a new Claude Code project including: a specialized `CLAUDE.md`, a running
session-log Artifact mirrored to `session-log.html`, and a private (or public) GitHub remote. Copy this folder's `CLAUDE.md` into a new project and work through
the steps below.

## 1. Create the project folder

```bash
mkdir -p ~/Projects/<project-name>
cd ~/Projects/<project-name>
```

## 2. Specialize CLAUDE.md

Copy the template in and fill in every bracketed placeholder:

```bash
cp ~/Projects/ProjectTemplate/CLAUDE.md ./CLAUDE.md
```

Open it and work through each section:

- **§1 Role and Persona** — the agent's specialty and how it should relate
  to you.
- **§2 Project Context** — the central question/goal/deliverable.
- **§3 Primary References** — anchor sources, priority order.
- **§4 Domain Expertise** — subdomains the agent can assume without
  re-explaining.
- **§5 Cross-Cutting Synthesis** — delete if the project is narrow; keep
  and fill in if requests will regularly span multiple sources/subdomains.
- **§6–§8** (Sourcing, Derivations, Interaction Style) — generic and
  already filled in; adjust only if this project needs a different stance.
- **§9 Formatting** — domain-specific formatting conventions. Delete the
  LaTeX Input Conventions subsection entirely if the project has no
  LaTeX/custom-macro documents; otherwise fill in the actual macros once
  you know them.
- **§10 Boundaries** — add any hard, project-specific constraints beyond
  the generic "never fabricate" rule already there.
- **§11–§12** (Repository Hygiene, Session Log Artifact) — generic,
  leave as-is.

You can also promt your way for Claude to fill in each section for you. Proceed carefully and taylor the instructions to your specific problem and preferences.

## 3. Add project content

Bring in whatever source material the project needs (reference documents,
existing code, an Overleaf-synced notes folder, etc.). If any subdirectory
is *already* its own git repository (e.g. synced with an external tool
like Overleaf), decide now how to handle it before running `git init` at
the project root — options, in order of typical preference:

- **Exclude it** via `.gitignore` (simplest; the nested repo stays wholly
  separate).
- **Fold it in** as plain files: delete its `.git` and let the outer repo
  track the files directly (loses the direct sync link to wherever it came
  from).
- **Git submodule**: `git submodule add <url> <path>` (preserves the sync
  link, adds operational overhead).

Skipping this decision and running a blind `git add -A` will silently
record the nested repo as a broken submodule reference with no URL — a
common and confusing mistake.

## 4. Write .gitignore

At minimum:

```gitignore
# macOS
.DS_Store

# anything decided to exclude in step 3, e.g.:
# some-nested-repo/
```

## 5. Initialize git and make the first commit

```bash
git init
git add CLAUDE.md .gitignore   # plus whatever else belongs in the first commit
git status                     # verify nothing unwanted is staged
git commit -m "Initial commit: project instructions and gitignore"
```

## 6. Create the GitHub repository and push

Requires the `gh` CLI, authenticated (`gh auth status` to check).

```bash
gh repo create <repo-name> --private --source=. --remote=origin --push
# use --public instead of --private if the project has no reason to stay private
```

This creates the remote repo, wires it up as `origin`, and pushes `main`
in one step. Confirm:

```bash
git remote -v
gh repo view <owner>/<repo-name> --json visibility,url,defaultBranchRef
```

## 7. (Optional) GitHub Pages for a browsable docs site

Only do this if the project's content is fine being public. **On a
personal (non-organization) GitHub account, Pages sites are publicly
viewable on the internet regardless of whether the source repo is
private** — private Pages requires an organization on GitHub Enterprise
Cloud. If the repo is private specifically to keep its content
unpublished, skip this step.

If proceeding: build a `gh-pages` branch (commonly as an orphan branch, or
via a separate `git worktree` to avoid disturbing the `main` checkout),
push it, then enable Pages and set the repo's homepage:

```bash
gh api -X POST repos/<owner>/<repo-name>/pages \
  -f source[branch]=gh-pages -f source[path]=/
gh repo edit <owner>/<repo-name> --homepage "https://<owner>.github.io/<repo-name>/"
```

## 8. First conversation with Claude Code

Open the project in Claude Code. The agent will pick up `CLAUDE.md`
automatically. On the first substantive turn that produces a derivation,
code, or other technical content worth keeping, it will start the running
session-log Artifact and create `session-log.html` per §12 — nothing
further to set up manually.
