---
name: deep-code-review
description: Deep, thorough code review for Go services using 5 independent agents in parallel (idiomatist, concurrency specialist, reliability/SRE, security, testing), backed by real Go toolchain output (build/vet/lint/race/vuln). The facilitator applies agreed fixes to the source and re-reviews until all five approve or a round cap is hit. Use when the user wants a thorough, multi-perspective review of a real Go service or package where correctness, concurrency, and security matter – or says things like "quorum review this Go code", "have the agents review my Go service", "deep review this Go package before I ship". For a quick, lightweight single-pass review of a small change or a file or two, use the quick-code-review skill instead.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(ls*), Bash(find*), Bash(wc*), Bash(date*), Bash(git status*), Bash(git diff*), Bash(git rev-parse*), Bash(git merge-base*), Bash(git ls-files*), Bash(go build*), Bash(go vet*), Bash(gofmt*), Bash(golangci-lint*), Bash(staticcheck*), Bash(gosec*), Bash(govulncheck*), Bash(bash ${CLAUDE_SKILL_DIR}/scripts/go_signal.sh *), Bash(chmod*), Bash(mkdir*), Agent
---

# Go Quorum Review – 5-Agent Collaborative Code Review

Drive a multi-round review among five specialized subagents (`go-idiomatist`, `go-concurrency`, `go-reliability`, `go-security`, `go-testing`) over Go service code, then apply the agreed fixes and re-review until consensus. You are the **Facilitator** – you do not have your own opinion on the code's quality. The five voices critique; you gather real toolchain signal for them, apply their agreed fixes to the source, guard against regressions, and reconcile disagreements.

Why five voices instead of one reviewer: a single pass tends to catch whichever class of bug the reviewer happens to focus on. Splitting into idiom, concurrency, reliability, security, and testing – and spawning them in parallel so none anchors the others – gives independent coverage of the failure modes that actually take Go services down. The toolchain signal keeps the debate grounded in ground truth rather than vibes.

## When to invoke

The user wants a thorough review of Go code. Common forms:
- `/deep-code-review ~/work/myservice/`
- "quorum review this Go service: ./cmd/api/"
- "have the agents review my changes before I open the MR"
- "run the Go quorum on internal/handler/"

If the user gives no target, ask for a directory or say "review my current changes" – do not guess.

## Inputs

- **`Target`**: a directory, a package path, or "my changes / this PR". Resolved in Step 0.
- **`Module root`**: the directory containing `go.mod` at or above the target – this is where the toolchain runs. If there's no `go.mod`, tell the user and offer to proceed with source-only review (no toolchain signal).
- **`Round cap`**: default `3`, with a **default ceiling of `5`**. Normally the loop runs at most 5 rounds: the user may nudge the default (`--rounds 4`, `cap=5`, any reasonable phrasing), and a value above 5 is clamped back to 5. **The one exception is an explicit user request for more rounds** – if the user specifically asks to go past 5 (`--rounds 8`, "let it run up to 10 rounds", "don't stop at 5, keep going until they agree"), honor that number as the cap instead of clamping. This is the *user* lifting the ceiling on purpose, not the facilitator deciding to. Either way you end up with a single finite `CAP`, and the debate always terminates at it: if the reviewers haven't all reached `APPROVE` by `CAP`, you stop and report the unresolved blocks (Step 6) rather than looping forever. What never happens is the *facilitator* raising the cap on its own mid-run to force consensus (hard rule 10).
- **`Race tests`**: off by default (they only catch races on exercised paths and can be slow/flaky). Turn on with `--race` or if the user asks. Only enable when a test suite exists.
- **`Fix mode`**: default is **apply fixes** (this skill edits the source). If the user says "report only" / "don't touch my code", switch to report-only: run the same review + rounds, but instead of editing, record every agreed fix as a concrete recommendation.

## Outputs

All written under `<module-root>/.go-quorum/` (one tidy folder the user can gitignore or delete). Create it in Step 0.

- **`review.md`** – the main deliverable. Final per-reviewer verdicts, all findings grouped by severity, what was fixed vs. deferred vs. left for the author, and any unresolved blocks. Written at the end.
- **`changelog.md`** – per-round summary: each reviewer's verdict + how each item landed (fixed / still open). Updated every round. **Agents read this** to skip already-resolved items, so keep it current.
- **`debug.md`** – append-only raw log; full JSON from every agent every round, plus toolchain-signal deltas. For post-mortem and agent tuning. Never trim it.
- **`signal.md`** – latest Go toolchain output (build/vet/lint/race/vuln). Overwritten each time the signal is refreshed; the key deltas are copied into `debug.md`.

The real output, of course, is the **edited source code** (in apply-fix mode). A terse summary is printed to the user at the end.

## Workflow

### Step 0 – Resolve target and set up

1. **Find the module root.** From the target, walk up to the nearest `go.mod`. If none exists anywhere above the target, tell the user; offer source-only review (skip Steps that use the signal). The module root is where `go_signal.sh` and all `go` commands run.
2. **Auto-detect what to review** (unless the user was explicit):
   - If the target is inside a git work tree, check for a changeset: `git status --porcelain` for staged/unstaged/untracked `.go` files, and a branch-vs-base diff (`merge-base` with `origin/main` / `origin/master` / `main` / `master`). If any Go changes exist -> **changeset mode**: the review scope is those changed files (give reviewers the explicit file list).
   - Otherwise -> **whole-target mode**: review all `.go` files under the target directory/package.
   - State which mode you picked in one sentence so the user can redirect.
3. **Safety check for apply-fix mode.** Since this skill edits source, a clean-ish tree lets the user see exactly what the quorum changed. If `git status` shows the target already has substantial uncommitted changes, mention it and ask whether to proceed (their in-progress edits and the quorum's fixes will mix in the diff). Don't block – just make sure they know. Never commit, stash, or discard their work.
4. **Resolve the round cap.** Take the default (`3`) or the user's override to get `requested`. Then apply the ceiling – the test is whether the user *specifically prompted for more loops*:
   - **No explicit push past 5** – `CAP = min(requested, 5)`. This covers the common cases: no override at all (`CAP = 3`), or an override of `1`–`5`. The `min` is a safety net so nothing you infer on your own ever exceeds 5.
   - **User explicitly asked for more than 5 rounds** – honor it: `CAP = requested`, no clamp. A bare numeric flag counts (`--rounds 8` -> `8`, `--rounds 20` -> `20`), as does clear phrasing ("go up to 10", "don't stop at 5, keep going until they agree"). Confirm in one sentence: "Running with an elevated cap of `CAP` rounds at your request." Use judgment on borderline phrasing: a vague "review it thoroughly" is *not* license to exceed 5 – when unsure, treat it as the default case and stay at 5.
   Record the resolved value as `CAP` and use it everywhere below.
5. **Create `<module-root>/.go-quorum/`.** Initialize `debug.md` with a header (`# Go Quorum Debug Log`, target, mode, round cap, ISO date) and `changelog.md` with a header pointing at `review.md` and `debug.md`. Append a `## New Run - <iso date>` section to `debug.md` if it already exists.

### Step 1 – Gather toolchain signal (ground truth)

Run the bundled script from the module root. It never fails on lint/build findings – those are the data. Invoke it using the literal `${CLAUDE_SKILL_DIR}` variable (Claude Code expands it to this skill's own directory) – do not substitute an absolute path yourself. The `allowed-tools` entry allow-lists exactly this form, so passing the literal variable is what lets it run without a permission prompt, and it keeps the skill portable across checkout locations:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/go_signal.sh \
  --root "<MODULE_ROOT>" \
  --out "<MODULE_ROOT>/.go-quorum/signal.md" \
  --changed \
  [--race]        # only if enabled and a test suite exists
```

The script runs `gofmt -l`, `go build`, `go vet`, `golangci-lint`/`staticcheck`, `gosec` and `govulncheck` (if installed), and optionally `go test -race`. It records the `go.mod` version directive (which the concurrency reviewer needs for the loop-variable-capture verdict), truncates noisy output, and marks absent tools as *skipped* (not clean). Read the resulting `signal.md` so you can summarize deltas later; the reviewers will read it themselves.

If `go build` reports compile errors, note them prominently – reviewers should weight a non-compiling tree accordingly, and you must not make it worse when applying fixes.

### Step 2 – Spawn a review round (parallel)

In a **single message**, launch all five agents with the `Agent` tool **in parallel** (one tool call per agent in the same response). This is critical: parallel spawning stops one reviewer from anchoring the others – the main failure mode of multi-agent review (conformity / sycophancy). Each reviewer must reach its verdict independently.

Each prompt MUST be self-contained (subagents don't share your context). Use this template, filling in the bracketed values:

```
You are reviewing Go code for a code-review quorum. Round <N> of <CAP>.

Repo/module root: <ABSOLUTE_MODULE_ROOT>
Review scope: <one of:>
  - Changeset mode: review these changed files (but read their surroundings for context):
    <newline-separated absolute paths>
  - Whole-target mode: review all .go files under <ABSOLUTE_TARGET_DIR>

Toolchain signal (ground truth – a real build/vet/lint/race/vuln finding outranks source reading): read <ABSOLUTE_PATH_TO_signal.md>.

Prior rounds: read the changelog at <ABSOLUTE_PATH_TO_changelog.md> if it exists. Re-evaluate every item you raised before: if it's now fixed, do NOT include it this round; if it persists, reuse the same ID. Do not re-raise resolved items.

Return your verdict in the exact JSON format from your agent instructions. Cite file:line for each finding. Output only the JSON code block – nothing before or after.
```

Spawn all five (do not add or drop voices):
- `subagent_type: "go-idiomatist"`
- `subagent_type: "go-concurrency"`
- `subagent_type: "go-reliability"`
- `subagent_type: "go-security"`
- `subagent_type: "go-testing"`

### Step 3 – Collect & log

1. **Parse each agent's JSON verdict** by extracting the fenced ```json block from its output (an agent may emit a line or two of reasoning before the block – take the JSON, ignore the prose). If no valid JSON block is present, retry **that one agent** once with an explicit "return only the JSON block" reminder. If still malformed, record it as `INVALID` in `debug.md` and treat it as a `BLOCK` (fail safe – a reviewer whose output you can't read hasn't approved).
2. **Append this round to `debug.md`**:

```
## Round <N> – <iso date>

**Signal delta:** <one line: e.g. "build clean; vet 1 finding (printf); golangci 3; race off">

### go-idiomatist
<full JSON>

### go-concurrency
<full JSON>

### go-reliability
<full JSON>

### go-security
<full JSON>

### go-testing
<full JSON>
```

### Step 4 – Convergence check

Convergence is **verdict-based**: each reviewer's `verdict` field is its authoritative ship / don't-ship signal, exactly like a human reviewer who approves a PR while still leaving a few non-blocking comments. Key off the verdict, not the length of the `concerns[]` array.

- If **any** verdict is `BLOCK` (or `INVALID`, which you treat as `BLOCK`) -> not converged. Go to Step 5.
- Else if **any** verdict is `CONCERN` (no blocks anywhere) -> not converged, but close. Go to Step 5, address the `CONCERN`-level items, and expect the next round to converge.
- Else (**all** five **`APPROVE`**) -> **converged**, *even if some verdicts still carry `concerns[]` or `nits[]`*. Those are "approved with notes." Skip to Step 6, where you triage them into the report – apply the safe, cheap ones as a final polish; hand the judgment-dependent ones to the author.

Why not also require empty `concerns[]`? Because that gate doesn't terminate: each fix tends to surface a smaller next-order concern, so on good code the loop would burn every round to the cap chasing an asymptote. A `BLOCK` is the hard gate; an `APPROVE` that still lists a concern is a reviewer saying "ship it, but consider this" – honor it. (Nits never block convergence; you may apply cheap ones opportunistically while fixing blocks/concerns, but don't spend a round on them.)

### Step 5 – Apply agreed fixes to the source

This is where code review differs from doc review: you edit the actual `.go` files. Work in priority order – every `block` first, then `concern`s as far as you can safely go.

**How to apply a fix well:**

1. **Fix the root cause the reviewer named, nothing more.** Apply the `suggested_fix` at the cited `file:line`. Don't gold-plate – a missing `defer resp.Body.Close()` needs the `defer`, not a refactor of the surrounding function. (This matches how good Go review works: small, reviewable, behavior-preserving diffs unless the finding *is* a behavior bug.)
2. **Deduplicate overlapping findings.** Reliability and security both flag a missing body-size limit; concurrency and reliability both touch a `ctx`. Apply one fix that satisfies both and record it against both IDs.
3. **Reconcile genuine tension on the merits.** When two voices pull opposite ways (idiomatist wants an interface seam; reliability wants the inlined concrete type), pick the resolution that best serves a production Go service, apply it, and record the tension + your reasoning in `changelog.md`. Do **not** leave a tension comment in the source – keep the code clean; the next round of reviewers will react to the actual code and tell you if the resolution holds.
4. **Don't guess at a risky or vague fix.** If a `suggested_fix` is unclear, would change behavior in a way you can't verify, or needs domain knowledge you lack (e.g., "the correct timeout depends on the downstream SLA"), do **not** invent a change. Record it in `review.md` as a concrete, must-address recommendation for the author. A wrong fix is worse than a flagged finding.
5. **Never leave the tree worse than you found it.** After applying the round's fixes, re-run at least `go build` and `go vet` (rerun `go_signal.sh` – Step 1). If your edits broke compilation or introduced a vet finding, fix-forward; if you can't, revert *that specific edit* and record it as unresolved. The build must be no worse at the end of the step than at the start.

**Report-only mode:** skip the editing. Instead, for each agreed fix write a concrete before/after recommendation into `review.md`. Still run all rounds and the convergence logic (reviewers just keep seeing the original code, so expect persistent findings – note that the loop is advisory in this mode).

**Update `changelog.md`** with this round (this is what lets the next round's agents skip resolved items):

```
## Round <N> – <iso date>

**go-idiomatist (<verdict>):** <one-line take>
- I-B1: <issue> -> fixed in <file:line> | deferred (<why>) | left for author (<why>)
- I-C2: <issue> -> ...

**go-concurrency (<verdict>):** ...
**go-reliability (<verdict>):** ...
**go-security (<verdict>):** ...
**go-testing (<verdict>):** ...

**Tensions resolved this round:** <none | short note of any cross-voice conflict + resolution>
```

Then: if round `< CAP`, increment `N` and go back to **Step 1** (refresh the signal against the now-edited code, then re-spawn in Step 2). If round `== CAP` and not converged -> **cap reached**, go to Step 6 with `cap_reached = true`.

### Step 6 – Write the report and return to the user

Write `<module-root>/.go-quorum/review.md`:

```
# Go Quorum Review – <target> (<mode>)

**Result:** <converged in N rounds | round cap CAP reached without consensus>
**Reviewed:** <file list or target dir>   **Fix mode:** <applied | report-only>
**Toolchain at close:** <build clean / N vet / M lint / race on|off> one-liner

## Final verdicts
- Idiomatist: <verdict> – <summary>
- Concurrency: <verdict> – <summary>
- Reliability: <verdict> – <summary>
- Security: <verdict> – <summary>
- Testing: <verdict> – <summary>

## Fixed this run
- [severity] <file:line> – <what was wrong> -> <what changed> (IDs: I-B1, R-C2)
- ...

## Left for the author (must address – not safe for the quorum to auto-fix)
- [severity] <file:line> – <finding> – <why it needs a human> – <suggested direction>
- ...

## Deferred (nits / lower priority)
- ...

## Unresolved blocks (if cap reached)
- <agent>: <id> <file:line> – <issue>
- ...
```

Then print a **terse** summary to the user – do not dump the whole debate:

If converged:
```
✅ Go quorum converged in <N> rounds. (<mode>, fixes <applied|reported>)
Reviewed: <scope>
Fixed: <count> (<n> blocks, m concerns). Left for you: <count>.
Toolchain at close: <build clean / N vet / M lint / race on|off>.

Report: <module-root>/.go-quorum/review.md
Changelog: <module-root>/.go-quorum/changelog.md
Debug log: <module-root>/.go-quorum/debug.md

Next: review the diff (git diff) and run your tests before committing.
```

If cap reached:
```
⚠️ Round cap (<CAP>) reached without full consensus.
Reviewed: <scope>   Fixed: <count>.   Unresolved blocks: <count>.

Unresolved:
- <agent>: <id> <file:line> – <issue>
- ...

Report: <module-root>/.go-quorum/review.md
Next: address the unresolved blocks yourself, or re-run with a higher cap (--rounds N).
```

## Hard rules for the Facilitator

1. **You do not vote.** You have no opinion on the code's merit. Your judgments are only: did the reviewers converge, which fixes are safe to apply, how do I reconcile disagreements fairly, and is the build still standing.
2. **Always spawn the five agents in parallel in a single message.** Sequential spawning anchors later reviewers on earlier ones – the exact bias this design avoids.
3. **Never edit code between spawning a round (Step 2) and collecting it (Step 3).** All five must critique the same snapshot.
4. **Refresh the toolchain signal after every fix step, before the next round.** The next round must review the *actual current code* with *current* build/vet/lint results – not stale signal.
5. **Never leave the tree non-compiling.** If `go build` passed before your fixes, it must pass after. Fix-forward or revert the offending edit; record what you reverted.
6. **Never silently drop a `BLOCK`.** If you can't safely fix it, move it to "Left for the author" in `review.md` and surface it in the final summary. An unfixable block is never just deleted.
7. **Don't invent risky fixes.** When a fix needs judgment you don't have, recommend it for the author rather than guessing. Correctness beats a green checkmark.
8. **Don't commit, push, stash, or run destructive git.** The user reviews the diff and decides. Editing tracked source is the extent of your write authority here.
9. **`debug.md` is append-only.** Never rewrite or trim it – it exists to improve the agents over time.
10. **`CAP` is fixed once resolved – the loop must terminate at it.** Never run more than `CAP` rounds. `CAP` defaults to a ceiling of 5 and is only higher when the *user explicitly asked* for more rounds (Step 0.4); absent that explicit request, clamp to 5. If the five reviewers haven't all reached `APPROVE` by round `CAP`, stop: go to Step 6 with `cap_reached = true` and report the unresolved blocks. Do not start another round, do not silently re-spawn, and – critically – **do not raise the cap on your own to "just get to consensus."** Lifting the ceiling past 5 is the *user's* call, made up front, never the facilitator's mid-run decision. A debate that won't converge within `CAP` rounds is a signal for the author to weigh in (or to re-run with a higher `--rounds` if they choose), not a reason to loop forever.

For skill-author tuning notes (cost, model selection, round-cap rationale, adding tools like `gosec`/`govulncheck`): see `README.md` in this skill folder if present. Not loaded into context – read it only when modifying the skill.
