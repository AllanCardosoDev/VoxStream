"""Testes unitários para voxstream.config."""

from __future__ import annotations

import pytest

from voxstream import config


class TestConfig:
    """Testes para as constantes de configuração."""

    def test_max_chars_positivo(self):
        """MAX_CHARS deve ser um inteiro positivo."""
        assert isinstance(config.MAX_CHARS, int)
        assert config.MAX_CHARS > 0

    def test_languages_e_dicionario(self):
        """LANGUAGES deve ser um dicionário."""
        assert isinstance(config.LANGUAGES, dict)

    def test_languages_nao_vazio(self):
        """LANGUAGES deve conter ao menos um idioma."""
        assert len(config.LANGUAGES) > 0

    def test_languages_contem_portugues(self):
        """LANGUAGES deve conter Português."""
        assert "pt" in config.LANGUAGES.values()

    def test_languages_contem_ingles(self):
        """LANGUAGES deve conter Inglês."""
        assert "en" in config.LANGUAGES.values()

    def test_languages_valores_sao_strings(self):
        """Todos os valores de LANGUAGES devem ser strings."""
        for key, value in config.LANGUAGES.items():
            assert isinstance(key, str), f"Chave inválida: {key!r}"
            assert isinstance(value, str), f"Valor inválido para '{key}': {value!r}"

    def test_tts_model_name_nao_vazio(self):
        """TTS_MODEL_NAME deve ser uma string não-vazia."""
        assert isinstance(config.TTS_MODEL_NAME, str)
        assert config.TTS_MODEL_NAME.strip() != ""

    def test_default_voice_label_nao_vazio(self):
        """DEFAULT_VOICE_LABEL deve ser uma string não-vazia."""
        assert isinstance(config.DEFAULT_VOICE_LABEL, str)
        assert config.DEFAULT_VOICE_LABEL.strip() != ""

    def test_voices_dir_nao_vazio(self):
        """VOICES_DIR deve ser uma string não-vazia."""
        assert isinstance(config.VOICES_DIR, str)
        assert config.VOICES_DIR.strip() != ""

    def test_coqui_tos_agreed_e_um(self):
        """COQUI_TOS_AGREED deve ser '1' para aceitar os termos automaticamente."""
        assert config.COQUI_TOS_AGREED == "1"
