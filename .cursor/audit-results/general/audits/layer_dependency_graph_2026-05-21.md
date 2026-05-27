---
generated: 2026-05-21
artifact: layer_dependency_graph
---

# Layer dependency graph

- Scripts root: `C:/Users/mdc0431/dev/ScriptCraft-Workspace/implementations/python/python-package/scriptcraft`
- Files scanned: 1635
- Imports analyzed (internal only): 1612
- Parse errors: 0
- Buckets: 54
- Unique bucket edges: 107
- Violating bucket edges: 0 (edges counted: 0)

## Buckets

- `competition_infra_level_0`
- `competition_infra_level_1`
- `competition_infra_level_2`
- `competition_infra_level_3`
- `competition_infra_level_4`
- `competition_infra_level_5`
- `competition_infra_level_6`
- `contest_level_arc_agi_2_level_0`
- `contest_level_arc_agi_2_level_1`
- `contest_level_arc_agi_2_level_2`
- `contest_level_arc_agi_2_level_3`
- `contest_level_arc_agi_2_level_4`
- `contest_level_arc_agi_2_level_5`
- `contest_level_arc_agi_2_level_6`
- `contest_level_arc_agi_2_level_7`
- `contest_level_arc_agi_2_level_8`
- `contest_level_cafa_level_0`
- `contest_level_cafa_level_1`
- `contest_level_cafa_level_2`
- `contest_level_cafa_level_3`
- `contest_level_cafa_level_4`
- `contest_level_cafa_other`
- `contest_level_csiro_level_0`
- `contest_level_csiro_level_1`
- `contest_level_csiro_level_2`
- `contest_level_csiro_level_3`
- `contest_level_csiro_level_4`
- `contest_level_csiro_level_5`
- `contest_level_csiro_level_6`
- `contest_level_csiro_level_7`
- `contest_level_rna3d_level_0`
- `contest_level_rna3d_level_1`
- `contest_level_rna3d_level_2`
- `contest_level_rna3d_level_3`
- `contest_level_rna3d_level_4`
- `devtools_impl_level_0`
- `devtools_impl_level_1`
- `devtools_impl_level_2`
- `devtools_impl_level_3`
- `devtools_infra_level_0`
- `devtools_infra_level_1`
- `devtools_infra_level_2`
- `external_other`
- `layer_0_level_0`
- `layer_0_level_1`
- `layer_0_level_10`
- `layer_0_level_2`
- `layer_0_level_3`
- `layer_0_level_4`
- `layer_0_level_5`
- `layer_0_level_6`
- `layer_0_level_7`
- `layer_0_level_8`
- `layer_0_level_9`

## Adjacency (bucket -> bucket, count)

### `competition_infra_level_0`
- `competition_infra_level_0`: 74
  - `layers/layer_1_competition/level_0_infra/level_0/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_0`
  - `layers/layer_1_competition/level_0_infra/level_0/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_0.abstractions`
  - `layers/layer_1_competition/level_0_infra/level_0/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_0.argparse_builders`
  - `layers/layer_1_competition/level_0_infra/level_0/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_0.argv_command_builders`
  - `layers/layer_1_competition/level_0_infra/level_0/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_0.artifacts`

### `competition_infra_level_1`
- `competition_infra_level_1`: 52
  - `layers/layer_1_competition/level_0_infra/level_1/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_1`
  - `layers/layer_1_competition/level_0_infra/level_1/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_1.artifact_io`
  - `layers/layer_1_competition/level_0_infra/level_1/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_1.commands`
  - `layers/layer_1_competition/level_0_infra/level_1/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_1.contest`
  - `layers/layer_1_competition/level_0_infra/level_1/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_1.decoding`

### `competition_infra_level_2`
- `competition_infra_level_2`: 14
  - `layers/layer_1_competition/level_0_infra/level_2/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_2`
  - `layers/layer_1_competition/level_0_infra/level_2/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_2.feature_extraction`
  - `layers/layer_1_competition/level_0_infra/level_2/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_2.grid_search`
  - `layers/layer_1_competition/level_0_infra/level_2/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_2.handlers`
  - `layers/layer_1_competition/level_0_infra/level_2/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_2.notebook`

### `competition_infra_level_3`
- `competition_infra_level_3`: 14
  - `layers/layer_1_competition/level_0_infra/level_3/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_3`
  - `layers/layer_1_competition/level_0_infra/level_3/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_3.lm_backend`
  - `layers/layer_1_competition/level_0_infra/level_3/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_3.trainer`
  - `layers/layer_1_competition/level_0_infra/level_3/lm_backend/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_3.lm_backend.backend_transformers`
  - `layers/layer_1_competition/level_0_infra/level_3/lm_backend/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_3.lm_backend.mock_backend`

### `competition_infra_level_4`
- `competition_infra_level_4`: 10
  - `layers/layer_1_competition/level_0_infra/level_4/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_4`
  - `layers/layer_1_competition/level_0_infra/level_4/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_4.fold_orchestration`
  - `layers/layer_1_competition/level_0_infra/level_4/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_4.lm_backends`
  - `layers/layer_1_competition/level_0_infra/level_4/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_4.lm_task_adaptation`
  - `layers/layer_1_competition/level_0_infra/level_4/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_4.trainer`

### `competition_infra_level_5`
- `competition_infra_level_5`: 3
  - `layers/layer_1_competition/level_0_infra/level_5/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_5`
  - `layers/layer_1_competition/level_0_infra/level_5/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_5.submission`
  - `layers/layer_1_competition/level_0_infra/level_5/submission/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_5.submission.formatting`

### `competition_infra_level_6`
- `competition_infra_level_6`: 3
  - `layers/layer_1_competition/level_0_infra/level_6/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_6`
  - `layers/layer_1_competition/level_0_infra/level_6/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_6.submission`
  - `layers/layer_1_competition/level_0_infra/level_6/submission/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_6.submission.regression_submission`

### `contest_level_arc_agi_2_level_0`
- `contest_level_arc_agi_2_level_0`: 41
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_0`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_0.arc_paths`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_0.config`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_0.decoding`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_0.grid`

### `contest_level_arc_agi_2_level_1`
- `contest_level_arc_agi_2_level_1`: 44
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_1`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_1.cli`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_1.datasets`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_1.eval`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_1.lm`

### `contest_level_arc_agi_2_level_2`
- `contest_level_arc_agi_2_level_2`: 25
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_2`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_2.cmd_submit`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_2.cmd_train_and_submit`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_2.cmd_tune_and_submit`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_2.decode_branches`

### `contest_level_arc_agi_2_level_3`
- `contest_level_arc_agi_2_level_3`: 9
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_3`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_3.extend_subparsers`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_3.lm_task_adaptation`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_3.neural_eval_score`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_3.postprocess_handlers`

### `contest_level_arc_agi_2_level_4`
- `contest_level_arc_agi_2_level_4`: 10
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_4`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_4.llm_tta_runner`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_4.lm`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_4.lm_task_adaptation`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_4.stages`

### `contest_level_arc_agi_2_level_5`
- `contest_level_arc_agi_2_level_5`: 1
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_5/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_5.runner`

### `contest_level_arc_agi_2_level_6`
- `contest_level_arc_agi_2_level_6`: 4
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_6/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_6`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_6/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_6.dispatch`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_6/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_6.single_stage`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_6/dispatch/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_6.dispatch.submit_strategy_dispatch`

### `contest_level_arc_agi_2_level_7`
- `contest_level_arc_agi_2_level_7`: 4
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_7/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_7`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_7/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_7.orchestration`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_7/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_7.submit`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_7/orchestration/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_7.orchestration.composites`

### `contest_level_arc_agi_2_level_8`
- `contest_level_arc_agi_2_level_8`: 3
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_8/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_8`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_8/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_8.handlers`
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/level_8/handlers/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_8.handlers.pipeline_handlers`

### `contest_level_cafa_level_0`
- `contest_level_cafa_level_0`: 14
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_0.config`
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_0.constants`
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_0.data_schema`
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_0.embedding_paths`
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_0.goa_filter`

### `contest_level_cafa_level_1`
- `contest_level_cafa_level_1`: 4
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_1.load_embeddings`
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_1.parameter_grids`
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_1.post_processor`
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_1.training`

### `contest_level_cafa_level_2`
- `contest_level_cafa_level_2`: 1
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_2.feature_extractor`

### `contest_level_cafa_level_3`
- `contest_level_cafa_level_3`: 1
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_3.ontology_data_preparer`

### `contest_level_cafa_level_4`
- `contest_level_cafa_level_4`: 1
  - `layers/layer_1_competition/level_1_impl/level_cafa/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_4.per_ontology_training`

### `contest_level_cafa_other`
- `contest_level_cafa_level_0`: 3
  - `layers/layer_1_competition/level_1_impl/level_cafa/registration.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_0.config`
  - `layers/layer_1_competition/level_1_impl/level_cafa/registration.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_0.data_schema`
  - `layers/layer_1_competition/level_1_impl/level_cafa/registration.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_0.paths`
- `contest_level_cafa_level_1`: 1
  - `layers/layer_1_competition/level_1_impl/level_cafa/registration.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_1.post_processor`

### `contest_level_csiro_level_0`
- `contest_level_csiro_level_0`: 27
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_0.aggregate`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_0.biomass_models`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_0.biomass_semantic_features`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_0.camera_trap`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_0.checkpoint_utils`

### `contest_level_csiro_level_1`
- `contest_level_csiro_level_1`: 11
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_1.best_variant`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_1.config_updater`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_1.e2e_ensemble_oof`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_1.factory`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_1.meta_models`

### `contest_level_csiro_level_2`
- `contest_level_csiro_level_2`: 8
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_2.csiro_regression_ensemble`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_2.e2e_training`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_2.regression_ensemble_pipeline`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_2.stacking_ensemble_pipeline`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_2.stacking_pipeline`

### `contest_level_csiro_level_3`
- `contest_level_csiro_level_3`: 4
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_3.ensemble_pipeline`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_3.regression_ensemble_oof`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_3.result_persistence`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_3.variant_selection_variants`

### `contest_level_csiro_level_4`
- `contest_level_csiro_level_4`: 4
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_4.feature_extraction`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_4.grid_search_context`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_4.handlers_ensemble`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_4.hybrid_stacking_pipeline`

### `contest_level_csiro_level_5`
- `contest_level_csiro_level_5`: 5
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_5/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_5.handlers_grid_search`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_5/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_5.handlers_stacking`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_5/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_5.handlers_submit`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_5/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_5.handlers_training`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_5/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_5.regression_training`

### `contest_level_csiro_level_6`
- `contest_level_csiro_level_6`: 1
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_6/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_6.train_and_export_pipeline`

### `contest_level_csiro_level_7`
- `contest_level_csiro_level_7`: 5
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_7/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_7.handlers`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_7/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_7.handlers_multi_variant`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_7/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_7.multi_variant_regression_training_pipeline`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_7/handlers.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_7.handlers_multi_variant`
  - `layers/layer_1_competition/level_1_impl/level_csiro/level_7/handlers_multi_variant.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_7.multi_variant_regression_training_pipeline`

### `contest_level_rna3d_level_0`
- `contest_level_rna3d_level_0`: 8
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_0.artifacts`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_0.config`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_0.data_schema`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_0.notebook_commands`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_0/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_0.paths`

### `contest_level_rna3d_level_1`
- `contest_level_rna3d_level_1`: 2
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_1.baseline_approx`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_1/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_1.scoring`

### `contest_level_rna3d_level_2`
- `contest_level_rna3d_level_2`: 6
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_2`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_2.orchestration`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_2/orchestration/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_2.orchestration.submission`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_2/orchestration/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_2.orchestration.train_and_submit`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_2/orchestration/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_2.orchestration.trainer_registry`

### `contest_level_rna3d_level_3`
- `contest_level_rna3d_level_3`: 3
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_3`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_3/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_3.training`
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_3/training/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_3.training.pipeline`

### `contest_level_rna3d_level_4`
- `contest_level_rna3d_level_4`: 1
  - `layers/layer_1_competition/level_1_impl/level_rna3d/level_4/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_4.handlers`

### `devtools_impl_level_0`
- `devtools_impl_level_0`: 28
  - `layers/layer_2_devtools/level_1_impl/level_0/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_0`
  - `layers/layer_2_devtools/level_1_impl/level_0/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_0.composed`
  - `layers/layer_2_devtools/level_1_impl/level_0/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_0.preparation`
  - `layers/layer_2_devtools/level_1_impl/level_0/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_0.regenerate_inits`
  - `layers/layer_2_devtools/level_1_impl/level_0/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_0.scan`

### `devtools_impl_level_1`
- `devtools_impl_level_1`: 18
  - `layers/layer_2_devtools/level_1_impl/level_1/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_1`
  - `layers/layer_2_devtools/level_1_impl/level_1/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_1.api_audit`
  - `layers/layer_2_devtools/level_1_impl/level_1/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_1.api_audit_checks`
  - `layers/layer_2_devtools/level_1_impl/level_1/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_1.api_audit_emit`
  - `layers/layer_2_devtools/level_1_impl/level_1/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_1.api_ci`

### `devtools_impl_level_2`
- `devtools_impl_level_2`: 16
  - `layers/layer_2_devtools/level_1_impl/level_2/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_2`
  - `layers/layer_2_devtools/level_1_impl/level_2/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_2.audit_artifact_bootstrap`
  - `layers/layer_2_devtools/level_1_impl/level_2/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_2.audit_artifact_schema_check`
  - `layers/layer_2_devtools/level_1_impl/level_2/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_2.audit_orchestrator_ops`
  - `layers/layer_2_devtools/level_1_impl/level_2/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_2.circular_deps`

### `devtools_infra_level_0`
- `devtools_infra_level_0`: 92
  - `layers/layer_2_devtools/level_0_infra/level_0/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_0`
  - `layers/layer_2_devtools/level_0_infra/level_0/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_0._codemod`
  - `layers/layer_2_devtools/level_0_infra/level_0/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_0.base_health_analyzer`
  - `layers/layer_2_devtools/level_0_infra/level_0/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_0.constants`
  - `layers/layer_2_devtools/level_0_infra/level_0/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_0.contest_configs`

### `devtools_infra_level_1`
- `devtools_infra_level_1`: 23
  - `layers/layer_2_devtools/level_0_infra/level_1/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_1`
  - `layers/layer_2_devtools/level_0_infra/level_1/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_1.checker`
  - `layers/layer_2_devtools/level_0_infra/level_1/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_1.dumper_presets`
  - `layers/layer_2_devtools/level_0_infra/level_1/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_1.health_analyzers`
  - `layers/layer_2_devtools/level_0_infra/level_1/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_1.hyperparameter_analysis`
- `devtools_infra_level_0`: 1
  - `layers/layer_2_devtools/level_0_infra/level_1/hyperparameter_analysis.py`: `import layers.layer_2_devtools.level_0_infra.level_0.hyperparameter`

### `devtools_infra_level_2`
- `devtools_infra_level_2`: 2
  - `layers/layer_2_devtools/level_0_infra/level_2/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_2.console_reporter`
  - `layers/layer_2_devtools/level_0_infra/level_2/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_2.reporter`

### `external_other`
- `external_other`: 514
  - `layers/__init__.py`: `import layers`
  - `layers/__init__.py`: `import layers.layer_0_core`
  - `layers/__init__.py`: `import layers.layer_1_competition`
  - `layers/__init__.py`: `import layers.layer_1_tools`
  - `layers/__init__.py`: `import layers.layer_2_devtools`
- `layer_0_level_0`: 3
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_0`
  - `layers/layer_2_testing/unit/test_levels/test_layer_1_infra_wiring.py`: `import layers.layer_0_core.level_0`
  - `layers/layer_2_testing/unit/test_levels/test_level_0_1_2_imports.py`: `import layers.layer_0_core.level_0`
- `competition_infra_level_1`: 2
  - `layers/layer_1_competition/level_0_infra/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_1`
  - `layers/layer_2_testing/unit/test_levels/test_layer_1_infra_wiring.py`: `import layers.layer_1_competition.level_0_infra.level_1`
- `layer_0_level_1`: 2
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_1`
  - `layers/layer_2_testing/unit/test_levels/test_level_0_1_2_imports.py`: `import layers.layer_0_core.level_1`
- `layer_0_level_2`: 2
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_2`
  - `layers/layer_2_testing/unit/test_levels/test_level_0_1_2_imports.py`: `import layers.layer_0_core.level_2`
- `competition_infra_level_0`: 1
  - `layers/layer_1_competition/level_0_infra/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_0`
- `competition_infra_level_2`: 1
  - `layers/layer_1_competition/level_0_infra/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_2`
- `competition_infra_level_3`: 1
  - `layers/layer_1_competition/level_0_infra/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_3`
- `competition_infra_level_4`: 1
  - `layers/layer_1_competition/level_0_infra/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_4`
- `competition_infra_level_5`: 1
  - `layers/layer_1_competition/level_0_infra/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_5`
- `competition_infra_level_6`: 1
  - `layers/layer_1_competition/level_0_infra/__init__.py`: `import layers.layer_1_competition.level_0_infra.level_6`
- `contest_level_arc_agi_2_level_0`: 1
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_0`
- `contest_level_arc_agi_2_level_1`: 1
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_1`
- `contest_level_arc_agi_2_level_2`: 1
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_2`
- `contest_level_arc_agi_2_level_3`: 1
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_3`
- `contest_level_arc_agi_2_level_4`: 1
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_4`
- `contest_level_arc_agi_2_level_5`: 1
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_5`
- `contest_level_arc_agi_2_level_6`: 1
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_6`
- `contest_level_arc_agi_2_level_7`: 1
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_7`
- `contest_level_arc_agi_2_level_8`: 1
  - `layers/layer_1_competition/level_1_impl/level_arc_agi_2/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_arc_agi_2.level_8`
- `contest_level_cafa_level_0`: 1
  - `layers/layer_1_competition/level_1_impl/level_cafa/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_0`
- `contest_level_cafa_level_1`: 1
  - `layers/layer_1_competition/level_1_impl/level_cafa/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_1`
- `contest_level_cafa_level_2`: 1
  - `layers/layer_1_competition/level_1_impl/level_cafa/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_2`
- `contest_level_cafa_level_3`: 1
  - `layers/layer_1_competition/level_1_impl/level_cafa/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_3`
- `contest_level_cafa_level_4`: 1
  - `layers/layer_1_competition/level_1_impl/level_cafa/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_cafa.level_4`
- `contest_level_csiro_level_0`: 1
  - `layers/layer_1_competition/level_1_impl/level_csiro/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_0`
- `contest_level_csiro_level_1`: 1
  - `layers/layer_1_competition/level_1_impl/level_csiro/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_1`
- `contest_level_csiro_level_2`: 1
  - `layers/layer_1_competition/level_1_impl/level_csiro/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_2`
- `contest_level_csiro_level_3`: 1
  - `layers/layer_1_competition/level_1_impl/level_csiro/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_3`
- `contest_level_csiro_level_4`: 1
  - `layers/layer_1_competition/level_1_impl/level_csiro/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_4`
- `contest_level_csiro_level_5`: 1
  - `layers/layer_1_competition/level_1_impl/level_csiro/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_5`
- `contest_level_csiro_level_6`: 1
  - `layers/layer_1_competition/level_1_impl/level_csiro/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_6`
- `contest_level_csiro_level_7`: 1
  - `layers/layer_1_competition/level_1_impl/level_csiro/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_csiro.level_7`
- `contest_level_rna3d_level_0`: 1
  - `layers/layer_1_competition/level_1_impl/level_rna3d/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_0`
- `contest_level_rna3d_level_1`: 1
  - `layers/layer_1_competition/level_1_impl/level_rna3d/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_1`
- `contest_level_rna3d_level_2`: 1
  - `layers/layer_1_competition/level_1_impl/level_rna3d/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_2`
- `contest_level_rna3d_level_3`: 1
  - `layers/layer_1_competition/level_1_impl/level_rna3d/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_3`
- `contest_level_rna3d_level_4`: 1
  - `layers/layer_1_competition/level_1_impl/level_rna3d/__init__.py`: `import layers.layer_1_competition.level_1_impl.level_rna3d.level_4`
- `devtools_impl_level_0`: 1
  - `layers/layer_2_devtools/level_1_impl/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_0`
- `devtools_impl_level_1`: 1
  - `layers/layer_2_devtools/level_1_impl/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_1`
- `devtools_impl_level_2`: 1
  - `layers/layer_2_devtools/level_1_impl/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_2`
- `devtools_impl_level_3`: 1
  - `layers/layer_2_devtools/level_1_impl/__init__.py`: `import layers.layer_2_devtools.level_1_impl.level_3`
- `devtools_infra_level_0`: 1
  - `layers/layer_2_devtools/level_0_infra/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_0`
- `devtools_infra_level_1`: 1
  - `layers/layer_2_devtools/level_0_infra/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_1`
- `devtools_infra_level_2`: 1
  - `layers/layer_2_devtools/level_0_infra/__init__.py`: `import layers.layer_2_devtools.level_0_infra.level_2`
- `layer_0_level_10`: 1
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_10`
- `layer_0_level_3`: 1
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_3`
- `layer_0_level_4`: 1
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_4`
- `layer_0_level_5`: 1
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_5`
- `layer_0_level_6`: 1
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_6`
- `layer_0_level_7`: 1
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_7`
- `layer_0_level_8`: 1
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_8`
- `layer_0_level_9`: 1
  - `layers/layer_0_core/__init__.py`: `import layers.layer_0_core.level_9`

### `layer_0_level_0`
- `layer_0_level_0`: 96
  - `layers/layer_0_core/level_0/__init__.py`: `import layers.layer_0_core.level_0`
  - `layers/layer_0_core/level_0/__init__.py`: `import layers.layer_0_core.level_0.abstractions`
  - `layers/layer_0_core/level_0/__init__.py`: `import layers.layer_0_core.level_0.cli`
  - `layers/layer_0_core/level_0/__init__.py`: `import layers.layer_0_core.level_0.config`
  - `layers/layer_0_core/level_0/__init__.py`: `import layers.layer_0_core.level_0.embeddings`

### `layer_0_level_1`
- `layer_0_level_1`: 130
  - `layers/layer_0_core/level_1/__init__.py`: `import layers.layer_0_core.level_1`
  - `layers/layer_0_core/level_1/__init__.py`: `import layers.layer_0_core.level_1.cli`
  - `layers/layer_0_core/level_1/__init__.py`: `import layers.layer_0_core.level_1.data`
  - `layers/layer_0_core/level_1/__init__.py`: `import layers.layer_0_core.level_1.evaluation`
  - `layers/layer_0_core/level_1/__init__.py`: `import layers.layer_0_core.level_1.features`

### `layer_0_level_10`
- `layer_0_level_10`: 3
  - `layers/layer_0_core/level_10/__init__.py`: `import layers.layer_0_core.level_10`
  - `layers/layer_0_core/level_10/__init__.py`: `import layers.layer_0_core.level_10.end_to_end_grid_search`
  - `layers/layer_0_core/level_10/end_to_end_grid_search/__init__.py`: `import layers.layer_0_core.level_10.end_to_end_grid_search.pipeline`

### `layer_0_level_2`
- `layer_0_level_2`: 61
  - `layers/layer_0_core/level_2/__init__.py`: `import layers.layer_0_core.level_2`
  - `layers/layer_0_core/level_2/__init__.py`: `import layers.layer_0_core.level_2.analysis`
  - `layers/layer_0_core/level_2/__init__.py`: `import layers.layer_0_core.level_2.dataloader`
  - `layers/layer_0_core/level_2/__init__.py`: `import layers.layer_0_core.level_2.ensemble_strategies`
  - `layers/layer_0_core/level_2/__init__.py`: `import layers.layer_0_core.level_2.feature_extractors`

### `layer_0_level_3`
- `layer_0_level_3`: 32
  - `layers/layer_0_core/level_3/__init__.py`: `import layers.layer_0_core.level_3`
  - `layers/layer_0_core/level_3/__init__.py`: `import layers.layer_0_core.level_3.dataloader`
  - `layers/layer_0_core/level_3/__init__.py`: `import layers.layer_0_core.level_3.ensemble`
  - `layers/layer_0_core/level_3/__init__.py`: `import layers.layer_0_core.level_3.ensemble_strategies`
  - `layers/layer_0_core/level_3/__init__.py`: `import layers.layer_0_core.level_3.features`

### `layer_0_level_4`
- `layer_0_level_4`: 26
  - `layers/layer_0_core/level_4/__init__.py`: `import layers.layer_0_core.level_4`
  - `layers/layer_0_core/level_4/__init__.py`: `import layers.layer_0_core.level_4.dataloaders`
  - `layers/layer_0_core/level_4/__init__.py`: `import layers.layer_0_core.level_4.ensemble`
  - `layers/layer_0_core/level_4/__init__.py`: `import layers.layer_0_core.level_4.features`
  - `layers/layer_0_core/level_4/__init__.py`: `import layers.layer_0_core.level_4.file_io`

### `layer_0_level_5`
- `layer_0_level_5`: 40
  - `layers/layer_0_core/level_5/__init__.py`: `import layers.layer_0_core.level_5`
  - `layers/layer_0_core/level_5/__init__.py`: `import layers.layer_0_core.level_5.batch_loading`
  - `layers/layer_0_core/level_5/__init__.py`: `import layers.layer_0_core.level_5.data_structure`
  - `layers/layer_0_core/level_5/__init__.py`: `import layers.layer_0_core.level_5.datasets`
  - `layers/layer_0_core/level_5/__init__.py`: `import layers.layer_0_core.level_5.ensembling`

### `layer_0_level_6`
- `layer_0_level_6`: 23
  - `layers/layer_0_core/level_6/__init__.py`: `import layers.layer_0_core.level_6`
  - `layers/layer_0_core/level_6/__init__.py`: `import layers.layer_0_core.level_6.ensembling`
  - `layers/layer_0_core/level_6/__init__.py`: `import layers.layer_0_core.level_6.grid_search`
  - `layers/layer_0_core/level_6/__init__.py`: `import layers.layer_0_core.level_6.metadata`
  - `layers/layer_0_core/level_6/__init__.py`: `import layers.layer_0_core.level_6.prediction`

### `layer_0_level_7`
- `layer_0_level_7`: 8
  - `layers/layer_0_core/level_7/__init__.py`: `import layers.layer_0_core.level_7`
  - `layers/layer_0_core/level_7/__init__.py`: `import layers.layer_0_core.level_7.factories`
  - `layers/layer_0_core/level_7/__init__.py`: `import layers.layer_0_core.level_7.grid_search`
  - `layers/layer_0_core/level_7/factories/__init__.py`: `import layers.layer_0_core.level_7.factories.create_ensembling_method`
  - `layers/layer_0_core/level_7/factories/__init__.py`: `import layers.layer_0_core.level_7.factories.tabular_model_factory`

### `layer_0_level_8`
- `layer_0_level_8`: 11
  - `layers/layer_0_core/level_8/__init__.py`: `import layers.layer_0_core.level_8`
  - `layers/layer_0_core/level_8/__init__.py`: `import layers.layer_0_core.level_8.grid_search`
  - `layers/layer_0_core/level_8/__init__.py`: `import layers.layer_0_core.level_8.regression`
  - `layers/layer_0_core/level_8/__init__.py`: `import layers.layer_0_core.level_8.training`
  - `layers/layer_0_core/level_8/grid_search/__init__.py`: `import layers.layer_0_core.level_8.grid_search.dataset_grid_search`

### `layer_0_level_9`
- `layer_0_level_9`: 10
  - `layers/layer_0_core/level_9/__init__.py`: `import layers.layer_0_core.level_9`
  - `layers/layer_0_core/level_9/__init__.py`: `import layers.layer_0_core.level_9.grid_search`
  - `layers/layer_0_core/level_9/__init__.py`: `import layers.layer_0_core.level_9.train_predict`
  - `layers/layer_0_core/level_9/__init__.py`: `import layers.layer_0_core.level_9.training`
  - `layers/layer_0_core/level_9/grid_search/__init__.py`: `import layers.layer_0_core.level_9.grid_search.dataset_grid_search_pipeline`

## Highlighted edges (potential violations)

- None

