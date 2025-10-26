import sys
from pathlib import Path


def setup_module_path(target_folder_name: str, app_path=None):
    if app_path is None:
        app_path = Path().cwd()

    _parts = app_path.parts
    _indexes = [_parts.index(i) for i in _parts if i == target_folder_name]
    assert len(_indexes) > 0, f"target folder not found in path: {_parts = }"
    assert len(_indexes) == 1, "duplicate folder names, make them unique!"

    _depth = len(_parts) - _indexes[0]
    _switch_to_here = app_path.parents[_depth - 2].as_posix()
    print(f"{_switch_to_here = }")

    sys.path.append(_switch_to_here)


setup_module_path(target_folder_name="parent_x")
