import importlib
from pathlib import Path

import environ

from constants import config, enum

env = environ.Env()

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

build_env = {
    enum.BuilEnv.LOCAL.value: "local",
    enum.BuilEnv.PRODUCTION.value: "production",
}[config.BUILD_ENVIRONMENT]

module_paths = [f"config.settings.{build_env}"]

for path in module_paths:
    module = importlib.import_module(path)
    globals().update(module.__dict__)
