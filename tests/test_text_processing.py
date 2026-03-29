"""Tests for voxstream.text_processing."""


from voxstream.text_processing import _split_by_words, split_text


class TestSplitByWords:
    def test_single_long_word(self):
        result = _split_by_words("superlongword", 5)
        assert result == ["superlongword"]

    def test_multiple_words(self):
        result = _split_by_words("one two three four five", 10)
        assert all(len(chunk) <= 10 for chunk in result)
        assert " ".join(result).replace("  ", " ") != ""

    def test_empty_string(self):
        result = _split_by_words("", 50)
        assert result == []


class TestSplitText:
    MAX = 50

    def test_short_text_returned_as_is(self):
        text = "Hello world."
        assert split_text(text, self.MAX) == [text]

    def test_text_at_exact_limit_returned_as_is(self):
        text = "A" * self.MAX
        assert split_text(text, self.MAX) == [text]

    def test_punctuation_preserved_exclamation(self):
        text = "Hello! " + "World. " * 5 + "Done!"
        parts = split_text(text, self.MAX)
        combined = " ".join(parts)
        assert "!" in combined

    def test_punctuation_preserved_question(self):
        text = "Are you there? " + "Yes I am. " * 5 + "Great?"
        parts = split_text(text, self.MAX)
        combined = " ".join(parts)
        assert "?" in combined

    def test_long_text_splits_into_multiple_parts(self):
        text = "This is sentence one. This is sentence two. This is sentence three. This is sentence four."
        parts = split_text(text, 40)
        assert len(parts) > 1
        for part in parts:
            assert len(part) <= 40

    def test_word_fallback_for_oversized_sentence(self):
        long_sentence = "word " * 30  # ~150 chars
        parts = split_text(long_sentence.strip(), 30)
        assert len(parts) > 1
        for part in parts:
            assert len(part) <= 30

    def test_empty_string(self):
        result = split_text("", 50)
        assert result == [""]

    def test_whitespace_only(self):
        result = split_text("   ", 50)
        assert result == ["   "]

    def test_respects_max_chars_default(self):
        from voxstream.config import MAX_CHARS

        long_text = ("Short sentence. " * 20).strip()
        parts = split_text(long_text)
        for part in parts:
            assert len(part) <= MAX_CHARS

    def test_single_sentence_over_limit_uses_word_fallback(self):
        sentence = "word " * 10  # 50 chars, no punctuation
        parts = split_text(sentence.strip(), 20)
        assert len(parts) >= 1
        for part in parts:
            assert len(part) <= 20 or len(part.split()) == 1

    def test_multiple_sentence_types(self):
        text = "Hello world. How are you? I am fine! Let us proceed."
        parts = split_text(text, 30)
        reconstructed = " ".join(parts)
        for punct in [".", "?", "!"]:
            if punct in text:
                assert punct in reconstructed

    def test_no_empty_parts(self):
        text = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five."
        parts = split_text(text, 30)
        assert all(p.strip() for p in parts)

    def test_returns_list(self):
        assert isinstance(split_text("hello"), list)

    def test_custom_max_chars(self):
        text = "Short. But repeated. " * 10
        parts_small = split_text(text, 30)
        parts_large = split_text(text, 200)
        assert len(parts_small) >= len(parts_large)
