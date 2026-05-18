import subprocess
import shlex
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    name: str
    command: str
    env: dict = field(default_factory=dict)
    cwd: Optional[str] = None
    ignore_errors: bool = False

    def run(self, extra_env: Optional[dict] = None) -> bool:
        import os
        env = {**os.environ, **self.env, **(extra_env or {})}
        try:
            result = subprocess.run(
                shlex.split(self.command),
                env=env,
                cwd=self.cwd,
                text=True,
            )
            return result.returncode == 0
        except Exception as e:
            if self.ignore_errors:
                return True
            raise RuntimeError(f"Task '{self.name}' failed: {e}") from e
