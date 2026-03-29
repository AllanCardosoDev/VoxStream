"""Componentes reutilizáveis de UI para o VoxStream."""

from __future__ import annotations

import streamlit as st

from ..audio_utils import build_zip
from ..config import DEFAULT_VOICE_LABEL, LANGUAGES, MAX_CHARS
from ..tts_engine import get_available_voices


def render_header() -> None:
    """Renderiza o cabeçalho principal da aplicação."""
    st.markdown(
        """
        <h1 class='vox-title'>🎤 VoxStream</h1>
        <p class='vox-subtitle'>Gerador de Voz Multilíngue com IA</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")


def render_text_inputs() -> tuple[str, str]:
    """Renderiza os campos de nome do áudio e texto de entrada.

    Returns
    -------
    tuple[str, str]
        ``(audio_name, text_input)``
    """
    audio_name: str = st.text_input(
        "Nome do áudio:",
        placeholder="Digite o nome base para o(s) arquivo(s)",
        help="Se o texto for dividido, será adicionado um número ao final (ex: nome1, nome2)",
    )

    text_input: str = st.text_area(
        "Digite o texto para converter em áudio:",
        height=200,
        placeholder="Digite seu texto aqui...",
    )

    return audio_name, text_input


def render_settings(voices_dir: str = "voices") -> tuple[str, str, float, bool, int]:
    """Renderiza o painel de configurações (coluna direita).

    Parameters
    ----------
    voices_dir:
        Diretório com arquivos WAV de referência de voz.

    Returns
    -------
    tuple
        ``(selected_voice, selected_language, speed, autoplay, custom_limit)``
    """
    st.subheader("⚙️ Configurações")

    # --- Seleção de voz ---
    available_voices = get_available_voices(voices_dir)
    if available_voices:
        voice_options = [DEFAULT_VOICE_LABEL] + available_voices
        selected_voice: str = st.selectbox("Voz:", voice_options)
    else:
        selected_voice = DEFAULT_VOICE_LABEL
        st.info("Adicione arquivos .wav na pasta 'voices'")

    # --- Seleção de idioma ---
    selected_language: str = st.selectbox(
        "Idioma:",
        list(LANGUAGES.keys()),
        index=0,
    )

    # --- Velocidade ---
    speed: float = st.slider("Velocidade:", 0.5, 2.0, 1.0, 0.1)

    # --- Opções adicionais ---
    st.markdown("### Opções")
    autoplay: bool = st.checkbox("Reproduzir automaticamente", value=True)

    custom_limit: int = st.number_input(
        "Limite de caracteres por parte:",
        min_value=50,
        max_value=500,
        value=MAX_CHARS,
        step=50,
    )

    return selected_voice, selected_language, speed, autoplay, int(custom_limit)


def render_audio_results(audios: list[dict], autoplay: bool, audio_name: str) -> None:
    """Renderiza os áudios gerados com controles de download.

    Parameters
    ----------
    audios:
        Lista de dicionários com ``"name"``, ``"data"`` e ``"text"``.
    autoplay:
        Se ``True``, reproduz automaticamente o primeiro áudio.
    audio_name:
        Nome base usado para nomear o arquivo ZIP de download.
    """
    st.markdown("---")
    st.subheader("🎵 Áudios Gerados")

    for i, audio in enumerate(audios):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.markdown(f"**{audio['name']}**")
            st.audio(audio["data"], format="audio/wav", autoplay=autoplay and i == 0)

        with col2:
            st.download_button(
                label="📥 Baixar",
                data=audio["data"],
                file_name=f"{audio['name']}.wav",
                mime="audio/wav",
                key=f"download_{i}",
            )

        with col3:
            with st.expander("📝 Texto"):
                st.text(audio["text"])

    if len(audios) > 1:
        st.markdown("---")
        zip_bytes = build_zip(audios)
        st.download_button(
            label="📦 Baixar Todos (ZIP)",
            data=zip_bytes,
            file_name=f"{audio_name}_completo.zip",
            mime="application/zip",
            key="download_all",
        )


def render_footer() -> None:
    """Renderiza o rodapé da aplicação."""
    st.markdown("---")
    st.markdown(
        "<div class='vox-footer'>VoxStream — Desenvolvido com ❤️ usando Streamlit e Coqui TTS</div>",
        unsafe_allow_html=True,
    )
