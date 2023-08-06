from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml
from d2b.hookspecs import hookimpl


__version__ = "1.0.0"


@hookimpl
def pre_run_logs(logger: logging.Logger):
    logger.info("d2b-yaml:version: %s", __version__)


@hookimpl
def load_config(path: Path) -> dict[str, Any]:
    return yaml.load(path.read_text(), Loader=yaml.SafeLoader)
