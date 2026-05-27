"""Mode registry and PipelineResult normalization for named runners."""

from typing import Any, Callable, Dict, Optional

from scriptcraft.layers.layer_0_core.level_0 import (
    NamedRegistry,
    PipelineResult,
)

ModeCallable = Callable[..., Any]


class NamedRegistryWithMetadata:
    """String-keyed registry with optional per-key metadata sidecar."""

    def __init__(self, *, registry_name: str, key_label: str = "Key") -> None:
        self._registry = NamedRegistry[ModeCallable](
            registry_name=registry_name,
            key_label=key_label,
        )
        self._metadata: Dict[str, dict[str, Any]] = {}

    def register(
        self,
        key: str,
        runner: ModeCallable,
        *,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        self._registry.set(key, runner)
        self._metadata[key] = metadata or {}

    def get(self, key: str) -> Optional[ModeCallable]:
        return self._registry.get(key)

    def list_keys(self) -> list[str]:
        return self._registry.list_keys()

    def get_metadata(self, key: str) -> Optional[dict[str, Any]]:
        return self._metadata.get(key)

    def require(self, key: str) -> ModeCallable:
        return self._registry.require(key)


class ModeRegistry(NamedRegistryWithMetadata):
    """Registry for named mode/workflow runners."""

    def __init__(self) -> None:
        super().__init__(registry_name="ModeRegistry", key_label="Mode")

    def register(
        self,
        mode: str,
        runner: ModeCallable,
        *,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        super().register(mode, runner, metadata=metadata)

    def list_modes(self) -> list[str]:
        return self.list_keys()

    def get_metadata(self, mode: str) -> Optional[dict[str, Any]]:
        return super().get_metadata(mode)


def normalize_callable_result(raw: Any, *, stage: str) -> PipelineResult:
    """Normalize dict or PipelineResult returns into PipelineResult."""
    if isinstance(raw, PipelineResult):
        return raw
    if isinstance(raw, dict):
        status_value = str(raw.get("status", "success")).lower()
        success = status_value in {"success", "ok", "passed", "pass", "true"}
        error = raw.get("error")
        outputs = list(raw.get("outputs") or [])
        dataset = raw.get("dataset")
        metadata = {
            **{
                k: v
                for k, v in raw.items()
                if k not in {"mode", "status", "outputs", "dataset", "error"}
            },
            "dataset": dataset,
            "outputs": outputs,
        }
        stage_name = str(raw.get("mode", stage))
        if success:
            return PipelineResult.ok(
                stage=stage_name,
                artifacts={"outputs": str(outputs)},
                metadata=metadata,
            )
        return PipelineResult.fail(
            stage=stage_name,
            error=str(error or f"Stage '{stage}' failed"),
            artifacts={"outputs": str(outputs)},
            metadata=metadata,
        )
    return PipelineResult.ok(stage=str(stage))


def execute_mode(
    runner: ModeCallable,
    *,
    mode: str,
    input_paths: Any = None,
    output_dir: Any = None,
    domain: Any = None,
    **kwargs: Any,
) -> PipelineResult:
    """Invoke a mode runner and normalize returns into PipelineResult."""
    try:
        raw = runner(
            input_paths=input_paths,
            output_dir=output_dir,
            domain=domain,
            **kwargs,
        )
        return normalize_callable_result(raw, stage=str(mode))
    except Exception as exc:
        return PipelineResult.fail(stage=str(mode), error=str(exc))


def get_mode(registry: ModeRegistry, mode_name: str) -> ModeCallable:
    return registry.require(mode_name)
