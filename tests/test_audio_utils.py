"""Tests for voxstream.audio_utils."""

import io
import zipfile

from voxstream.audio_utils import create_zip, get_available_voices


class TestGetAvailableVoices:
    def test_nonexistent_directory_returns_empty(self, tmp_path):
        result = get_available_voices(tmp_path / "does_not_exist")
        assert result == []

    def test_empty_directory_returns_empty(self, tmp_path):
        result = get_available_voices(tmp_path)
        assert result == []

    def test_directory_with_wav_files_returns_stems(self, tmp_path):
        (tmp_path / "voice_a.wav").write_bytes(b"")
        (tmp_path / "voice_b.wav").write_bytes(b"")
        result = get_available_voices(tmp_path)
        assert sorted(result) == ["voice_a", "voice_b"]

    def test_mixed_files_returns_only_wav_stems(self, tmp_path):
        (tmp_path / "good.wav").write_bytes(b"")
        (tmp_path / "bad.mp3").write_bytes(b"")
        (tmp_path / "ugly.txt").write_bytes(b"")
        result = get_available_voices(tmp_path)
        assert result == ["good"]

    def test_returns_sorted_list(self, tmp_path):
        for name in ["zebra.wav", "alpha.wav", "mango.wav"]:
            (tmp_path / name).write_bytes(b"")
        result = get_available_voices(tmp_path)
        assert result == sorted(result)

    def test_path_string_input(self, tmp_path):
        (tmp_path / "voice.wav").write_bytes(b"")
        result = get_available_voices(str(tmp_path))
        assert result == ["voice"]

    def test_returns_list_type(self, tmp_path):
        assert isinstance(get_available_voices(tmp_path), list)

    def test_file_as_path_returns_empty(self, tmp_path):
        f = tmp_path / "not_a_dir.wav"
        f.write_bytes(b"")
        result = get_available_voices(f)
        assert result == []


class TestCreateZip:
    def test_creates_valid_zip(self):
        audios = [{"name": "clip1", "data": b"WAVE_DATA_1"}]
        result = create_zip(audios)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            assert "clip1.wav" in zf.namelist()

    def test_multiple_files_in_zip(self):
        audios = [
            {"name": "a", "data": b"data_a"},
            {"name": "b", "data": b"data_b"},
        ]
        result = create_zip(audios)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            assert sorted(zf.namelist()) == ["a.wav", "b.wav"]

    def test_zip_file_contents_match(self):
        payload = b"hello wave"
        audios = [{"name": "test", "data": payload}]
        result = create_zip(audios)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            assert zf.read("test.wav") == payload

    def test_empty_list_returns_valid_zip(self):
        result = create_zip([])
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            assert zf.namelist() == []

    def test_returns_bytes(self):
        assert isinstance(create_zip([]), bytes)
