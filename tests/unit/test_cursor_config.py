"""Tests for Cursor / persisted DeepSeek API key helpers."""

from __future__ import annotations

import json

import pytest

from tools import cursor_config as cc


@pytest.fixture
def isolated_config_dir(tmp_path, monkeypatch):
    cfg_root = tmp_path / ".automotive-cursor-agents"
    monkeypatch.setattr(cc, "user_config_dir", lambda: cfg_root)
    return cfg_root


def test_save_and_load_stored_key(isolated_config_dir):
    path = cc.user_config_path()
    assert not path.exists()

    cc.save_deepseek_api_key("sk-test-key-123")
    assert path.is_file()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data.get(cc.KEY_FIELD) == "sk-test-key-123"

    assert cc.load_stored_deepseek_key() == "sk-test-key-123"


def test_resolve_prefers_env(isolated_config_dir, monkeypatch):
    cc.save_deepseek_api_key("sk-from-file")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-from-env")
    assert cc.resolve_deepseek_api_key() == "sk-from-env"


def test_clear_stored_key(isolated_config_dir):
    cc.save_deepseek_api_key("sk-x")
    assert cc.clear_stored_deepseek_key() is True
    assert cc.load_stored_deepseek_key() is None
