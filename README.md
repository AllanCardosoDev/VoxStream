# VoxStream 🎤

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/AllanCardosoDev/VoxStream/actions/workflows/ci.yml/badge.svg)](https://github.com/AllanCardosoDev/VoxStream/actions/workflows/ci.yml)

> Gerador de voz multilíngue com IA — powered by [Streamlit](https://streamlit.io/) e [Coqui TTS (XTTS v2)](https://github.com/coqui-ai/TTS).

---

## ✨ Funcionalidades

- 🌍 **16 idiomas** suportados (Português, Inglês, Espanhol, Francês, e mais)
- 🎭 **Clonagem de voz** — use arquivos `.wav` para definir o timbre do narrador
- ⚡ **Divisão automática** de textos longos com preservação de pontuação
- 📦 **Download individual ou em ZIP** dos áudios gerados
- 🎛️ **Controle de velocidade** de fala
- 🐳 **Docker** pronto para uso

---

## 📋 Requisitos do sistema

| Componente | Versão mínima |
|---|---|
| Python | 3.11 |
| RAM | 8 GB |
| Disco | ~5 GB (modelo XTTS v2) |
| GPU (opcional) | CUDA 11.8+ |

---

## 🚀 Instalação

### Opção 1 — Local

```bash
# 1. Clone o repositório
git clone https://github.com/AllanCardosoDev/VoxStream.git
cd VoxStream

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie a aplicação
streamlit run app.py
```

### Opção 2 — Docker

```bash
docker build -t voxstream .
docker run -p 8501:8501 voxstream
```

### Opção 3 — Makefile

```bash
make install   # instala dependências
make run       # inicia a aplicação
make test      # executa os testes
make lint      # verifica estilo de código
```

---

## 🎙️ Como usar

1. **Nome do áudio** — Informe um nome base (ex.: `narração`).
2. **Texto** — Cole ou escreva o texto que será narrado.
3. **Voz** — Escolha uma das vozes disponíveis ou use a voz padrão.
4. **Idioma** — Selecione o idioma do texto.
5. **Velocidade** — Ajuste a velocidade de fala (0.5× a 2×).
6. Clique em **🎙️ Gerar Áudio** e aguarde.

> Textos com mais de 200 caracteres são divididos automaticamente em partes
> menores, respeitando a pontuação original.

---

## 🎭 Adicionando vozes customizadas

Coloque arquivos `.wav` na pasta `voices/`:

```
voices/
├── minha_voz.wav       # ~10–30 s de áudio limpo
└── narrador.wav
```

Requisitos para os arquivos de voz:
- Formato WAV, 22050 Hz ou superior
- Mono ou estéreo
- Sem ruído de fundo
- Duração recomendada: 6–30 segundos

---

## 🗂️ Estrutura do projeto

```
VoxStream/
├── app.py                    # Entry point (streamlit run app.py)
├── voxstream/
│   ├── __init__.py
│   ├── config.py             # Constantes e configurações
│   ├── tts_engine.py         # Motor TTS (carregamento e geração)
│   ├── text_processing.py    # Divisão e processamento de texto
│   ├── audio_utils.py        # Utilitários de áudio (ZIP, entries)
│   └── ui/
│       ├── __init__.py
│       ├── components.py     # Componentes reutilizáveis de UI
│       ├── sidebar.py        # Sidebar
│       └── styles.py         # CSS customizado
├── tests/
│   ├── test_text_processing.py
│   ├── test_audio_utils.py
│   └── test_config.py
├── voices/                   # Amostras de voz para clonagem
├── .streamlit/config.toml    # Tema do Streamlit
├── .github/workflows/ci.yml  # GitHub Actions CI
├── Dockerfile
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 🤝 Contribuição

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) para saber como contribuir.

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais informações.
