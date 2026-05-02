"""
Common tool patterns and utilities.

This module provides simple functions to create tools with standard patterns.
"""

from typing import Any, Dict, Callable, Type, Tuple
from pathlib import Path

from layers.layer_1_tools.level_0_infra.level_0.file_ops import find_first_data_file
from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_data
from layers.layer_1_tools.level_0_infra.level_1.tool_dispatcher import dispatch_tool
from layers.layer_1_tools.level_0_infra.level_2.processing import setup_tool_files
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool
from layers.layer_1_tools.level_0_infra.level_? import save_data


# ─────────────────────────────────────────────────────────────
# TOOL FACTORY
# ─────────────────────────────────────────────────────────────

def create_standard_tool(
    tool_type: str,
    name: str,
    description: str,
    func: Callable,
    **kwargs: Any
) -> Type[BaseTool]:

    requires_dictionary: bool = kwargs.get("requires_dictionary", True)

    class StandardTool(BaseTool):
        def __init__(self) -> None:
            super().__init__(name=name, description=description)

        def validate_input(self, input_data: Any) -> bool:
            return True

        def run(self, *args: Any, **kwargs: Any) -> None:
            pass

        def validate(self, domain: str, input_path: str, output_path: str, paths: Dict[str, Any]) -> None:
            if tool_type != "validation":
                return

            if requires_dictionary:
                dataset_file, dictionary_file = setup_tool_files(paths, domain, name)
                if not dataset_file or not dictionary_file:
                    return
                func(domain, dataset_file, dictionary_file, output_path, paths)
            else:
                dataset_file = find_first_data_file(input_path)
                if not dataset_file:
                    log_and_print(f"❌ No input file found for {domain}")
                    return
                func(domain, dataset_file, output_path, paths)

        def transform(
            self,
            domain: str,
            input_path: str | Path,
            output_path: str | Path,
            paths: Dict[str, Any] | None = None
        ) -> None:

            if tool_type != "transformation":
                return

            try:
                dataset_file = find_first_data_file(input_path)
                if not dataset_file:
                    log_and_print(f"❌ No input file found for {domain}")
                    return

                df = load_data(dataset_file)
                transformed = func(df, domain)

                save_data(transformed, output_path, format="excel")
                log_and_print(f"✅ Transformed data saved to: {output_path}")

            except Exception as e:
                log_and_print(f"❌ Error processing {domain}: {e}")

        def check(self, domain: str, input_path: str, output_path: str, paths: Dict[str, Any]) -> None:
            if tool_type != "checker":
                return

            if requires_dictionary:
                dataset_file, dictionary_file = setup_tool_files(paths, domain, name)
                if not dataset_file or not dictionary_file:
                    return
                results = func(dataset_file, dictionary_file, domain)
            else:
                dataset_file = find_first_data_file(input_path)
                if not dataset_file:
                    log_and_print(f"❌ No input file found for {domain}")
                    return
                results = func(dataset_file, domain)

            if results is not None:
                save_data(results, output_path, format="excel")

    return StandardTool


# ─────────────────────────────────────────────────────────────
# RUNNER FACTORY (NOW CLEAN)
# ─────────────────────────────────────────────────────────────

def create_runner_function(
    tool_class: Type[BaseTool],
    **default_kwargs: Any
) -> Callable[[str, str, str, Dict[str, Any]], None]:

    def runner(domain: str, input_path: str, output_path: str, paths: Dict[str, Any], **kwargs: Any) -> None:

        tool = tool_class(
            name=tool_class.__name__,
            description=getattr(tool_class, "__doc__", "") or ""
        )

        execution_kwargs = {**default_kwargs, **kwargs}

        dispatch_tool(
            tool,
            domain,
            input_path,
            output_path,
            paths,
            **execution_kwargs,
        )

    return runner


# ─────────────────────────────────────────────────────────────
# SIMPLE TOOL FACTORY (UNCHANGED)
# ─────────────────────────────────────────────────────────────

def create_simple_tool(
    name: str,
    description: str,
    process_func: Callable,
    tool_type: str = "validation",
    **kwargs: Any
) -> Tuple[Type[BaseTool], Callable]:

    tool_class = create_standard_tool(tool_type, name, description, process_func, **kwargs)
    runner_func = create_runner_function(tool_class)

    return tool_class, runner_func