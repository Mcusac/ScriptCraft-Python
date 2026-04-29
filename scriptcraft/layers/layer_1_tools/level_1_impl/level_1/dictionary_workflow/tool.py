"""DictionaryWorkflow tool implementation (level_1)."""

from pathlib import Path
from typing import Any, Optional, Union

from layers.layer_1_pypi.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_pypi.level_1_impl.level_0.dictionary_workflow import (
    run_complete_workflow,
    log_workflow_summary,
)


class DictionaryWorkflow(BaseTool):
    """Tool for complete dictionary enhancement workflow."""

    def __init__(self) -> None:
        super().__init__(
            name="Dictionary Workflow",
            description="📚 Complete dictionary enhancement workflow tool",
            tool_name="dictionary_workflow",
        )

        tool_config = self.get_tool_config()
        self.default_workflow_steps = tool_config.get(
            "default_workflow_steps", ["prepare", "split", "enhance"]
        )
        self.default_merge_strategy = tool_config.get("default_merge_strategy", "outer")
        self.default_enhancement_strategy = tool_config.get(
            "default_enhancement_strategy", "append"
        )

    def run(
        self,
        input_paths: Optional[list[Union[str, Path]]] = None,
        dictionary_paths: Optional[list[Union[str, Path]]] = None,
        output_dir: Optional[Union[str, Path]] = None,
        workflow_steps: Optional[list[str]] = None,
        merge_strategy: Optional[str] = None,
        enhancement_strategy: Optional[str] = None,
        domain_column: Optional[str] = None,
        clean_data: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        self.log_start()

        try:
            if not self.validate_input_files(input_paths or []):
                raise ValueError("❌ No input supplement files provided")

            if not self.validate_input_files(dictionary_paths or []):
                raise ValueError("❌ No input dictionary files provided")

            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)

            resolved_workflow_steps = workflow_steps or self.default_workflow_steps
            resolved_merge_strategy = merge_strategy or self.default_merge_strategy
            resolved_enhancement_strategy = (
                enhancement_strategy or self.default_enhancement_strategy
            )
            resolved_domain_column = domain_column or "domain"
            resolved_clean_data = clean_data if clean_data is not None else True

            results = run_complete_workflow(
                input_paths=input_paths or [],
                dictionary_paths=dictionary_paths or [],
                output_dir=output_path,
                workflow_steps=resolved_workflow_steps,
                merge_strategy=resolved_merge_strategy,
                enhancement_strategy=resolved_enhancement_strategy,
                domain_column=resolved_domain_column,
                clean_data=resolved_clean_data,
                **kwargs,
            )

            log_workflow_summary(results, output_path)
            self.log_completion()

        except Exception as e:
            self.log_error(f"Error: {e}")
            raise

