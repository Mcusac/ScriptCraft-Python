# Release Manager custom plugins

Custom release workflows are loaded from Python modules beside the tool package:

`level_1_impl/level_4/release_manager/plugins/custom_<mode>.py`

## Contract

Each plugin module must define:

| Symbol | Type | Description |
|--------|------|-------------|
| `MODE` | `str` | Workflow name passed as `release_manager` CLI first argument |
| `WORKFLOW` | callable | `(input_paths, output_dir, domain=None, **kwargs) -> None` |
| `INFO` | `dict` (optional) | Metadata; should include `"description"` |

Registration uses `load_custom_plugins` from `level_0/release_manager/custom_plugin_loader.py`.

## Example

```python
MODE = "my_release"

INFO = {"description": "Custom release steps for my package"}

def WORKFLOW(input_paths, output_dir, domain=None, **kwargs):
    ...
```

## Builtin modes

Use builtin modes (`pypi`, `python_package`, `workspace`, `workspace_sync`, `sync`) from `level_3/release_manager/plugins.py` instead of duplicating them as custom plugins.

See [ARCHITECTURE_phase8.md](../../ARCHITECTURE_phase8.md) (§2 Implementation layer patterns) for the full implementation-layer layout.
