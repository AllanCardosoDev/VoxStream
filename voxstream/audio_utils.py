"""Audio utility helpers for VoxStream."""

import io
import zipfile
from pathlib import Path


def get_available_voices(voices_dir: str | Path = "voices") -> list[str]:
    """Return the stems of all ``.wav`` files found in *voices_dir*.

    Parameters
    ----------
    voices_dir:
        Directory to scan. Defaults to ``"voices"`` relative to cwd.

    Returns
    -------
    list[str]
        Sorted list of voice name stems (filename without extension).
    """
    directory = Path(voices_dir)
    if not directory.exists() or not directory.is_dir():
        return []
    return sorted(f.stem for f in directory.glob("*.wav"))


def create_zip(audios: list[dict]) -> bytes:
    """Compress a list of audio dicts into a ZIP archive.

    Parameters
    ----------
    audios:
        Each dict must have ``"name"`` (str) and ``"data"`` (bytes) keys.

    Returns
    -------
    bytes
        Raw ZIP archive bytes ready for download.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for audio in audios:
            zf.writestr(f"{audio['name']}.wav", audio["data"])
    return buffer.getvalue()
