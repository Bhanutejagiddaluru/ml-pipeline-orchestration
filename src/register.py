import shutil
from pathlib import Path

def register(model_path, out_dir='artifacts/registry'):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    dst=Path(out_dir)/'model.pkl'; shutil.copy(model_path, dst)
    return str(dst)
