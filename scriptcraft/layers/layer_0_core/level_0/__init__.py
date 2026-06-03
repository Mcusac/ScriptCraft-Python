"""Auto-generated mixed exports."""


from . import (
    abstractions,
    cli,
    config,
    constants,
    embeddings,
    errors,
    grid_search,
    ontology,
    paths,
    prediction_guards,
    processing,
    protein_features,
    runtime,
    scoring,
    training,
    validation,
    vision,
)

from .abstractions import *
from .cli import *
from .config import *
from .constants import *
from .embeddings import *
from .errors import *
from .grid_search import *
from .ontology import *
from .paths import *
from .prediction_guards import *
from .processing import *
from .protein_features import *
from .runtime import *
from .scoring import *
from .training import *
from .validation import *
from .vision import *

from .dataframe_diff import (
    CoreDataFrameComparer,
    DataFrameDiffResult,
)

from .dataframe_primitives import (
    get_dataframe_summary,
    get_merge_summary,
    outer_merge_with_indicator,
    project_columns_available,
    project_columns_required,
    safe_eq,
    shallow_compare_dataframes,
)

from .outlier_eligibility import should_skip_outlier_detection

from .schema_contracts import (
    require_columns,
    require_exact_columns,
)

__all__ = (
    list(abstractions.__all__)
    + list(cli.__all__)
    + list(config.__all__)
    + list(constants.__all__)
    + list(embeddings.__all__)
    + list(errors.__all__)
    + list(grid_search.__all__)
    + list(ontology.__all__)
    + list(paths.__all__)
    + list(prediction_guards.__all__)
    + list(processing.__all__)
    + list(protein_features.__all__)
    + list(runtime.__all__)
    + list(scoring.__all__)
    + list(training.__all__)
    + list(validation.__all__)
    + list(vision.__all__)
    + [
        "CoreDataFrameComparer",
        "DataFrameDiffResult",
        "get_dataframe_summary",
        "get_merge_summary",
        "outer_merge_with_indicator",
        "project_columns_available",
        "project_columns_required",
        "require_columns",
        "require_exact_columns",
        "safe_eq",
        "shallow_compare_dataframes",
        "should_skip_outlier_detection",
    ]
)
