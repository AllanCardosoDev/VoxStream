# VoxStream 🎤

[![CI](https://github.com/AllanCardosoDev/VoxStream/actions/workflows/ci.yml/badge.svg)](https://github.com/AllanCardosoDev/VoxStream/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B.svg)](https://streamlit.io)

> Gerador de voz multilíngue com IA, powered by **Coqui TTS XTTS v2** e **Streamlit**.

---

## ✨ Funcionalidades

- 🌍 **16 idiomas** suportados (Português, Inglês, Espanhol, Francês e mais)
- 🎭 **Clonagem de voz** com arquivos `.wav` de referência
- ✂️ **Divisão inteligente de texto** — textos longos são segmentados automaticamente preservando a pontuação
- 📦 **Download individual ou em ZIP** de todos os áudios gerados
- ⚡ **Reprodução automática** do primeiro áudio gerado
- 🎚️ **Controle de velocidade** de fala (0.5× a 2.0×)

---

## 📋 Requisitos do sistema

| Componente | Versão mínima |
|------------|--------------|
| Python     | 3.11         |
| RAM        | 8 GB         |
| Espaço em disco | ~3 GB (modelo XTTS v2) |

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/AllanCardosoDev/VoxStream.git
cd VoxStream
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
streamlit run app.py
```

Ou, usando o `Makefile`:

```bash
make run
```

---

## 🐳 Docker

```bash
# Build
docker build -t voxstream .

# Run
docker run -p 8501:8501 voxstream
```

Acesse em: [http://localhost:8501](http://localhost:8501)

---

## 🎙️ Como adicionar vozes customizadas

1. Grave ou obtenha um arquivo `.wav` com a voz desejada (recomendado: 6–30 segundos, boa qualidade de áudio, sem ruído de fundo)
2. Coloque o arquivo na pasta `voices/`
3. Reinicie a aplicação — a voz aparecerá automaticamente no seletor

Vozes incluídas por padrão:
- `arnold.wav` — voz masculina
- `female_01.wav` — voz feminina 1
- `female_02.wav` — voz feminina 2

---

## 🗂️ Estrutura do projeto

```
VoxStream/
├── app.py                      # Entrypoint — streamlit run app.py
├── requirements.txt            # Dependências com versões fixas
├── runtime.txt                 # Versão do Python
├── Dockerfile                  # Imagem Docker
├── Makefile                    # Atalhos de desenvolvimento
├── pyproject.toml              # Metadados do projeto e ferramentas
├── .env.example                # Variáveis de ambiente de exemplo
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── .streamlit/
│   └── config.toml             # Configuração do Streamlit
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de CI
├── voices/                     # Arquivos WAV de referência de voz
│   ├── arnold.wav
│   ├── female_01.wav
│   └── female_02.wav
├── voxstream/                  # Pacote principal
│   ├── __init__.py
│   ├── config.py               # Constantes e configurações
│   ├── tts_engine.py           # Carregamento do modelo e geração de áudio
│   ├── text_processing.py      # Segmentação de texto
│   ├── audio_utils.py          # Empacotamento ZIP e utilitários de áudio
│   └── ui/
│       ├── __init__.py
│       ├── components.py       # Componentes reutilizáveis da UI
│       ├── sidebar.py          # Barra lateral
│       └── styles.py           # CSS customizado
└── tests/                      # Testes unitários
    ├── __init__.py
    ├── test_config.py
    ├── test_text_processing.py
    └── test_audio_utils.py
```

---

## 🧪 Testes

```bash
# Todos os testes
make test

# Com cobertura
make test-cov
```

---

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de contribuição.

---

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---

<div align="center">
Desenvolvido com ❤️ usando <a href="https://streamlit.io">Streamlit</a> e <a href="https://github.com/coqui-ai/TTS">Coqui TTS</a>
</div>
