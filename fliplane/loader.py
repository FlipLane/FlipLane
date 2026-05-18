import yaml
from pathlib import Path
from .pipeline import Pipeline
from .lane import Lane
from .task import Task


def load_pipeline(path: str = "fliplane.yaml") -> Pipeline:
    config = yaml.safe_load(Path(path).read_text())

    pipeline = Pipeline(name=config.get("name", "pipeline"))
    pipeline.active_lane = config.get("default_lane")

    for lane_cfg in config.get("lanes", []):
        lane = Lane(
            name=lane_cfg["name"],
            description=lane_cfg.get("description", ""),
            env=lane_cfg.get("env", {}),
        )
        for task_cfg in lane_cfg.get("tasks", []):
            task = Task(
                name=task_cfg["name"],
                command=task_cfg["run"],
                env=task_cfg.get("env", {}),
                cwd=task_cfg.get("cwd"),
                ignore_errors=task_cfg.get("ignore_errors", False),
            )
            lane.add_task(task)
        pipeline.add_lane(lane)

    if pipeline.active_lane is None and pipeline.lanes:
        pipeline.active_lane = next(iter(pipeline.lanes))

    return pipeline
