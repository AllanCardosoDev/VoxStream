"""Testes unitários para voxstream.audio_utils."""

from __future__ import annotations

import io
import zipfile

import pytest

from voxstream.audio_utils import build_zip


class TestBuildZip:
    """Testes para a função build_zip."""

    def _make_fake_wav(self, label: str = "test") -> bytes:
        """Retorna bytes que simulam um arquivo WAV mínimo."""
        return b"RIFF" + b"\x00" * 4 + b"WAVE" + label.encode()

    def test_retorna_bytes(self):
        """build_zip deve retornar bytes."""
        audios = [{"name": "audio1", "data": self._make_fake_wav("a1")}]
        result = build_zip(audios)
        assert isinstance(result, bytes)

    def test_zip_valido(self):
        """O resultado deve ser um ZIP válido."""
        audios = [{"name": "audio1", "data": self._make_fake_wav("a1")}]
        result = build_zip(audios)
        assert zipfile.is_zipfile(io.BytesIO(result))

    def test_contem_arquivos_wav(self):
        """Cada áudio deve gerar um arquivo .wav no ZIP."""
        audios = [
            {"name": "faixa1", "data": self._make_fake_wav("f1")},
            {"name": "faixa2", "data": self._make_fake_wav("f2")},
        ]
        result = build_zip(audios)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            names = zf.namelist()
        assert "faixa1.wav" in names
        assert "faixa2.wav" in names

    def test_conteudo_preservado(self):
        """O conteúdo de cada arquivo WAV deve ser preservado no ZIP."""
        data = self._make_fake_wav("conteudo")
        audios = [{"name": "meu_audio", "data": data}]
        result = build_zip(audios)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            extracted = zf.read("meu_audio.wav")
        assert extracted == data

    def test_lista_vazia(self):
        """build_zip com lista vazia deve retornar um ZIP válido sem arquivos."""
        result = build_zip([])
        assert zipfile.is_zipfile(io.BytesIO(result))
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            assert zf.namelist() == []

    def test_multiplos_audios(self):
        """Todos os áudios da lista devem estar no ZIP."""
        n = 5
        audios = [{"name": f"audio{i}", "data": self._make_fake_wav(str(i))} for i in range(n)]
        result = build_zip(audios)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            assert len(zf.namelist()) == n
