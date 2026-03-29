"""Testes unitários para voxstream.audio_utils."""

from __future__ import annotations

import io
import zipfile

from voxstream.audio_utils import AudioEntry, build_audio_entry, create_zip


class TestBuildAudioEntry:
    def test_returns_correct_fields(self) -> None:
        entry = build_audio_entry(name="teste", data=b"fakewav", text="Olá")
        assert entry["name"] == "teste"
        assert entry["data"] == b"fakewav"
        assert entry["text"] == "Olá"

    def test_entry_is_typed_dict(self) -> None:
        entry = build_audio_entry(name="x", data=b"", text="")
        assert isinstance(entry, dict)


class TestCreateZip:
    def _make_entries(self, count: int = 2) -> list[AudioEntry]:
        return [
            build_audio_entry(name=f"audio{i}", data=f"wav{i}".encode(), text=f"texto {i}")
            for i in range(count)
        ]

    def test_returns_bytes(self) -> None:
        entries = self._make_entries()
        result = create_zip(entries)
        assert isinstance(result, bytes)

    def test_zip_contains_correct_files(self) -> None:
        entries = self._make_entries(3)
        zip_bytes = create_zip(entries)
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            names = set(zf.namelist())
        assert names == {"audio0.wav", "audio1.wav", "audio2.wav"}

    def test_zip_file_contents_match(self) -> None:
        entries = self._make_entries(1)
        zip_bytes = create_zip(entries)
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            content = zf.read("audio0.wav")
        assert content == b"wav0"

    def test_empty_list_creates_empty_zip(self) -> None:
        zip_bytes = create_zip([])
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            assert zf.namelist() == []
