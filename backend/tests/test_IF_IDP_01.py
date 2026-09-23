import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.auth.idp import DEV_ACTOR_ID, Identity, get_verifier, require_identity

TEST_HEADER = "X-Test-Identity"


# app เล็กสำหรับ test เพราะ T-03 ยังไม่มี endpoint จริง
def make_app() -> FastAPI:
    app = FastAPI()

    @app.get("/protected")
    def protected(identity: Identity = Depends(require_identity)) -> dict:
        return {"actor_id": identity.actor_id}

    return app


# ตัวตรวจจำลองของ test: มี header ถือว่ายืนยันตัวตนแล้ว
def fake_verifier(request) -> Identity | None:
    actor = request.headers.get(TEST_HEADER)
    return Identity(actor_id=actor) if actor else None


# T-03 / IF-IDP-01: request ที่ไม่มีผลยืนยันตัวตนถูกปฏิเสธ
def test_IF_IDP_01_rejects_request_without_identity() -> None:
    app = make_app()
    app.dependency_overrides[get_verifier] = lambda: fake_verifier
    res = TestClient(app).get("/protected")
    assert res.status_code == 401


# T-03 / IF-IDP-01: request ที่มีผลยืนยันตัวตนผ่าน และได้ actor_id
def test_IF_IDP_01_accepts_request_with_identity() -> None:
    app = make_app()
    app.dependency_overrides[get_verifier] = lambda: fake_verifier
    res = TestClient(app).get("/protected", headers={TEST_HEADER: "nurse-01"})
    assert res.status_code == 200
    assert res.json() == {"actor_id": "nurse-01"}


# T-03 / IF-IDP-01: ค่าเริ่มต้น (ไม่ตั้ง AUTH_MODE) ปฏิเสธทุก request
def test_IF_IDP_01_default_rejects_all(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AUTH_MODE", raising=False)
    res = TestClient(make_app()).get("/protected", headers={TEST_HEADER: "nurse-01"})
    assert res.status_code == 401


# T-03 / IF-IDP-01: AUTH_MODE=dev ใช้ตัวตรวจจำลองตอนพัฒนา
def test_IF_IDP_01_dev_mode_accepts_dev_user(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AUTH_MODE", "dev")
    res = TestClient(make_app()).get("/protected")
    assert res.status_code == 200
    assert res.json() == {"actor_id": DEV_ACTOR_ID}
