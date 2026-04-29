# ScriptCraft (Python Package)

ScriptCraft is a Python package for reusable automation, data processing, and workflow tooling.

This repository currently contains:
- A PyPI-first Python package under `scriptcraft/`
- A layered codebase (see `scriptcraft/layers/`), including `scriptcraft/layers/layer_1_pypi/`
- Kaggle/CLI runner helpers that are being consolidated (kept for now while refactoring)

## Installation

For development:

```bash
pip install -e .
```

## Quick start

```python
import scriptcraft
print(scriptcraft.__version__)
```

## Documentation

- Kaggle / competition framework notes: `docs/kaggle.md`
- Release usage guide: `docs/RELEASE_USAGE_GUIDE.md`
- Package architecture: `docs/package_architecture.md`

