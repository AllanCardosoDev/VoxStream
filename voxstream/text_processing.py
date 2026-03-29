"""Módulo de processamento de texto para o VoxStream.

Fornece utilitários para segmentar textos longos em partes menores
adequadas para síntese de voz, preservando a pontuação original.
"""

from __future__ import annotations

import logging
import re

from .config import MAX_CHARS

logger = logging.getLogger(__name__)

# Padrão que captura delimitadores de sentença, mantendo-os no resultado.
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")


def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Divide *text* em segmentos de no máximo *max_chars* caracteres.

    O algoritmo preserva a pontuação original e tenta quebrar nos limites
    de sentenças (`.`, `!`, `?`).  Se uma sentença individual for maior que
    *max_chars*, ela é dividida na fronteira de palavras.

    Parameters
    ----------
    text:
        Texto de entrada a ser segmentado.
    max_chars:
        Número máximo de caracteres por segmento.  Deve ser ≥ 1.

    Returns
    -------
    list[str]
        Lista com um ou mais segmentos não-vazios.

    Examples
    --------
    >>> split_text("Olá mundo!", max_chars=50)
    ['Olá mundo!']
    >>> parts = split_text("A. B. C.", max_chars=4)
    >>> all(len(p) <= 4 for p in parts)
    True
    """
    text = text.strip()
    if not text:
        logger.warning("split_text recebeu texto vazio.")
        return []

    if len(text) <= max_chars:
        return [text]

    # Divide nas fronteiras de sentença preservando a pontuação.
    sentences: list[str] = _SENTENCE_BOUNDARY.split(text)

    parts: list[str] = []
    current: str = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # A sentença cabe no segmento atual.
        candidate = (current + " " + sentence).strip() if current else sentence
        if len(candidate) <= max_chars:
            current = candidate
        else:
            # Salva o segmento atual e começa um novo.
            if current:
                parts.append(current)
            # A sentença pode ainda ser maior que max_chars → quebra por palavras.
            if len(sentence) > max_chars:
                parts.extend(_split_by_words(sentence, max_chars))
                current = ""
            else:
                current = sentence

    if current:
        parts.append(current)

    logger.debug("Texto dividido em %d parte(s).", len(parts))
    return parts


def _split_by_words(text: str, max_chars: int) -> list[str]:
    """Divide *text* na fronteira de palavras quando excede *max_chars*.

    Parameters
    ----------
    text:
        Texto que excede *max_chars* caracteres e não contém
        delimitadores de sentença aproveitáveis.
    max_chars:
        Limite de caracteres por segmento.

    Returns
    -------
    list[str]
        Segmentos resultantes, cada um com no máximo *max_chars* caracteres
        (exceto se uma palavra individual for maior que *max_chars*).
    """
    words = text.split()
    parts: list[str] = []
    current = ""

    for word in words:
        candidate = (current + " " + word).strip() if current else word
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                parts.append(current)
            # Palavra maior que o limite: mantém inteira em um segmento próprio.
            current = word

    if current:
        parts.append(current)

    return parts
