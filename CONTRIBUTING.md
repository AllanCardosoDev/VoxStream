# Contributing to VoxStream

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/AllanCardosoDev/VoxStream.git
cd VoxStream
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest ruff
```

## Running Tests

```bash
pytest tests/ -v
```

## Code Style

We use `ruff` for linting:

```bash
ruff check .
```

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a pull request
