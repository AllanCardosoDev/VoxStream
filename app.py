import streamlit as st
import os
import time
import zipfile
import io
import tempfile
from pathlib import Path
from TTS.api import TTS

# Configuração do Coqui TTS
os.environ["COQUI_TOS_AGREED"] = "1"

# Configurações
MAX_CHARS = 200  # Limite de caracteres por parte
LANGUAGES = {
    "Portuguese": "pt",
    "English": "en", 
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Polish": "pl",
    "Turkish": "tr",
    "Russian": "ru",
    "Dutch": "nl",
    "Czech": "cs",
    "Arabic": "ar",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Hungarian": "hu",
    "Korean": "ko"
}

# Inicialização do modelo
@st.cache_resource
def load_model():
    try:
        return TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    except Exception as e:
        st.error(f"Erro ao carregar modelo: {str(e)}")
        return None

# Função para obter vozes disponíveis
def get_available_voices():
    voices_dir = Path("voices")
    if not voices_dir.exists():
        return []
    return [f.stem for f in voices_dir.glob("*.wav")]

# Função para dividir texto
def split_text(text, max_chars=MAX_CHARS):
    """Divide texto em partes menores respeitando pontuação"""
    if len(text) <= max_chars:
        return [text]
    
    parts = []
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    current_part = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        if len(current_part) + len(sentence) + 1 <= max_chars:
            current_part += sentence + ". "
        else:
            if current_part:
                parts.append(current_part.strip())
            current_part = sentence + ". "
    
    if current_part:
        parts.append(current_part.strip())
    
    return parts

# Configuração da página
st.set_page_config(
    page_title="VoxStream - Gerador de Voz Multilíngue", 
    page_icon="🎤", 
    layout="wide"
)

# Título principal com destaque
st.markdown("""
    <h1 style='text-align: center; color: #1E88E5; margin-bottom: 0;'>
        VoxStream
    </h1>
    <h3 style='text-align: center; color: #666; margin-top: 0;'>
        Gerador de Voz Multilíngue com IA
    </h3>
    """, unsafe_allow_html=True)

st.markdown("---")

# Inicializar session state
if 'generated_audios' not in st.session_state:
    st.session_state.generated_audios = []

# Carregar modelo
model = load_model()

if model is None:
    st.error("Erro ao carregar o modelo TTS. Por favor, recarregue a página.")
    st.stop()

# Interface principal
col1, col2 = st.columns([2, 1])

with col1:
    # Nome do áudio
    audio_name = st.text_input(
        "Nome do áudio:",
        placeholder="Digite o nome base para o(s) arquivo(s)",
        help="Se o texto for dividido, será adicionado um número ao final (ex: nome1, nome2)"
    )
    
    # Área de texto
    text_input = st.text_area(
        "Digite o texto para converter em áudio:",
        height=200,
        placeholder="Digite seu texto aqui..."
    )
    
    # Pré-visualização de divisão
    if text_input:
        parts = split_text(text_input)
        if len(parts) > 1:
            st.info(f"ℹ️ Texto será dividido em {len(parts)} partes")

with col2:
    st.subheader("⚙️ Configurações")
    
    # Seleção de voz
    available_voices = get_available_voices()
    if available_voices:
        voice_options = ["Voz Padrão"] + available_voices
        selected_voice = st.selectbox("Voz:", voice_options)
    else:
        selected_voice = "Voz Padrão"
        st.info("Adicione arquivos .wav na pasta 'voices'")
    
    # Seleção de idioma
    selected_language = st.selectbox(
        "Idioma:",
        list(LANGUAGES.keys()),
        index=0
    )
    
    # Velocidade
    speed = st.slider("Velocidade:", 0.5, 2.0, 1.0, 0.1)
    
    # Opções adicionais
    st.markdown("### Opções")
    autoplay = st.checkbox("Reproduzir automaticamente", value=True)
    
    # Limite de caracteres
    custom_limit = st.number_input(
        "Limite de caracteres por parte:",
        min_value=50,
        max_value=500,
        value=MAX_CHARS,
        step=50
    )

# Botão de geração
if st.button("🎙️ Gerar Áudio", type="primary", disabled=not text_input):
    if not audio_name:
        st.warning("⚠️ Por favor, forneça um nome para o áudio")
    else:
        # Dividir texto
        parts = split_text(text_input, custom_limit)
        total_parts = len(parts)
        
        # Limpar áudios anteriores
        st.session_state.generated_audios = []
        
        # Barra de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, part in enumerate(parts):
            status_text.text(f"Gerando parte {i+1} de {total_parts}...")
            progress_bar.progress((i + 1) / total_parts)
            
            try:
                # Gerar nome do arquivo
                if total_parts > 1:
                    file_name = f"{audio_name}{i+1}"
                else:
                    file_name = audio_name
                
                # Configurar voz
                speaker_wav = None
                if selected_voice != "Voz Padrão":
                    speaker_wav = str(Path("voices") / f"{selected_voice}.wav")
                
                # Gerar áudio usando arquivo temporário
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                    temp_path = temp_file.name
                
                # Gerar áudio no arquivo temporário
                model.tts_to_file(
                    text=part,
                    file_path=temp_path,
                    speaker_wav=speaker_wav,
                    language=LANGUAGES[selected_language],
                    speed=speed
                )
                
                # Ler o arquivo gerado
                with open(temp_path, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                
                # Remover arquivo temporário
                os.unlink(temp_path)
                
                # Salvar no session state
                st.session_state.generated_audios.append({
                    'name': file_name,
                    'data': audio_bytes,
                    'text': part
                })
                    
            except Exception as e:
                st.error(f"Erro na parte {i+1}: {str(e)}")
        
        status_text.text("✅ Geração concluída!")
        progress_bar.progress(1.0)

# Exibir resultados
if st.session_state.generated_audios:
    st.markdown("---")
    st.subheader("🎵 Áudios Gerados")
    
    # Downloads individuais
    for i, audio in enumerate(st.session_state.generated_audios):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{audio['name']}**")
            st.audio(audio['data'], format='audio/wav', autoplay=autoplay and i==0)
        
        with col2:
            st.download_button(
                label="📥 Baixar",
                data=audio['data'],
                file_name=f"{audio['name']}.wav",
                mime="audio/wav",
                key=f"download_{i}"
            )
        
        with col3:
            with st.expander("📝 Texto"):
                st.text(audio['text'])
    
    # Download todos em ZIP
    if len(st.session_state.generated_audios) > 1:
        st.markdown("---")
        
        # Criar ZIP em memória
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for audio in st.session_state.generated_audios:
                zip_file.writestr(f"{audio['name']}.wav", audio['data'])
        
        st.download_button(
            label="📦 Baixar Todos (ZIP)",
            data=zip_buffer.getvalue(),
            file_name=f"{audio_name}_completo.zip",
            mime="application/zip",
            key="download_all"
        )

# Sidebar com logo VoxStream
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h2 style='color: #1E88E5;'>VoxStream</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("ℹ️ Informações")
    st.markdown(f"""
    ### Configurações Atuais
    - Limite: {custom_limit} caracteres
    - Idioma: {selected_language}
    - Voz: {selected_voice}
    
    ### Estatísticas
    - Áudios gerados: {len(st.session_state.generated_audios)}
    - Caracteres total: {len(text_input)}
    """)
    
    st.markdown("---")
    st.markdown("""
    ### Como usar
    1. Digite um nome para o áudio
    2. Cole ou digite seu texto
    3. Escolha voz e idioma
    4. Clique em 'Gerar Áudio'
    
    Textos longos serão divididos automaticamente!
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>VoxStream - Desenvolvido com ❤️ usando Streamlit e Coqui TTS</p>
    </div>
    """, unsafe_allow_html=True)
