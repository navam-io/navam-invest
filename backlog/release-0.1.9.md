# Release 0.1.9

## Status
Published

## Features

### New Capabilities
- **Local File Reading**: Added capability to read and analyze local files from the working directory
  - New tools: `read_local_file` and `list_local_files`
  - Security features:
    - Path validation to prevent directory traversal attacks
    - Restricted to current working directory only
    - Safe file extension whitelist (CSV, JSON, Excel, Markdown, OFX/QFX, etc.)
    - 10MB file size limit
  - Integrated with both Portfolio and Research agents
  - Users can now analyze their portfolio CSV files, transaction data, and investment notes directly
  - Comprehensive test coverage (12 tests, 82% coverage for file_reader.py)

### Use Cases Enabled
- Import and analyze portfolio holdings from CSV/Excel files
- Read transaction history files for analysis
- Access local investment research notes and documents
- Process financial data exports (OFX/QFX formats)
- Analyze custom JSON data structures

## Release Date
2025-10-06

## PyPI Package
https://pypi.org/project/navam-invest/0.1.9/
