"""Configurações e constantes do VoxStream."""

import os
from pathlib import Path

# Aceitar os termos de serviço do Coqui TTS
os.environ["COQUI_TOS_AGREED"] = "1"

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
BASE_DIR: Path = Path(__file__).resolve().parent.parent
VOICES_DIR: Path = BASE_DIR / "voices"

# ---------------------------------------------------------------------------
# Configurações do modelo TTS
# ---------------------------------------------------------------------------
TTS_MODEL: str = "tts_models/multilingual/multi-dataset/xtts_v2"
TTS_DEVICE: str = "cpu"

# ---------------------------------------------------------------------------
# Limites de processamento de texto
# ---------------------------------------------------------------------------
MAX_CHARS: int = 200
MIN_CHARS: int = 50
MAX_CHARS_LIMIT: int = 500
CHARS_STEP: int = 50

# ---------------------------------------------------------------------------
# Idiomas suportados pelo XTTS v2
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

DEFAULT_LANGUAGE: str = "Português"
DEFAULT_VOICE: str = "Voz Padrão"
DEFAULT_SPEED: float = 1.0
MIN_SPEED: float = 0.5
MAX_SPEED: float = 2.0
SPEED_STEP: float = 0.1

# ---------------------------------------------------------------------------
# Configurações de logging
# ---------------------------------------------------------------------------
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
