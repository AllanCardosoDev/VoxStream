"""Constants and environment-based configuration for VoxStream."""

import logging
import os

# ---------------------------------------------------------------------------
# TTS model
# ---------------------------------------------------------------------------
TTS_MODEL: str = "tts_models/multilingual/multi-dataset/xtts_v2"

# ---------------------------------------------------------------------------
# Inference device
# ---------------------------------------------------------------------------
TTS_DEVICE: str = os.environ.get("TTS_DEVICE", "cpu")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))

# ---------------------------------------------------------------------------
# Text splitting
# ---------------------------------------------------------------------------
MAX_CHARS: int = 200

# ---------------------------------------------------------------------------
# Supported languages
# ---------------------------------------------------------------------------
LANGUAGES: dict[str, str] = {
    "Portuguese": "pt",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Polish": "pl",
    "Turkish": "tr",
    "Russian": "ru",
    "Dutch": "nl",
    "Czech": "cs",
    "Arabic": "ar",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Hungarian": "hu",
    "Korean": "ko",
}
