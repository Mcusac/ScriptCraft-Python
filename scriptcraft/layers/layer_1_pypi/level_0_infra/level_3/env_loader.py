import os

from pathlib import Path

from layers.layer_1_pypi.level_0_infra.level_2.root_schema import Config


def load_from_environment() -> Config:
    tool_name = os.environ.get("TOOL_TO_SHIP", os.environ.get("TOOL_NAME", "unknown_tool"))

    tool_config = {
        "tool_name": tool_name,
        "description": os.environ.get(
            "TOOL_DESCRIPTION",
            f"🔧 {tool_name.replace('_', ' ').title()}",
        ),
        "entry_command": os.environ.get("ENTRY_COMMAND", "main.py"),
        "packages": os.environ.get("TOOL_PACKAGES", "").split()
        if os.environ.get("TOOL_PACKAGES")
        else [],
    }

    if tool_name == "rhq_form_autofiller":
        tool_config.update(
            {
                "url_template": os.environ.get("URL_TEMPLATE", ""),
                "browser_timeout": int(os.environ.get("RHQ_BROWSER_TIMEOUT", "60")),
                "form_wait_time": int(os.environ.get("RHQ_FORM_WAIT_TIME", "10")),
                "auto_login": os.environ.get("RHQ_AUTO_LOGIN", "true").lower() == "true",
            }
        )

    config = Config()
    config.tools[tool_name] = tool_config

    config.workspace_root = Path.cwd()
    return config