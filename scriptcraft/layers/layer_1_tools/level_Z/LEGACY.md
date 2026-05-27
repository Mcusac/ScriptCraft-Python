# level_Z — legacy surface (intentional freeze)

`level_Z` holds frozen copies of asset updater/reconciliation flows and dictionary
checker plugins used by older entrypoints and tests.

## Canonical implementation

Use `layer_1_impl` for all new work:

| Legacy (`level_Z`) | Canonical (`level_1_impl`) |
|--------------------|----------------------------|
| `level_Z.asset_updater.*` | `level_1_impl.level_0` … `level_7` `asset_updater` |
| `level_Z.asset_reconciliation.*` | `level_1_impl` `asset_reconciliation` levels 0–8 |
| `level_1_impl/level_Z/dictionary_driven_checker_plugins` | Prefer `release_manager_plugins` / infra validators |

## Migration rule

1. Change callers/tests to import from `level_1_impl` level barrels.
2. Do not add features under `level_Z`.
3. Remove `level_Z` only after zero remaining imports (search: `level_Z.`).

## Remaining intentional consumers

- `layer_2_testing` tests migrating to `level_1_impl` (see test module imports).
- `level_Z.asset_management_orchestrator` until orchestration moves to impl L6/L7.
