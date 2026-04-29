from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PathConfig:
    scripts_dir: Path = field(default_factory=lambda: Path("scripts"))
    common_dir: Path = field(default_factory=lambda: Path("scripts/common"))
    tools_dir: Path = field(default_factory=lambda: Path("scripts/tools"))
    templates_dir: Path = field(default_factory=lambda: Path("templates/distributable_template"))
    export_dir: Path = field(default_factory=lambda: Path("distributables"))
    output_dir: Path = field(default_factory=lambda: Path("output"))
    input_dir: Path = field(default_factory=lambda: Path("input"))
    qc_output_dir: Path = field(default_factory=lambda: Path("qc_output"))