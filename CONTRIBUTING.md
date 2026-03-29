# Contribuindo com o VoxStream

Obrigado por considerar contribuir! 🎉

## Como contribuir

1. **Fork** o repositório
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```
3. Faça suas alterações e adicione testes quando aplicável
4. Execute os testes:
   ```bash
   make test
   ```
5. Verifique o estilo de código:
   ```bash
   make lint
   ```
6. Faça commit seguindo o padrão [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat: adiciona suporte a novo idioma
   fix: corrige divisão de texto com hífen
   docs: atualiza README com instruções de Docker
   ```
7. Abra um **Pull Request** descrevendo suas mudanças

## Relatando bugs

Use o [sistema de issues](https://github.com/AllanCardosoDev/VoxStream/issues) com:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Versão do Python e do sistema operacional

## Sugerindo melhorias

Abra uma issue com o label `enhancement` descrevendo:
- O que você gostaria de ver
- Por que seria útil
- Possível implementação (opcional)

## Diretrizes de código

- Use **type hints** em todas as funções
- Adicione **docstrings** no estilo Google
- Mantenha funções pequenas e focadas
- Escreva testes para novas funcionalidades

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [MIT License](LICENSE).
