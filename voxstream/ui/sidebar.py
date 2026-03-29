"""Sidebar rendering for VoxStream."""

import streamlit as st


def render_sidebar(
    *,
    char_limit: int,
    language: str,
    voice: str,
    audio_count: int,
    text_length: int,
) -> None:
    """Render the application sidebar.

    Parameters
    ----------
    char_limit:
        Currently configured character limit per chunk.
    language:
        Selected language name.
    voice:
        Selected voice name.
    audio_count:
        Number of audios generated in the current session.
    text_length:
        Length of the current input text.
    """
    with st.sidebar:
        st.markdown(
            "<div style='text-align: center; padding: 20px;'>"
            "<h2 style='color: #1E88E5;'>VoxStream</h2>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.header("ℹ️ Informações")
        st.markdown(
            f"""
### Configurações Atuais
- Limite: {char_limit} caracteres
- Idioma: {language}
- Voz: {voice}

### Estatísticas
- Áudios gerados: {audio_count}
- Caracteres total: {text_length}
"""
        )

        st.markdown("---")
        st.markdown(
            """
### Como usar
1. Digite um nome para o áudio
2. Cole ou digite seu texto
3. Escolha voz e idioma
4. Clique em 'Gerar Áudio'

Textos longos serão divididos automaticamente!
"""
        )
