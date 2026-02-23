"""Typeless Voice Data Analyzer - AI-First CLI"""

import json
import platform
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console

from src.ai.analyzer import AIAnalyzer
from src.ai.fixtures import generate_mock_analyses
from src.config import get_settings
from src.factories.repository_factory import RepositoryFactory
from src.main.generator import BrutalistHTMLGenerator
from src.services.ai_insights import AIInsightsService
from src.services.app_usage import AppUsageService
from src.services.content_analysis import ContentAnalysisService
from src.services.efficiency import EfficiencyService
from src.services.overview import OverviewService
from src.services.time_trends import TimeTrendsService
from src.services.usage_habits import UsageHabitsService

app = typer.Typer(name="typeless", help="Typeless voice data analyzer")
cache_app = typer.Typer(help="Cache management")
app.add_typer(cache_app, name="cache")

console = Console()


# ── Helpers ───────────────────────────────────────────────────────────────────


def _export_from_database(db_path: Path, output_path: Path) -> Path:
    """Export voice records from Typeless SQLite database to JSON."""
    if not db_path.exists():
        console.print(f"[red]✗ Database not found: {db_path}[/red]")
        console.print(
            "\n[yellow]Please confirm Typeless is installed, or set TYPELESS_DB_PATH in .env[/yellow]"
        )
        raise typer.Exit(1)

    console.print(f"[cyan]Exporting from database:[/cyan] {db_path}")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, created_at,
                   COALESCE(refined_text, edited_text, '') as content,
                   duration, focused_app_name, focused_app_window_title
            FROM history
            WHERE refined_text IS NOT NULL AND refined_text != ''
            ORDER BY created_at
        """)
        rows = cursor.fetchall()

    if not rows:
        console.print("[yellow]Warning: no valid records in database[/yellow]")
        raise typer.Exit(1)

    data = []
    for id_val, created_at, content, duration, app_name, window_title in rows:
        try:
            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            timestamp = int(dt.timestamp())
        except (ValueError, AttributeError):
            timestamp = 0
        data.append(
            {
                "id": id_val,
                "timestamp": timestamp,
                "content": content,
                "duration": duration or 0,
                "app_name": app_name or "",
                "window_title": window_title or "",
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    console.print(f"[green]✓ Exported {len(data)} records[/green]")
    return output_path


def _open_in_browser(path: Path) -> None:
    """Open HTML report in the default browser (cross-platform)."""
    try:
        system = platform.system()
        if system == "Darwin":
            subprocess.run(["open", str(path)], check=True)
        elif system == "Windows":
            import os

            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", str(path)], check=True)
    except Exception:
        pass  # browser open failure is non-fatal


# ── Main command ──────────────────────────────────────────────────────────────


@app.command()
def analyze(
    input: Path = typer.Option(
        None,
        "-i",
        "--input",
        help="Path to Typeless exported JSON file (omit to auto-export from database)",
    ),
    output: Path = typer.Option(
        Path("output/personal/Typeless_Report.html"),
        "-o",
        "--output",
        help="Output HTML file path",
    ),
    lang: str = typer.Option(
        None, "-l", "--lang", help="Report language: zh or en (default from .env)"
    ),
    mock: bool = typer.Option(False, "-m", "--mock", help="Use mock data (skip AI and database)"),
    mock_count: int = typer.Option(500, "--mock-count", help="Number of mock records"),
    force_refresh: bool = typer.Option(
        False, "--force-refresh", help="Force re-run AI analysis (ignore cache)"
    ),
    no_open: bool = typer.Option(False, "--no-open", help="Do not open browser after generation"),
) -> None:
    """Analyze Typeless voice data and generate AI insights report."""
    settings = get_settings()
    report_lang = lang or settings.report_lang

    # ── 1. Load data ──────────────────────────────────────────────────────────
    if mock:
        with console.status(f"[cyan]Generating {mock_count} mock records..."):
            repo = RepositoryFactory().create_mock_repository()
            repo.generate_mock(count=mock_count)
            data = repo.get_all()
        console.print(f"[cyan]✓ Mock data:[/cyan] {len(data)} records")
    else:
        if input:
            if not input.exists():
                console.print(f"[red]✗ File not found: {input}[/red]")
                raise typer.Exit(1)
            json_path = input
        else:
            db_path = settings.get_db_path()
            json_path = Path("data/raw/temp_export.json")
            _export_from_database(db_path, json_path)

        with console.status("[cyan]Loading data..."):
            repo = RepositoryFactory().create_json_repository(json_path)
            data = repo.get_all()

        console.print(f"[cyan]✓ Loaded:[/cyan] {len(data)} records")

    # ── 2. AI analysis ────────────────────────────────────────────────────────
    if mock:
        with console.status("[cyan]Generating mock AI analyses..."):
            ai_analyses = generate_mock_analyses(list(data))
        console.print(f"[cyan]✓ Mock AI analyses:[/cyan] {len(ai_analyses)}")
    else:
        if not settings.ai_api_key:
            console.print(
                "\n[red]✗ AI API Key not found[/red]\n\n"
                "Configure in [bold].env[/bold]:\n"
                "  [yellow]AI_API_KEY=your_api_key_here[/yellow]\n"
                "  [yellow]AI_PRIMARY_PROVIDER=zhipu[/yellow]\n\n"
                "Supported providers: zhipu · deepseek · openai · anthropic · moonshot · alibaba\n"
                "See [bold].env.example[/bold] to get started.\n"
            )
            raise typer.Exit(1)

        from src.ai.base import ModelConfig, ProviderType

        try:
            primary_provider = ProviderType(settings.ai_primary_provider)
        except ValueError:
            console.print(f"[red]✗ Unsupported provider: {settings.ai_primary_provider}[/red]")
            raise typer.Exit(1)

        primary_config = ModelConfig(
            provider=primary_provider,
            model_name=settings.ai_primary_model,
            api_key=settings.ai_api_key,
        )

        fallback_configs = []
        if settings.ai_fallback_provider and settings.ai_fallback_api_key:
            try:
                fb_provider = ProviderType(settings.ai_fallback_provider)
                fb_model = "deepseek-v3" if fb_provider.value == "deepseek" else "gpt-4o-mini"
                fallback_configs.append(
                    ModelConfig(
                        provider=fb_provider,
                        model_name=fb_model,
                        api_key=settings.ai_fallback_api_key,
                    )
                )
            except ValueError:
                pass

        console.print(
            f"[dim]AI: {settings.ai_primary_provider}/{settings.ai_primary_model} "
            f"| concurrency: {settings.ai_concurrency} "
            f"| budget: ¥{settings.ai_max_cost_per_run}[/dim]"
        )

        analyzer = AIAnalyzer(
            primary=primary_config,
            fallbacks=fallback_configs,
            concurrency=settings.ai_concurrency,
            max_cost_cny=settings.ai_max_cost_per_run,
            force_refresh=force_refresh,
        )
        try:
            ai_analyses = analyzer.analyze(data)
        except KeyboardInterrupt:
            console.print(
                "\n[yellow]⚠ Interrupted — progress saved, next run will resume from checkpoint[/yellow]"
            )
            raise typer.Exit(1)

        summary = (
            f"[green]✓ AI analysis done[/green]"
            f"  cached: [cyan]{analyzer.cache_hits}[/cyan]"
            f"  new: [cyan]{analyzer.new_entries}[/cyan]"
            f"  cost: [yellow]¥{analyzer.run_cost:.4f}[/yellow]"
        )
        if analyzer.failed_count:
            summary += f"  [red]failed: {analyzer.failed_count}[/red]"
        console.print(summary)
        if analyzer.failed_count:
            console.print(
                f"[yellow]⚠ {analyzer.failed_count} record(s) failed AI analysis"
                f" (API error) — these entries have no AI insights in the report[/yellow]"
            )

    # ── 3. Statistical analysis ───────────────────────────────────────────────
    with console.status("[cyan]Running statistical analysis..."):
        overview = OverviewService(data).get_stats()
        habits = UsageHabitsService(data).get_habits()
        trends = TimeTrendsService(data).get_trends()
        efficiency = EfficiencyService(data, report_lang).get_metrics()
        app_usage = AppUsageService(data).get_app_usage()
        content = ContentAnalysisService(data, report_lang).analyze_content()
        ai_insights = AIInsightsService(ai_analyses, list(data)).get_insights()

    console.print("[green]✓ Statistical analysis done[/green]")

    # ── 4. Generate report ────────────────────────────────────────────────────
    result = {
        "overview": overview.model_dump(),
        "usage_habits": habits.model_dump(),
        "time_trends": trends.model_dump(),
        "efficiency_metrics": efficiency.model_dump(),
        "app_usage": app_usage.model_dump(),
        "content_deep_dive": content.model_dump(),
        "ai_insights": ai_insights,
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with console.status("[cyan]Generating HTML report..."):
        generator = BrutalistHTMLGenerator(lang=report_lang)
        generator.generate(result, str(output))

    console.print(f"\n[bold green]✓ Report generated:[/bold green] {output}")
    console.print(f"  records: {overview.total_records:,}")
    console.print(f"  words: {overview.total_words:,}")
    console.print(f"  active days: {overview.active_days}")

    if not no_open and settings.auto_open_report:
        _open_in_browser(output)


# ── Cache subcommands ─────────────────────────────────────────────────────────


@cache_app.command("status")
def cache_status() -> None:
    """Show AI analysis cache status."""
    from src.ai.cache import AICache

    settings = get_settings()
    cache_path = Path("data/ai_cache.json")

    if not cache_path.exists():
        console.print("[yellow]Cache file not found (no AI analysis run yet)[/yellow]")
        return

    cache = AICache(
        cache_path,
        model=settings.ai_primary_model,
        provider=settings.ai_primary_provider,
    )
    stats = cache.stats()

    console.print("\n[bold]📊 Cache status[/bold]")
    console.print(f"  cached entries: [cyan]{stats['total']:,}[/cyan]")
    console.print(f"  model: [cyan]{stats['provider']} / {stats['model']}[/cyan]")
    console.print(f"  last updated: [cyan]{stats['last_updated'][:19]}[/cyan]")
    size_mb = stats["size_bytes"] / 1024 / 1024
    console.print(f"  cache size: [cyan]{size_mb:.1f} MB[/cyan]")


@cache_app.command("clear")
def cache_clear(
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
) -> None:
    """Clear AI analysis cache."""
    if not yes:
        confirmed = typer.confirm("Clear all AI analysis cache? (next run will re-call the AI API)")
        if not confirmed:
            console.print("[yellow]Cancelled[/yellow]")
            return

    from src.ai.cache import AICache

    settings = get_settings()
    cache_path = Path("data/ai_cache.json")
    cache = AICache(
        cache_path, model=settings.ai_primary_model, provider=settings.ai_primary_provider
    )
    cache.clear()
    console.print("[green]✓ Cache cleared[/green]")


# ── Cost command ──────────────────────────────────────────────────────────────


@app.command("cost")
def show_cost() -> None:
    """Show historical AI API cost records."""
    from rich.table import Table

    cost_log_path = Path("data/cost_log.json")

    if not cost_log_path.exists():
        console.print("[yellow]No cost records yet (no AI analysis run)[/yellow]")
        return

    with open(cost_log_path, encoding="utf-8") as f:
        records = json.load(f)

    if not records:
        console.print("[yellow]No cost records found[/yellow]")
        return

    total = sum(r.get("cost_cny", 0) for r in records)
    console.print(f"\n[bold]💰 Cost records (total ¥{total:.2f})[/bold]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Date", style="dim")
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("New", justify="right")
    table.add_column("Cached", justify="right")
    table.add_column("Tokens", justify="right")
    table.add_column("Cost (CNY)", justify="right", style="cyan")

    for r in reversed(records[-20:]):
        table.add_row(
            r.get("date", "")[:19],
            r.get("provider", ""),
            r.get("model", ""),
            str(r.get("new_entries", 0)),
            str(r.get("cache_hits", 0)),
            f"{r.get('tokens', 0):,}",
            f"¥{r.get('cost_cny', 0):.4f}",
        )

    console.print(table)


if __name__ == "__main__":
    app()
