"""Sidebar do VoxStream."""

from __future__ import annotations

import logging

import streamlit as st

from voxstream.audio_utils import AudioEntry
from voxstream.config import LANGUAGES
from voxstream.text_processing import count_chars

logger = logging.getLogger(__name__)


def render_sidebar(
    audios: list[AudioEntry],
    text_input: str,
    selected_language: str,
    selected_voice: str,
    custom_limit: int,
) -> None:
    """Renderiza a sidebar com informações, histórico e guia de uso.

    Args:
        audios: Áudios gerados na sessão atual.
        text_input: Texto atualmente digitado pelo usuário.
        selected_language: Nome do idioma selecionado.
        selected_voice: Nome da voz selecionada.
        custom_limit: Limite de caracteres configurado.
    """
    with st.sidebar:
        st.markdown(
            "<div style='text-align:center;padding:20px;'>"
            "<h2 style='color:#1E88E5;'>🎤 VoxStream</h2>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.header("ℹ️ Informações")
        st.markdown(
            f"""
### Configurações Atuais
- **Limite:** {custom_limit} caracteres
- **Idioma:** {selected_language} (`{LANGUAGES.get(selected_language, '?')}`)
- **Voz:** {selected_voice}

### Estatísticas da Sessão
- Áudios gerados: **{len(audios)}**
- Caracteres no texto: **{count_chars(text_input)}**
"""
        )

        if audios:
            st.markdown("---")
            st.markdown("### 🕘 Histórico")
            for audio in audios:
                st.markdown(f"- 🔊 `{audio['name']}.wav`")

        st.markdown("---")
        st.markdown(
            """
### Como usar
1. Digite um **nome** para o áudio
2. Cole ou escreva seu **texto**
3. Escolha a **voz** e o **idioma**
4. Clique em **Gerar Áudio**

Textos longos são divididos automaticamente!
"""
        )
