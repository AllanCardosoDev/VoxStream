"""Configurações e constantes do VoxStream."""

import logging

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# TTS
# ---------------------------------------------------------------------------

#: Aceita automaticamente os termos de uso do Coqui TTS.
COQUI_TOS_AGREED: str = "1"

#: Nome do modelo XTTS v2 usado para síntese de voz.
TTS_MODEL_NAME: str = "tts_models/multilingual/multi-dataset/xtts_v2"

# ---------------------------------------------------------------------------
# Processamento de texto
# ---------------------------------------------------------------------------

#: Número máximo de caracteres por segmento de áudio.
MAX_CHARS: int = 200

# ---------------------------------------------------------------------------
# Idiomas suportados
# ---------------------------------------------------------------------------

LANGUAGES: dict[str, str] = {
    "Português": "pt",
    "English": "en",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it",
    "Polski": "pl",
    "Türkçe": "tr",
    "Русский": "ru",
    "Nederlands": "nl",
    "Čeština": "cs",
    "العربية": "ar",
    "中文": "zh-cn",
    "日本語": "ja",
    "Magyar": "hu",
    "한국어": "ko",
}

# ---------------------------------------------------------------------------
# Caminhos padrão
# ---------------------------------------------------------------------------

#: Diretório que contém os arquivos de voz de referência (.wav).
VOICES_DIR: str = "voices"

#: Voz padrão exibida na UI quando nenhuma voz customizada é selecionada.
DEFAULT_VOICE_LABEL: str = "Voz Padrão"
