#!/usr/bin/env python3
"""Generate Phase 1 keep-vs-drain review artifacts for level_1_impl."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
IMPL = (
    ROOT
    / "implementations/python/python-package/scriptcraft/layers/layer_1_tools/level_1_impl"
)
OUT_MD = Path(__file__).resolve().parent / "layer_1_impl_phase1_keep_vs_drain_review.md"
OUT_JSON = Path(__file__).resolve().parent / "layer_1_impl_phase1_keep_vs_drain_review.json"

ENTRYPOINT_NAMES = frozenset(
    {
        "main.py",
        "runner.py",
        "orchestrator.py",
        "entrypoint.py",
        "tool.py",
        "cli.py",
        "standalone.py",
    }
)
ENTRYPOINT_SUFFIXES = ("_main.py",)

# tool folder name -> entrypoint chain (relative paths under level_1_impl)
TOOL_ENTRYPOINTS: dict[str, list[str]] = {
    "asset_reconciliation": [
        "level_8/asset_reconciliation/main.py",
        "level_7/asset_reconciliation/runner.py",
        "level_6/asset_reconciliation/orchestrator.py",
    ],
    "asset_updater": [
        "level_7/asset_updater/main.py",
        "level_6/asset_updater/asset_update_api.py",
        "level_5/asset_updater/loop_runner.py",
    ],
    "dictionary_driven_checker": [
        "level_8/dictionary_driven_checker/tool.py",
        "level_7/dictionary_driven_checker/core.py",
        "level_1/dictionary_driven_checker/runner.py",
    ],
    "dictionary_cleaner": [
        "level_6/dictionary_cleaner/entrypoint.py",
        "level_5/dictionary_cleaner/tool.py",
        "level_4/dictionary_cleaner/cleaner.py",
    ],
    "function_auditor": [
        "level_5/function_auditor/entrypoint.py",
        "level_4/function_auditor/tool.py",
        "level_3/function_auditor/batch_mode.py",
    ],
    "automated_labeler": [
        "level_3/automated_labeler/entrypoint.py",
        "level_2/automated_labeler/tool.py",
        "level_0/automated_labeler/labeling.py",
    ],
    "data_content_comparer": [
        "level_2/data_content_comparer/entrypoint.py",
        "level_1/data_content_comparer/tool.py",
        "level_0/data_content_comparer/compare.py",
    ],
    "dictionary_workflow": [
        "level_2/dictionary_workflow/entrypoint.py",
        "level_1/dictionary_workflow/tool.py",
        "level_1/dictionary_workflow/workflow.py",
    ],
    "date_format_standardizer": [
        "level_1/date_format_standardizer/entrypoint.py",
        "level_0/date_format_standardizer/tool.py",
    ],
    "generic_release_tool": [
        "level_3/generic_release_tool/cli.py",
        "level_4/generic_release_tool/standalone.py",
        "level_2/generic_release_tool/tool.py",
    ],
    "release_manager": [
        "level_4/release_manager/cli.py",
        "level_2/release_manager/tool.py",
        "level_0/release_manager/argv_compat.py",
    ],
    "git_workspace_tool": [
        "level_3/git_workspace_tool/cli.py",
        "level_4/git_workspace_tool/standalone.py",
        "level_1/git_workspace_tool/tool.py",
    ],
    "git_submodule_tool": [
        "level_4/git_submodule_tool/cli.py",
        "level_3/git_submodule_tool/tool.py",
        "level_1/git_submodule_tool/operations.py",
    ],
    "pypi_release_tool": [
        "level_3/pypi_release_tool/cli.py",
        "level_2/pypi_release_tool/tool.py",
        "level_0/pypi_release_tool/ops_upload.py",
    ],
    "schema_detector": [
        "level_1/schema_detector/schema_detector_main.py",
        "level_2/schema_detector/detector.py",
        "level_1/schema_detector/schema_builder.py",
    ],
    "rhq_form_autofiller": [
        "level_3/rhq_form_autofiller_main.py",
        "level_2/rhq_flow.py",
        "level_1/rhq_form_autolfiller/panel_filler.py",
    ],
    "score_totals_checker": [
        "level_1/score_totals_checker_main.py",
        "level_0/score_totals_checker/totals.py",
    ],
    "dictionary_validator": [
        "level_1/dictionary_validator_main.py",
        "level_1/compare_columns.py",
    ],
    "medvisit_integrity_validator": [
        "level_1/medvisit_integrity_validator_main.py",
    ],
    "feature_change_checker": [
        "level_1/feature_change_checker_main.py",
        "level_0/feature_change_checker/between_visits.py",
    ],
}

MOVE_INFRA_EXACT: dict[str, str] = {
    "level_0/browser_context.py": "Thin frame shim; infra owns frame_context",
    "level_0/rhq_form_autofiller/browser.py": "Re-export shim for selenium_launch",
    "level_0/generic_release_tool/steps_docs.py": "Duplicate stub; full impl in infra steps_docs",
    "level_0/plugins.py": "Cross-tool plugin bootstrap belongs in infra registry",
    "level_0/setup_basic_tool_environment.py": "Generic env bootstrap",
    "level_0/git_workspace_tool/operations.py": "Git ops overlap infra GitService",
    "level_0/compare_columns/types.py": "Generic comparison types",
    "level_1/compare_columns.py": "Column-set compare helper; multi-tool consumer",
    "level_0/data_content_comparer/compare.py": "Generic compare engine",
    "level_0/data_content_comparer/datasets.py": "Generic dataset loading",
    "level_0/data_content_comparer/inputs.py": "Generic input parsing",
    "level_0/data_content_comparer/logging_setup.py": "Generic logging setup",
    "level_0/data_content_comparer/reporting.py": "Generic reporting",
    "level_0/dictionary_driven_checker/dictionary_validation.py": "Generic validation primitives",
    "level_0/function_auditor/function_extractor.py": "Partially duplicated in infra function_auditor",
    "level_0/function_auditor/persistence.py": "Generic persistence pattern",
    "level_0/function_auditor/reporter.py": "Generic report formatting",
    "level_0/function_auditor/usage_searcher.py": "Generic usage search",
    "level_4/git_pipelines.py": "Cross-tool git pipeline factory",
    "level_5/release_cli.py": "Multi-tool release CLI aggregator",
    "level_5/development_usage.py": "Dev harness; not tool domain",
    "level_Z/pipeline_utils.py": "Broken shared pipeline helpers; fix then move",
    "level_Z/setup_scriptcraft_in_project.py": "Project setup utility; not tool impl",
}

MANUAL_SPLIT_EXACT: dict[str, str] = {
    "level_0/asset_updater/browser_actions.py": "Playwright actions mix domain selectors + browser primitives",
    "level_0/asset_updater/credentials.py": "Credential loading mixes RHQ env + updater domain",
    "level_1/asset_updater/credentials_loader.py": "Orchestrates credential flow; split mechanism vs domain",
    "level_3/asset_updater/session_manager.py": "Session lifecycle mixes browser infra + updater flow",
    "level_1/data_content_comparer/plugins.py": "Dual registration with infra get_plugin vs local MODE_REGISTRY",
    "level_0/release_manager_plugins/registry.py": "Separate registry from infra plugin_registry",
    "level_3/dictionary_driven_checker_validators.py": "Side-effect @register_validator imports",
    "level_1/generic_release_tool/pipelines.py": "Workflow keep; stale git step imports need rewire to infra",
    "level_3/custom_release_script.py": "Ad-hoc release script; classify after consumer audit",
}

TEMP_SHIM_EXACT: dict[str, str] = {
    "level_0/rhq_form_autofiller_env.py": "Env shim during browser/env drain",
}

TOOL_RISKS: dict[str, list[str]] = {
    "asset_reconciliation": [
        "MERGED_DETECTORS registry (level_3/registry.py) wires detectors by import path",
        "Facade star-imports across L5-L8 load many modules at import time",
        "Moving detectors without registry update breaks pipeline",
    ],
    "asset_updater": [
        "Playwright + credential order depends on rhq_form_autofiller_env",
        "browser_context ties to asset_updater constants selector",
        "loop_recovery_workflow is critical L4 piece beyond top-3 chain",
    ],
    "dictionary_driven_checker": [
        "@register_validator and level_Z plugins require import-order side effects",
        "Validators at L3 must stay importable before tool run",
    ],
    "data_content_comparer": [
        "Dual plugin paths: infra get_plugin vs impl MODE_REGISTRY",
        "Mode plugins in level_0/data_content_comparer_plugins are domain modes",
    ],
    "release_manager": [
        "ReleaseWorkflowRegistry separate from infra plugin_registry",
        "Cross-tool release_cli aggregates multiple CLIs",
    ],
    "generic_release_tool": [
        "pipelines.py may still import drained git steps from impl level_0",
        "steps_docs stub duplicates infra implementation",
    ],
    "git_workspace_tool": [
        "operations.py overlaps infra git; stale import paths possible",
    ],
    "rhq_form_autofiller": [
        "Typo package rhq_form_autolfiller affects imports",
        "Split across level_0, level_1, level_2, level_3 loose files",
    ],
    "schema_detector": [
        "Two BaseTool classes at L1 and L2; discovery could pick wrong class",
    ],
    "feature_change_checker": [
        "No wired CLI via create_entrypoint_main; class-only export",
    ],
    "level_Z": [
        "pipeline_utils has broken imports referencing deleted modules",
    ],
    "_global": [
        "Auto-generated __init__.py __all__ chains must be regenerated after moves",
        "UnifiedRegistry scans empty layer_1_tools/tools/",
        "pyproject console_scripts may reference stale layer_1_pypi paths",
    ],
}


# Proposed end-state: files that remain in level_1_impl after full drain.
# Other tool files are expected to relocate to level_0_infra (mechanism or domain modules).
TARGET_STAYS_IN_IMPL: dict[str, frozenset[str]] = {
    "asset_reconciliation": frozenset(
        {
            "level_8/asset_reconciliation/main.py",
            "level_7/asset_reconciliation/runner.py",
            "level_6/asset_reconciliation/orchestrator.py",
        }
    ),
    "asset_updater": frozenset(
        {
            "level_7/asset_updater/main.py",
            "level_6/asset_updater/asset_update_api.py",
            "level_5/asset_updater/loop_runner.py",
            # Critical orchestration beyond strict CLI chain
            "level_4/asset_updater/row_executor.py",
            "level_4/asset_updater/loop_recovery_workflow.py",
        }
    ),
    "dictionary_driven_checker": frozenset(
        {
            "level_8/dictionary_driven_checker/tool.py",
            "level_7/dictionary_driven_checker/core.py",
            "level_1/dictionary_driven_checker/runner.py",
            "level_3/dictionary_driven_checker_validators.py",
            "level_Z/dictionary_driven_checker_plugins/date_plugin.py",
            "level_Z/dictionary_driven_checker_plugins/numeric_plugin.py",
            "level_Z/dictionary_driven_checker_plugins/text_plugin.py",
        }
    ),
    "dictionary_cleaner": frozenset(
        {
            "level_6/dictionary_cleaner/entrypoint.py",
            "level_5/dictionary_cleaner/tool.py",
            "level_4/dictionary_cleaner/cleaner.py",
        }
    ),
    "function_auditor": frozenset(
        {
            "level_5/function_auditor/entrypoint.py",
            "level_4/function_auditor/tool.py",
            "level_3/function_auditor/cli.py",
        }
    ),
    "automated_labeler": frozenset(
        {
            "level_3/automated_labeler/entrypoint.py",
            "level_2/automated_labeler/tool.py",
        }
    ),
    "data_content_comparer": frozenset(
        {
            "level_2/data_content_comparer/entrypoint.py",
            "level_1/data_content_comparer/tool.py",
        }
    ),
    "dictionary_workflow": frozenset(
        {
            "level_2/dictionary_workflow/entrypoint.py",
            "level_1/dictionary_workflow/tool.py",
        }
    ),
    "date_format_standardizer": frozenset(
        {
            "level_1/date_format_standardizer/entrypoint.py",
            "level_0/date_format_standardizer/tool.py",
        }
    ),
    "generic_release_tool": frozenset(
        {
            "level_3/generic_release_tool/cli.py",
            "level_2/generic_release_tool/tool.py",
        }
    ),
    "release_manager": frozenset(
        {
            "level_4/release_manager/cli.py",
            "level_2/release_manager/tool.py",
        }
    ),
    "git_workspace_tool": frozenset(
        {
            "level_3/git_workspace_tool/cli.py",
            "level_1/git_workspace_tool/tool.py",
        }
    ),
    "git_submodule_tool": frozenset(
        {
            "level_4/git_submodule_tool/cli.py",
            "level_3/git_submodule_tool/tool.py",
        }
    ),
    "pypi_release_tool": frozenset(
        {
            "level_3/pypi_release_tool/cli.py",
            "level_2/pypi_release_tool/tool.py",
        }
    ),
    "schema_detector": frozenset(
        {
            "level_1/schema_detector/schema_detector_main.py",
            "level_2/schema_detector/detector.py",
        }
    ),
    "rhq_form_autofiller": frozenset(
        {
            "level_3/rhq_form_autofiller_main.py",
            "level_2/rhq_flow.py",
        }
    ),
    "score_totals_checker": frozenset(
        {
            "level_1/score_totals_checker_main.py",
        }
    ),
    "dictionary_validator": frozenset(
        {
            "level_1/dictionary_validator_main.py",
        }
    ),
    "medvisit_integrity_validator": frozenset(
        {
            "level_1/medvisit_integrity_validator_main.py",
        }
    ),
    "feature_change_checker": frozenset(
        {
            "level_1/feature_change_checker_main.py",
        }
    ),
    "data_content_comparer_plugins": frozenset(
        {
            "level_0/data_content_comparer_plugins/standard_mode.py",
            "level_0/data_content_comparer_plugins/domain_old_vs_new_mode.py",
            "level_0/data_content_comparer_plugins/release_consistency_mode.py",
            "level_0/data_content_comparer_plugins/rhq_mode.py",
        }
    ),
    "release_manager_plugins": frozenset(
        {
            "level_0/release_manager_plugins/pypi_plugin.py",
            "level_0/release_manager_plugins/python_package_plugin.py",
            "level_0/release_manager_plugins/workspace_sync_plugin.py",
            "level_1/release_manager_plugins/workspace_plugin.py",
        }
    ),
}


@dataclass
class FileDecision:
    path: str
    tool: str
    classification: str
    rationale: str
    in_entrypoint_chain: bool = False
    target_stays_in_impl: bool = False
    end_state_note: str = ""


def _tool_from_path(rel: str) -> str:
    m = re.search(r"level_\d+/([^/]+)/", rel)
    if m:
        return m.group(1)
    m = re.search(r"level_\d+/([^/]+\.py)", rel)
    if m and m.group(1) not in ENTRYPOINT_NAMES:
        base = m.group(1)
        if base.endswith("_main.py"):
            return base.replace("_main.py", "").replace("_main", "")
    # loose mains at level_1
    for name in (
        "dictionary_validator",
        "medvisit_integrity_validator",
        "feature_change_checker",
        "score_totals_checker",
        "compare_columns",
        "rhq_form_autofiller",
        "rhq",
    ):
        if name.replace("_", "") in rel.replace("_", ""):
            return name if name != "rhq" else "rhq"
    if "rhq_form_autofiller" in rel or "rhq_form_autolfiller" in rel or "rhq_flow" in rel:
        return "rhq_form_autofiller"
    if "rhq_login" in rel:
        return "rhq_form_autofiller"
    if rel.startswith("level_0/data_content_comparer_plugins"):
        return "data_content_comparer_plugins"
    if rel.startswith("level_0/release_manager_plugins"):
        return "release_manager_plugins"
    if rel.startswith("level_1/release_manager_plugins"):
        return "release_manager_plugins"
    if rel.startswith("level_Z/dictionary_driven_checker_plugins"):
        return "dictionary_driven_checker_plugins"
    if "git_pipelines" in rel or "release_cli" in rel:
        return "release_cluster"
    if rel.startswith("level_Z/"):
        return "level_Z_meta"
    if "/__init__.py" in rel or rel.endswith("__init__.py"):
        parts = rel.split("/")
        if len(parts) >= 2 and parts[1] not in (
            "__init__.py",
            "level_0",
            "level_1",
            "level_2",
            "level_3",
            "level_4",
            "level_5",
            "level_6",
            "level_7",
            "level_8",
            "level_Z",
        ):
            return parts[1]
        return "_package"
    return "_cross_cutting"


def _is_entrypoint_file(rel: str) -> bool:
    name = Path(rel).name
    if name in ENTRYPOINT_NAMES or name.endswith(ENTRYPOINT_SUFFIXES):
        return True
    return any(rel == p for paths in TOOL_ENTRYPOINTS.values() for p in paths)


def _target_stays(rel: str, tool: str) -> tuple[bool, str]:
    if rel.endswith("/__init__.py") or rel == "__init__.py":
        return True, "Package __init__ stays during transition; slim __all__ after drain"
    stays = TARGET_STAYS_IN_IMPL.get(tool, frozenset())
    if rel in stays:
        return True, "Proposed end-state: remains in level_1_impl"
    if tool in TARGET_STAYS_IN_IMPL:
        return False, "Proposed end-state: drain to level_0_infra (domain or mechanism module)"
    if tool in ("_package", "_cross_cutting", "release_cluster", "level_Z_meta"):
        if rel in MOVE_INFRA_EXACT or rel in TEMP_SHIM_EXACT or rel in MANUAL_SPLIT_EXACT:
            return False, "Cross-cutting: drain to infra"
        return True, "Level/package aggregator until tree restructured"
    # Thin / helper tools without explicit target set
    if _is_entrypoint_file(rel) or Path(rel).name in ("tool.py", "cli.py", "entrypoint.py"):
        return True, "Thin tool: entrypoint surface stays in impl"
    return False, "Default drain candidate for tools without explicit target set"


def _classify(rel: str, tool: str) -> tuple[str, str]:
    stays, end_note = _target_stays(rel, tool)
    if stays and _is_entrypoint_file(rel):
        return "KEEP_IMPL", "Entrypoint chain (target end-state)"

    if rel in MOVE_INFRA_EXACT:
        return "MOVE_INFRA", MOVE_INFRA_EXACT[rel]
    if rel in MANUAL_SPLIT_EXACT:
        return "MANUAL_SPLIT", MANUAL_SPLIT_EXACT[rel]
    if rel in TEMP_SHIM_EXACT:
        return "TEMP_SHIM", TEMP_SHIM_EXACT[rel]

    name = Path(rel).name
    if name == "__init__.py":
        return "KEEP_IMPL", "Package API aggregation; regenerate __all__ after child moves"

    if _is_entrypoint_file(rel):
        return "KEEP_IMPL", "Tool entrypoint chain or CLI surface"

    if name in ("tool.py", "entrypoint.py", "cli.py", "standalone.py", "main.py", "runner.py", "orchestrator.py"):
        return "KEEP_IMPL", "Named entrypoint/orchestration surface"

    # Domain signals
    domain_keywords = (
        "constants",
        "mappings",
        "tag_rules",
        "schema.py",
        "rules",
        "predicates",
        "detection",
        "workflow",
        "pipeline",
        "plugin",
        "plugins",
        "env.py",
        "_env.py",
        "credentials",
        "selectors",
        "waits",
        "panel_filler",
        "rhq",
        "asset_",
        "form_",
        "merge_",
        "dictionary",
        "validator",
        "checker",
        "labeler",
        "schema_detector",
        "release_manager",
        "git_",
        "pypi",
    )
    if any(k in rel.lower() for k in domain_keywords):
        if tool in ("data_content_comparer_plugins", "release_manager_plugins", "dictionary_driven_checker_plugins"):
            return "KEEP_IMPL", "Tool-specific plugin/mode registration"
        if "pipeline" in rel and "git_pipelines" not in rel:
            return "KEEP_IMPL", "Domain workflow composition"
        if tool.endswith("_plugins") or "plugins" in rel:
            return "KEEP_IMPL", "Plugin registration with side effects"
        if "env" in name or "credentials" in name:
            return "KEEP_IMPL", "Tool-specific environment/bootstrap"
        return "KEEP_IMPL", "Domain semantics or tool workflow"

    return "KEEP_IMPL", "Default: remain in impl until explicit drain target in infra"


def _entrypoint_chain_flag(rel: str, tool: str) -> bool:
    paths = TOOL_ENTRYPOINTS.get(tool, [])
    return rel in paths


def main() -> None:
    files = sorted(p.relative_to(IMPL).as_posix() for p in IMPL.rglob("*.py"))
    decisions: list[FileDecision] = []
    for rel in files:
        tool = _tool_from_path(rel)
        classification, rationale = _classify(rel, tool)
        stays, end_note = _target_stays(rel, tool)
        if not stays and classification == "KEEP_IMPL" and tool in TARGET_STAYS_IN_IMPL:
            if rel.endswith("/__init__.py"):
                classification = "KEEP_IMPL"
                rationale = "Package aggregator until tool tree collapsed"
            elif rel != "level_3/dictionary_driven_checker_validators.py":
                classification = "MOVE_INFRA"
                rationale = f"Drain candidate: {end_note}"
        decisions.append(
            FileDecision(
                path=rel,
                tool=tool,
                classification=classification,
                rationale=rationale,
                in_entrypoint_chain=_entrypoint_chain_flag(rel, tool),
                target_stays_in_impl=stays,
                end_state_note=end_note,
            )
        )

    counts: dict[str, int] = {}
    target_stays_count = 0
    target_drain_count = 0
    for d in decisions:
        counts[d.classification] = counts.get(d.classification, 0) + 1
        if d.target_stays_in_impl:
            target_stays_count += 1
        else:
            target_drain_count += 1

    tools = sorted({d.tool for d in decisions if d.tool not in ("_package", "_cross_cutting")})
    keep_by_tool: dict[str, list[str]] = {}
    for d in decisions:
        if d.classification == "KEEP_IMPL" and d.tool not in ("_package", "_cross_cutting", "level_Z_meta", "release_cluster"):
            keep_by_tool.setdefault(d.tool, []).append(d.path)

    phase2_queue = [
        d.path
        for d in decisions
        if d.classification in ("MOVE_INFRA", "TEMP_SHIM")
    ]
    manual_queue = [d.path for d in decisions if d.classification == "MANUAL_SPLIT"]

    payload = {
        "schema": "layer_1_impl_phase1_keep_vs_drain_review.v1",
        "generated": str(date.today()),
        "root": str(IMPL),
        "summary": {
            "total_files": len(decisions),
            "counts": counts,
            "target_end_state_stays_in_impl": target_stays_count,
            "target_end_state_drain": target_drain_count,
            "tools_reviewed": len(tools),
        },
        "target_stays_in_impl_by_tool": {
            k: sorted(v) for k, v in sorted(TARGET_STAYS_IN_IMPL.items())
        },
        "tool_entrypoint_chains_current": TOOL_ENTRYPOINTS,
        "tool_risks": TOOL_RISKS,
        "stays_in_impl_by_tool": {
            k: sorted(v) for k, v in sorted(keep_by_tool.items())
        },
        "phase2_move_queue_low_risk": sorted(
            [p for p in phase2_queue if p in TEMP_SHIM_EXACT or p in MOVE_INFRA_EXACT and "broken" not in MOVE_INFRA_EXACT.get(p, "").lower()]
        ),
        "phase2_move_queue": sorted(phase2_queue),
        "phase2_manual_queue": sorted(manual_queue),
        "files": [asdict(d) for d in decisions],
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "---",
        f"generated: {date.today()}",
        "artifact: layer_1_impl_phase1_keep_vs_drain_review",
        "schema: layer_1_impl_phase1_keep_vs_drain_review.v1",
        f"root: {IMPL}",
        "---",
        "",
        "# Phase 1 Review: `level_1_impl` Keep-vs-Drain",
        "",
        "## Summary",
        "",
        f"- **Files reviewed:** {len(decisions)}",
        f"- **Tools/packages:** {len(tools)}",
        "",
        "| Classification | Count |",
        "|---|---:|",
    ]
    for k in ("KEEP_IMPL", "MOVE_INFRA", "MANUAL_SPLIT", "TEMP_SHIM"):
        lines.append(f"| {k} | {counts.get(k, 0)} |")
    lines.append("")
    lines.append("### Target end-state (proposed)")
    lines.append("")
    lines.append(f"- **Stay in impl:** {target_stays_count} files")
    lines.append(f"- **Drain to infra:** {target_drain_count} files")

    lines.extend(
        [
            "",
            "## Rubric (applied)",
            "",
            "- **KEEP_IMPL:** Tool identity, domain rules, workflows, plugins, entrypoint chain.",
            "- **MOVE_INFRA:** Reusable mechanism, multi-tool helpers, duplicates of infra modules.",
            "- **MANUAL_SPLIT:** Mixed domain+mechanism or registry coupling requiring split.",
            "- **TEMP_SHIM:** Backward-compat re-export; delete after callers migrate.",
            "",
            "## Per-tool entrypoint chains (equivalents of runner/orchestrator/main)",
            "",
        ]
    )
    lines.append("### Current chains (as-is today)")
    lines.append("")
    for tool, chain in sorted(TOOL_ENTRYPOINTS.items()):
        lines.append(f"#### `{tool}`")
        for p in chain:
            lines.append(f"- `{p}`")
        lines.append("")

    lines.append("### Target stays in impl (proposed end-state)")
    lines.append("")
    for tool, chain in sorted(TARGET_STAYS_IN_IMPL.items()):
        lines.append(f"#### `{tool}` ({len(chain)} files)")
        for p in sorted(chain):
            lines.append(f"- `{p}`")
        lines.append("")

    lines.append("## Per-tool migration risks")
    lines.append("")
    for tool, risks in sorted(TOOL_RISKS.items()):
        lines.append(f"### `{tool}`")
        for r in risks:
            lines.append(f"- {r}")
        lines.append("")

    lines.append("## What stays in impl (target end state)")
    lines.append("")
    lines.append(
        "After draining, each tool should retain its **entrypoint chain** plus **domain-only** modules. "
        "Counts below are Phase 1 KEEP_IMPL classifications (includes `__init__.py` aggregators)."
    )
    lines.append("")
    lines.append("| Tool | KEEP_IMPL files | Entrypoint chain files |")
    lines.append("|---|---:|---:|")
    for tool in sorted(keep_by_tool.keys()):
        chain_n = sum(1 for p in keep_by_tool[tool] if p in TOOL_ENTRYPOINTS.get(tool, []))
        lines.append(f"| `{tool}` | {len(keep_by_tool[tool])} | {chain_n} |")

    lines.extend(
        [
            "",
            "## Phase 2 move queue (ordered: shims and clear infra duplicates first)",
            "",
        ]
    )
    for p in payload["phase2_move_queue_low_risk"]:
        d = next(x for x in decisions if x.path == p)
        lines.append(f"- `{p}` — **{d.classification}**: {d.rationale}")
    lines.append("")
    lines.append("## Phase 2 manual / split queue")
    lines.append("")
    for p in payload["phase2_manual_queue"]:
        d = next(x for x in decisions if x.path == p)
        lines.append(f"- `{p}` — **{d.classification}**: {d.rationale}")

    thin_tools = [
        "date_format_standardizer",
        "score_totals_checker",
        "dictionary_validator",
        "medvisit_integrity_validator",
        "feature_change_checker",
    ]
    lines.extend(
        [
            "",
            "## Phase 2 recommended execution order",
            "",
            "1. **Shims and duplicates** — `TEMP_SHIM` and `MOVE_INFRA` rows in low-risk queue (browser shims, `steps_docs` stub, `compare_columns`).",
            "2. **Cross-cutting infra** — `plugins.py`, `git_pipelines.py`, `release_cli.py`, `setup_basic_tool_environment.py`.",
            "3. **Thin tools** — "
            + ", ".join(f"`{t}`" for t in thin_tools)
            + " (few files; validate entrypoint factory wiring).",
            "4. **Medium stacks** — release/git/schema/workflow families.",
            "5. **Deep stacks last** — `asset_reconciliation`, `asset_updater`, `dictionary_driven_checker` (registry/import-order risk).",
            "",
            "**Blockers before deep-stack moves:** fix `level_Z/pipeline_utils.py` imports; rewire `generic_release_tool/pipelines.py` to infra git steps; align `pyproject.toml` console_scripts.",
            "",
        ]
    )

    lines.extend(
        [
            "",
            "## Full file decision matrix",
            "",
            "| Path | Tool | Class | Target stays | Current chain | Rationale |",
            "|---|---|---|:---:|:---:|---|",
        ]
    )
    for d in decisions:
        chain = "yes" if d.in_entrypoint_chain else ""
        stays = "yes" if d.target_stays_in_impl else "no"
        lines.append(
            f"| `{d.path}` | `{d.tool}` | {d.classification} | {stays} | {chain} | {d.rationale} |"
        )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print("Counts:", counts)


if __name__ == "__main__":
    main()
