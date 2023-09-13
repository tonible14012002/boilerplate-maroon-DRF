from pathlib import Path
import importlib
import environ

env = environ.Env()

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

build_env = env.str("BUILD_ENVIRONMENT", "local")
module_paths = [
    f'config.settings.{build_env}',
]

for path in module_paths:
    module = importlib.import_module(path)
    globals().update(module.__dict__)
