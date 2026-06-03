# Layer drain execution status

**Last updated:** 2026-06-03 (Phase 4 hygiene complete; drain plan closed)

Layer drain moves `level_0_infra` **C** (domain) code into `level_1_impl` and promotes **A** (generic) code into `layer_0_core`, while keeping **B** (tool machinery) in infra. Phases 1–4 of the dependency-first drain plan are **complete**.

**Plan reference:** Cursor plan `finish_drain_dependency-first_fdf1e85a` (supersedes `layer_drain_planning_155da675` for tier/import gates).

---

## 2026-06-03 — Phase 1 `dictionary_driven_checker` **Done**

### Infra consolidation (within-infra DAG)

| Tier | Module | Class | Status |
|------|--------|-------|--------|
| L2 | `dictionary_validation.py`, `validate_against_dictionary` | B | Kept |
| L3 | `column_scan`, `normalization`, `outlier_flagging`, `value_check`, `special_validators` | B | Consolidated (moved off L2 where same-tier imports required) |
| L4 | `format_column_scan`, `range_scan`, `rare_value_scan`, `outlier_scan` | B | Kept; relative imports → barrel imports |
| L6 | `config_access.py` | B | Kept |
| L2 | `checker_config.py` (upward L5 import) | — | **Deleted** |
| L3/L4 | duplicate scan copies, `dictionary_driven_checker_validators.py`, orphan `*_validator.py` | — | **Deleted** |

### Impl stack

| Tier | Module | Status |
|------|--------|--------|
| L0 | `models`, `dictionary_finder` | Done (validators removed from L0 barrel) |
| L1 | `runner.py`, `date_validator`, `numeric_validator`, `text_validator` | Done (single registration path) |
| L2 | `core.py` | Done |
| L3 | `tool.py` | Done |
| L4 | `entrypoint.py` | Done |

**Call chain:**

```text
impl L4 entrypoint → impl L3 tool → impl L2 core → impl L1 runner → infra L2 validate_against_dictionary
```

### Classification (dictionary slice)

| Symbol / area | A/B/C | Disposition |
|---------------|-------|-------------|
| Column scan guards, empty result helpers | A (core L1) | Already in core; infra L3 wraps with logging |
| `validate_against_dictionary` orchestration | B | Infra L2 |
| Scan suite (format/range/rare/outlier) | B | Infra L4 |
| Pattern/categorical/coded/calculated validators | B | Infra L3 `special_validators` |
| Date/numeric/text validators | C | Impl L1 (side-effect registration in `tool.py`) |
| Config access | B | Infra L6 |

### Architecture gates added

- `test_logic_files_do_not_use_relative_imports_in_infra_or_impl`
- `test_impl_same_tree_imports_do_not_point_upward`
- `test_dictionary_driven_checker_runner.py` (3 tests: missing column skip, plugin fallback, warning vs error)

### Verification (2026-06-03)

```text
test_import_patterns                    8 passed
test_phase3_infra_candidates            5 passed
test_layer_boundaries (relative/impl)   2 passed
test_dictionary_driven_checker_runner   3 passed
architecture bundle (excl. mode_runner) 1383 passed, 332 skipped
```

---

## 2026-06-03 — Phase 2.1 `asset_reconciliation` **Corrected**

Initial drain moved all **31** domain modules into **impl** L0–L5 and pushed runner/CLI to L6/L7 — that bloated impl and did not mirror other tools.

**Correct split:**

| Layer | Role |
|-------|------|
| **infra L0–L5** | Domain DAG (constants, detection, merge, pipelines) — dependency tiers unchanged |
| **impl L0** | `runner.py` only (`run`, `run_asset_form_comparison`) — infra + core only |
| **impl L1** | `entrypoint.py` — CLI |

```text
impl L1 entrypoint → impl L0 run → infra L5 ingest → infra L4 merge → infra L3/L1/L2 domain
```

Generic helpers (`standardize_columns`, `TagNormalizationMode`, `sanitize_scalar_tag`, `log_and_print`) remain on **infra L0/L1**.

### Verification (2026-06-03 correction)

```text
test_import_patterns                    8 passed
test_layer_boundaries (relative/impl)   2 passed
test_phase3_infra_candidates            5 passed
spot: from level_1_impl.level_0 import run, run_asset_update  ok
```

---

## 2026-06-03 — Phase 2.1 `asset_reconciliation` (superseded drain)

~~Moved all **31** infra C modules from `level_0_infra/level_0–5/asset_reconciliation/` into matching **impl** tiers.~~ **Superseded** by correction above — domain restored to infra; impl kept lean at L1+L4.

<details>
<summary>Original drain notes (historical)</summary>

Moved all **31** infra C modules into impl L0–L7. Removed empty infra AR packages.

| Tier | Module | Role |
|------|--------|------|
| L0 | `constants`, `schema`, … | Domain contracts |
| L1–L5 | detection, merge, pipelines | Domain transforms |
| L6 | `runner.py` | I/O + orchestration |
| L7 | `entrypoint.py` | CLI |

</details>

---

## 2026-06-03 — Tier fixes (non-drain, dependency-legal)

| Change | Rationale |
|--------|-----------|
| `domain_old_vs_new_mode.py` → **impl L1** `data_content_comparer/` | Imports impl L0 helpers + infra L4; L0 floor violated at prior location |
| `location_lookup_workflow.py` → **infra L3** `asset_updater/` | Imports infra L2 `complete_modal_lookup` |
| `run_asset_form_comparison` merged into **impl L1** `asset_reconciliation/runner.py` | Prior impl L0 orchestrator imported core + infra (framework imports → min L1) |
| **Superseded:** full AR drain moved runner to **impl L6**, CLI to **impl L7** | Reverted — domain on **infra L0–L5**; lean **impl L0** runner + **impl L1** entrypoint |
| Root infra barrel | L10–L12 not star-exported (regenerate guard) |
| `level_10 copy/` | Removed (no remaining imports) |

---

## Wave 0 — Lowest risk

**Status:** Substantially complete.

| Item | Status |
|------|--------|
| Dedupe (`CompareColumnsResult`, `VALUE_TYPE_MAP`, `MISSING_VALUE_CODES`) | Done |
| `eval()` removal in dictionary validation | Done |
| `get_clean_numeric_series` → core delegate | Done |
| `path_resolver` / `workflow_registry` shims trimmed | Done |
| Root infra barrel (no L10–12 star export) | Done |
| `normalize_list` / dead tree cleanup | Done |

**Deviation:** `level_7/main_runner.py` and `level_8/patterns.py` restored (optional helpers) rather than deleted.

---

## Wave 1 — Core extractions

**Status:** Complete.

---

## Wave 2 — Medium risk

**Status:** Mostly complete.

| Item | Status |
|------|--------|
| `FlaggedValue` → core | Done |
| Comparer roles documented / unified entrypoints | Done |
| Handlers / `logging_handlers` merge | **Done** — `create_*` merged into `handlers.py`; `logging_handlers.py` removed |
| `subprocess_ops` / `git_service` consolidation | **Done** — both delegate to core `run_command`; typed wrappers retained (`CommandResult`, `GitResult`) |

---

## Wave 3 — Infra → impl restructuring

**Status:** **Complete** (2026-06-03).

### `asset_reconciliation` / `asset_updater` (Phase 2.1)

**Status:** **Done** (2026-06-03).

| Family | impl | infra |
|--------|------|-------|
| `asset_reconciliation` | L0 `runner.py`, L1 `entrypoint.py` | L0–L5 domain DAG |
| `asset_updater` | L0 `runner.py` (`run_asset_update`, `run_asset_update_loop`), L1 `entrypoint.py` | L0–L5 browser/session automation |

```text
impl L1 entrypoint → impl L0 run → infra L0–L5
```

Removed split impl modules (`loop_runner`, `asset_update_api`, L2 `main.py`). Domain stays on infra; impl is top boundary only.

### `release_*` C shards (Phase 2.2)

**Status:** **Mostly done** — no bulk move required.

| Area | Disposition |
|------|-------------|
| `release_pipelines` CLI/subcommands | **B** — stays infra L4/L5 |
| `release_consistency_mode` comparison engine | **A/C** — infra L0–L1; mode handler at impl L1 `data_content_comparer/release_consistency_mode.py` |
| `release_manager` tool/plugins | **impl** L0–L6 per existing normalized layout |

Remaining 2.2 work: tier worksheet on any new release C modules if added; no open mass-drain batch.

### Greenfield families (Phase 3) — **Done** (2026-06-03)

Smallest caller count first; domain on infra, lean impl top (L0 tool/engine + L4 entrypoint unless noted).

| Family | Infra | Impl | Notes |
|--------|-------|------|-------|
| `browser` | L0–L2 shared lib only | No tool package | Infra-only; no drain action |
| `dictionary_cleaner` | `clean_data` → L3 `file_clean.py`; parsers/normalizer at L2–L3 | L0 `tool.py` + L4 `entrypoint.py` | Removed impl L0 `cleaner.py`; fixed circular import + tier (L3 imports L3 parsers directly) |
| `schema_detector` | L0–L1 services | L0 `SchemaDetector` engine + L1 `SchemaDetectorTool` + L4 entrypoint | Engine no longer inherits `BaseTool` |
| `function_auditor` | `resolve_batch_target` → L3 `batch_target_resolver.py` | L0 `tool.py` + L4 entrypoint | Deleted impl L1 `cli.py` shim |
| `automated_labeler` | Domain on infra | L3 `tool.py` + L4 entrypoint | Already lean |
| `rhq_form_autofiller` | Domain on infra | L0 `tool.py` + L4 entrypoint | Duplicate impl domain files absent |

**Verification (2026-06-03):**

```text
test_layer_boundaries                   854 passed, 334 skipped
test_phase3_infra_candidates            5 passed
test_function_auditor_cli               3 passed
test_phase3_greenfield_entrypoints_exist  (in layer_boundaries) passed
```

**Note:** `test_import_patterns` requires optional `torchvision` (core augmentation import chain); not a Phase 3 regression.

---

## Phase 4 — Deferred hygiene — **Done** (2026-06-03)

| Item | Action | Status |
|------|--------|--------|
| `logging_handlers.py` | Merged `create_file_handler` / `create_console_handler` into `handlers.py` | Done |
| `subprocess_ops` / `git_service` | Documented shared core `run_command` delegation; kept typed result wrappers | Done |
| `level_10 copy/` | Stale duplicate tree | Already absent on disk |
| `level_1/git/probes.py` | Superseded by `GitService` | Already removed |
| Root infra barrel | L10–L12 not star-exported | Guard maintained |
| Backlog doc refresh | `ARCHITECTURE_backlog.md` audit date + drain closeout | Done |

**Optional follow-ups** (not blocking drain closeout): promote handler factories to core `setup_logging` path; Phase 2 impl entrypoint normalization for families listed in [`ARCHITECTURE_backlog.md`](ARCHITECTURE_backlog.md).

**Verification (2026-06-03):**

```text
test_layer_boundaries                   854 passed, 334 skipped
test_phase3_infra_candidates            5 passed
test_phase8_backlog_closure             (architecture bundle)
```

---

## Verification

From `implementations/python/python-package` with `.venv/Scripts/python.exe`:

```text
pytest scriptcraft/layers/layer_2_testing/test_import_patterns.py -q
pytest scriptcraft/layers/layer_2_testing/unit/test_architecture/test_phase3_infra_candidates.py -q
pytest scriptcraft/layers/layer_2_testing/unit/test_architecture/ --ignore=scriptcraft/layers/layer_2_testing/unit/test_architecture/test_mode_runner.py -q
```

Spot import:

```text
python -c "from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import run, run_asset_update; print('ok')"
```

---

## Related docs

- Canonical patterns: [`ARCHITECTURE_phase8.md`](ARCHITECTURE_phase8.md)
- Deferred backlog: [`ARCHITECTURE_backlog.md`](ARCHITECTURE_backlog.md)
