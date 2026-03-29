"""Tests for voxstream.config."""

import voxstream.config as cfg


class TestConfigConstants:
    def test_max_chars_is_int(self):
        assert isinstance(cfg.MAX_CHARS, int)

    def test_max_chars_positive(self):
        assert cfg.MAX_CHARS > 0

    def test_max_chars_default_value(self):
        assert cfg.MAX_CHARS == 200

    def test_languages_is_dict(self):
        assert isinstance(cfg.LANGUAGES, dict)

    def test_languages_not_empty(self):
        assert len(cfg.LANGUAGES) > 0

    def test_languages_has_portuguese(self):
        assert "Portuguese" in cfg.LANGUAGES
        assert cfg.LANGUAGES["Portuguese"] == "pt"

    def test_languages_has_english(self):
        assert "English" in cfg.LANGUAGES
        assert cfg.LANGUAGES["English"] == "en"

    def test_tts_model_is_str(self):
        assert isinstance(cfg.TTS_MODEL, str)

    def test_tts_model_not_empty(self):
        assert cfg.TTS_MODEL.strip() != ""

    def test_tts_device_is_str(self):
        assert isinstance(cfg.TTS_DEVICE, str)

    def test_log_level_is_str(self):
        assert isinstance(cfg.LOG_LEVEL, str)

    def test_languages_values_are_strings(self):
        for key, val in cfg.LANGUAGES.items():
            assert isinstance(key, str)
            assert isinstance(val, str)

    def test_all_16_languages_present(self):
        expected_keys = {
            "Portuguese", "English", "Spanish", "French", "German",
            "Italian", "Polish", "Turkish", "Russian", "Dutch",
            "Czech", "Arabic", "Chinese", "Japanese", "Hungarian", "Korean",
        }
        assert expected_keys == set(cfg.LANGUAGES.keys())
