# Release 0.1.31

## Status
Published to PyPI on October 08, 2025

## Features

### 🎨 Enhanced TUI User Experience

**Real-Time Processing Indicators** - Multi-level visual feedback system:

- **Smart Input Disabling**: Input field automatically grays out and becomes uneditable during agent processing
  - Prevents race conditions and duplicate query submissions
  - Clear visual affordance that system is working
  - Industry-standard pattern (ChatGPT, Claude.ai)

- **Live Status Updates**: Dynamic placeholder text changes during processing
  - Ready state: `"Ask about stocks or economic indicators..."`
  - Processing state: `"⏳ Processing your request..."`
  - Provides immediate feedback on system state

- **Footer Progress Tracking**: Real-time status in app footer bar
  - `"Initializing agents..."` during startup
  - `"Agent: {Name} | Ready"` when idle
  - `"Processing..."` during agent execution
  - Shows current active agent context

- **Error Recovery**: Robust state management with try/finally blocks
  - Input always re-enables, even on errors or crashes
  - Auto-focus returns to input when ready for next query
  - Never leaves user with disabled/stuck interface

**Benefits**:
- ✅ Eliminates confusion during long operations or pauses
- ✅ Clear multi-level feedback (input + placeholder + footer)
- ✅ Prevents accidental duplicate submissions
- ✅ Graceful recovery from all error conditions

### 🔧 Agent Response Improvements

**Full Response Delivery** - Increased token limits:

- **Issue Fixed**: Agent responses were getting truncated mid-sentence (e.g., "unmat..." instead of "unmatched")
- **Root Cause**: ChatAnthropic was using default `max_tokens` limit (4096 tokens)
- **Solution**: Set `max_tokens=8192` for all agents and workflows

**Updated Components**:
- ✅ Portfolio agent (`portfolio.py`)
- ✅ Research agent (`research.py`)
- ✅ Quill agent (`quill.py`)
- ✅ Screen Forge agent (`screen_forge.py`)
- ✅ Macro Lens agent (`macro_lens.py`)
- ✅ Earnings Whisperer agent (`earnings_whisperer.py`)
- ✅ Investment Analysis workflow (`investment_analysis.py`)

**Impact**: Agents can now generate responses up to 8192 tokens (~6,000-8,000 words) without truncation

### 📝 Documentation Updates

**Professional README.md Redesign**:

- ✅ Updated with v0.1.31 features (processing indicators, full response fix)
- ✅ Added "Real-Time Processing Feedback" example workflow
- ✅ Enhanced "Interactive Terminal UI" section with UX improvements
- ✅ Mermaid architecture diagram for visual system overview
- ✅ Collapsible sections for progressive disclosure
- ✅ Rich tables for API status and data sources
- ✅ Current roadmap with accurate development status

### 🧪 Quality Improvements

**Code Quality**:
- ✅ Consistent agent initialization patterns across all files
- ✅ Proper error handling with try/finally blocks in TUI
- ✅ DRY principle: Agent display name mapping for status updates
- ✅ Comprehensive inline documentation for UX features

---

## Technical Details

### Files Modified

**TUI (User Experience)**:
- `src/navam_invest/tui/app.py` - Added processing indicators and input state management

**Agents (Response Quality)**:
- `src/navam_invest/agents/portfolio.py`
- `src/navam_invest/agents/research.py`
- `src/navam_invest/agents/quill.py`
- `src/navam_invest/agents/screen_forge.py`
- `src/navam_invest/agents/macro_lens.py`
- `src/navam_invest/agents/earnings_whisperer.py`

**Workflows**:
- `src/navam_invest/workflows/investment_analysis.py`

**Documentation**:
- `README.md` - Comprehensive update with latest features

### Breaking Changes

None. This release is fully backward compatible with v0.1.30.

### Migration Guide

No migration needed. Users simply need to update via:
```bash
pip install --upgrade navam-invest
```

---

## Release Date
October 08, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.31/
