#!/usr/bin/env python3
"""Quick test of the /api command functionality."""

import asyncio

from rich.console import Console
from rich.table import Table

from navam_invest.utils import check_all_apis


async def main():
    """Test API checker."""
    console = Console()

    console.print("\n[bold cyan]Testing API Checker...[/bold cyan]\n")
    console.print("[dim]Checking connectivity to all APIs...[/dim]\n")

    # Run checks
    results = await check_all_apis()

    # Create table
    table = Table(
        title="API Status Report",
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
    )
    table.add_column("API Provider", style="cyan", width=18)
    table.add_column("Status", width=18)
    table.add_column("Details", style="dim", width=50)

    # Add rows
    for result in results:
        status = result["status"]
        if "✅" in status:
            status_styled = f"[green]{status}[/green]"
        elif "❌" in status:
            status_styled = f"[red]{status}[/red]"
        elif "⚠️" in status:
            status_styled = f"[yellow]{status}[/yellow]"
        else:
            status_styled = f"[dim]{status}[/dim]"

        table.add_row(result["api"], status_styled, result["details"])

    console.print(table)

    # Summary
    working = sum(1 for r in results if "✅" in r["status"])
    failed = sum(1 for r in results if "❌" in r["status"])
    not_configured = sum(1 for r in results if "⚪" in r["status"])

    console.print(
        f"\n[bold]Summary:[/bold] {working} working • {failed} failed • {not_configured} not configured\n"
    )

    if failed > 0:
        console.print(
            "[yellow]💡 Tip:[/yellow] Check your .env file for correct API keys\n"
        )


if __name__ == "__main__":
    asyncio.run(main())
