"""TTS model loading and audio generation."""

import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def load_model(model_name: str, device: str):
    """Load and return the Coqui TTS model.

    Parameters
    ----------
    model_name:
        Coqui model identifier (e.g. ``"tts_models/multilingual/multi-dataset/xtts_v2"``).
    device:
        Torch device string, e.g. ``"cpu"`` or ``"cuda"``.
    """
    from TTS.api import TTS  # noqa: PLC0415 – deferred to keep import fast

    return TTS(model_name).to(device)


def generate_audio(
    model,
    text: str,
    language: str,
    speaker_wav: Optional[str] = None,
    speed: float = 1.0,
) -> bytes:
    """Generate TTS audio and return raw WAV bytes.

    Parameters
    ----------
    model:
        Loaded Coqui TTS model instance.
    text:
        Input text to synthesise.
    language:
        BCP-47 language code understood by the model (e.g. ``"pt"``).
    speaker_wav:
        Optional path to a reference ``.wav`` file for voice cloning.
    speed:
        Playback speed multiplier (0.5 – 2.0).

    Raises
    ------
    FileNotFoundError
        If *speaker_wav* is provided but the file does not exist.
    """
    if speaker_wav is not None and not Path(speaker_wav).exists():
        raise FileNotFoundError(f"Voice file not found: {speaker_wav}")

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".wav")
    os.close(tmp_fd)
    try:
        model.tts_to_file(
            text=text,
            file_path=tmp_path,
            speaker_wav=speaker_wav,
            language=language,
            speed=speed,
        )
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            logger.warning("Could not remove temp file: %s", tmp_path)
