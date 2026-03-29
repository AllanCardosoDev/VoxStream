"""Processamento e divisão de texto para o VoxStream."""

from __future__ import annotations

import logging
import re

from voxstream.config import MAX_CHARS

logger = logging.getLogger(__name__)


def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Divide *text* em partes menores respeitando pontuação.

    O algoritmo tenta manter as partes dentro de *max_chars* caracteres.
    A divisão é feita respeitando a pontuação original (`.`, `!`, `?`).
    Quando uma sentença individual excede *max_chars*, aplica-se um fallback
    que quebra o texto por palavras.

    Args:
        text: Texto completo a ser dividido.
        max_chars: Número máximo de caracteres por parte.

    Returns:
        Lista de strings com as partes do texto.  Se o texto for menor ou
        igual a *max_chars*, retorna uma lista com o texto completo.
    """
    text = text.strip()
    if not text:
        return []

    if len(text) <= max_chars:
        return [text]

    # Divide mantendo os delimitadores de sentença no final de cada trecho
    raw_sentences: list[str] = [
        s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()
    ]

    parts: list[str] = []
    current_part: str = ""

    for sentence in raw_sentences:
        # Sentença maior que max_chars → fallback por palavras
        if len(sentence) > max_chars:
            if current_part:
                parts.append(current_part.strip())
                current_part = ""
            parts.extend(_split_by_words(sentence, max_chars))
            continue

        candidate = (current_part + " " + sentence).strip() if current_part else sentence
        if len(candidate) <= max_chars:
            current_part = candidate
        else:
            if current_part:
                parts.append(current_part.strip())
            current_part = sentence

    if current_part:
        parts.append(current_part.strip())

    logger.debug("Texto dividido em %d parte(s) (max_chars=%d).", len(parts), max_chars)
    return parts


def _split_by_words(text: str, max_chars: int) -> list[str]:
    """Divide *text* em partes por palavras quando nenhuma sentença cabe.

    Args:
        text: Texto a ser dividido.
        max_chars: Limite de caracteres por parte.

    Returns:
        Lista de strings com as partes.
    """
    words = text.split()
    parts: list[str] = []
    current_part: str = ""

    for word in words:
        candidate = (current_part + " " + word).strip() if current_part else word
        if len(candidate) <= max_chars:
            current_part = candidate
        else:
            if current_part:
                parts.append(current_part.strip())
            # Palavra sozinha maior que o limite → forçar inclusão
            current_part = word

    if current_part:
        parts.append(current_part.strip())

    return parts


def count_chars(text: str) -> int:
    """Retorna o número de caracteres em *text*.

    Args:
        text: Texto a ser contado.

    Returns:
        Número de caracteres.
    """
    return len(text)
