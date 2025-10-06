# Release 0.1.4

## Documentation Enhancement - Product Vision & Architecture

### Feature

**Enhanced Project Documentation**: Added comprehensive "Product Vision & Architecture" section to CLAUDE.md with crisp references to product specs and TUI design principles.

### Implementation Details

#### 1. Product Vision Section
Added clear articulation of Navam Invest's value proposition:
- **Target Users**: Retail investors managing $50K–$1M portfolios
- **Core Value**: Institutional-grade intelligence without 1% AUM fees
- **Approach**: Specialized AI agents using free public data sources

#### 2. Architecture Stack Overview
Documented 5-layer architecture with references to detailed specs:
1. Agent Orchestration (LangGraph)
2. AI Reasoning (Claude + multi-model support)
3. User Interface (Textual TUI + Typer CLI)
4. Data Sources (FRED, SEC EDGAR, Alpha Vantage)
5. Packaging (Python library)

#### 3. TUI/CLI Design Principles
Captured key design decisions from `refer/specs/tui-spec-by-chatgpt.md`:
- Chat-first conversational interface
- Textual framework for full-screen TUI
- Rich integration for formatting
- Async streaming for real-time responses
- Session persistence with SQLite/SQLModel
- Slash commands for agent switching
- Terminal-native keybindings

#### 4. Implementation Status Tracking
Added current status markers:
- ✅ v0.1.3: Core agents, API tools, TUI, CLI
- 🚧 Next: Additional agents, enhanced panels, persistence

### Files Modified
1. `CLAUDE.md` - Added "Product Vision & Architecture" section with references to `refer/specs/about.md` and `refer/specs/tui-spec-by-chatgpt.md`
2. `pyproject.toml` - Incremented version 0.1.3 → 0.1.4
3. `src/navam_invest/cli.py` - Updated version display to 0.1.4

### Benefits
- ✅ Clear project vision for all contributors
- ✅ Explicit references to authoritative spec documents
- ✅ Design principles captured for consistent implementation
- ✅ Roadmap visibility with status markers
- ✅ Improved onboarding for new developers

### Documentation References
- `refer/specs/about.md` - Product vision and tech stack details
- `refer/specs/tui-spec-by-chatgpt.md` - TUI/CLI architecture and implementation patterns

### Release Date
2025-10-05

### Version
0.1.4 (Alpha)
