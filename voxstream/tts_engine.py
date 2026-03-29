"""Motor de síntese de voz (TTS) do VoxStream."""

from __future__ import annotations

import logging
import os
import tempfile

from voxstream.config import TTS_DEVICE, TTS_MODEL, VOICES_DIR

logger = logging.getLogger(__name__)


def load_model():  # type: ignore[return]
    """Carrega e retorna o modelo XTTS v2.

    Usa ``@st.cache_resource`` quando chamado a partir da camada de UI.
    Esta função pode ser chamada diretamente em testes — sem Streamlit.

    Returns:
        Instância de ``TTS`` configurada para CPU, ou ``None`` em caso de erro.
    """
    try:
        from TTS.api import TTS  # noqa: PLC0415  (import local intencional)

        logger.info("Carregando modelo TTS: %s no dispositivo '%s'.", TTS_MODEL, TTS_DEVICE)
        model = TTS(TTS_MODEL).to(TTS_DEVICE)
        logger.info("Modelo TTS carregado com sucesso.")
        return model
    except Exception:
        logger.exception("Falha ao carregar o modelo TTS.")
        return None


def get_available_voices() -> list[str]:
    """Retorna os nomes (sem extensão) dos arquivos de voz disponíveis.

    Returns:
        Lista ordenada com os stems dos arquivos ``.wav`` em ``VOICES_DIR``.
    """
    if not VOICES_DIR.exists():
        logger.warning("Diretório de vozes não encontrado: %s", VOICES_DIR)
        return []
    voices = sorted(f.stem for f in VOICES_DIR.glob("*.wav"))
    logger.debug("Vozes disponíveis: %s", voices)
    return voices


def generate_audio(
    model,
    text: str,
    language: str,
    speaker_voice: str | None,
    speed: float = 1.0,
) -> bytes:
    """Gera áudio a partir de *text* usando o modelo TTS.

    Args:
        model: Instância do modelo TTS (retornada por :func:`load_model`).
        text: Texto a ser convertido em áudio.
        language: Código do idioma (ex.: ``"pt"``).
        speaker_voice: Nome da voz (sem extensão) ou ``None`` para voz padrão.
        speed: Velocidade de fala.  Padrão ``1.0``.

    Returns:
        Bytes do arquivo WAV gerado.

    Raises:
        FileNotFoundError: Se o arquivo de voz ``speaker_voice`` não existir.
        RuntimeError: Em caso de falha na síntese.
    """
    speaker_wav: str | None = None
    if speaker_voice:
        voice_path = VOICES_DIR / f"{speaker_voice}.wav"
        if not voice_path.exists():
            raise FileNotFoundError(
                f"Arquivo de voz não encontrado: {voice_path}"
            )
        speaker_wav = str(voice_path)

    temp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            temp_path = tmp.name

        logger.debug(
            "Gerando áudio — idioma=%s, voz=%s, speed=%.1f, chars=%d.",
            language,
            speaker_voice or "padrão",
            speed,
            len(text),
        )
        model.tts_to_file(
            text=text,
            file_path=temp_path,
            speaker_wav=speaker_wav,
            language=language,
            speed=speed,
        )

        with open(temp_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        logger.debug("Áudio gerado com sucesso (%d bytes).", len(audio_bytes))
        return audio_bytes

    except Exception:
        logger.exception("Erro durante a geração de áudio.")
        raise
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
            logger.debug("Arquivo temporário removido: %s", temp_path)


def estimate_generation_time(num_chars: int, num_parts: int) -> float:
    """Estima o tempo de geração em segundos (aproximação conservadora).

    Args:
        num_chars: Total de caracteres a gerar.
        num_parts: Número de partes em que o texto foi dividido.

    Returns:
        Estimativa em segundos.
    """
    # ~2 s por parte + 0.05 s por caractere (baseado em benchmarks empíricos)
    return num_parts * 2.0 + num_chars * 0.05
