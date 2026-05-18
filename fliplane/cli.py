import click
from rich.console import Console
from rich.table import Table
from .loader import load_pipeline

console = Console()


@click.group()
def main():
    """FlipLane — local Python pipeline runner."""
    pass


@main.command()
@click.argument("lane", required=False)
@click.option("-f", "--file", default="fliplane.yaml", help="Pipeline config file")
def run(lane, file):
    """Run a pipeline lane (defaults to active lane)."""
    try:
        pipeline = load_pipeline(file)
        success = pipeline.run(lane_name=lane)
        raise SystemExit(0 if success else 1)
    except (ValueError, FileNotFoundError) as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1) from e


@main.command()
@click.option("-f", "--file", default="fliplane.yaml", help="Pipeline config file")
def run_all(file):
    """Run all lanes in the pipeline."""
    try:
        pipeline = load_pipeline(file)
        success = pipeline.run_all()
        raise SystemExit(0 if success else 1)
    except (ValueError, FileNotFoundError) as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1) from e


@main.command()
@click.argument("lane")
@click.option("-f", "--file", default="fliplane.yaml", help="Pipeline config file")
def flip(lane, file):
    """Show what would run if you flip to a different lane."""
    try:
        pipeline = load_pipeline(file)
        if lane not in pipeline.lanes:
            console.print(f"[red]Lane '{lane}' not found.[/red]")
            raise SystemExit(1)
        console.print(f"\n[bold]Flipping to lane:[/bold] [yellow]{lane}[/yellow]")
        for task in pipeline.lanes[lane].tasks:
            console.print(f"  [blue]▶[/blue] {task.name}: [dim]{task.command}[/dim]")
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1) from e


@main.command()
@click.option("-f", "--file", default="fliplane.yaml", help="Pipeline config file")
def list(file):
    """List all lanes and tasks in the pipeline."""
    try:
        pipeline = load_pipeline(file)
        table = Table(title=f"Pipeline: {pipeline.name}")
        table.add_column("Lane", style="yellow")
        table.add_column("Task", style="cyan")
        table.add_column("Command", style="dim")
        table.add_column("Active", justify="center")

        for lane_name, lane in pipeline.lanes.items():
            active = "✔" if lane_name == pipeline.active_lane else ""
            for i, task in enumerate(lane.tasks):
                table.add_row(
                    lane_name if i == 0 else "",
                    task.name,
                    task.command,
                    active if i == 0 else "",
                )
        console.print(table)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1) from e
