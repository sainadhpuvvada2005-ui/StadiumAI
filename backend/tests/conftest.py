import os
import tempfile
from pathlib import Path

TEST_DB = Path(tempfile.gettempdir()) / "stadiumai_pytest.sqlite"
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("ENVIRONMENT", "test")
