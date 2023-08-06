"""Yet another Django env"""

__version__ = "0.1.3"

import json
import os


def update_settings_from_env(settings_dict):
    """
    Return dictionary, updated by environment variables values.
    Used to configure django settings.
    Can be called like 'update_settings_from_env(locals()) in settings module'
    Examples of variables, which will affect settings:
    DJANGO__STATIC_URL
    DJANGO__REST_FRAMEWORK__PAGE_SIZE
    DJANGO__AUTH_PASSWORD_VALIDATORS__0__NAME
    True/False or ints (0,1,2...) values of env variables will be converted to python type (bool or int).
    """
    env_prefix = 'DJANGO'
    settings_paths_list = []

    for k, v in settings_dict.items():
        if not k.startswith('__') and k != 'self':
            settings_paths_list += _traverse_paths(k, v)

    for setting in settings_paths_list:
        new_value = os.environ.get(f'{env_prefix}__{setting}')
        if new_value is not None:
            _change_setting(settings_dict, setting, new_value)


def _try_int(v):
    try:
        return int(v)
    except ValueError:
        return v


def _to_typed(value: str):
    if value.startswith('[') and value.endswith(']'):
        return json.loads(value)
    elif value == 'True':
        return True
    elif value == 'False':
        return False

    return _try_int(value)


def _change_setting(settings, path, value):
    index = path.split('__')[0]
    if index != path:
        _change_setting(settings[_try_int(index)], '__'.join(path.split('__')[1:]), value)
    else:
        settings[_try_int(index)] = _to_typed(value)


def _traverse_paths(current_path, value):
    settings_list = []

    if isinstance(value, str) or isinstance(value, bool) or isinstance(value, int):
        settings_list.append(current_path)

    elif isinstance(value, list):
        settings_list.append(current_path)
        for i, v in enumerate(value):
            settings_list += _traverse_paths(f'{current_path}__{i}', v)
    elif isinstance(value, dict):
        for k, v in value.items():
            settings_list += _traverse_paths(f'{current_path}__{k}', v)

    return settings_list
