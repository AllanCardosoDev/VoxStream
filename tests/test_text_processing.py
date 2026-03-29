"""Testes unitários para voxstream.text_processing."""

from __future__ import annotations

from voxstream.text_processing import _split_by_words, count_chars, split_text

# ---------------------------------------------------------------------------
# split_text
# ---------------------------------------------------------------------------

class TestSplitText:
    def test_text_within_limit_returns_single_part(self) -> None:
        text = "Olá, mundo!"
        result = split_text(text, max_chars=50)
        assert result == [text]

    def test_empty_string_returns_empty_list(self) -> None:
        assert split_text("", max_chars=50) == []

    def test_whitespace_only_returns_empty_list(self) -> None:
        assert split_text("   ", max_chars=50) == []

    def test_text_exactly_at_limit_returns_single_part(self) -> None:
        text = "A" * 50
        result = split_text(text, max_chars=50)
        assert result == [text]

    def test_split_respects_sentence_boundaries(self) -> None:
        text = "Primeira sentença. Segunda sentença. Terceira sentença."
        result = split_text(text, max_chars=30)
        # Cada parte deve ter no máximo 30 chars
        for part in result:
            assert len(part) <= 30

    def test_split_preserves_exclamation_mark(self) -> None:
        text = "Atenção! Isso é importante. Continue lendo por favor."
        result = split_text(text, max_chars=30)
        joined = " ".join(result)
        # A exclamação não deve ser perdida
        assert "!" in joined

    def test_split_preserves_question_mark(self) -> None:
        text = "Como você está? Espero que bem. Até logo."
        result = split_text(text, max_chars=25)
        joined = " ".join(result)
        assert "?" in joined

    def test_sentence_larger_than_limit_uses_word_fallback(self) -> None:
        long_word_sentence = "Esta é uma sentença extremamente longa sem pontuação que ultrapassa o limite"
        result = split_text(long_word_sentence, max_chars=20)
        assert len(result) > 1
        for part in result:
            # O único caso aceitável de exceder é uma palavra sozinha maior que limit
            words_in_part = part.split()
            if len(words_in_part) > 1:
                assert len(part) <= 20

    def test_multiple_sentences_grouped_correctly(self) -> None:
        text = "Um. Dois. Três. Quatro. Cinco."
        result = split_text(text, max_chars=15)
        assert len(result) >= 1
        for part in result:
            assert len(part) <= 15

    def test_returns_list_of_strings(self) -> None:
        text = "Texto de teste para verificar o tipo de retorno."
        result = split_text(text, max_chars=10)
        assert isinstance(result, list)
        for part in result:
            assert isinstance(part, str)

    def test_no_empty_parts(self) -> None:
        text = "Sentença um. Sentença dois. Sentença três."
        result = split_text(text, max_chars=20)
        for part in result:
            assert part.strip() != ""

    def test_custom_max_chars(self) -> None:
        text = "a" * 100
        result_100 = split_text(text, max_chars=100)
        result_50 = split_text(text, max_chars=50)
        assert len(result_100) <= len(result_50)


# ---------------------------------------------------------------------------
# _split_by_words
# ---------------------------------------------------------------------------

class TestSplitByWords:
    def test_single_word_within_limit(self) -> None:
        assert _split_by_words("hello", 10) == ["hello"]

    def test_words_split_correctly(self) -> None:
        text = "um dois três quatro cinco"
        result = _split_by_words(text, max_chars=9)
        for part in result:
            words = part.split()
            if len(words) > 1:
                assert len(part) <= 9

    def test_word_larger_than_limit_included_alone(self) -> None:
        text = "supercalifragilisticexpialidocious"
        result = _split_by_words(text, max_chars=5)
        assert len(result) == 1
        assert result[0] == text


# ---------------------------------------------------------------------------
# count_chars
# ---------------------------------------------------------------------------

class TestCountChars:
    def test_empty_string(self) -> None:
        assert count_chars("") == 0

    def test_simple_string(self) -> None:
        assert count_chars("abc") == 3

    def test_unicode(self) -> None:
        assert count_chars("café") == 4
