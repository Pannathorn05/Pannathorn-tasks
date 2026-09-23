import pytest
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import config
from app.main import app


# T-01 / CON-TECH-01: app อ่าน DATABASE_URL จาก config
def test_T01_config_reads_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@db:5432/booking")
    assert config.get_database_url() == "postgresql+psycopg://user:pass@db:5432/booking"


# T-01 / CON-TECH-01: ไม่ได้ตั้ง DATABASE_URL ต้องแจ้ง error ไม่เดาค่าเริ่มต้น
def test_T01_config_requires_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError):
        config.get_database_url()


# T-01 / CON-TECH-01: conftest สร้าง session SQLite ในหน่วยความจำ
def test_T01_db_session_is_sqlite_in_memory(db_session: Session) -> None:
    assert db_session.bind.url.render_as_string() == "sqlite:///:memory:"
    assert db_session.execute(text("SELECT 1")).scalar_one() == 1


# T-01 / CON-TECH-01: มี FastAPI app ให้ router ของ task ถัดไปมาต่อ
def test_T01_app_created() -> None:
    assert isinstance(app, FastAPI)
