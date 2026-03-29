"""Main UI component rendering for VoxStream."""


import streamlit as st

from voxstream.audio_utils import create_zip
from voxstream.config import LANGUAGES, MAX_CHARS


def render_main_column(available_voices: list[str]) -> tuple[str, str, str, str, float, bool, int]:
    """Render the two-column main UI and return user inputs.

    Returns
    -------
    tuple
        ``(audio_name, text_input, selected_voice, selected_language,
           speed, autoplay, custom_limit)``
    """
    col1, col2 = st.columns([2, 1])

    with col1:
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

    with col2:
        st.subheader("⚙️ Configurações")

        if available_voices:
            voice_options = ["Voz Padrão"] + available_voices
            selected_voice: str = st.selectbox("Voz:", voice_options)
        else:
            selected_voice = "Voz Padrão"
            st.info("Adicione arquivos .wav na pasta 'voices'")

        selected_language: str = st.selectbox(
            "Idioma:",
            list(LANGUAGES.keys()),
            index=0,
        )

        speed: float = st.slider("Velocidade:", 0.5, 2.0, 1.0, 0.1)

        st.markdown("### Opções")
        autoplay: bool = st.checkbox("Reproduzir automaticamente", value=True)

        custom_limit: int = st.number_input(
            "Limite de caracteres por parte:",
            min_value=50,
            max_value=500,
            value=MAX_CHARS,
            step=50,
        )

    return audio_name, text_input, selected_voice, selected_language, speed, autoplay, custom_limit


def render_results(audios: list[dict], audio_name: str, autoplay: bool) -> None:
    """Render the generated audio results section.

    Parameters
    ----------
    audios:
        List of audio dicts with ``"name"``, ``"data"``, and ``"text"`` keys.
    audio_name:
        Base name used for the ZIP archive filename.
    autoplay:
        Whether the first audio should autoplay.
    """
    if not audios:
        return

    st.markdown("---")
    st.subheader("🎵 Áudios Gerados")

    for i, audio in enumerate(audios):
        c1, c2, c3 = st.columns([3, 1, 1])

        with c1:
            st.markdown(f"**{audio['name']}**")
            st.audio(audio["data"], format="audio/wav", autoplay=autoplay and i == 0)

        with c2:
            st.download_button(
                label="📥 Baixar",
                data=audio["data"],
                file_name=f"{audio['name']}.wav",
                mime="audio/wav",
                key=f"download_{i}",
            )

        with c3:
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
