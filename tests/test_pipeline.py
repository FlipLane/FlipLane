from fliplane import Pipeline, Lane, Task


def test_pipeline_add_lane():
    pipeline = Pipeline("test")
    lane = Lane("dev")
    pipeline.add_lane(lane)
    assert "dev" in pipeline.lanes
    assert pipeline.active_lane == "dev"


def test_pipeline_flip():
    pipeline = Pipeline("test")
    pipeline.add_lane(Lane("dev"))
    pipeline.add_lane(Lane("prod"))
    pipeline.flip("prod")
    assert pipeline.active_lane == "prod"


def test_lane_add_task():
    lane = Lane("dev")
    task = Task("hello", "echo hello")
    lane.add_task(task)
    assert len(lane.tasks) == 1
    assert lane.tasks[0].name == "hello"


def test_task_run_success():
    task = Task("echo", "echo hello")
    assert task.run() is True


def test_task_run_failure():
    task = Task("fail", "false", ignore_errors=False)
    assert task.run() is False


def test_loader(tmp_path):
    config = tmp_path / "fliplane.yaml"
    config.write_text("""
name: myapp
default_lane: dev
lanes:
  - name: dev
    tasks:
      - name: greet
        run: echo hello
""")
    from fliplane.loader import load_pipeline
    pipeline = load_pipeline(str(config))
    assert pipeline.name == "myapp"
    assert pipeline.active_lane == "dev"
    assert len(pipeline.lanes["dev"].tasks) == 1
