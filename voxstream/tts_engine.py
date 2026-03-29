"""Motor TTS do VoxStream.

Responsável por carregar o modelo Coqui XTTS v2 e gerar áudio a partir
de texto, com suporte a vozes de referência personalizadas.
"""

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

from .config import COQUI_TOS_AGREED, LANGUAGES, TTS_MODEL_NAME

logger = logging.getLogger(__name__)

# Aceita os termos de uso do Coqui TTS de forma não-interativa.
os.environ["COQUI_TOS_AGREED"] = COQUI_TOS_AGREED


def load_model() -> Optional[object]:
    """Carrega e retorna o modelo XTTS v2.

    O modelo é pesado (~1,8 GB) e deve ser mantido em cache via
    ``@st.cache_resource`` na camada da UI.

    Returns
    -------
    TTS | None
        Instância do modelo TTS ou ``None`` em caso de falha.
    """
    try:
        from TTS.api import TTS  # type: ignore[import]

        logger.info("Carregando modelo TTS: %s", TTS_MODEL_NAME)
        model = TTS(TTS_MODEL_NAME).to("cpu")
        logger.info("Modelo TTS carregado com sucesso.")
        return model
    except Exception:
        logger.exception("Falha ao carregar o modelo TTS.")
        return None


def get_available_voices(voices_dir: str = "voices") -> list[str]:
    """Retorna a lista de nomes de voz disponíveis no diretório *voices_dir*.

    Parameters
    ----------
    voices_dir:
        Caminho para o diretório contendo arquivos ``.wav`` de referência.

    Returns
    -------
    list[str]
        Nomes dos arquivos ``.wav`` sem extensão, em ordem alfabética.
    """
    path = Path(voices_dir)
    if not path.exists():
        logger.warning("Diretório de vozes não encontrado: %s", voices_dir)
        return []
    voices = sorted(f.stem for f in path.glob("*.wav"))
    logger.debug("%d voz(es) encontrada(s) em '%s'.", len(voices), voices_dir)
    return voices


def generate_audio(
    model: object,
    text: str,
    language: str,
    speed: float = 1.0,
    speaker_wav: Optional[str] = None,
) -> bytes:
    """Gera áudio WAV a partir de *text* usando o *model* TTS.

    Utiliza um arquivo temporário para a saída do modelo e garante a sua
    remoção mesmo em caso de erro.

    Parameters
    ----------
    model:
        Instância do modelo TTS (retornada por :func:`load_model`).
    text:
        Texto a ser sintetizado.
    language:
        Código do idioma conforme :data:`~voxstream.config.LANGUAGES`
        (ex.: ``"pt"``, ``"en"``).
    speed:
        Fator de velocidade de fala (0.5–2.0).
    speaker_wav:
        Caminho para o arquivo ``.wav`` de referência de voz.  Se ``None``,
        usa a voz padrão do modelo.

    Returns
    -------
    bytes
        Conteúdo binário do arquivo WAV gerado.

    Raises
    ------
    ValueError
        Se *language* não for um código de idioma válido.
    FileNotFoundError
        Se *speaker_wav* for informado mas o arquivo não existir.
    RuntimeError
        Se a síntese de voz falhar por qualquer outro motivo.
    """
    valid_codes = set(LANGUAGES.values())
    if language not in valid_codes:
        raise ValueError(
            f"Código de idioma inválido: '{language}'. "
            f"Valores aceitos: {sorted(valid_codes)}"
        )

    if speaker_wav is not None and not Path(speaker_wav).exists():
        raise FileNotFoundError(
            f"Arquivo de voz de referência não encontrado: '{speaker_wav}'"
        )

    temp_path: Optional[str] = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            temp_path = tmp.name

        logger.debug(
            "Gerando áudio | idioma=%s | velocidade=%.1f | voz=%s | texto='%s...'",
            language,
            speed,
            speaker_wav or "padrão",
            text[:40],
        )

        model.tts_to_file(  # type: ignore[attr-defined]
            text=text,
            file_path=temp_path,
            speaker_wav=speaker_wav,
            language=language,
            speed=speed,
        )

        with open(temp_path, "rb") as f:
            audio_bytes = f.read()

        logger.info("Áudio gerado: %d bytes.", len(audio_bytes))
        return audio_bytes

    except (ValueError, FileNotFoundError):
        raise
    except Exception as exc:
        raise RuntimeError(f"Falha ao gerar áudio: {exc}") from exc
    finally:
        if temp_path and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
                logger.debug("Arquivo temporário removido: %s", temp_path)
            except OSError:
                logger.warning(
                    "Não foi possível remover arquivo temporário: %s", temp_path
                )
