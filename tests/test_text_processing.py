"""Testes unitários para voxstream.text_processing."""

from __future__ import annotations

import pytest

from voxstream.text_processing import split_text, _split_by_words


class TestSplitText:
    """Testes para a função split_text."""

    def test_texto_curto_retorna_lista_com_um_elemento(self):
        """Texto menor que max_chars não deve ser dividido."""
        text = "Olá, mundo!"
        result = split_text(text, max_chars=50)
        assert result == [text]

    def test_texto_exatamente_no_limite(self):
        """Texto com exatamente max_chars caracteres não deve ser dividido."""
        text = "A" * 200
        result = split_text(text, max_chars=200)
        assert result == [text]

    def test_texto_vazio_retorna_lista_vazia(self):
        """Texto vazio deve retornar lista vazia."""
        result = split_text("", max_chars=200)
        assert result == []

    def test_texto_somente_espacos_retorna_lista_vazia(self):
        """Texto com apenas espaços deve retornar lista vazia."""
        result = split_text("   ", max_chars=200)
        assert result == []

    def test_divisao_preserva_ponto_de_exclamacao(self):
        """O ponto de exclamação deve ser preservado, não substituído por ponto."""
        text = "Olá! Como vai você? Tudo bem."
        result = split_text(text, max_chars=15)
        joined = " ".join(result)
        assert "!" in joined
        assert "?" in joined

    def test_divisao_preserva_ponto_de_interrogacao(self):
        """O ponto de interrogação deve ser preservado."""
        text = "Você está bem? Espero que sim."
        result = split_text(text, max_chars=20)
        joined = " ".join(result)
        assert "?" in joined

    def test_todos_segmentos_respeitam_limite(self):
        """Todos os segmentos devem ter comprimento ≤ max_chars."""
        text = (
            "Esta é uma frase longa. Esta é outra frase longa. "
            "E mais uma frase aqui. Acabando com esta última frase."
        )
        max_chars = 40
        result = split_text(text, max_chars=max_chars)
        for part in result:
            assert len(part) <= max_chars, f"Parte muito longa: '{part}' ({len(part)} chars)"

    def test_sem_partes_vazias(self):
        """Nenhum segmento deve ser vazio ou conter apenas espaços."""
        text = "Primeira sentença. Segunda sentença. Terceira sentença."
        result = split_text(text, max_chars=25)
        for part in result:
            assert part.strip() != ""

    def test_conteudo_preservado(self):
        """O conteúdo do texto original deve estar presente nos segmentos."""
        text = "Olá mundo! Como você está?"
        result = split_text(text, max_chars=15)
        joined = " ".join(result)
        # Palavras-chave devem aparecer no resultado
        assert "Olá" in joined
        assert "mundo" in joined

    def test_sentenca_maior_que_limite_dividida_por_palavras(self):
        """Sentença maior que max_chars deve ser dividida na fronteira de palavras."""
        text = "Esta é uma sentença muito longa que excede o limite de caracteres definido"
        max_chars = 20
        result = split_text(text, max_chars=max_chars)
        assert len(result) > 1
        for part in result:
            assert len(part) <= max_chars or " " not in part  # palavra longa: exceção

    def test_retorna_lista(self):
        """O retorno deve ser sempre uma lista."""
        assert isinstance(split_text("Teste"), list)

    def test_multiplas_sentencas(self):
        """Texto com múltiplas sentenças deve ser dividido corretamente."""
        sentences = ["Frase um.", "Frase dois.", "Frase três.", "Frase quatro."]
        text = " ".join(sentences)
        result = split_text(text, max_chars=15)
        assert len(result) >= 2


class TestSplitByWords:
    """Testes para a função auxiliar _split_by_words."""

    def test_texto_curto_retorna_um_segmento(self):
        result = _split_by_words("Olá mundo", max_chars=20)
        assert result == ["Olá mundo"]

    def test_texto_longo_dividido(self):
        text = "um dois tres quatro cinco"
        result = _split_by_words(text, max_chars=10)
        assert len(result) > 1

    def test_todos_segmentos_respeitam_limite(self):
        text = "palavra1 palavra2 palavra3 palavra4 palavra5"
        max_chars = 15
        result = _split_by_words(text, max_chars=max_chars)
        for part in result:
            # Exceção: palavra individual maior que limite
            assert len(part) <= max_chars or " " not in part

    def test_palavra_unica_longa(self):
        """Uma palavra mais longa que max_chars deve aparecer em seu próprio segmento."""
        word = "supercalifragilísticaexpialidocioso"
        result = _split_by_words(word, max_chars=10)
        assert len(result) == 1
        assert result[0] == word
