## Purpose

This file gives concise, actionable guidance for AI coding agents editing scripts in this small TFWR (The Farmer Was Replaced) save workspace.
Focus: making safe, small edits to the game's script files under the Save0 folder, using the game's builtin names and patterns found in `__builtins__.py`.

## Big picture

- This workspace contains per-save script files (example: `f0.py`, `f1.py`, `f2.py`) that implement a game's drone automation logic. The game engine executes these scripts; they are written in a Python-like DSL whose global builtins and constants are documented in `__builtins__.py`.
- `__builtins__.py` is an editor-support shim (types and constants): it defines `Items`, `Entities`, `Grounds`, `Unlocks`, and common function names (e.g. `move`, `plant`, `till`, `harvest`, `get_pos_x`). Do not assume conventional Python runtime semantics — treat this as a language spec.

## Key files and patterns (examples)

- `f0.py` — high-level orchestration. Example: it imports `f1` and calls `f1.resetPosition()` then loops over the farm calling `plant(f1.getEntityForSpot(i,j))` and movement functions `move(East)` / `move(North)`.
- `f1.py` — reusable helpers. Examples: `resetPosition()`, `moveToPosition(x,y)`, `handleSpotHarvestingProcess()` and `getEntityForSpot(x,y)`. `getEntityForSpot` uses modular arithmetic on `x` to pick Entities (Sunflower, Pumpkin, Tree, Carrot, Grass).
- `f2.py` — currently empty; available for new helper modules or experiments.
- `save.json` — metadata and UI state (open files, serialized inventory). Useful for reproducing editor state but not required for code edits.

## Conventions & constraints (from discovered code)

- Builtin names are case-sensitive and often Camel_Case (e.g. `Items.Water`, `Grounds.Soil`, `Entities.Sunflower`). Use exact names from `__builtins__.py` to avoid runtime errors.
- Movement constants: `North`, `South`, `East`, `West`. Use `move(Direction)` and helpers like `moveToPosition(x,y)` when available.
- Many helpers rely on global functions provided by the engine: `get_pos_x()`, `get_pos_y()`, `get_world_size()`, `can_harvest()`, `use_item(...)`, `till()`, `plant(...)`, `harvest()`.
- The language supports `import` to reuse other files (see `f0.py` importing `f1`). Keep imports minimal and refer to functions by module-qualified names when appropriate (e.g. `f1.getEntityForSpot`).

## Debugging and testing hints (repo-discoverable)

- There is no project build system in the repo; code is validated by running the game and loading the save that contains these scripts.
- Useful engine features and unlocks found in `__builtins__.py`: `Unlocks.Debug`, `Unlocks.Debug_2`, `Unlocks.Simulation`, `Unlocks.Import`, `Unlocks.Functions`. When editing, prefer small, incremental changes and verify behavior in-game.
- The save's unlock list includes `quick_print`/`print` and other debug helpers — rely on these for lightweight runtime tracing.

## Safe edit checklist for AI edits

1. Preserve public helper names in `f1.py` (e.g. `resetPosition`, `moveToPosition`, `handleSpotHarvestingProcess`) unless refactoring across all imports.
2. When adding logic, follow existing patterns: small functions, use engine builtins (e.g. `get_pos_x()`), avoid introducing heavy Python-only constructs that the engine may not support.
3. If touching `__builtins__.py`, only do so for documentation/typing improvements. Treat it as the language contract — do not rely on Python runtime behavior changes there.
4. Add tests by creating a small script (e.g. `f2.py`) that calls the function under test and prints observable state — then verify in the game.

## What to ask for when you need clarification

- If uncertain whether a builtin or behavior exists at runtime, ask for the exact name under `__builtins__.py` or provide a minimal migration patch and a short test script (example: add `f2.py` with a `self_test()` that calls `moveToPosition(0,0)` and prints `get_pos_x(), get_pos_y()`).

## Example prompts for the maintainer

- "Add a small helper in `f1.py` that returns True when a tile is harvestable without changing existing helper signatures." (Provide a 6–12 line patch and a one-line test in `f2.py`.)
- "Refactor `f0.py` to call `f1.plantCompanionAndReturn()` where applicable; preserve existing loop ordering and movement calls." (Provide a precise diff and explain runtime change in 1–2 lines.)

---
If anything in the guide is unclear or missing (for example, how scripts are loaded by the game on your machine), tell me which parts to expand and I will iterate. 
