"""CLI/pipeline entrypoint for the dictionary workflow tool."""

from typing import Any

from layers.layer_1_pypi.level_1_impl.level_0.main_common import create_entrypoint_main
from layers.layer_1_pypi.level_1_impl.level_1.dictionary_workflow.tool import DictionaryWorkflow


def _workflow_run_kwargs(args) -> dict[str, Any]:
    return {
        "input_paths": args.input_paths,
        "dictionary_paths": args.dictionary_paths,
        "output_dir": args.output_dir,
        "workflow_steps": args.workflow_steps,
        "merge_strategy": args.merge_strategy,
        "enhancement_strategy": args.enhancement_strategy,
        "domain_column": args.domain_column,
        "clean_data": args.clean_data,
    }


main = create_entrypoint_main(
    DictionaryWorkflow,
    tool_name="dictionary_workflow",
    description="📚 Complete dictionary enhancement workflow tool",
    parser_kind="dictionary_workflow",
    run_kwargs_builder=_workflow_run_kwargs,
)

