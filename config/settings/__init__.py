from pathlib import Path
import importlib
import environ

env = environ.Env

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

module_paths = [
    'config.settings.local',
]

for path in module_paths:
    module = importlib.import_module(path)
    globals().update(module.__dict__)
