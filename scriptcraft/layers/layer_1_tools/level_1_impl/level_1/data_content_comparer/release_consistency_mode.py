"""Orchestration for release-consistency comparison mode."""

from typing import Any, Dict, List, Optional, Sequence

from pathlib import Path

from scriptcraft.layers.layer_0_core.level_0 import PathLike
from scriptcraft.layers.layer_0_core.level_4 import load_csv_raw

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    extract_release_number,
    find_first_match,
    log_and_print,
    select_files,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import (
    get_domain_config,
    get_release_config,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    compare_release_dataframes,
)


def _resolve_diff_mode(kwargs: dict[str, Any]) -> str:
    raw = kwargs.get("comparison_mode") or kwargs.get("filter_mode") or "old_only"
    value = str(raw).strip().lower()
    return "filtered" if value in {"filtered", "filter"} else "block"


def _compare_pair(
    *,
    old_path: Path,
    new_path: Path,
    dataset: str,
    output_dir: Path,
    diff_mode: str,
    debug: bool,
    old_label: str = "R_old",
    new_label: str = "R_new",
) -> None:
    df_old = load_csv_raw(str(old_path), dtype=str)
    df_new = load_csv_raw(str(new_path), dtype=str)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{dataset}_changed_rows.csv"
    compare_release_dataframes(
        df_old,
        df_new,
        dataset,
        output_file,
        diff_mode,
        old_label,
        new_label,
        debug=debug,
    )


def _discover_release_pair(
    domain_dir: Path,
    domain_cfg: dict[str, Any],
    release_cfg: dict[str, Any],
) -> Optional[tuple[Path, Path]]:
    pattern = str(release_cfg.get("release_file_pattern", "HD Release *.csv"))
    number_re = str(release_cfg.get("release_number_regex", r"HD Release (\d+)"))
    fallbacks = list(release_cfg.get("fallback_patterns") or ["HD Release *.csv"])

    files = select_files(domain_dir, [pattern, *fallbacks])
    numbered: List[tuple[int, Path]] = []
    for path in files:
        number = extract_release_number(path.name, number_re)
        if number is not None:
            numbered.append((number, path))

    if len(numbered) >= 2:
        ordered = sorted(numbered, key=lambda item: item[0])
        return ordered[-2][1], ordered[-1][1]

    old_name = domain_cfg.get("r5_filename") or domain_cfg.get("old_filename")
    new_name = domain_cfg.get("r6_filename") or domain_cfg.get("new_filename")
    if old_name and new_name:
        old_path = domain_dir / str(old_name)
        new_path = domain_dir / str(new_name)
        if old_path.exists() and new_path.exists():
            return old_path, new_path
        old_match = find_first_match(domain_dir, str(old_name), fallbacks)
        new_match = find_first_match(domain_dir, str(new_name), fallbacks)
        if old_match and new_match:
            return old_match, new_match

    if len(numbered) == 1:
        log_and_print(f"⚠️ Only one release file found under {domain_dir}", level="warning")
    return None


def _run_domain(
    domain: str,
    output_dir: Path,
    diff_mode: str,
    debug: bool,
) -> Dict[str, Any]:
    release_cfg = get_release_config()
    domain_cfg = get_domain_config(domain) or {}
    base_path = Path(str(release_cfg.get("base_path", "data/domains")))
    domain_dir = base_path / domain

    if not domain_dir.exists():
        raise FileNotFoundError(f"Domain directory not found: {domain_dir}")

    pair = _discover_release_pair(domain_dir, domain_cfg, release_cfg)
    if pair is None:
        raise FileNotFoundError(f"Could not find release pair for domain: {domain}")

    old_path, new_path = pair
    log_and_print(f"🔍 {domain}: {old_path.name} vs {new_path.name}")
    _compare_pair(
        old_path=old_path,
        new_path=new_path,
        dataset=domain,
        output_dir=output_dir,
        diff_mode=diff_mode,
        debug=debug,
    )
    return {
        "mode": "release_consistency",
        "status": "success",
        "error": None,
        "outputs": [str(output_dir / f"{domain}_changed_rows.csv")],
        "domain": domain,
    }


def release_consistency_comparison_mode(
    input_paths: Optional[Sequence[PathLike]],
    output_dir: PathLike,
    domain: Optional[str] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Compare release CSV pairs (manual paths, single domain, or all configured domains)."""
    out = Path(output_dir)
    diff_mode = _resolve_diff_mode(kwargs)
    debug = bool(kwargs.get("debug", False))

    try:
        if input_paths and len(input_paths) >= 2:
            dataset = domain or "Manual"
            _compare_pair(
                old_path=Path(input_paths[0]),
                new_path=Path(input_paths[1]),
                dataset=dataset,
                output_dir=out,
                diff_mode=diff_mode,
                debug=debug,
            )
            return {
                "mode": "release_consistency",
                "status": "success",
                "error": None,
                "outputs": [str(out / f"{dataset}_changed_rows.csv")],
                "domain": dataset,
            }

        if domain:
            return _run_domain(domain, out, diff_mode, debug)

        release_cfg = get_release_config()
        domains_cfg = release_cfg.get("domains") or {}
        domain_names = list(domains_cfg.keys()) if isinstance(domains_cfg, dict) else []
        if not domain_names:
            raise ValueError(
                "release_consistency mode requires --domain, two input files, or domains in config"
            )

        processed: List[str] = []
        failures: List[str] = []
        outputs: List[str] = []

        for name in domain_names:
            try:
                result = _run_domain(name, out, diff_mode, debug)
                processed.append(name)
                outputs.extend(result.get("outputs") or [])
            except Exception as exc:
                log_and_print(f"❌ {name}: {exc}", level="error")
                failures.append(f"{name}: {exc}")

        if failures and not processed:
            return {
                "mode": "release_consistency",
                "status": "failed",
                "error": "; ".join(failures),
                "outputs": outputs,
                "processed_domains": processed,
                "failed_domains": failures,
            }

        return {
            "mode": "release_consistency",
            "status": "success" if not failures else "failed",
            "error": "; ".join(failures) if failures else None,
            "outputs": outputs,
            "processed_domains": processed,
            "failed_domains": failures,
        }
    except Exception as exc:
        return {
            "mode": "release_consistency",
            "status": "failed",
            "error": str(exc),
            "outputs": [],
        }
