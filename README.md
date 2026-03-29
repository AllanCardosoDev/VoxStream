# 🎤 VoxStream

**Gerador de Voz Multilíngue com IA**

VoxStream é uma aplicação web desenvolvida com [Streamlit](https://streamlit.io) e [Coqui TTS (XTTS v2)](https://github.com/coqui-ai/TTS) que converte texto em áudio em múltiplos idiomas, com suporte a clonagem de voz.

## ✨ Funcionalidades

- 🌍 16 idiomas suportados (Português, Inglês, Espanhol, Francês, etc.)
- 🎭 Clonagem de voz com arquivos `.wav` personalizados
- ✂️ Divisão automática de textos longos respeitando pontuação
- 📦 Download individual ou em ZIP
- ⚡ Interface amigável com Streamlit

## 🚀 Como executar

### Pré-requisitos

- Python 3.11+
- ~10 GB de espaço em disco (modelo XTTS v2)

### Instalação

```bash
git clone https://github.com/AllanCardosoDev/VoxStream.git
cd VoxStream
pip install -r requirements.txt
```

### Execução

```bash
streamlit run app.py
```

### Com Docker

```bash
docker build -t voxstream .
docker run -p 8501:8501 voxstream
```

## 📁 Estrutura do Projeto

```
VoxStream/
├── app.py                  # Ponto de entrada da aplicação
├── voxstream/              # Pacote principal
│   ├── config.py           # Configurações e constantes
│   ├── tts_engine.py       # Motor TTS (carregamento de modelo e geração)
│   ├── text_processing.py  # Processamento e divisão de texto
│   ├── audio_utils.py      # Utilitários de áudio
│   └── ui/                 # Componentes de interface
│       ├── components.py
│       ├── sidebar.py
│       └── styles.py
├── tests/                  # Testes unitários
├── voices/                 # Arquivos .wav para clonagem de voz
├── requirements.txt
└── Dockerfile
```

## 🧪 Testes

```bash
pip install pytest ruff
pytest tests/ -v
```

## 🐳 Docker

O `Dockerfile` inclui health check e está configurado para rodar com usuário não-root.

## 📝 Licença

MIT — veja [LICENSE](LICENSE).
