"""VoxStream – entry point."""

import os

# Must be set before importing TTS
os.environ["COQUI_TOS_AGREED"] = "1"

import streamlit as st  # noqa: E402

from voxstream.audio_utils import get_available_voices
from voxstream.config import LANGUAGES, TTS_DEVICE, TTS_MODEL
from voxstream.text_processing import split_text
from voxstream.tts_engine import generate_audio, load_model
from voxstream.ui.components import render_main_column, render_results
from voxstream.ui.sidebar import render_sidebar
from voxstream.ui.styles import inject_custom_css

# ---------------------------------------------------------------------------
# Page config (must be first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="VoxStream - Gerador de Voz Multilíngue",
    page_icon="🎤",
    layout="wide",
)

inject_custom_css()

st.markdown(
    "<h1 class='main-title'>VoxStream</h1>"
    "<h3 class='sub-title'>Gerador de Voz Multilíngue com IA</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "generated_audios" not in st.session_state:
    st.session_state.generated_audios = []

# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------


@st.cache_resource
def _load_model():
    try:
        return load_model(TTS_MODEL, TTS_DEVICE)
    except Exception as exc:
        st.error(f"Erro ao carregar modelo: {exc}")
        return None


model = _load_model()

if model is None:
    st.error("Erro ao carregar o modelo TTS. Por favor, recarregue a página.")
    st.stop()

# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------
available_voices = get_available_voices()

audio_name, text_input, selected_voice, selected_language, speed, autoplay, custom_limit = (
    render_main_column(available_voices)
)

# Split preview
if text_input:
    parts_preview = split_text(text_input, custom_limit)
    if len(parts_preview) > 1:
        st.info(f"ℹ️ Texto será dividido em {len(parts_preview)} partes")

# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------
if st.button("🎙️ Gerar Áudio", type="primary", disabled=not text_input):
    if not audio_name:
        st.warning("⚠️ Por favor, forneça um nome para o áudio")
    else:
        parts = split_text(text_input, custom_limit)
        total_parts = len(parts)
        st.session_state.generated_audios = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, part in enumerate(parts):
            status_text.text(f"Gerando parte {i + 1} de {total_parts}...")
            progress_bar.progress((i + 1) / total_parts)

            try:
                file_name = f"{audio_name}{i + 1}" if total_parts > 1 else audio_name

                speaker_wav = None
                if selected_voice != "Voz Padrão":
                    from pathlib import Path

                    speaker_wav = str(Path("voices") / f"{selected_voice}.wav")

                audio_bytes = generate_audio(
                    model,
                    text=part,
                    language=LANGUAGES[selected_language],
                    speaker_wav=speaker_wav,
                    speed=speed,
                )

                st.session_state.generated_audios.append(
                    {"name": file_name, "data": audio_bytes, "text": part}
                )

            except Exception as exc:
                st.error(f"Erro na parte {i + 1}: {exc}")

        status_text.text("✅ Geração concluída!")
        progress_bar.progress(1.0)

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
render_results(st.session_state.generated_audios, audio_name, autoplay)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
render_sidebar(
    char_limit=custom_limit,
    language=selected_language,
    voice=selected_voice,
    audio_count=len(st.session_state.generated_audios),
    text_length=len(text_input) if text_input else 0,
)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div class='footer'>"
    "<p>VoxStream - Desenvolvido com ❤️ usando Streamlit e Coqui TTS</p>"
    "</div>",
    unsafe_allow_html=True,
)
