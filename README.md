# Project Template

Reusable template for starting a new Claude Code project including: a specialized `CLAUDE.md`, a running
session-log Artifact mirrored to an HTML file in the repo (`cl-log.html` in
this one — the name is a per-project choice, see §12 of `CLAUDE.md`), and a private (or public) GitHub remote. Copy this folder's `CLAUDE.md` into a new project and work through
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

Decide public vs. private first. Default to `--private` unless the project
has a specific reason to be visible to anyone (it's a template, a public
demo, documentation meant to be shared widely, etc.) — it's easy to flip a
private repo public later (`gh repo edit <owner>/<repo-name>
--visibility public`), but treat the reverse (public → private) as one-way:
assume anything ever pushed public has already been seen and mirrored, so
don't rely on flipping visibility later to un-expose it. If step 7 (GitHub
Pages) is in the plan, read its limitation note below before deciding —
on a personal account it overrides the repo's own visibility for
whatever content ends up published.

```bash
gh repo create <repo-name> --private --source=. --remote=origin --push
# use --public instead of --private if the project should be publicly visible
```

This creates the remote repo, wires it up as `origin`, and pushes `main`
in one step. Confirm:

```bash
git remote -v
gh repo view <owner>/<repo-name> --json visibility,url,defaultBranchRef
```

## 7. (Optional) GitHub Pages: a docs site that rebuilds itself

Only do this if the project's content is fine being public.

**Limitation for personal (non-organization) GitHub accounts:** a Pages
site is publicly viewable on the internet regardless of the source repo's
visibility — there is no private-Pages option outside a GitHub Enterprise
Cloud organization. A private repo with Pages enabled keeps its code and
history hidden but leaks whatever the Pages site itself renders. If the
repo is private specifically to keep its content unpublished, skip this
step, or scope carefully what the generated page actually includes.

This template's own site (`site/template.html`, `site/build.py`,
`.github/workflows/pages.yml`) is a working reference for the pattern: a
GitHub Actions workflow rebuilds a static HTML shell from `README.md` on
every push to `main` that touches it, and deploys via GitHub's native
Actions-based Pages deployment — no `gh-pages` branch to hand-maintain.
See it live at the repo's homepage, or in the source for the exact shape.

**To set this up for a new project, prompting Claude Code is a valid and
often faster path than doing it by hand** — this is an AI-assisted
template, and this is one-time, low-stakes-to-redo setup work. For
example:

> Set up a GitHub Actions workflow that rebuilds and deploys a docs site
> to GitHub Pages whenever README.md (or the site source) changes on
> main. Use `~/Projects/ProjectTemplate/site/` as a reference for the
> pattern — a `template.html` shell plus a small build script that
> renders the docs into it — but write fresh copy and design for this
> project's own subject matter rather than copying the template's page
> verbatim. Use native GitHub Actions Pages deployment (`build_type:
> workflow`), not a `gh-pages` branch.

The shape to ask for (or build by hand) is:

- A `site/template.html` shell (styling, any static sections) with a
  placeholder for generated content, and a `site/build.py` that renders
  the project's docs (e.g. `README.md`) into that placeholder and writes
  `dist/index.html`.
- `.github/workflows/pages.yml`, triggered on `push` to `main`
  (path-filtered to the docs source and `site/**`), that builds and
  deploys via `actions/configure-pages`, `actions/upload-pages-artifact`,
  and `actions/deploy-pages`.

One-time setup: create the Pages site with Actions as its source —

```bash
gh api -X POST repos/<owner>/<repo-name>/pages -f build_type=workflow
# if Pages was already enabled some other way (e.g. a gh-pages branch),
# use -X PUT instead of -X POST to switch it
```

Then push to `main` to trigger the first build, and set the homepage:

```bash
gh repo edit <owner>/<repo-name> --homepage "https://<owner>.github.io/<repo-name>/"
```

## 8. First conversation with Claude Code

Open the project in Claude Code. The agent will pick up `CLAUDE.md`
automatically. On the first substantive turn that produces a derivation,
code, or other technical content worth keeping, it will start the running
session-log Artifact and create its mirror file per §12 — nothing further
to set up manually.
