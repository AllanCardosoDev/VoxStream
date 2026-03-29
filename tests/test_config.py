"""Testes unitários para voxstream.config."""

from __future__ import annotations

import os

from voxstream.config import (
    DEFAULT_LANGUAGE,
    DEFAULT_SPEED,
    DEFAULT_VOICE,
    LANGUAGES,
    MAX_CHARS,
    MAX_SPEED,
    MIN_CHARS,
    MIN_SPEED,
    TTS_MODEL,
    VOICES_DIR,
)


class TestConfig:
    def test_languages_not_empty(self) -> None:
        assert len(LANGUAGES) > 0

    def test_languages_values_are_strings(self) -> None:
        for key, val in LANGUAGES.items():
            assert isinstance(key, str)
            assert isinstance(val, str)

    def test_portuguese_in_languages(self) -> None:
        assert "Português" in LANGUAGES
        assert LANGUAGES["Português"] == "pt"

    def test_max_chars_positive(self) -> None:
        assert MAX_CHARS > 0

    def test_min_chars_less_than_max(self) -> None:
        assert MIN_CHARS < MAX_CHARS

    def test_speed_range_valid(self) -> None:
        assert MIN_SPEED > 0
        assert MAX_SPEED > MIN_SPEED
        assert MIN_SPEED <= DEFAULT_SPEED <= MAX_SPEED

    def test_default_language_in_languages(self) -> None:
        assert DEFAULT_LANGUAGE in LANGUAGES

    def test_default_voice_is_string(self) -> None:
        assert isinstance(DEFAULT_VOICE, str)

    def test_tts_model_is_string(self) -> None:
        assert isinstance(TTS_MODEL, str)
        assert len(TTS_MODEL) > 0

    def test_voices_dir_is_path(self) -> None:
        from pathlib import Path
        assert isinstance(VOICES_DIR, Path)

    def test_coqui_tos_env_var_set(self) -> None:
        assert os.environ.get("COQUI_TOS_AGREED") == "1"
