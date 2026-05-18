from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .lane import Lane


@dataclass
class Pipeline:
    name: str
    lanes: Dict[str, Lane] = field(default_factory=dict)
    active_lane: Optional[str] = None

    def add_lane(self, lane: Lane) -> "Pipeline":
        self.lanes[lane.name] = lane
        if self.active_lane is None:
            self.active_lane = lane.name
        return self

    def flip(self, lane_name: str) -> "Pipeline":
        if lane_name not in self.lanes:
            raise ValueError(f"Lane '{lane_name}' not found in pipeline '{self.name}'")
        self.active_lane = lane_name
        return self

    def run(self, lane_name: Optional[str] = None, console=None) -> bool:
        from rich.console import Console
        out = console or Console()

        target = lane_name or self.active_lane
        if target is None:
            raise ValueError("No lane specified and no active lane set")
        if target not in self.lanes:
            raise ValueError(f"Lane '{target}' not found")

        out.print(f"\n[bold magenta]Pipeline:[/bold magenta] [white]{self.name}[/white]")
        success = self.lanes[target].run(console=out)

        if success:
            out.print(f"\n[bold green]Pipeline '{self.name}' completed successfully.[/bold green]")
        else:
            out.print(f"\n[bold red]Pipeline '{self.name}' failed.[/bold red]")
        return success

    def run_all(self, console=None) -> bool:
        from rich.console import Console
        out = console or Console()

        out.print(f"\n[bold magenta]Pipeline:[/bold magenta] [white]{self.name}[/white] (all lanes)")
        for lane in self.lanes.values():
            if not lane.run(console=out):
                return False
        return True
