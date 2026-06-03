# layer_2_testing

Tests for ScriptCraft `python-package` layer imports and Phase 1 tool wiring.

## Phase 1 verification (release manager + data content comparer)

From `implementations/python/python-package` with `PYTHONPATH` set to this directory:

```powershell
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"
& ".venv\Scripts\python.exe" -m pytest scriptcraft/layers/layer_2_testing/unit/test_common/test_release_workflow_registry.py scriptcraft/layers/layer_2_testing/unit/test_common/test_release_manager_plugins.py scriptcraft/layers/layer_2_testing/unit/test_common/test_release_manager_cli.py scriptcraft/layers/layer_2_testing/unit/test_common/test_data_content_comparer_modes.py scriptcraft/layers/layer_2_testing/unit/test_architecture/test_layer_boundaries.py -q
& ".venv\Scripts\python.exe" scriptcraft/layers/layer_2_testing/test_import_patterns.py
& ".venv\Scripts\python.exe" -m pytest scriptcraft/layers/layer_2_testing/test_package_integrity.py::TestToolFunctionality -q
```

Phase 1 layout (under `level_1_impl`):

- L0 `release_manager/` — registry, PyPI dist, build/git, workspace version, workspace sync
- L1 `release_manager/` — PyPI steps, `workspace_release_pipeline`
- L2 `release_manager/` — `python_package_plugin`, `workspace_release_mode`
- L3 `release_manager/` — `load_builtin_plugins`; L3 `data_content_comparer/` — tool
- L4 `data_content_comparer/entrypoint.py`; L4 `release_manager/tool.py`
- L5 `release_manager/help_text.py`; L6 `release_manager/cli.py` (canonical CLI)

## Run all tests (use project venv)

```powershell
& ".venv\Scripts\python.exe" -m pytest scriptcraft/layers/layer_2_testing -q
```

Many legacy tests still target removed `scriptcraft.common` / `scriptcraft.tools` paths; use the Phase 1 command block above for migration sign-off.

Optional: set `SCRIPTCRAFT_REQUIRE_VENV=1` to fail collection when not running inside a venv.
