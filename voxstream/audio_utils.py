"""Utilitários de áudio para o VoxStream.

Funções auxiliares para empacotar múltiplos arquivos WAV em um ZIP
e outras operações de I/O relacionadas a áudio.
"""

from __future__ import annotations

import io
import logging
import zipfile

logger = logging.getLogger(__name__)


def build_zip(audios: list[dict]) -> bytes:
    """Empacota uma lista de áudios gerados em um arquivo ZIP em memória.

    Parameters
    ----------
    audios:
        Lista de dicionários com as chaves:

        * ``"name"`` (``str``) — nome base do arquivo (sem extensão).
        * ``"data"`` (``bytes``) — conteúdo binário do WAV.

    Returns
    -------
    bytes
        Conteúdo do arquivo ZIP pronto para download.

    Examples
    --------
    >>> audios = [{"name": "audio1", "data": b"RIFF..."}, {"name": "audio2", "data": b"RIFF..."}]
    >>> zip_bytes = build_zip(audios)
    >>> isinstance(zip_bytes, bytes)
    True
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for audio in audios:
            filename = f"{audio['name']}.wav"
            zf.writestr(filename, audio["data"])
            logger.debug("Adicionado ao ZIP: %s (%d bytes)", filename, len(audio["data"]))

    zip_bytes = buffer.getvalue()
    logger.info("ZIP criado com %d arquivo(s): %d bytes.", len(audios), len(zip_bytes))
    return zip_bytes
