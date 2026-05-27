---
generated: 2026-05-21
artifact: layer_1_impl_phase1_keep_vs_drain_review
schema: layer_1_impl_phase1_keep_vs_drain_review.v1
root: C:\Users\mdc0431\dev\ScriptCraft-Workspace\implementations\python\python-package\scriptcraft\layers\layer_1_tools\level_1_impl
---

# Phase 1 Review: `level_1_impl` Keep-vs-Drain

## Summary

- **Files reviewed:** 283
- **Tools/packages:** 28

| Classification | Count |
|---|---:|
| KEEP_IMPL | 151 |
| MOVE_INFRA | 122 |
| MANUAL_SPLIT | 9 |
| TEMP_SHIM | 1 |

### Target end-state (proposed)

- **Stay in impl:** 146 files
- **Drain to infra:** 137 files

## Rubric (applied)

- **KEEP_IMPL:** Tool identity, domain rules, workflows, plugins, entrypoint chain.
- **MOVE_INFRA:** Reusable mechanism, multi-tool helpers, duplicates of infra modules.
- **MANUAL_SPLIT:** Mixed domain+mechanism or registry coupling requiring split.
- **TEMP_SHIM:** Backward-compat re-export; delete after callers migrate.

## Per-tool entrypoint chains (equivalents of runner/orchestrator/main)

### Current chains (as-is today)

#### `asset_reconciliation`
- `level_8/asset_reconciliation/main.py`
- `level_7/asset_reconciliation/runner.py`
- `level_6/asset_reconciliation/orchestrator.py`

#### `asset_updater`
- `level_7/asset_updater/main.py`
- `level_6/asset_updater/asset_update_api.py`
- `level_5/asset_updater/loop_runner.py`

#### `automated_labeler`
- `level_3/automated_labeler/entrypoint.py`
- `level_2/automated_labeler/tool.py`
- `level_0/automated_labeler/labeling.py`

#### `data_content_comparer`
- `level_2/data_content_comparer/entrypoint.py`
- `level_1/data_content_comparer/tool.py`
- `level_0/data_content_comparer/compare.py`

#### `date_format_standardizer`
- `level_1/date_format_standardizer/entrypoint.py`
- `level_0/date_format_standardizer/tool.py`

#### `dictionary_cleaner`
- `level_6/dictionary_cleaner/entrypoint.py`
- `level_5/dictionary_cleaner/tool.py`
- `level_4/dictionary_cleaner/cleaner.py`

#### `dictionary_driven_checker`
- `level_8/dictionary_driven_checker/tool.py`
- `level_7/dictionary_driven_checker/core.py`
- `level_1/dictionary_driven_checker/runner.py`

#### `dictionary_validator`
- `level_1/dictionary_validator_main.py`
- `level_1/compare_columns.py`

#### `dictionary_workflow`
- `level_2/dictionary_workflow/entrypoint.py`
- `level_1/dictionary_workflow/tool.py`
- `level_1/dictionary_workflow/workflow.py`

#### `feature_change_checker`
- `level_1/feature_change_checker_main.py`
- `level_0/feature_change_checker/between_visits.py`

#### `function_auditor`
- `level_5/function_auditor/entrypoint.py`
- `level_4/function_auditor/tool.py`
- `level_3/function_auditor/batch_mode.py`

#### `generic_release_tool`
- `level_3/generic_release_tool/cli.py`
- `level_4/generic_release_tool/standalone.py`
- `level_2/generic_release_tool/tool.py`

#### `git_submodule_tool`
- `level_4/git_submodule_tool/cli.py`
- `level_3/git_submodule_tool/tool.py`
- `level_1/git_submodule_tool/operations.py`

#### `git_workspace_tool`
- `level_3/git_workspace_tool/cli.py`
- `level_4/git_workspace_tool/standalone.py`
- `level_1/git_workspace_tool/tool.py`

#### `medvisit_integrity_validator`
- `level_1/medvisit_integrity_validator_main.py`

#### `pypi_release_tool`
- `level_3/pypi_release_tool/cli.py`
- `level_2/pypi_release_tool/tool.py`
- `level_0/pypi_release_tool/ops_upload.py`

#### `release_manager`
- `level_4/release_manager/cli.py`
- `level_2/release_manager/tool.py`
- `level_0/release_manager/argv_compat.py`

#### `rhq_form_autofiller`
- `level_3/rhq_form_autofiller_main.py`
- `level_2/rhq_flow.py`
- `level_1/rhq_form_autolfiller/panel_filler.py`

#### `schema_detector`
- `level_1/schema_detector/schema_detector_main.py`
- `level_2/schema_detector/detector.py`
- `level_1/schema_detector/schema_builder.py`

#### `score_totals_checker`
- `level_1/score_totals_checker_main.py`
- `level_0/score_totals_checker/totals.py`

### Target stays in impl (proposed end-state)

#### `asset_reconciliation` (3 files)
- `level_6/asset_reconciliation/orchestrator.py`
- `level_7/asset_reconciliation/runner.py`
- `level_8/asset_reconciliation/main.py`

#### `asset_updater` (5 files)
- `level_4/asset_updater/loop_recovery_workflow.py`
- `level_4/asset_updater/row_executor.py`
- `level_5/asset_updater/loop_runner.py`
- `level_6/asset_updater/asset_update_api.py`
- `level_7/asset_updater/main.py`

#### `automated_labeler` (2 files)
- `level_2/automated_labeler/tool.py`
- `level_3/automated_labeler/entrypoint.py`

#### `data_content_comparer` (2 files)
- `level_1/data_content_comparer/tool.py`
- `level_2/data_content_comparer/entrypoint.py`

#### `data_content_comparer_plugins` (4 files)
- `level_0/data_content_comparer_plugins/domain_old_vs_new_mode.py`
- `level_0/data_content_comparer_plugins/release_consistency_mode.py`
- `level_0/data_content_comparer_plugins/rhq_mode.py`
- `level_0/data_content_comparer_plugins/standard_mode.py`

#### `date_format_standardizer` (2 files)
- `level_0/date_format_standardizer/tool.py`
- `level_1/date_format_standardizer/entrypoint.py`

#### `dictionary_cleaner` (3 files)
- `level_4/dictionary_cleaner/cleaner.py`
- `level_5/dictionary_cleaner/tool.py`
- `level_6/dictionary_cleaner/entrypoint.py`

#### `dictionary_driven_checker` (7 files)
- `level_1/dictionary_driven_checker/runner.py`
- `level_3/dictionary_driven_checker_validators.py`
- `level_7/dictionary_driven_checker/core.py`
- `level_8/dictionary_driven_checker/tool.py`
- `level_Z/dictionary_driven_checker_plugins/date_plugin.py`
- `level_Z/dictionary_driven_checker_plugins/numeric_plugin.py`
- `level_Z/dictionary_driven_checker_plugins/text_plugin.py`

#### `dictionary_validator` (1 files)
- `level_1/dictionary_validator_main.py`

#### `dictionary_workflow` (2 files)
- `level_1/dictionary_workflow/tool.py`
- `level_2/dictionary_workflow/entrypoint.py`

#### `feature_change_checker` (1 files)
- `level_1/feature_change_checker_main.py`

#### `function_auditor` (3 files)
- `level_3/function_auditor/cli.py`
- `level_4/function_auditor/tool.py`
- `level_5/function_auditor/entrypoint.py`

#### `generic_release_tool` (2 files)
- `level_2/generic_release_tool/tool.py`
- `level_3/generic_release_tool/cli.py`

#### `git_submodule_tool` (2 files)
- `level_3/git_submodule_tool/tool.py`
- `level_4/git_submodule_tool/cli.py`

#### `git_workspace_tool` (2 files)
- `level_1/git_workspace_tool/tool.py`
- `level_3/git_workspace_tool/cli.py`

#### `medvisit_integrity_validator` (1 files)
- `level_1/medvisit_integrity_validator_main.py`

#### `pypi_release_tool` (2 files)
- `level_2/pypi_release_tool/tool.py`
- `level_3/pypi_release_tool/cli.py`

#### `release_manager` (2 files)
- `level_2/release_manager/tool.py`
- `level_4/release_manager/cli.py`

#### `release_manager_plugins` (4 files)
- `level_0/release_manager_plugins/pypi_plugin.py`
- `level_0/release_manager_plugins/python_package_plugin.py`
- `level_0/release_manager_plugins/workspace_sync_plugin.py`
- `level_1/release_manager_plugins/workspace_plugin.py`

#### `rhq_form_autofiller` (2 files)
- `level_2/rhq_flow.py`
- `level_3/rhq_form_autofiller_main.py`

#### `schema_detector` (2 files)
- `level_1/schema_detector/schema_detector_main.py`
- `level_2/schema_detector/detector.py`

#### `score_totals_checker` (1 files)
- `level_1/score_totals_checker_main.py`

## Per-tool migration risks

### `_global`
- Auto-generated __init__.py __all__ chains must be regenerated after moves
- UnifiedRegistry scans empty layer_1_tools/tools/
- pyproject console_scripts may reference stale layer_1_pypi paths

### `asset_reconciliation`
- MERGED_DETECTORS registry (level_3/registry.py) wires detectors by import path
- Facade star-imports across L5-L8 load many modules at import time
- Moving detectors without registry update breaks pipeline

### `asset_updater`
- Playwright + credential order depends on rhq_form_autofiller_env
- browser_context ties to asset_updater constants selector
- loop_recovery_workflow is critical L4 piece beyond top-3 chain

### `data_content_comparer`
- Dual plugin paths: infra get_plugin vs impl MODE_REGISTRY
- Mode plugins in level_0/data_content_comparer_plugins are domain modes

### `dictionary_driven_checker`
- @register_validator and level_Z plugins require import-order side effects
- Validators at L3 must stay importable before tool run

### `feature_change_checker`
- No wired CLI via create_entrypoint_main; class-only export

### `generic_release_tool`
- pipelines.py may still import drained git steps from impl level_0
- steps_docs stub duplicates infra implementation

### `git_workspace_tool`
- operations.py overlaps infra git; stale import paths possible

### `level_Z`
- pipeline_utils has broken imports referencing deleted modules

### `release_manager`
- ReleaseWorkflowRegistry separate from infra plugin_registry
- Cross-tool release_cli aggregates multiple CLIs

### `rhq_form_autofiller`
- Typo package rhq_form_autolfiller affects imports
- Split across level_0, level_1, level_2, level_3 loose files

### `schema_detector`
- Two BaseTool classes at L1 and L2; discovery could pick wrong class

## What stays in impl (target end state)

After draining, each tool should retain its **entrypoint chain** plus **domain-only** modules. Counts below are Phase 1 KEEP_IMPL classifications (includes `__init__.py` aggregators).

| Tool | KEEP_IMPL files | Entrypoint chain files |
|---|---:|---:|
| `asset_reconciliation` | 13 | 3 |
| `asset_updater` | 13 | 3 |
| `automated_labeler` | 6 | 2 |
| `compare_columns` | 2 | 0 |
| `data_content_comparer` | 5 | 2 |
| `data_content_comparer_plugins` | 5 | 0 |
| `date_format_standardizer` | 4 | 2 |
| `dictionary_cleaner` | 10 | 3 |
| `dictionary_driven_checker` | 8 | 3 |
| `dictionary_driven_checker_plugins` | 4 | 0 |
| `dictionary_validator` | 1 | 1 |
| `dictionary_workflow` | 5 | 2 |
| `feature_change_checker` | 2 | 1 |
| `function_auditor` | 9 | 2 |
| `generic_release_tool` | 7 | 2 |
| `git_submodule_tool` | 6 | 2 |
| `git_workspace_tool` | 6 | 2 |
| `medvisit_integrity_validator` | 1 | 1 |
| `pypi_release_tool` | 5 | 2 |
| `release_manager` | 7 | 2 |
| `release_manager_plugins` | 6 | 0 |
| `rhq` | 4 | 0 |
| `rhq_form_autofiller` | 2 | 1 |
| `rhq_form_autolfiller` | 2 | 0 |
| `schema_detector` | 5 | 2 |
| `score_totals_checker` | 2 | 1 |

## Phase 2 move queue (ordered: shims and clear infra duplicates first)

- `level_0/browser_context.py` — **MOVE_INFRA**: Thin frame shim; infra owns frame_context
- `level_0/compare_columns/types.py` — **MOVE_INFRA**: Generic comparison types
- `level_0/data_content_comparer/compare.py` — **MOVE_INFRA**: Generic compare engine
- `level_0/data_content_comparer/datasets.py` — **MOVE_INFRA**: Generic dataset loading
- `level_0/data_content_comparer/inputs.py` — **MOVE_INFRA**: Generic input parsing
- `level_0/data_content_comparer/logging_setup.py` — **MOVE_INFRA**: Generic logging setup
- `level_0/data_content_comparer/reporting.py` — **MOVE_INFRA**: Generic reporting
- `level_0/dictionary_driven_checker/dictionary_validation.py` — **MOVE_INFRA**: Generic validation primitives
- `level_0/function_auditor/function_extractor.py` — **MOVE_INFRA**: Partially duplicated in infra function_auditor
- `level_0/function_auditor/persistence.py` — **MOVE_INFRA**: Generic persistence pattern
- `level_0/function_auditor/reporter.py` — **MOVE_INFRA**: Generic report formatting
- `level_0/function_auditor/usage_searcher.py` — **MOVE_INFRA**: Generic usage search
- `level_0/generic_release_tool/steps_docs.py` — **MOVE_INFRA**: Duplicate stub; full impl in infra steps_docs
- `level_0/git_workspace_tool/operations.py` — **MOVE_INFRA**: Git ops overlap infra GitService
- `level_0/plugins.py` — **MOVE_INFRA**: Cross-tool plugin bootstrap belongs in infra registry
- `level_0/rhq_form_autofiller/browser.py` — **MOVE_INFRA**: Re-export shim for selenium_launch
- `level_0/rhq_form_autofiller_env.py` — **TEMP_SHIM**: Env shim during browser/env drain
- `level_0/setup_basic_tool_environment.py` — **MOVE_INFRA**: Generic env bootstrap
- `level_4/git_pipelines.py` — **MOVE_INFRA**: Cross-tool git pipeline factory
- `level_5/development_usage.py` — **MOVE_INFRA**: Dev harness; not tool domain
- `level_5/release_cli.py` — **MOVE_INFRA**: Multi-tool release CLI aggregator
- `level_Z/setup_scriptcraft_in_project.py` — **MOVE_INFRA**: Project setup utility; not tool impl

## Phase 2 manual / split queue

- `level_0/asset_updater/browser_actions.py` — **MANUAL_SPLIT**: Playwright actions mix domain selectors + browser primitives
- `level_0/asset_updater/credentials.py` — **MANUAL_SPLIT**: Credential loading mixes RHQ env + updater domain
- `level_0/release_manager_plugins/registry.py` — **MANUAL_SPLIT**: Separate registry from infra plugin_registry
- `level_1/asset_updater/credentials_loader.py` — **MANUAL_SPLIT**: Orchestrates credential flow; split mechanism vs domain
- `level_1/data_content_comparer/plugins.py` — **MANUAL_SPLIT**: Dual registration with infra get_plugin vs local MODE_REGISTRY
- `level_1/generic_release_tool/pipelines.py` — **MANUAL_SPLIT**: Workflow keep; stale git step imports need rewire to infra
- `level_3/asset_updater/session_manager.py` — **MANUAL_SPLIT**: Session lifecycle mixes browser infra + updater flow
- `level_3/custom_release_script.py` — **MANUAL_SPLIT**: Ad-hoc release script; classify after consumer audit
- `level_3/dictionary_driven_checker_validators.py` — **MANUAL_SPLIT**: Side-effect @register_validator imports

## Phase 2 recommended execution order

1. **Shims and duplicates** — `TEMP_SHIM` and `MOVE_INFRA` rows in low-risk queue (browser shims, `steps_docs` stub, `compare_columns`).
2. **Cross-cutting infra** — `plugins.py`, `git_pipelines.py`, `release_cli.py`, `setup_basic_tool_environment.py`.
3. **Thin tools** — `date_format_standardizer`, `score_totals_checker`, `dictionary_validator`, `medvisit_integrity_validator`, `feature_change_checker` (few files; validate entrypoint factory wiring).
4. **Medium stacks** — release/git/schema/workflow families.
5. **Deep stacks last** — `asset_reconciliation`, `asset_updater`, `dictionary_driven_checker` (registry/import-order risk).

**Blockers before deep-stack moves:** fix `level_Z/pipeline_utils.py` imports; rewire `generic_release_tool/pipelines.py` to infra git steps; align `pyproject.toml` console_scripts.


## Full file decision matrix

| Path | Tool | Class | Target stays | Current chain | Rationale |
|---|---|---|:---:|:---:|---|
| `__init__.py` | `_package` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/__init__.py` | `_package` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/asset_reconciliation/__init__.py` | `asset_reconciliation` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/asset_reconciliation/constants.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/asset_reconciliation/location_constants.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/asset_reconciliation/mappings.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/asset_reconciliation/schema.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/asset_reconciliation/tag_rules.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/asset_updater/__init__.py` | `asset_updater` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/asset_updater/browser_actions.py` | `asset_updater` | MANUAL_SPLIT | no |  | Playwright actions mix domain selectors + browser primitives |
| `level_0/asset_updater/constants.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/asset_updater/credentials.py` | `asset_updater` | MANUAL_SPLIT | no |  | Credential loading mixes RHQ env + updater domain |
| `level_0/asset_updater/errors.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/asset_updater/page_waits.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/automated_labeler/__init__.py` | `automated_labeler` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/automated_labeler/docx_template.py` | `automated_labeler` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/automated_labeler/labeling.py` | `automated_labeler` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/automated_labeler/paths.py` | `automated_labeler` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/automated_labeler/persistence.py` | `automated_labeler` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/automated_labeler/types.py` | `automated_labeler` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/browser_context.py` | `_cross_cutting` | MOVE_INFRA | no |  | Thin frame shim; infra owns frame_context |
| `level_0/compare_columns/__init__.py` | `compare_columns` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/compare_columns/types.py` | `compare_columns` | MOVE_INFRA | no |  | Generic comparison types |
| `level_0/data_content_comparer/__init__.py` | `data_content_comparer` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/data_content_comparer/compare.py` | `data_content_comparer` | MOVE_INFRA | no | yes | Generic compare engine |
| `level_0/data_content_comparer/datasets.py` | `data_content_comparer` | MOVE_INFRA | no |  | Generic dataset loading |
| `level_0/data_content_comparer/inputs.py` | `data_content_comparer` | MOVE_INFRA | no |  | Generic input parsing |
| `level_0/data_content_comparer/logging_setup.py` | `data_content_comparer` | MOVE_INFRA | no |  | Generic logging setup |
| `level_0/data_content_comparer/reporting.py` | `data_content_comparer` | MOVE_INFRA | no |  | Generic reporting |
| `level_0/data_content_comparer_plugins/__init__.py` | `data_content_comparer_plugins` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/data_content_comparer_plugins/domain_old_vs_new_mode.py` | `data_content_comparer_plugins` | KEEP_IMPL | yes |  | Tool-specific plugin/mode registration |
| `level_0/data_content_comparer_plugins/release_consistency_mode.py` | `data_content_comparer_plugins` | KEEP_IMPL | yes |  | Tool-specific plugin/mode registration |
| `level_0/data_content_comparer_plugins/rhq_mode.py` | `data_content_comparer_plugins` | KEEP_IMPL | yes |  | Tool-specific plugin/mode registration |
| `level_0/data_content_comparer_plugins/standard_mode.py` | `data_content_comparer_plugins` | KEEP_IMPL | yes |  | Tool-specific plugin/mode registration |
| `level_0/date_format_standardizer/__init__.py` | `date_format_standardizer` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/date_format_standardizer/tool.py` | `date_format_standardizer` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_0/dictionary_cleaner/__init__.py` | `dictionary_cleaner` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/dictionary_cleaner/fix_counts.py` | `dictionary_cleaner` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/dictionary_cleaner/types.py` | `dictionary_cleaner` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/dictionary_cleaner/value_types.py` | `dictionary_cleaner` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/dictionary_driven_checker/__init__.py` | `dictionary_driven_checker` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/dictionary_driven_checker/dictionary_driven_checker_env.py` | `dictionary_driven_checker` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/dictionary_driven_checker/dictionary_finder.py` | `dictionary_driven_checker` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/dictionary_driven_checker/dictionary_validation.py` | `dictionary_driven_checker` | MOVE_INFRA | no |  | Generic validation primitives |
| `level_0/dictionary_driven_checker/models.py` | `dictionary_driven_checker` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/dictionary_driven_checker/types.py` | `dictionary_driven_checker` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/dictionary_workflow/__init__.py` | `dictionary_workflow` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/dictionary_workflow/enhance.py` | `dictionary_workflow` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/dictionary_workflow/summary.py` | `dictionary_workflow` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/dictionary_workflow/supplements.py` | `dictionary_workflow` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/feature_change_checker/__init__.py` | `feature_change_checker` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/feature_change_checker/between_visits.py` | `feature_change_checker` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/feature_change_checker/categorized.py` | `feature_change_checker` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/function_auditor/__init__.py` | `function_auditor` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/function_auditor/function_extractor.py` | `function_auditor` | MOVE_INFRA | no |  | Partially duplicated in infra function_auditor |
| `level_0/function_auditor/persistence.py` | `function_auditor` | MOVE_INFRA | no |  | Generic persistence pattern |
| `level_0/function_auditor/reporter.py` | `function_auditor` | MOVE_INFRA | no |  | Generic report formatting |
| `level_0/function_auditor/usage_searcher.py` | `function_auditor` | MOVE_INFRA | no |  | Generic usage search |
| `level_0/generic_release_tool/__init__.py` | `generic_release_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/generic_release_tool/steps_docs.py` | `generic_release_tool` | MOVE_INFRA | no |  | Duplicate stub; full impl in infra steps_docs |
| `level_0/git_submodule_tool/__init__.py` | `git_submodule_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/git_workspace_tool/__init__.py` | `git_workspace_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/git_workspace_tool/operations.py` | `git_workspace_tool` | MOVE_INFRA | no |  | Git ops overlap infra GitService |
| `level_0/plugins.py` | `_cross_cutting` | MOVE_INFRA | no |  | Cross-tool plugin bootstrap belongs in infra registry |
| `level_0/pypi_release_tool/__init__.py` | `pypi_release_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/pypi_release_tool/ops_upload.py` | `pypi_release_tool` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/release_manager/__init__.py` | `release_manager` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/release_manager/argv_compat.py` | `release_manager` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/release_manager_plugins/__init__.py` | `release_manager_plugins` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/release_manager_plugins/pypi_plugin.py` | `release_manager_plugins` | KEEP_IMPL | yes |  | Tool-specific plugin/mode registration |
| `level_0/release_manager_plugins/python_package_plugin.py` | `release_manager_plugins` | KEEP_IMPL | yes |  | Tool-specific plugin/mode registration |
| `level_0/release_manager_plugins/registry.py` | `release_manager_plugins` | MANUAL_SPLIT | no |  | Separate registry from infra plugin_registry |
| `level_0/release_manager_plugins/workspace_sync_plugin.py` | `release_manager_plugins` | KEEP_IMPL | yes |  | Tool-specific plugin/mode registration |
| `level_0/rhq/__init__.py` | `rhq` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/rhq/credentials_io.py` | `rhq` | KEEP_IMPL | no |  | Tool-specific environment/bootstrap |
| `level_0/rhq_form_autofiller/__init__.py` | `rhq_form_autofiller` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/rhq_form_autofiller/browser.py` | `rhq_form_autofiller` | MOVE_INFRA | no |  | Re-export shim for selenium_launch |
| `level_0/rhq_form_autofiller/constants.py` | `rhq_form_autofiller` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/rhq_form_autofiller/data.py` | `rhq_form_autofiller` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/rhq_form_autofiller/language.py` | `rhq_form_autofiller` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/rhq_form_autofiller_env.py` | `rhq_form_autofiller` | TEMP_SHIM | no |  | Env shim during browser/env drain |
| `level_0/schema_detector/__init__.py` | `schema_detector` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/schema_detector/data_loader.py` | `schema_detector` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/schema_detector/models.py` | `schema_detector` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/schema_detector/privacy_classifier.py` | `schema_detector` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/schema_detector/type_inference.py` | `schema_detector` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/score_totals_checker/__init__.py` | `score_totals_checker` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_0/score_totals_checker/totals.py` | `score_totals_checker` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_0/setup_basic_tool_environment.py` | `_cross_cutting` | MOVE_INFRA | no |  | Generic env bootstrap |
| `level_1/__init__.py` | `_package` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/asset_reconciliation/__init__.py` | `asset_reconciliation` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/asset_reconciliation/asset_filters.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/contracts.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/debug_print.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/detection/__init__.py` | `asset_reconciliation` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/asset_reconciliation/detection/duplicates.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/detection/missing.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/detection/off_campus.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/form_debug.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/form_utils.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/location_primitives.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/sanity_checks.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/text_canonicalizer.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_reconciliation/validators.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_updater/__init__.py` | `asset_updater` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/asset_updater/asset_post_update_step.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_updater/asset_search_step.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_updater/asset_update_page_workflow.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_updater/credentials_loader.py` | `asset_updater` | MANUAL_SPLIT | no |  | Orchestrates credential flow; split mechanism vs domain |
| `level_1/asset_updater/current_asset_details_workflow.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_updater/login_workflow.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_updater/lookup_modal_workflow.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_updater/offsite_workflow.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/asset_updater/state_detector.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/automated_labeler/__init__.py` | `automated_labeler` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/automated_labeler/labeling_mode.py` | `automated_labeler` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/automated_labeler/template_mode.py` | `automated_labeler` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/compare_columns.py` | `compare_columns` | KEEP_IMPL | yes |  | Entrypoint chain (target end-state) |
| `level_1/data_content_comparer/__init__.py` | `data_content_comparer` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/data_content_comparer/plugins.py` | `data_content_comparer` | MANUAL_SPLIT | no |  | Dual registration with infra get_plugin vs local MODE_REGISTRY |
| `level_1/data_content_comparer/tool.py` | `data_content_comparer` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_1/date_format_standardizer/__init__.py` | `date_format_standardizer` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/date_format_standardizer/entrypoint.py` | `date_format_standardizer` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_1/dictionary_cleaner/__init__.py` | `dictionary_cleaner` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/dictionary_cleaner/numeric_keys.py` | `dictionary_cleaner` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/dictionary_driven_checker/__init__.py` | `dictionary_driven_checker` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/dictionary_driven_checker/runner.py` | `dictionary_driven_checker` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_1/dictionary_validator_main.py` | `dictionary_validator` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_1/dictionary_workflow/__init__.py` | `dictionary_workflow` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/dictionary_workflow/tool.py` | `dictionary_workflow` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_1/dictionary_workflow/workflow.py` | `dictionary_workflow` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/feature_change_checker_main.py` | `feature_change_checker` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_1/function_auditor/__init__.py` | `function_auditor` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/function_auditor/auditor.py` | `function_auditor` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/generic_release_tool/__init__.py` | `generic_release_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/generic_release_tool/pipelines.py` | `generic_release_tool` | MANUAL_SPLIT | no |  | Workflow keep; stale git step imports need rewire to infra |
| `level_1/generic_release_tool/version_resolver.py` | `generic_release_tool` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/git_submodule_tool/__init__.py` | `git_submodule_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/git_submodule_tool/operations.py` | `git_submodule_tool` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/git_workspace_tool/__init__.py` | `git_workspace_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/git_workspace_tool/tool.py` | `git_workspace_tool` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_1/medvisit_integrity_validator_main.py` | `medvisit_integrity_validator` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_1/release_manager/__init__.py` | `release_manager` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/release_manager_plugins/__init__.py` | `release_manager_plugins` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/release_manager_plugins/workspace_plugin.py` | `release_manager_plugins` | KEEP_IMPL | yes |  | Tool-specific plugin/mode registration |
| `level_1/rhq_form_autolfiller/__init__.py` | `rhq_form_autolfiller` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/rhq_form_autolfiller/panel_filler.py` | `rhq_form_autolfiller` | KEEP_IMPL | yes |  | Entrypoint chain (target end-state) |
| `level_1/rhq_login_actions.py` | `rhq` | KEEP_IMPL | no |  | Domain semantics or tool workflow |
| `level_1/schema_detector/__init__.py` | `schema_detector` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_1/schema_detector/column_analyzer.py` | `schema_detector` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/schema_detector/outputs.py` | `schema_detector` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/schema_detector/schema_builder.py` | `schema_detector` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_1/schema_detector/schema_detector_main.py` | `schema_detector` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_1/score_totals_checker_main.py` | `score_totals_checker` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_2/__init__.py` | `_package` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/asset_reconciliation/__init__.py` | `asset_reconciliation` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/asset_reconciliation/change_detector.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/asset_reconciliation/debug_hooks.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/asset_reconciliation/form_reshape.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/asset_reconciliation/key_semantics.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/asset_reconciliation/location_transforms.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/asset_reconciliation/tag_pipeline.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/asset_reconciliation/transforms.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/asset_reconciliation/validation.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/asset_updater/__init__.py` | `asset_updater` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/asset_updater/custodian_lookup_workflow.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/asset_updater/diagnostics.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/asset_updater/location_lookup_workflow.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/automated_labeler/__init__.py` | `automated_labeler` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/automated_labeler/tool.py` | `automated_labeler` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_2/data_content_comparer/__init__.py` | `data_content_comparer` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/data_content_comparer/entrypoint.py` | `data_content_comparer` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_2/dictionary_cleaner/__init__.py` | `dictionary_cleaner` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/dictionary_cleaner/language_blocks.py` | `dictionary_cleaner` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/dictionary_workflow/__init__.py` | `dictionary_workflow` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/dictionary_workflow/entrypoint.py` | `dictionary_workflow` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_2/function_auditor/__init__.py` | `function_auditor` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/function_auditor/batch.py` | `function_auditor` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/function_auditor/file_discovery.py` | `function_auditor` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/function_auditor/single_file_mode.py` | `function_auditor` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_2/generic_release_tool/__init__.py` | `generic_release_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/generic_release_tool/tool.py` | `generic_release_tool` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_2/pypi_release_tool/__init__.py` | `pypi_release_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/pypi_release_tool/tool.py` | `pypi_release_tool` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_2/release_manager/__init__.py` | `release_manager` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/release_manager/tool.py` | `release_manager` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_2/rhq_flow.py` | `rhq` | KEEP_IMPL | yes |  | Entrypoint chain (target end-state) |
| `level_2/schema_detector/__init__.py` | `schema_detector` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_2/schema_detector/detector.py` | `schema_detector` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_3/__init__.py` | `_package` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/asset_reconciliation/__init__.py` | `asset_reconciliation` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/asset_reconciliation/key_normalizer.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_3/asset_reconciliation/location_normalizer.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_3/asset_reconciliation/registry.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_3/asset_updater/__init__.py` | `asset_updater` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/asset_updater/asset_update_step.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_3/asset_updater/dataset_loader.py` | `asset_updater` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_3/asset_updater/session_manager.py` | `asset_updater` | MANUAL_SPLIT | no |  | Session lifecycle mixes browser infra + updater flow |
| `level_3/automated_labeler/__init__.py` | `automated_labeler` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/automated_labeler/entrypoint.py` | `automated_labeler` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_3/custom_release_script.py` | `_cross_cutting` | MANUAL_SPLIT | no |  | Ad-hoc release script; classify after consumer audit |
| `level_3/dictionary_cleaner/__init__.py` | `dictionary_cleaner` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/dictionary_cleaner/expected_values.py` | `dictionary_cleaner` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_3/dictionary_cleaner/value_parser.py` | `dictionary_cleaner` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_3/dictionary_driven_checker_validators.py` | `_cross_cutting` | MANUAL_SPLIT | no |  | Side-effect @register_validator imports |
| `level_3/function_auditor/__init__.py` | `function_auditor` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/function_auditor/batch_mode.py` | `function_auditor` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_3/function_auditor/cli.py` | `function_auditor` | KEEP_IMPL | yes |  | Entrypoint chain (target end-state) |
| `level_3/function_auditor/examples.py` | `function_auditor` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_3/generic_release_tool/__init__.py` | `generic_release_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/generic_release_tool/cli.py` | `generic_release_tool` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_3/git_submodule_tool/__init__.py` | `git_submodule_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/git_submodule_tool/tool.py` | `git_submodule_tool` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_3/git_workspace_tool/__init__.py` | `git_workspace_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/git_workspace_tool/cli.py` | `git_workspace_tool` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_3/pypi_release_tool/__init__.py` | `pypi_release_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/pypi_release_tool/cli.py` | `pypi_release_tool` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_3/release_manager/__init__.py` | `release_manager` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_3/release_manager/help_text.py` | `release_manager` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_3/rhq_form_autofiller_main.py` | `rhq_form_autofiller` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_4/__init__.py` | `_package` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_4/asset_reconciliation/__init__.py` | `asset_reconciliation` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_4/asset_reconciliation/asset_normalizer.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_4/asset_reconciliation/form_transform.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_4/asset_reconciliation/merge_key_preparer.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_4/asset_updater/__init__.py` | `asset_updater` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_4/asset_updater/loop_recovery_workflow.py` | `asset_updater` | KEEP_IMPL | yes |  | Domain semantics or tool workflow |
| `level_4/asset_updater/row_executor.py` | `asset_updater` | KEEP_IMPL | yes |  | Domain semantics or tool workflow |
| `level_4/dictionary_cleaner/__init__.py` | `dictionary_cleaner` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_4/dictionary_cleaner/cleaner.py` | `dictionary_cleaner` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_4/dictionary_cleaner/normalizer.py` | `dictionary_cleaner` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_4/function_auditor/__init__.py` | `function_auditor` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_4/function_auditor/tool.py` | `function_auditor` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_4/generic_release_tool/__init__.py` | `generic_release_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_4/generic_release_tool/standalone.py` | `generic_release_tool` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_4/git_pipelines.py` | `release_cluster` | MOVE_INFRA | no |  | Cross-tool git pipeline factory |
| `level_4/git_submodule_tool/__init__.py` | `git_submodule_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_4/git_submodule_tool/cli.py` | `git_submodule_tool` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_4/git_workspace_tool/__init__.py` | `git_workspace_tool` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_4/git_workspace_tool/standalone.py` | `git_workspace_tool` | MOVE_INFRA | no | yes | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_4/release_manager/__init__.py` | `release_manager` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_4/release_manager/cli.py` | `release_manager` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_5/__init__.py` | `_package` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_5/asset_reconciliation/__init__.py` | `asset_reconciliation` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_5/asset_reconciliation/asset_pipeline.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_5/asset_reconciliation/form_pipeline.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_5/asset_reconciliation/merge_pipeline.py` | `asset_reconciliation` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_5/asset_updater/__init__.py` | `asset_updater` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_5/asset_updater/loop_runner.py` | `asset_updater` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_5/development_usage.py` | `_cross_cutting` | MOVE_INFRA | no |  | Dev harness; not tool domain |
| `level_5/dictionary_cleaner/__init__.py` | `dictionary_cleaner` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_5/dictionary_cleaner/tool.py` | `dictionary_cleaner` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_5/function_auditor/__init__.py` | `function_auditor` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_5/function_auditor/entrypoint.py` | `function_auditor` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_5/release_cli.py` | `release_cluster` | MOVE_INFRA | no |  | Multi-tool release CLI aggregator |
| `level_6/__init__.py` | `_package` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_6/asset_reconciliation/__init__.py` | `asset_reconciliation` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_6/asset_reconciliation/orchestrator.py` | `asset_reconciliation` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_6/asset_updater/__init__.py` | `asset_updater` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_6/asset_updater/asset_update_api.py` | `asset_updater` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_6/dictionary_cleaner/__init__.py` | `dictionary_cleaner` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_6/dictionary_cleaner/entrypoint.py` | `dictionary_cleaner` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_6/dictionary_driven_checker/__init__.py` | `dictionary_driven_checker` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_6/dictionary_driven_checker/normalization.py` | `dictionary_driven_checker` | MOVE_INFRA | no |  | Drain candidate: Proposed end-state: drain to level_0_infra (domain or mechanism module) |
| `level_7/__init__.py` | `_package` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_7/asset_reconciliation/__init__.py` | `asset_reconciliation` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_7/asset_reconciliation/runner.py` | `asset_reconciliation` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_7/asset_updater/__init__.py` | `asset_updater` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_7/asset_updater/main.py` | `asset_updater` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_7/dictionary_driven_checker/__init__.py` | `dictionary_driven_checker` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_7/dictionary_driven_checker/core.py` | `dictionary_driven_checker` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_8/__init__.py` | `_package` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_8/asset_reconciliation/__init__.py` | `asset_reconciliation` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_8/asset_reconciliation/main.py` | `asset_reconciliation` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_8/dictionary_driven_checker/__init__.py` | `dictionary_driven_checker` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_8/dictionary_driven_checker/tool.py` | `dictionary_driven_checker` | KEEP_IMPL | yes | yes | Entrypoint chain (target end-state) |
| `level_Z/__init__.py` | `level_Z_meta` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_Z/dictionary_driven_checker_plugins/__init__.py` | `dictionary_driven_checker_plugins` | KEEP_IMPL | yes |  | Package API aggregation; regenerate __all__ after child moves |
| `level_Z/dictionary_driven_checker_plugins/date_plugin.py` | `dictionary_driven_checker_plugins` | KEEP_IMPL | no |  | Tool-specific plugin/mode registration |
| `level_Z/dictionary_driven_checker_plugins/numeric_plugin.py` | `dictionary_driven_checker_plugins` | KEEP_IMPL | no |  | Tool-specific plugin/mode registration |
| `level_Z/dictionary_driven_checker_plugins/text_plugin.py` | `dictionary_driven_checker_plugins` | KEEP_IMPL | no |  | Tool-specific plugin/mode registration |
| `level_Z/pipeline_utils.py` | `level_Z_meta` | MOVE_INFRA | no |  | Broken shared pipeline helpers; fix then move |
| `level_Z/setup_scriptcraft_in_project.py` | `level_Z_meta` | MOVE_INFRA | no |  | Project setup utility; not tool impl |
