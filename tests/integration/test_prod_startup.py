import os
import subprocess
from pathlib import Path


def test_prod_startup_and_restart_scripts_dry_run():
    repo_root = Path(__file__).resolve().parents[2]
    start_script = repo_root / "scripts" / "prod-start.sh"
    restart_script = repo_root / "scripts" / "prod-restart.sh"

    env = os.environ.copy()
    env["PROD_DRY_RUN"] = "1"

    start_result = subprocess.run(
        ["bash", str(start_script)],
        check=True,
        env=env,
        capture_output=True,
        text=True,
    )
    restart_result = subprocess.run(
        ["bash", str(restart_script)],
        check=True,
        env=env,
        capture_output=True,
        text=True,
    )

    assert "DRY RUN" in start_result.stdout
    assert "DRY RUN" in restart_result.stdout
