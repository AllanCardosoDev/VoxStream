"""VoxStream — Entrypoint principal.

Execute com:
    streamlit run app.py
"""

from __future__ import annotations

import logging

import streamlit as st

from voxstream.config import DEFAULT_VOICE_LABEL, LANGUAGES
from voxstream.text_processing import split_text
from voxstream.tts_engine import generate_audio, load_model
from voxstream.ui.components import (
    render_audio_results,
    render_footer,
    render_header,
    render_settings,
    render_text_inputs,
)
from voxstream.ui.sidebar import render_sidebar
from voxstream.ui.styles import inject_styles

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuração da página (deve ser a primeira chamada Streamlit)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="VoxStream - Gerador de Voz Multilíngue",
    page_icon="🎤",
    layout="wide",
)

inject_styles()

# ---------------------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------------------

render_header()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "generated_audios" not in st.session_state:
    st.session_state.generated_audios = []

# ---------------------------------------------------------------------------
# Carregamento do modelo (cacheado)
# ---------------------------------------------------------------------------


@st.cache_resource(show_spinner="Carregando modelo TTS…")
def _load_model():
    return load_model()


model = _load_model()

if model is None:
    st.error("❌ Erro ao carregar o modelo TTS. Por favor, recarregue a página.")
    st.stop()

# ---------------------------------------------------------------------------
# Layout principal
# ---------------------------------------------------------------------------

col_left, col_right = st.columns([2, 1])

with col_left:
    audio_name, text_input = render_text_inputs()

    if text_input:
        # Pré-visualização da divisão usando o limite padrão
        preview_parts = split_text(text_input)
        if len(preview_parts) > 1:
            chars = len(text_input)
            st.info(
                f"ℹ️ Texto será dividido em **{len(preview_parts)}** partes "
                f"({chars} caracteres no total)"
            )
        else:
            st.caption(f"📝 {len(text_input)} caracteres")

with col_right:
    selected_voice, selected_language, speed, autoplay, custom_limit = render_settings()

# ---------------------------------------------------------------------------
# Botão de geração
# ---------------------------------------------------------------------------

if st.button("🎙️ Gerar Áudio", type="primary", disabled=not text_input):
    if not audio_name:
        st.warning("⚠️ Por favor, forneça um nome para o áudio.")
    else:
        parts = split_text(text_input, custom_limit)
        total_parts = len(parts)

        st.session_state.generated_audios = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        language_code = LANGUAGES[selected_language]
        speaker_wav = (
            f"voices/{selected_voice}.wav"
            if selected_voice != DEFAULT_VOICE_LABEL
            else None
        )

        for i, part in enumerate(parts):
            status_text.text(f"Gerando parte {i + 1} de {total_parts}…")
            progress_bar.progress((i + 1) / total_parts)

            try:
                file_name = f"{audio_name}{i + 1}" if total_parts > 1 else audio_name

                audio_bytes = generate_audio(
                    model=model,
                    text=part,
                    language=language_code,
                    speed=speed,
                    speaker_wav=speaker_wav,
                )

                st.session_state.generated_audios.append(
                    {"name": file_name, "data": audio_bytes, "text": part}
                )

            except FileNotFoundError as exc:
                st.error(f"🔊 Arquivo de voz não encontrado: {exc}")
                logger.error("Arquivo de voz não encontrado: %s", exc)
            except RuntimeError as exc:
                st.error(f"❌ Erro na parte {i + 1}: {exc}")
                logger.error("Erro ao gerar parte %d: %s", i + 1, exc)

        status_text.text("✅ Geração concluída!")
        progress_bar.progress(1.0)

# ---------------------------------------------------------------------------
# Resultados
# ---------------------------------------------------------------------------

if st.session_state.generated_audios:
    render_audio_results(
        audios=st.session_state.generated_audios,
        autoplay=autoplay,
        audio_name=audio_name,
    )

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

render_sidebar(
    custom_limit=custom_limit,
    selected_language=selected_language,
    selected_voice=selected_voice,
    num_audios=len(st.session_state.generated_audios),
    num_chars=len(text_input),
)

# ---------------------------------------------------------------------------
# Rodapé
# ---------------------------------------------------------------------------

render_footer()
