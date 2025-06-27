import yaml
from importlib import import_module
from typing import Dict, Any

def load_tools() -> Dict[str, Any]:
    """Load enabled tools from config/tools.yaml."""
    cfg = yaml.safe_load(open("config/tools.yaml"))
    tools = {}
    for name, conf in cfg.items():
        if conf.get("enabled", False):
            module = import_module(f"app.tools.{name}")
            tool = module.create(conf)
            tools[module.ScholarTool.METHOD] = tool
    return tools
