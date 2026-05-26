# NovaPlay Game Generation

## Overview
This harness walks the agent through generating ONE novel NovaPlay
game per run. Output is a single Python source file at
`prior-games/<game_id>/<game_id>.py` that
subclasses `novaengine.NovaBaseGame`, plus a sibling `metadata.json`. The
file must conform to §3.4 of the NovaPlay Technical Report (core
knowledge priors only; novel vs. preexisting video games AND vs. the
prior-games corpus; multiple mechanics per environment; 
tutorial level first; difficulty by composition; turn-based; opaque
4-character ID).

The harness is offline pre-competition tooling. The user MAY pass an optional one-line seed describing a
desired mechanic; if absent, the agent picks autonomously, consulting
the static taxonomy of 25 reference games AND the cumulative
prior-games corpus to avoid repeating mechanics.

## FSM

```
                  ┌─────────┐
                  │  START  │
                  └────┬────┘
                       │
                       ▼
              ┌─────────────────┐
              │      study      │
              └────────┬────────┘
                       │ 25 evidence-layer analyses
                       │ + 3 source files + tech-report
                       │ design rules digested into
                       │ workspace/study-notes.md
                       ▼
              ┌─────────────────┐
              │  pick_mechanic  │
              └────────┬────────┘
                       │ mechanic chosen,
                       │ 4-char ID generated
                       ▼
              ┌─────────────────┐
              │   write_spec    │◄──────────────┐
              └────────┬────────┘               │
                       │ 9-section              │ checklist or
                       │ spec written           │ novelty issue
                       ▼                        │
              ┌─────────────────┐               │
              │  critique_spec  │───────────────┘
              └────────┬────────┘
                       │ all 26 checks pass
                       │ + NOVEL
                       ▼
              ┌─────────────────┐
              │    implement    │
              └────────┬────────┘
                       │ <id>.py + metadata.json
                       │ written under prior-games/<id>/
                       ▼
              ┌─────────────────┐
              │   smoke_test    │◄──────────────┐
              └────────┬────────┘               │
                       │ pass             fail  │
                       │                  (cap: │
                       │                  6 visits)
                       │                        │
                       │           ┌────────────┴────┐
                       │           │ fix_implementa- │
                       │           │ tion (edit src) │
                       │           └─────────────────┘
                       ▼
              ┌─────────────────┐
              │    finalize     │
              └────────┬────────┘
                       │ index row appended,
                       │ final-report.md written
                       ▼
                  ┌─────────┐
                  │ TERMINAL│
                  └─────────┘
```

## Starting State
states/study.md

## Human in the Loop
not allowed

## Notes
- Repo root is the host agent's working directory. All paths in
  this harness are relative to that root.
- Optional run input: a one-line seed string. The user passes it
  inline (e.g. via the run-harness skill argument) or leaves it
  empty for autonomous mode.
- All harness deliverables (state IO logs, mechanic-pick, spec,
  critique notes, final report) go under the per-run workspace
  (`<WORKSPACE>` per the run-harness skill = `runs/<run_id>/workspace/`
  relative to this harness root).
- The generated game (`<game_id>.py` + `metadata.json`) goes
  DIRECTLY under `prior-games/<game_id>/`,
  not under the per-run workspace. This is intentional: once
  generated, the game IS prior-games corpus data for future runs.
- The cumulative `prior-games/index.md`
  is the source of truth for novelty checks. It is read at the start
  of every run and appended to in `finalize`.