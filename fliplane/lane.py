from dataclasses import dataclass, field
from typing import List, Optional
from .task import Task


@dataclass
class Lane:
    name: str
    tasks: List[Task] = field(default_factory=list)
    env: dict = field(default_factory=dict)
    description: str = ""

    def add_task(self, task: Task) -> "Lane":
        self.tasks.append(task)
        return self

    def run(self, console=None) -> bool:
        from rich.console import Console
        out = console or Console()

        out.print(f"\n[bold cyan]Lane:[/bold cyan] [yellow]{self.name}[/yellow]")
        if self.description:
            out.print(f"  [dim]{self.description}[/dim]")

        for task in self.tasks:
            out.print(f"  [blue]▶[/blue] Running task: [bold]{task.name}[/bold]")
            out.print(f"    [dim]{task.command}[/dim]")
            success = task.run(extra_env=self.env)
            if success:
                out.print(f"  [green]✔[/green] {task.name}")
            else:
                out.print(f"  [red]✘[/red] {task.name} failed")
                if not task.ignore_errors:
                    return False
        return True
