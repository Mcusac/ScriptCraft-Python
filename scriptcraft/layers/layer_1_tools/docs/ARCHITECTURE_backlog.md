# ScriptCraft Architecture Backlog

What remains after the Layer Cleanup Migration Roadmap (Phases 1–8). For completed work, canonical patterns, and evidence, see [`ARCHITECTURE_phase8.md`](ARCHITECTURE_phase8.md).

**Last audited:** 2026-06-03 (dependency-first drain Phases 1–4 closed)  
**Regression anchor (architecture gates):** 1400+ passed in the closeout bundle (see §Regression below).

---

## Roadmap completion summary

| Phase | Roadmap status | Verified |
|-------|----------------|----------|
| **1 — Impl internal cleanup** | Closed | Hotspot slices done; entrypoints guarded by `test_phase1_tool_entrypoints_exist` |
| **2 — Impl normalization** | Closed | Patterns in Phase 8 §2; **follow-ups remain** (see below) |
| **3 — Infra preparation** | Closed | Inventory + gates in Phase 8 §5; **extraction not executed** |
| **4 — Infra cleanup** | Closed | DAG fix, splits, alias ledger; architecture tests green |
| **5 — Infra normalization** | Closed | Canonical dispatch/config/registry/CLI; tests green |
| **6 — Core migration prep** | Closed | Inventory, naming matrix, automated gates |
| **7 — Core P0 migration** | Closed (P0 only) | C6-01/C6-02 promoted; **P1+ backlog remains** |
| **8 — Post-migration cleanup** | Closed | Facades removed, exports pruned, docs consolidated |

Phases 1–8 are **complete as roadmap milestones**. This file tracks **optional and deferred work** only.

---

## 2026-06-01 closeout update (supersedes older backlog rows)

The following plan workstreams were executed and verified in code/tests:

- C6-03 complete: generic loader extracted to infra (`level_0/file_plugin_loader.py`) and impl loader delegates.
- C6-04 complete: comparison error handling moved to `level_1/comparison_errors.py` and uses core `swallow_errors`.
- C6-05 complete: core path resolver abstractions promoted; tools resolver kept as workspace adapter.
- C6-06 complete: `DataFrameComparer` now supports injectable `id_columns`.
- Phase 3 Batch A/B complete: plugin loading and generic workflow registry mechanics extracted.
- Phase 2 follow-up normalization complete for touched families: dictionary validator, feature change checker, medvisit integrity validator, git workspace tool, and RHQ form autofiller entrypoint/shim cleanup.
- Phase 8 deferred cleanup complete: `legacy_loader` removed, stale audit artifact removed, release pipeline test/doc naming updated.
- **2026-06-03 drain closeout:** `logging_handlers.py` merged into `handlers.py`; `subprocess_ops`/`git_service` documented as core `run_command` delegates; greenfield families (Phase 3) and Wave 3 restructuring complete per [`DRAIN_EXECUTION_STATUS.md`](DRAIN_EXECUTION_STATUS.md).

Remaining backlog is intentionally deferred:

- C6-D1..C6-D6 (tool-domain surfaces remain intentionally non-core)
- Phase 3 Batch C (`dictionary_driven_checker/runner.py`) — canonical at `level_1_impl/level_1/.../runner.py`; impl-only (C6-D6); infra extraction deferred

---

## Priority overview

| Priority | Area | IDs / theme |
|----------|------|-------------|
| **High** | Core conditional promotion | C6-03–C6-06 |
| **Medium** | Infra extraction | Phase 3 Batches A–B |
| **Medium** | Impl layout normalization | Phase 2 follow-ups |
| **Low** | Core import hygiene | C6-07–C6-09 |
| **Low** | Config fallback removal | `legacy_loader` sunset |
| **Defer** | Tool-domain surfaces | C6-D1–C6-D6, Phase 3 Batch C |

---

## Phase 7 core backlog (primary technical queue)

Promote only after re-running Phase 6 migration gates per candidate (`test_phase6_core_candidates.py`, extend as needed).

### P1 — Conditional (decouple, then promote)

| ID | Current location | Blocker | Target / action |
|----|------------------|---------|-----------------|
| **C6-03** | `level_1_impl/level_0/release_manager/custom_plugin_loader.py` | Uses tools `log_and_print`; release-specific attribute names | Infra extract with neutral `PluginWorkflowRegistryProtocol` (Phase 3 Batch A), then optional core `file_plugin_loader` |
| **C6-04** | `level_0_infra/level_2/comparison_errors.py` | Depends on `emitter.log_and_print` | Align with core logging primitive; promote decorator or keep tools adapter |
| **C6-05** | `level_0_infra/level_0/path_resolver.py` | `WorkspacePathResolver` is workspace-specific | Promote **ABC + `build_domain_paths` only**; keep workspace resolver in tools |
| **C6-06** | `level_0_infra/level_3/dataframe_comparer.py` | Hard-coded `WorkspaceConfig` id columns | Inject `id_columns: Sequence[str]`; keep orchestration in tools |

### P2 — Consolidate (already in core; document + dedupe imports)

| ID | Symbol | Action |
|----|--------|--------|
| **C6-07** | `NamedRegistry` | Single documented import path; reduce duplicate discovery in tools |
| **C6-08** | `ModeRegistry`, `execute_mode` | Confirm all mode plugins use `layer_0_core.level_1.runtime` barrel |
| **C6-09** | `get_typed_plugin` | Document vs tools `PluginRegistry`; no duplicate loaders |

### Defer — not core candidates (document only)

| ID | Surface | Reason |
|----|---------|--------|
| **C6-D1** | `Config`, `PathConfig` | Workspace/study orchestration |
| **C6-D2** | `StepPipelineEngine` | Homonym with core `LifecyclePipelineBase` |
| **C6-D3** | Registry/CLI stack (L8–L12) | Tool discovery framework |
| **C6-D4** | `dispatch_tool`, `tool_dispatcher` | Tool lifecycle vocabulary |
| **C6-D5** | `ReleaseWorkflowRegistry` | Release metadata — impl-only |
| **C6-D6** | `level_1_impl/level_1/dictionary_driven_checker/runner.py` | Dictionary column conventions — impl-only |

**Before each promotion batch:** update deprecated ledger in Phase 8 §4; extend `test_phase7_core_migration.py` or add phase-specific architecture tests.

---

## Phase 3 infra extraction backlog

Inventory and gates were completed; **Batch A/B were executed**. Only Batch C remains deferred by design.

### Batch A — `custom_plugin_loader` (ties to C6-03)

- **From:** `level_1_impl/level_0/release_manager/custom_plugin_loader.py`
- **To:** `level_0_infra` generic plugin loader (then core if gates pass)
- **Contract:** `PluginWorkflowRegistryProtocol` + `load_plugins(registry, plugins_dir, pattern) -> int`
- **Gates:** `test_phase3_infra_candidates.py` (`test_custom_plugin_loader_*`)
- **Tests to add:** malformed plugin rejection, duplicate workflow skip

### Batch B — `ReleaseWorkflowRegistry` generic split

- **From:** `level_1_impl/level_0/release_manager/registry.py`
- **Action:** Split generic named-workflow mechanics from release metadata filters
- **Ownership:** Release registry stays impl; generic mechanics may become infra

### Batch C — `dictionary_driven_checker/runner.py` (defer)

- **Ownership:** Stay in impl at `level_1_impl/level_1/dictionary_driven_checker/runner.py` until dictionary-domain mapping is decoupled
- **Coverage gap:** No direct unit tests for runner (noted at Phase 3 closeout)
- **Tests to add:** missing column, plugin fallback, warning/error split

---

## Phase 2 implementation normalization follow-ups

Not blocking Phases 3–8. Migrate when touching each family.

| Family | Current layout | Target |
|--------|----------------|--------|
| `dictionary_validator`, `feature_change_checker` | L0 combined `*_main.py` | L3/L4 tool + L4 `entrypoint.py` |
| `scores_totals_checker` | L0 `score_totals_checker_main.py` | L4 entrypoint |
| `git_workspace_tool`, `git_submodule_tool`, `rhq_form_autofiller` | L0 `tool.py`, L1 `cli.py` if present | L3/L4 tool + L4 entrypoint |
| `medvisit_integrity_validator` | L0 service + L1 tool | L3 tool + L4 entrypoint |
| `asset_updater` | L0 `runner.py` + L1 `entrypoint.py` | **Done** (Phase 2.1 lean pattern) |
| `function_auditor` tool | L0 tool + L4 entrypoint | **Done** (Phase 3); tier bump optional when refactored |

**Workflow:** use level barrels; run `regenerate_package_inits --fix` after moves; do not hand-edit `__init__.py`.

---

## Phase 8 deferred cleanup

| Item | Location | Action |
|------|----------|--------|
| **Legacy config loader** | `level_3/legacy_loader.py` + branch in `level_4/yaml_loader.py` | **Closed** — fallback removed; legacy shape handled in unified loader |
| **Stale audit artifact** | `.cursor/audit-results/.../public_symbol_export_check_2026-05-21.json` | **Closed** — removed stale artifact |
| **Release pipeline import doc drift** | Phase 8 §3 mentions submodule path | **Closed** — standardized on `level_3` barrel usage/tests |
| **`logging_handlers.py`** | `level_0_infra/level_0/` | **Closed** — merged into `handlers.py` (2026-06-03 drain Phase 4) |
| **`level_10 copy/`** | `level_0_infra/` | **Closed** — stale duplicate absent |

---

## Hygiene and documentation (optional)

| Item | Notes |
|------|-------|
| Rename `test_release_pipeline_factory.py` | **Closed** — renamed to `test_generic_release_pipelines.py` |
| `level_Z/development_usage.py` | Marked experimental; consider move to `docs/examples/` |
| Phase 8 §9 in canonical doc | Slimmed to pointer here to avoid duplicate backlog tables |

---

## Regression commands

From `implementations/python/python-package` with project venv:

**Architecture gate bundle (Phases 3–8):**

```text
.\.venv\Scripts\python.exe -m pytest scriptcraft/layers/layer_2_testing/unit/test_architecture/test_layer_boundaries.py scriptcraft/layers/layer_2_testing/unit/test_infra/test_phase5_registry_cli.py scriptcraft/layers/layer_2_testing/unit/test_architecture/test_phase3_infra_candidates.py scriptcraft/layers/layer_2_testing/unit/test_architecture/test_phase6_core_candidates.py scriptcraft/layers/layer_2_testing/unit/test_architecture/test_phase7_core_migration.py scriptcraft/layers/layer_2_testing/unit/test_infra/test_phase4_splits.py scriptcraft/layers/layer_2_testing/unit/test_common/test_generic_release_pipelines.py scriptcraft/layers/layer_2_testing/unit/test_infra/test_file_plugin_loader.py scriptcraft/layers/layer_2_testing/unit/test_architecture/test_phase8_backlog_closure.py -q
```

**Phase 1 sign-off subset** (see `layer_2_testing/README.md`):

```text
.\.venv\Scripts\python.exe -m pytest scriptcraft/layers/layer_2_testing/unit/test_common/test_release_workflow_registry.py scriptcraft/layers/layer_2_testing/unit/test_common/test_release_manager_plugins.py scriptcraft/layers/layer_2_testing/unit/test_common/test_release_manager_cli.py scriptcraft/layers/layer_2_testing/unit/test_common/test_data_content_comparer_modes.py scriptcraft/layers/layer_2_testing/unit/test_architecture/test_layer_boundaries.py -q
```

---

## Suggested resume order

1. **C6-D\*** and **Batch C** — revisit only if new multi-consumer evidence appears  
2. **C6-07–C6-09** — periodic documentation/import hygiene pass  
3. **Optional tooling/doc cleanup** — only when touching adjacent files  

---

## Related docs

- **Canonical architecture (completed phases):** [`ARCHITECTURE_phase8.md`](ARCHITECTURE_phase8.md)
- **Release manager plugins (operational):** [`release_manager/plugins/README.md`](release_manager/plugins/README.md)
- **Master roadmap:** `layer_cleanup_migration_plan_327bd1a9.plan.md` (Cursor plans)
- **Agent rules:** `.cursor/rules/impl-layer-patterns.mdc`, `.cursor/rules/architecture.mdc`
