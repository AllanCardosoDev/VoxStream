"""Estilos CSS customizados para o VoxStream."""

from __future__ import annotations

import streamlit as st

_MAIN_CSS = """
<style>
/* Paleta de cores */
:root {
    --primary: #1E88E5;
    --secondary: #666666;
    --bg-card: #f8f9fa;
    --border: #dee2e6;
}

/* Cabeçalho principal */
.vox-title {
    text-align: center;
    color: var(--primary);
    margin-bottom: 0;
    font-size: 2.5rem;
    font-weight: 700;
}

.vox-subtitle {
    text-align: center;
    color: var(--secondary);
    margin-top: 0;
    font-size: 1.1rem;
}

/* Card de áudio gerado */
.audio-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.5rem;
}

/* Rodapé */
.vox-footer {
    text-align: center;
    color: var(--secondary);
    font-size: 0.85rem;
    padding: 1rem 0;
}
</style>
"""


def inject_styles() -> None:
    """Injeta o CSS customizado na página Streamlit."""
    st.markdown(_MAIN_CSS, unsafe_allow_html=True)
