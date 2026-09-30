"""
CLI interface for pixelforge (Web UI workbench launcher).
"""

import webbrowser
import typer
import uvicorn
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="pixelforge",
    help="Fast and interactive Web UI workbench for image conversion (SVG vectorization & WebP compression).",
    add_completion=False,
)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Bind host address."),
    port: int = typer.Option(8000, "--port", "-p", help="Bind port number."),
    open_browser: bool = typer.Option(True, "--open-browser/--no-open-browser", help="Auto open browser on start."),
):
    """
    Launch interactive Web UI workbench for drag-and-drop image conversion.
    """
    if ctx.invoked_subcommand is not None:
        return

    url = f"http://{host}:{port}"
    console.print(
        Panel(
            f"[bold green]✨ PixelForge Web UI is running![/bold green]\n\n"
            f"🔗 Local URL: [bold cyan underline]{url}[/bold cyan underline]\n"
            f"💡 Supported modes: [yellow]SVG Vectorization (VTracer)[/yellow] & [yellow]WebP Compression[/yellow]\n\n"
            f"[dim]Press Ctrl+C to stop the server.[/dim]",
            title="[bold magenta]Workbench Started[/bold magenta]",
        )
    )

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    from .server import app as fastapi_app
    uvicorn.run(fastapi_app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    app()
