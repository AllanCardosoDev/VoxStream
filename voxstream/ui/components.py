"""Componentes reutilizáveis de UI do VoxStream."""

from __future__ import annotations

import logging

import streamlit as st

from voxstream.audio_utils import AudioEntry, create_zip
from voxstream.config import (
    CHARS_STEP,
    DEFAULT_LANGUAGE,
    DEFAULT_SPEED,
    DEFAULT_VOICE,
    LANGUAGES,
    MAX_CHARS,
    MAX_CHARS_LIMIT,
    MAX_SPEED,
    MIN_CHARS,
    MIN_SPEED,
    SPEED_STEP,
)
from voxstream.text_processing import count_chars, split_text
from voxstream.tts_engine import estimate_generation_time, get_available_voices

logger = logging.getLogger(__name__)


def render_header() -> None:
    """Renderiza o cabeçalho principal da aplicação."""
    st.markdown(
        """
        <h1 style='text-align:center;color:#1E88E5;margin-bottom:0;'>
            🎤 VoxStream
        </h1>
        <h3 style='text-align:center;color:#666;margin-top:0;'>
            Gerador de Voz Multilíngue com IA
        </h3>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")


def render_footer() -> None:
    """Renderiza o rodapé da aplicação."""
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;color:#666;'>"
        "<p>VoxStream — Desenvolvido com ❤️ usando Streamlit e Coqui TTS</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_text_inputs() -> tuple[str, str]:
    """Renderiza os campos de nome e texto do áudio.

    Returns:
        Tupla ``(audio_name, text_input)``.
    """
    audio_name: str = st.text_input(
        "Nome do áudio:",
        placeholder="Digite o nome base para o(s) arquivo(s)",
        help="Se o texto for dividido será adicionado um número ao final (ex.: nome1, nome2)",
    )

    text_input: str = st.text_area(
        "Digite o texto para converter em áudio:",
        height=200,
        placeholder="Digite seu texto aqui…",
    )

    # Contador de caracteres em tempo real
    char_count = count_chars(text_input)
    _render_char_counter(char_count)

    return audio_name, text_input


def _render_char_counter(char_count: int) -> None:
    """Renderiza o contador de caracteres abaixo do text_area."""
    css_class = "char-counter over-limit" if char_count > MAX_CHARS else "char-counter"
    st.markdown(
        f"<div class='{css_class}'>{char_count} caractere(s)</div>",
        unsafe_allow_html=True,
    )


def render_split_preview(text_input: str, custom_limit: int) -> None:
    """Exibe uma pré-visualização da divisão do texto quando aplicável.

    Args:
        text_input: Texto fornecido pelo usuário.
        custom_limit: Limite de caracteres configurado pelo usuário.
    """
    if not text_input:
        return
    parts = split_text(text_input, custom_limit)
    if len(parts) > 1:
        est = estimate_generation_time(count_chars(text_input), len(parts))
        st.info(
            f"ℹ️ Texto será dividido em **{len(parts)}** partes "
            f"— estimativa de geração: ~{est:.0f} s"
        )


def render_settings() -> tuple[str, str, float, bool, int]:
    """Renderiza o painel de configurações (coluna direita).

    Returns:
        Tupla ``(selected_voice, selected_language, speed, autoplay, custom_limit)``.
    """
    st.subheader("⚙️ Configurações")

    # Voz
    available_voices = get_available_voices()
    if available_voices:
        voice_options = [DEFAULT_VOICE] + available_voices
        selected_voice: str = st.selectbox("Voz:", voice_options)
    else:
        selected_voice = DEFAULT_VOICE
        st.info("Adicione arquivos .wav na pasta 'voices' para usar vozes customizadas.")

    # Idioma
    selected_language: str = st.selectbox(
        "Idioma:",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(DEFAULT_LANGUAGE),
    )

    # Velocidade
    speed: float = st.slider("Velocidade:", MIN_SPEED, MAX_SPEED, DEFAULT_SPEED, SPEED_STEP)

    st.markdown("### Opções")
    autoplay: bool = st.checkbox("Reproduzir automaticamente", value=True)

    # Limite de caracteres
    custom_limit: int = st.number_input(
        "Limite de caracteres por parte:",
        min_value=MIN_CHARS,
        max_value=MAX_CHARS_LIMIT,
        value=MAX_CHARS,
        step=CHARS_STEP,
    )

    return selected_voice, selected_language, speed, autoplay, custom_limit


def render_audio_results(audios: list[AudioEntry], audio_name: str, autoplay: bool) -> None:
    """Renderiza os áudios gerados com controles de reprodução e download.

    Args:
        audios: Lista de entradas de áudio.
        audio_name: Nome base usado na geração (para o ZIP).
        autoplay: Se ``True``, o primeiro áudio é reproduzido automaticamente.
    """
    if not audios:
        return

    st.markdown("---")
    st.subheader("🎵 Áudios Gerados")

    for i, audio in enumerate(audios):
        col_player, col_dl, col_text = st.columns([3, 1, 1])

        with col_player:
            st.markdown(
                f"<div class='audio-card'><strong>{audio['name']}</strong></div>",
                unsafe_allow_html=True,
            )
            st.audio(audio["data"], format="audio/wav", autoplay=autoplay and i == 0)

        with col_dl:
            st.download_button(
                label="📥 Baixar",
                data=audio["data"],
                file_name=f"{audio['name']}.wav",
                mime="audio/wav",
                key=f"download_{i}",
            )

        with col_text:
            with st.expander("📝 Texto"):
                st.text(audio["text"])

    if len(audios) > 1:
        st.markdown("---")
        zip_bytes = create_zip(audios)
        st.download_button(
            label="📦 Baixar Todos (ZIP)",
            data=zip_bytes,
            file_name=f"{audio_name}_completo.zip",
            mime="application/zip",
            key="download_all",
        )
