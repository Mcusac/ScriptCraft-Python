
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_tools.level_1_impl.level_0.dictionary_workflow.enhance import enhance_dictionaries
from layers.layer_1_tools.level_1_impl.level_0.dictionary_workflow.supplements import prepare_supplements, split_supplements_by_domain


def run_complete_workflow(
    input_paths: List[Union[str, Path]],
    dictionary_paths: List[Union[str, Path]],
    output_dir: Union[str, Path],
    workflow_steps: Optional[List[str]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Run the complete dictionary enhancement workflow."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if workflow_steps is None:
        workflow_steps = ["prepare", "split", "enhance"]

    log_and_print(f"🚀 Starting Dictionary Workflow with steps: {', '.join(workflow_steps)}")

    results: Dict[str, Any] = {}
    prepared_supplements = None

    if "prepare" in workflow_steps:
        log_and_print("📋 Step 1: Preparing supplements...")
        prepared_supplements = prepare_supplements(
            input_paths=input_paths,
            output_path=output_dir / "prepared_supplements.csv",
            **kwargs,
        )
        results["prepared_supplements"] = prepared_supplements
        log_and_print("✅ Step 1 completed")

    if "split" in workflow_steps:
        log_and_print("✂️ Step 2: Splitting supplements by domain...")
        if prepared_supplements is None:
            prepared_supplements = results.get("prepared_supplements")
        if prepared_supplements is None:
            prepared_supplements = prepare_supplements(input_paths=input_paths, **kwargs)
            results["prepared_supplements"] = prepared_supplements

        split_dir = output_dir / "split_supplements"
        domain_supplements = split_supplements_by_domain(
            supplements_data=prepared_supplements,
            output_dir=split_dir,
            **kwargs,
        )
        results["domain_supplements"] = domain_supplements
        log_and_print("✅ Step 2 completed")

    if "enhance" in workflow_steps:
        log_and_print("🔧 Step 3: Enhancing dictionaries...")
        split_dir = output_dir / "split_supplements"
        enhanced_dir = output_dir / "enhanced_dictionaries"

        supplement_paths: List[Union[str, Path]] = [split_dir] if "domain_supplements" in results else input_paths

        enhanced_dictionaries = enhance_dictionaries(
            dictionary_paths=dictionary_paths,
            supplement_paths=supplement_paths,
            output_dir=enhanced_dir,
            **kwargs,
        )
        results["enhanced_dictionaries"] = enhanced_dictionaries
        log_and_print("✅ Step 3 completed")

    log_and_print("🎉 Dictionary Workflow completed successfully!")
    return results

