from enum import Enum


class ToolMaturity(Enum):
    EXPERIMENTAL = "experimental"
    BETA = "beta"
    STABLE = "stable"
    MATURE = "mature"
    DEPRECATED = "deprecated"


class DistributionType(Enum):
    STANDALONE = "standalone"
    PIPELINE_ONLY = "pipeline"
    HYBRID = "hybrid"


class ComponentType(Enum):
    TOOL = "tool"
    CHECKER = "checker"
    VALIDATOR = "validator"
    TRANSFORMER = "transformer"
    ENHANCEMENT = "enhancement"
    PLUGIN = "plugin"