# Contribuindo com o VoxStream 🎤

Obrigado pelo interesse em contribuir! Este documento descreve o processo para enviar contribuições ao projeto.

---

## 📋 Código de Conduta

Ao participar deste projeto, você concorda em manter um ambiente respeitoso e inclusivo para todos os colaboradores.

---

## 🚀 Como contribuir

### 1. Fork e clone

```bash
git clone https://github.com/SEU_USUARIO/VoxStream.git
cd VoxStream
```

### 2. Crie uma branch

Use um nome descritivo seguindo o padrão:

```bash
git checkout -b feat/minha-funcionalidade
# ou
git checkout -b fix/descricao-do-bug
```

### 3. Configure o ambiente de desenvolvimento

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-cov
```

### 4. Faça suas alterações

- Siga as convenções de estilo já presentes no código
- Adicione **type hints** em todas as funções novas
- Adicione **docstrings** em português (BR) no padrão NumPy/Google
- Escreva testes para qualquer nova funcionalidade

### 5. Execute os testes

```bash
make test
```

Todos os testes devem passar antes de abrir um PR.

### 6. Commit e push

```bash
git add .
git commit -m "feat: descrição clara da mudança"
git push origin feat/minha-funcionalidade
```

### 7. Abra um Pull Request

Abra um PR no repositório original descrevendo:
- O que foi feito
- Por que a mudança é necessária
- Como testar

---

## 📐 Padrões de código

| Item | Padrão |
|------|--------|
| Estilo | PEP 8 |
| Type hints | Obrigatório em funções públicas |
| Docstrings | PT-BR, formato Google/NumPy |
| Testes | `pytest`, cobertura mínima de 80% |
| Commits | [Conventional Commits](https://www.conventionalcommits.org/) |

---

## 🐛 Reportando bugs

Abra uma [issue](https://github.com/AllanCardosoDev/VoxStream/issues) com:

1. **Descrição** clara do problema
2. **Passos para reproduzir**
3. **Comportamento esperado** vs **comportamento atual**
4. **Ambiente** (SO, versão do Python, versão das dependências)

---

## 💡 Sugerindo funcionalidades

Abra uma [issue](https://github.com/AllanCardosoDev/VoxStream/issues) com a tag `enhancement` descrevendo:

1. O problema que a funcionalidade resolve
2. Como você imagina que ela funcionaria
3. Alternativas consideradas

---

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [Licença MIT](LICENSE).
