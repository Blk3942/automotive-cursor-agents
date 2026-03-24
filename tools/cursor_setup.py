"""
First-time (and optional re-) configuration for Cursor / local use: DeepSeek API key.

Usage:
  python -m tools.cursor_setup
  python -m tools.cursor_setup --force
  python -m tools.cursor_setup --status
  python -m tools.cursor_setup --clear

Console script (after pip install -e .):
  automotive-cursor-setup
"""

from __future__ import annotations

import argparse
import getpass
import sys
from pathlib import Path
from typing import List, Optional

# Support: ``python tools/cursor_setup.py`` (IDE “Run file”) — repo root must be on path
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.cursor_config import (
    clear_stored_deepseek_key,
    explain_setup_hint,
    is_deepseek_configured,
    resolve_deepseek_api_key,
    save_deepseek_api_key,
    user_config_path,
)


def _try_load_dotenv() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Save DeepSeek API key for automotive tools (Cursor / local)."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Prompt for a new key even if one is already saved",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show whether a key is available (env or file), without revealing it",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Remove saved key from disk (environment variable unaffected)",
    )
    args = parser.parse_args(argv)

    _try_load_dotenv()

    if args.clear:
        if clear_stored_deepseek_key():
            print(f"Removed saved key from {user_config_path()}")
        else:
            print("No saved key in config file.")
        return 0

    if args.status:
        if resolve_deepseek_api_key():
            src = (
                "environment (DEEPSEEK_API_KEY)"
                if __import__("os").environ.get("DEEPSEEK_API_KEY", "").strip()
                else f"file ({user_config_path()})"
            )
            print(f"DeepSeek API key: configured ({src})")
        else:
            print("DeepSeek API key: not configured")
            print(explain_setup_hint())
        return 0

    if not args.force and is_deepseek_configured():
        print("DeepSeek API key is already available (environment and/or saved file).")
        print(f"  Saved key file (if any): {user_config_path()}")
        print("  Replace saved key: python -m tools.cursor_setup --force")
        print("  Remove saved key only: python -m tools.cursor_setup --clear")
        return 0

    if not sys.stdin.isatty():
        print(
            "No TTY: set DEEPSEEK_API_KEY in the environment, or run this command in a terminal.",
            file=sys.stderr,
        )
        return 1

    print(
        "Enter your DeepSeek API key (from https://platform.deepseek.com/). "
        "Input is hidden."
    )
    key = getpass.getpass("DeepSeek API key: ").strip()
    if not key:
        print("Empty key; aborted.", file=sys.stderr)
        return 1

    path = save_deepseek_api_key(key)
    print(f"Saved. Key stored at: {path}")
    print("Priority at runtime: DEEPSEEK_API_KEY env > this file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
