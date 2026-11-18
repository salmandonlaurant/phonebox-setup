import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, r"C:\Users\Admin\Desktop\NexusInsight")

from nexus_insight import _load_dotenv

for name in ("NI_TEST_A", "NI_TEST_B", "NI_TEST_C", "NI_TEST_D", "NI_TEST_E"):
    os.environ.pop(name, None)
os.environ["NI_TEST_B"] = "real-env-wins"

with tempfile.TemporaryDirectory() as tmp:
    env_path = Path(tmp) / ".env"
    env_path.write_text(
        "\ufeff# comment\n"
        "NI_TEST_A=plain value\n"
        "NI_TEST_B=from-file\n"
        "NI_TEST_C=\"quoted # value\"\n"
        "NI_TEST_D=value # trailing comment\n"
        "export NI_TEST_E='exported'\n"
        "INVALID LINE\n",
        encoding="utf-8",
    )
    _load_dotenv(env_path)

print("A:", repr(os.environ.get("NI_TEST_A")))
print("B:", repr(os.environ.get("NI_TEST_B")))
print("C:", repr(os.environ.get("NI_TEST_C")))
print("D:", repr(os.environ.get("NI_TEST_D")))
print("E:", repr(os.environ.get("NI_TEST_E")))
assert os.environ.get("NI_TEST_A") == "plain value"
assert os.environ.get("NI_TEST_B") == "real-env-wins"
assert os.environ.get("NI_TEST_C") == "quoted # value"
assert os.environ.get("NI_TEST_D") == "value"
assert os.environ.get("NI_TEST_E") == "exported"
print("dotenv ok")
