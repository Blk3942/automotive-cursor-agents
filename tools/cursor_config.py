"""
Cursor / local IDE integration — persisted DeepSeek API key.

Stores configuration under the user home directory (not the git repo):
  ~/.automotive-cursor-agents/config.json

Priority for resolving the key (highest first):
  1. Environment variable DEEPSEEK_API_KEY
  2. Value in the config file (saved by cursor_setup)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

CONFIG_DIRNAME = ".automotive-cursor-agents"
CONFIG_FILENAME = "config.json"
KEY_FIELD = "deepseek_api_key"


def user_config_dir() -> Path:
    """Directory for user-level automotive-cursor config."""
    return Path.home() / CONFIG_DIRNAME


def user_config_path() -> Path:
    return user_config_dir() / CONFIG_FILENAME


def _load_raw_config() -> Dict[str, Any]:
    path = user_config_path()
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def load_stored_deepseek_key() -> Optional[str]:
    """Return API key from saved config file only (ignores environment)."""
    data = _load_raw_config()
    key = data.get(KEY_FIELD)
    if isinstance(key, str) and key.strip():
        return key.strip()
    return None


def resolve_deepseek_api_key() -> Optional[str]:
    """
    Resolve DeepSeek API key: environment first, then persisted file.
    Returns None if not configured.
    """
    env = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if env:
        return env
    return load_stored_deepseek_key()


def save_deepseek_api_key(api_key: str) -> Path:
    """Persist key to user config. Returns path written."""
    key = api_key.strip()
    if not key:
        raise ValueError("API key is empty")

    cfg_dir = user_config_dir()
    cfg_dir.mkdir(parents=True, exist_ok=True)
    path = user_config_path()

    data = _load_raw_config()
    data[KEY_FIELD] = key
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    try:
        path.chmod(0o600)
    except OSError:
        pass

    return path


def clear_stored_deepseek_key() -> bool:
    """Remove key from file. Returns True if file was updated."""
    path = user_config_path()
    if not path.is_file():
        return False
    data = _load_raw_config()
    if KEY_FIELD not in data:
        return False
    del data[KEY_FIELD]
    if data:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    else:
        try:
            path.unlink()
        except OSError:
            pass
    return True


def is_deepseek_configured() -> bool:
    return resolve_deepseek_api_key() is not None


def explain_setup_hint() -> str:
    return (
        "Configure DeepSeek: run `python -m tools.cursor_setup` from the repo root, "
        "or set environment variable DEEPSEEK_API_KEY."
    )


def ensure_configured_or_exit() -> str:
    """Return resolved key or print hint and exit with code 1."""
    key = resolve_deepseek_api_key()
    if key:
        return key
    print(explain_setup_hint(), file=sys.stderr)
    sys.exit(1)
