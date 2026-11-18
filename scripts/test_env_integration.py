import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, r"C:\Users\Admin\Desktop\NexusInsight")

root = Path(r"C:\Users\Admin\Desktop\NexusInsight")
env_path = root / ".env"
backup = None
if env_path.exists():
    backup = env_path.read_bytes()

data_dir = Path(tempfile.mkdtemp(prefix="ni-envtest-"))
try:
    env_path.write_text(
        "\n".join(
            [
                "DEMO_MODE=true",
                "COMPANY_NAME=Env Loaded Co",
                "ENVIRONMENT=EnvTest",
                f"DATA_DIR={data_dir}",
                "CACHE_MINUTES=17",
                "APP_PASSWORD=env-test-password",
                "",
            ]
        ),
        encoding="utf-8",
    )
    from nexus_insight import create_app

    app = create_app()
    settings = app.extensions["store"].settings()
    public = app.extensions["store"].public_settings()
    print("company:", settings["company_name"])
    print("environment:", settings["environment"])
    print("cache:", settings["cache_minutes"])
    print("demo:", settings["demo_mode"])
    print("auth_enabled:", public["app_auth_enabled"])
    print("env_keys:", public.get("env_keys"))
    assert settings["company_name"] == "Env Loaded Co"
    assert settings["environment"] == "EnvTest"
    assert settings["cache_minutes"] == 17
    assert settings["demo_mode"] is True
    assert public["app_auth_enabled"] is True
    print("env integration ok")
finally:
    if backup is None:
        env_path.unlink(missing_ok=True)
    else:
        env_path.write_bytes(backup)
    shutil.rmtree(data_dir, ignore_errors=True)
