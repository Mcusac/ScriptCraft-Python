"""
Pipeline factory for creating pipelines from configuration.

This module provides the factory pattern for dynamically creating pipelines
from configuration files and managing pipeline dependencies.
"""

import importlib
from functools import partial

from typing import Dict, List, Callable, Any, Optional

from layers.layer_1_tools.level_0_infra.level_2.pipeline_base import BasePipeline, PipelineStep
from layers.layer_1_tools.level_0_infra.level_2.root_schema import Config


def import_function(import_path: str) -> Callable[..., Any]:
    """
    Dynamically imports a function from its string path.
    
    Args:
        import_path: Full dotted path to the function
    
    Returns:
        Callable function object
    """
    module_path, func_name = import_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)


def build_step(step_def: Dict[str, Any]) -> PipelineStep:
    """
    Builds a pipeline step from a config dictionary.
    
    This version is fully configuration-driven and does NOT contain
    any hardcoded tool-specific logic.
    
    Args:
        step_def: Dictionary with step configuration
    
    Returns:
        PipelineStep object
    """
    func = import_function(step_def["func"])

    # Generic, config-driven kwargs injection (replaces all hardcoded logic)
    extra_kwargs = step_def.get("extra_kwargs") or step_def.get("partial_kwargs") or {}

    if extra_kwargs:
        func = partial(func, **extra_kwargs)

    return PipelineStep(
        name=step_def["name"],
        log_filename=step_def["log"],
        qc_func=func,
        input_key=step_def.get("input_key", "raw_data"),
        output_filename=step_def.get("output_filename"),
        check_exists=step_def.get("check_exists", False),
        run_mode=step_def.get("run_mode", "domain"),
        tags=step_def.get("tags", [])
    )


class PipelineFactory:
    """Factory class for creating pipelines from configuration."""
    
    def __init__(self, config_obj: Optional[Any] = None) -> None:
        """Initialize the pipeline factory.
        
        Args:
            config_obj: Optional Config object. If None, loads default config.
        """
        if config_obj is None:
            try:
                config_obj = Config.from_yaml("config.yaml")
            except Exception:
                config_obj = type('Config', (), {
                    'pipelines': {},
                    'pipeline_descriptions': {},
                    'domains': []
                })()

        self.config_obj = config_obj
        self.config = {
            "pipelines": getattr(config_obj, 'pipelines', {}),
            "pipeline_descriptions": getattr(config_obj, "pipeline_descriptions", {})
        }
        self.pipeline_defs = self.config.get("pipelines", {})
        self.pipelines: Dict[str, BasePipeline] = {}

    def _build_pipeline(self, name: str, pipeline_config: Any) -> BasePipeline:
        """
        Build a pipeline from its configuration.
        """
        config_obj = self.config_obj

        if isinstance(pipeline_config, dict) and "steps" in pipeline_config:
            description = pipeline_config.get("description", "")
            steps_or_refs = pipeline_config["steps"]
        else:
            description = ""
            steps_or_refs = pipeline_config

        pipeline = BasePipeline(config_obj, name=name, description=description)

        for item in steps_or_refs:
            if isinstance(item, dict):
                if "func" in item:
                    pipeline.add_step(build_step(item))
                elif "ref" in item:
                    ref_pipeline = self.pipelines.get(item["ref"])
                    if ref_pipeline:
                        for step in ref_pipeline.steps:
                            pipeline.add_step(step)
            else:
                ref_pipeline = self.pipelines.get(item)
                if ref_pipeline:
                    for step in ref_pipeline.steps:
                        pipeline.add_step(step)

        return pipeline

    def create_pipelines(self) -> Dict[str, BasePipeline]:
        """
        Create all pipelines defined in config.
        """
        for name, pipeline_config in self.pipeline_defs.items():
            if isinstance(pipeline_config, dict) and "steps" in pipeline_config:
                steps_list = pipeline_config["steps"]
            else:
                steps_list = pipeline_config

            if all(not isinstance(item, dict) or "func" in item for item in steps_list):
                self.pipelines[name] = self._build_pipeline(name, pipeline_config)

        for name, pipeline_config in self.pipeline_defs.items():
            if name not in self.pipelines:
                self.pipelines[name] = self._build_pipeline(name, pipeline_config)

        return self.pipelines


def get_pipeline_steps() -> Dict[str, List[PipelineStep]]:
    """
    Get all pipeline steps defined in config.yaml.
    """
    factory = PipelineFactory()
    pipelines = factory.create_pipelines()
    return {name: pipeline.steps for name, pipeline in pipelines.items()}