"""Sidebar do VoxStream."""

from __future__ import annotations

import streamlit as st


def render_sidebar(
    custom_limit: int,
    selected_language: str,
    selected_voice: str,
    num_audios: int,
    num_chars: int,
) -> None:
    """Renderiza a barra lateral com informações e instruções de uso.

    Parameters
    ----------
    custom_limit:
        Limite de caracteres configurado pelo usuário.
    selected_language:
        Idioma selecionado (nome legível).
    selected_voice:
        Voz selecionada (nome legível).
    num_audios:
        Número de áudios já gerados na sessão.
    num_chars:
        Total de caracteres do texto atual.
    """
    with st.sidebar:
        st.markdown(
            "<div style='text-align: center; padding: 20px;'>"
            "<h2 style='color: #1E88E5;'>🎤 VoxStream</h2>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.header("ℹ️ Informações")
        st.markdown(
            f"""
            ### Configurações Atuais
            - **Limite:** {custom_limit} caracteres
            - **Idioma:** {selected_language}
            - **Voz:** {selected_voice}

            ### Estatísticas
            - **Áudios gerados:** {num_audios}
            - **Caracteres no texto:** {num_chars}
            """
        )

        st.markdown("---")
        st.markdown(
            """
            ### Como usar
            1. Digite um nome para o áudio
            2. Cole ou digite seu texto
            3. Escolha voz e idioma
            4. Clique em **Gerar Áudio**

            Textos longos serão divididos automaticamente!
            """
        )

        st.markdown("---")
        st.markdown(
            """
            ### Sobre
            VoxStream usa o modelo **XTTS v2** da Coqui TTS para
            gerar voz com clonagem de voz de alta qualidade em
            16 idiomas.
            """
        )
