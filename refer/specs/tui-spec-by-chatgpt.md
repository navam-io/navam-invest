Awesome—here’s a battle-tested, Python-first stack for a **chat-style TUI + CLI** around your LangGraph agents in Navam Invest.

# Core picks (what I’d use)

**CLI command layer**

* **Typer** – modern, type-hinted CLI (subcommands, help, completion) with minimal boilerplate.
* **Rich** – colored output, tables, markdown, progress bars, tracebacks.
* **Rich-click** (optional) – pretty formatting for Click/Typer help.

**Interactive chat TUI (full screen)**

* **Textual** – event-driven TUI framework from Rich authors (layouts, panels, inputs, scroll, mouse support).
* **Textual-Dev** – hot-reload dev server (`textual run --dev`).
* **Textualize Markdown** – use Rich’s Markdown renderer inside Textual views.

**Lightweight REPL (alt path if you want minimal UI)**

* **prompt-toolkit** – readline-style chat input with multiline editing, history, completions, keybindings.
* **InquirerPy** or **questionary** – quick menus/prompts when you don’t need a full TUI.

**Streaming & async**

* **anyio** (or native `asyncio`) – task groups for concurrent streaming.
* **httpx** (async client) – if you call external APIs/tools.
* **websockets** (optional) – if you ever stream from a local server or tool.

**Markdown, rendering, and formatting**

* **Rich Markdown** – render model output with headings, code blocks, tables.
* **Pygments** – syntax highlighting in code blocks.

**State, config, and profiles**

* **pydantic-settings** – load config from `.env`, env vars, or `settings.toml`.
* **typer-config** (optional) – map CLI options to config files.
* **sqlite + SQLModel** (or **DuckDB**) – small, embeddable store for chat logs, portfolios, caches.

**Progress & task feedback**

* **Rich Progress** – spinners/progress for “screening”, “optimizing”, “backtesting”.
* **tqdm-rich** (optional) – drop-in progress with Rich skin for batch ops.

**Observability ( super useful with agents )**

* **loguru** – simple structured logging.
* **OpenTelemetry** + **opentelemetry-exporter-otlp** – trace runs/steps/tools.
* **rich-traceback** – great DX for errors in terminal.

**Testing & scaffolding**

* **pytest**, **pytest-asyncio**
* **ruff**, **black**, **mypy**
* **uv** or **poetry** for env + packaging.

---

# Two implementation patterns

## A) Full-screen TUI (Textual)

Best for a **chat pane + side panels** (portfolio, positions, watchlists) and **live streaming tokens**.

* **Layout**

  * Left: Conversation (auto-scroll, markdown).
  * Right top: “Run details” (active graph node, tool call, latency).
  * Right bottom: “Portfolio/Screeners/Tasks”.
  * Bottom: Input bar with history and slash-commands (`/screen`, `/optimize`, `/help`).
* **Why Textual**: You get reactive widgets, keybindings, mouse, resizable panes, and Rich rendering out-of-the-box.

## B) Minimal chat CLI (prompt-toolkit + Typer)

Great for **fast iteration** and scripting. Offers multiline editing, history, completion, and streaming line updates.

---

# Suggested pip installs

```bash
uv add typer rich rich-click textual textual-dev httpx anyio pydantic pydantic-settings sqlmodel sqlite-utils loguru \
    prompt-toolkit inquirerpy pygments opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

*(Pick Textual **or** prompt-toolkit as your primary UI; you can keep both during exploration.)*

---

# Integration notes for LangGraph

* Run your graph with **async streaming callbacks** and push tokens to:

  * **Textual**: append to a `RichLog` or `Markdown` widget in a background task (`await worker.start()` with `TaskGroup`).
  * **prompt-toolkit**: use a background task to write to a Rich console above the input buffer.
* Expose **agent step events** (node start/end, tool invocations, latency) and render in a side panel with **live Rich tables**.
* Provide **slash commands** mapped to Typer subcommands for reproducible runs:
  `navam screen --universe sp500 --pe-lt 20`, `navam optimize --goal "max Sharpe" --constraints "..."`
* Persist chat threads, user profiles, and portfolios to **SQLite/SQLModel**; let the user switch profiles via a quick picker.

---

# Tiny starter blueprints

## Option A: Typer entrypoint that launches Textual

```python
# app.py
import typer
from textual.app import App, ComposeResult
from textual.widgets import Footer, Input, RichLog
from rich.markdown import Markdown
import asyncio

cli = typer.Typer()

class ChatUI(App):
    CSS = "Screen {layout: vertical} #log {height: 1fr} #input {height: 3}"
    def compose(self) -> ComposeResult:
        yield RichLog(id="log")
        yield Input(placeholder="Type a message (enter to send)…", id="input")
        yield Footer()

    async def on_input_submitted(self, msg: Input.Submitted) -> None:
        text = msg.value.strip()
        self.query_one("#input", Input).value = ""
        log = self.query_one("#log", RichLog)
        log.write(f"[bold cyan]>[/] {text}")
        # TODO: call LangGraph and stream tokens:
        for token in ["Opt", "imiz", "ing", " …"]:
            await asyncio.sleep(0.1)
            log.write(Markdown(token), expand=False)

@cli.command()
def tui():
    ChatUI().run()

if __name__ == "__main__":
    cli()
```

## Option B: prompt-toolkit chat loop with Rich output

```python
# chat.py
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.markdown import Markdown
import anyio

console = Console()
session = PromptSession(history=FileHistory(".navam_history"))

async def stream_reply(user_text: str):
    # TODO: wire to LangGraph async generator
    for token in ["Scree", "ning", " ", "100", " symbols", " …"]:
        yield token
        await anyio.sleep(0.05)

async def main():
    while True:
        user = await anyio.to_thread.run_sync(session.prompt, "> ")
        if user.strip().lower() in {"quit", "exit"}:
            break
        console.print(f"[bold cyan]>[/] {user}")
        async for tok in stream_reply(user):
            console.print(Markdown(tok), end="")

if __name__ == "__main__":
    anyio.run(main)
```

---

# Nice-to-haves for Navam Invest

* **Slash-command router** in Textual (map `/screen`, `/optimize`, `/rebalance`, `/explain`).
* **Portable keybindings** (e.g., `Ctrl+K` open command palette; `Ctrl+R` run last workflow).
* **Session recording**: save all agent runs (inputs, outputs, timings) to SQLite for auditability.
* **Theme**: Rich styles to match your pastel Navam brand (kept minimal for accessibility).
* **Graph viz**: render the active LangGraph plan with **graphviz** and show a thumbnail in TUI.

---

If you want, I can scaffold a minimal repo with Typer + Textual wired to a sample LangGraph node and streaming callbacks—ready to run with `uv run navam tui`.
