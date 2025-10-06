# Active Backlog

[ ] When running `navam invest` and user enters the `/porfolio` or `/research` commands. Provide few usable prompt examples which provide good coverage of all tools. Add `/examples` command to randomly rotate among a pre-hydrated set of prompts based on the agent active.

[ ] When running `navam invest` provide `/quit` command to quit instead of control+q as the latter interferes with VS Code terminal. Similarly add `/clear` command to clear chat. Update the chat footer accordingly. Add `/help` command to chat footer.

[ ] Provide a capability to read files within the folder where `navam invest` is running and bring files content into conversation context.

[ ] Make user prompt area multi-line capable.

[ ] Create next release of `navam_invest` package which adds more agents and tools based on refer/specs/api-tools.md prioritized list of APIs.

## Completed Items

All completed features have been moved to their respective release files:
- `release-0.1.0.md` - Initial package scaffold, CLAUDE.md enhancement, and minimal first release with LangGraph/Anthropic API/TUI/agents
- `release-0.1.1.md` - PyPI publication
- `release-0.1.2.md` - Configuration error handling patch
- `release-0.1.3.md` - CLI command improvement (navam invest)
- `release-0.1.4.md` - Product vision & architecture documentation
- `release-0.1.5.md` - Tier 1 API tools expansion (FMP, Treasury, SEC EDGAR) + Agent-tool integration (17 tools, 100% utilization) + Secure API key management
