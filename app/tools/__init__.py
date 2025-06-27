import yaml
from importlib import import_module
from typing import Any, Dict

def load_tools() -> Dict[str, Any]:

    # Read YAML config
    with open("config/tools.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    tools: Dict[str, Any] = {}
    for name, conf in cfg.items():
        # Only load tools that are enabled
        if not conf.get("enabled", False):
            continue
        # Dynamically import tool module (e.g. app.tools.scholar_tool)
        module = import_module(f"app.tools.{name}")
        # Factory function create() returns our tool instance
        tool = module.create(conf)
        # Register under its METHOD constant
        tools[module.ScholarTool.METHOD] = tool

    return tools
