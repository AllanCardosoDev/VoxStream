"""Estilos CSS customizados para o VoxStream."""

from __future__ import annotations

CUSTOM_CSS: str = """
<style>
/* ─── Paleta ─────────────────────────────────────────────────────────────── */
:root {
    --primary:   #1E88E5;
    --secondary: #42A5F5;
    --accent:    #0D47A1;
    --bg-card:   #F8F9FA;
    --text-muted:#666666;
}

/* ─── Botão primário ────────────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: opacity 0.2s ease;
}
.stButton > button[kind="primary"]:hover { opacity: 0.88; }

/* ─── Cards de áudio ────────────────────────────────────────────────────── */
.audio-card {
    background: var(--bg-card);
    border-left: 4px solid var(--primary);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 4px rgba(0,0,0,.08);
}

/* ─── Contador de caracteres ────────────────────────────────────────────── */
.char-counter {
    font-size: 0.78rem;
    color: var(--text-muted);
    text-align: right;
}
.char-counter.over-limit { color: #E53935; font-weight: 600; }

/* ─── Sidebar ───────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #EFF6FF 0%, #FFFFFF 100%);
}
</style>
"""


def apply_styles() -> str:
    """Retorna o bloco HTML com os estilos customizados.

    Returns:
        String HTML com a tag ``<style>`` pronta para ser injetada via
        ``st.markdown(..., unsafe_allow_html=True)``.
    """
    return CUSTOM_CSS
