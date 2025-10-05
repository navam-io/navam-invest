# navam-invest

AI agents and tools for the retail investor

## Overview

`navam-invest` is a Python package that provides AI-powered agents and tools designed to help retail investors make informed investment decisions. Built with modern AI technologies, it aims to democratize access to sophisticated investment analysis and automation.

## Features

- **AI Agents**: Intelligent agents powered by Claude to assist with investment research and analysis
- **Investment Tools**: Suite of tools for portfolio management, market analysis, and decision support
- **Extensible Architecture**: Modular design allowing easy integration and customization

## Installation

```bash
pip install navam-invest
```

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip or your preferred package manager

### Setting up the development environment

1. Clone the repository:
```bash
git clone https://github.com/navam-io/navam-invest.git
cd navam-invest
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package in editable mode with development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **Ruff**: Linting
- **MyPy**: Type checking

Run all checks:
```bash
black src/ tests/
ruff check src/ tests/
mypy src/
```

## Project Structure

```
navam-invest/
├── src/
│   └── navam_invest/      # Main package source code
│       └── __init__.py
├── tests/                 # Test suite
│   └── __init__.py
├── pyproject.toml        # Package configuration and dependencies
├── README.md             # This file
├── LICENSE               # MIT License
└── .gitignore           # Git ignore patterns
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- **Homepage**: https://github.com/navam-io/navam-invest
- **Repository**: https://github.com/navam-io/navam-invest
- **Issues**: https://github.com/navam-io/navam-invest/issues
