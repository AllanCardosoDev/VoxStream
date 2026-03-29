"""Utilitários de áudio para o VoxStream."""

from __future__ import annotations

import io
import logging
import zipfile
from typing import TypedDict

logger = logging.getLogger(__name__)


class AudioEntry(TypedDict):
    """Representa um áudio gerado pelo VoxStream."""

    name: str
    data: bytes
    text: str


def create_zip(audios: list[AudioEntry]) -> bytes:
    """Cria um arquivo ZIP em memória com todos os áudios fornecidos.

    Args:
        audios: Lista de entradas de áudio (cada uma com ``name`` e ``data``).

    Returns:
        Bytes do arquivo ZIP gerado.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for audio in audios:
            zf.writestr(f"{audio['name']}.wav", audio["data"])
    zip_bytes = zip_buffer.getvalue()
    logger.debug("ZIP criado com %d faixa(s) (%d bytes).", len(audios), len(zip_bytes))
    return zip_bytes


def build_audio_entry(name: str, data: bytes, text: str) -> AudioEntry:
    """Constrói uma entrada de áudio tipada.

    Args:
        name: Nome do arquivo (sem extensão).
        data: Bytes do arquivo WAV.
        text: Trecho de texto que originou o áudio.

    Returns:
        :class:`AudioEntry` preenchida.
    """
    return AudioEntry(name=name, data=data, text=text)
