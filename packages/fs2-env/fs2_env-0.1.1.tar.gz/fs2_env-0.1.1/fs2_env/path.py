import os
import re
from typing import Dict, List


class PathNode:
    def __init__(self, name, contents: List = None, display: str = None) -> None:
        self.name = name
        self.contents = contents

        if not display:
            self.display = name
        else:
            self.display = display


def get_data_path_key(current_data_path_abspath: str) -> str:
    data_path_key_regex = '\d{8}-\d{6}-intermediate|\d{8}-\d{6}'

    path_key_match = re.search(data_path_key_regex, current_data_path_abspath)
    if not path_key_match:
        raise AttributeError(f'Invalid data path key.\n'
                             f'current_data_path: {current_data_path_abspath}\n'
                             f'key match pattern: {data_path_key_regex}')

    return path_key_match.group()


def parse_data_layout(layout: PathNode) -> Dict:
    paths = dict()
    traverse_stack = []

    def _register_path(path_key, path_items: List):
        if path_key in paths:
            raise ValueError(f'path key "{path_key}" duplicates')

        paths[path_key] = os.path.sep.join(path_items)


    def _traverse(d: PathNode):
        if not d.contents:
            _register_path(path_key=d.name, path_items=traverse_stack + [d.display])
            traverse_stack.append(d.display)
            return

        traverse_stack.append(d.display)
        _register_path(path_key=d.name, path_items=traverse_stack)

        for content in d.contents:
            if isinstance(content, PathNode):
                _traverse(content)

                traverse_stack.pop()

    _traverse(layout)

    return paths


def get_fs2_paths(base_path: str, current_data_path: str = None) -> Dict:
    from .data_layout import fs2_data_layout

    data_layout = parse_data_layout(fs2_data_layout)
    current_data_path_key = get_data_path_key(current_data_path) if current_data_path else 'current_data_template'
    # if current_data_path:
        # current_data_path_key = get_data_path_key(current_data_path)
    data_layout = {k: os.path.join(base_path, re.sub('current_data_template', current_data_path_key, path))
                   for k, path in data_layout.items()}

    return data_layout
