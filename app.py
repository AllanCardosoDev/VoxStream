"""VoxStream — ponto de entrada da aplicação Streamlit.

Execute com:
    streamlit run app.py
"""

from __future__ import annotations

import logging

import streamlit as st

from voxstream.audio_utils import build_audio_entry
from voxstream.config import LANGUAGES, LOG_DATE_FORMAT, LOG_FORMAT
from voxstream.text_processing import split_text
from voxstream.tts_engine import generate_audio, load_model
from voxstream.ui.components import (
    render_audio_results,
    render_footer,
    render_header,
    render_settings,
    render_split_preview,
    render_text_inputs,
)
from voxstream.ui.sidebar import render_sidebar
from voxstream.ui.styles import apply_styles

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuração da página (deve ser a primeira chamada Streamlit)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="VoxStream - Gerador de Voz Multilíngue",
    page_icon="🎤",
    layout="wide",
)

# Injetar estilos customizados
st.markdown(apply_styles(), unsafe_allow_html=True)

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
# Carregar modelo (cacheado pelo Streamlit)
# ---------------------------------------------------------------------------
@st.cache_resource
def _load_model():  # type: ignore[return]
    return load_model()


model = _load_model()

if model is None:
    st.error("❌ Erro ao carregar o modelo TTS. Por favor, recarregue a página.")
    st.stop()

# ---------------------------------------------------------------------------
# Interface principal — colunas
# ---------------------------------------------------------------------------
col_main, col_settings = st.columns([2, 1])

with col_main:
    audio_name, text_input = render_text_inputs()

with col_settings:
    selected_voice, selected_language, speed, autoplay, custom_limit = render_settings()

# Pré-visualização da divisão do texto
with col_main:
    render_split_preview(text_input, custom_limit)

# ---------------------------------------------------------------------------
# Botão de geração
# ---------------------------------------------------------------------------
if st.button("🎙️ Gerar Áudio", type="primary", disabled=not text_input):
    if not audio_name:
        st.warning("⚠️ Por favor, forneça um nome para o áudio.")
    else:
        parts = split_text(text_input, custom_limit)
        total_parts = len(parts)
        lang_code = LANGUAGES[selected_language]
        speaker_voice = selected_voice if selected_voice != "Voz Padrão" else None

        st.session_state.generated_audios = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, part in enumerate(parts):
            status_text.text(f"Gerando parte {i + 1} de {total_parts}…")
            progress_bar.progress((i + 1) / total_parts)

            try:
                file_name = f"{audio_name}{i + 1}" if total_parts > 1 else audio_name
                audio_bytes = generate_audio(
                    model=model,
                    text=part,
                    language=lang_code,
                    speaker_voice=speaker_voice,
                    speed=speed,
                )
                st.session_state.generated_audios.append(
                    build_audio_entry(name=file_name, data=audio_bytes, text=part)
                )
                logger.info("Parte %d/%d gerada: '%s'.", i + 1, total_parts, file_name)

            except FileNotFoundError as exc:
                st.error(f"❌ Arquivo de voz não encontrado: {exc}")
                logger.error("Arquivo de voz ausente: %s", exc)
            except Exception as exc:
                st.error(f"❌ Erro na parte {i + 1}: {exc}")
                logger.exception("Erro ao gerar parte %d.", i + 1)

        status_text.text("✅ Geração concluída!")
        progress_bar.progress(1.0)

# ---------------------------------------------------------------------------
# Resultados
# ---------------------------------------------------------------------------
render_audio_results(
    audios=st.session_state.generated_audios,
    audio_name=audio_name,
    autoplay=autoplay,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
render_sidebar(
    audios=st.session_state.generated_audios,
    text_input=text_input,
    selected_language=selected_language,
    selected_voice=selected_voice,
    custom_limit=custom_limit,
)

# ---------------------------------------------------------------------------
# Rodapé
# ---------------------------------------------------------------------------
render_footer()
