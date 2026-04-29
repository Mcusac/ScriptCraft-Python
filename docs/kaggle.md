# Kaggle / ML Competition Framework (notes)

This repository includes code that originated in a Kaggle-focused competition framework. While the primary deliverable is an importable Python package, these notes capture the Kaggle usage patterns during the transition.

## Local layout to mimic Kaggle

To mirror Kaggle paths locally:

- `input/` ↔ `/kaggle/input/`
- `working/` ↔ `/kaggle/working/`

Place the competition data under `input/<competition-slug>/` and (optionally) place this repo under `input/<repo-name>/`.

## Notebook pathing

Historically, notebooks inserted the framework onto `sys.path`. During consolidation, prefer importing through the packaged namespace when possible.

If you still need to run the legacy runner layout inside notebooks, see `scriptcraft/path_bootstrap.py` and `scriptcraft/run.py`.

