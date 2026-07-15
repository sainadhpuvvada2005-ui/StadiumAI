import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.security.jwt import create_access_token, decode_token
from app.security.passwords import hash_password, verify_password


def unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}@example.com"


def register(client: TestClient, role: str = "fan") -> dict:
    email = unique_email(role)
    response = client.post("/api/v1/auth/register", json={
        "email": email,
        "full_name": f"{role.title()} User",
        "password": "password1234",
        "role": role,
        "preferred_language": "en",
    })
    assert response.status_code == 201, response.text
    data = response.json()
    data["email"] = email
    return data


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_auth_register_login_me_logout_and_validation():
    with TestClient(app) as client:
        created = register(client, "fan")
        duplicate = client.post("/api/v1/auth/register", json={
            "email": created["email"],
            "full_name": "Fan User",
            "password": "password1234",
            "role": "fan",
            "preferred_language": "en",
        })
        assert duplicate.status_code == 409
        login = client.post("/api/v1/auth/login", json={"email": created["email"], "password": "password1234"})
        assert login.status_code == 200
        token = login.json()["access_token"]
        me = client.get("/api/v1/auth/me", headers=auth_headers(token))
        assert me.status_code == 200
        assert me.json()["email"] == created["email"]
        bad_login = client.post("/api/v1/auth/login", json={"email": created["email"], "password": "wrongpassword"})
        assert bad_login.status_code == 401
        forgot = client.post("/api/v1/auth/forgot-password", json={"email": created["email"]})
        assert forgot.status_code == 200
        logout = client.post("/api/v1/auth/logout")
        assert logout.status_code == 200


def test_jwt_and_password_helpers():
    hashed = hash_password("password1234")
    assert hashed != "password1234"
    assert verify_password("password1234", hashed)
    assert not verify_password("wrongpassword", hashed)
    token = create_access_token("user-1", "fan")
    payload = decode_token(token)
    assert payload.sub == "user-1"
    assert payload.role == "fan"


def test_rbac_admin_and_dashboard_access():
    with TestClient(app) as client:
        fan = register(client, "fan")
        admin = register(client, "admin")
        blocked = client.get("/api/v1/admin/users", headers=auth_headers(fan["access_token"]))
        assert blocked.status_code == 403
        users = client.get("/api/v1/admin/users", headers=auth_headers(admin["access_token"]))
        assert users.status_code == 200
        assert isinstance(users.json(), list)
        fan_dashboard = client.get("/api/v1/dashboards/fan", headers=auth_headers(fan["access_token"]))
        assert fan_dashboard.status_code == 200
        admin_dashboard = client.get("/api/v1/dashboards/admin", headers=auth_headers(admin["access_token"]))
        assert admin_dashboard.status_code == 200


def test_ai_crowd_sustainability_and_incidents():
    with TestClient(app) as client:
        fan = register(client, "fan")
        volunteer = register(client, "volunteer")
        crowd = client.get("/api/v1/dashboards/crowd", headers=auth_headers(fan["access_token"]))
        assert crowd.status_code == 200
        assert len(crowd.json()) >= 1
        sustainability = client.get("/api/v1/dashboards/sustainability", headers=auth_headers(fan["access_token"]))
        assert sustainability.status_code == 200
        assert "carbon_kg" in sustainability.json()
        ai = client.post("/api/v1/ai/chat", headers=auth_headers(fan["access_token"]), json={"message": "Which gate is safest?", "language": "en", "context": {}})
        assert ai.status_code == 200
        assert "answer" in ai.json()
        incident = client.post("/api/v1/incidents", headers=auth_headers(volunteer["access_token"]), json={"type": "medical", "zone": "Gate B", "description": "Guest needs medical help"})
        assert incident.status_code == 200
        assert incident.json()["priority"] == "high"
        listed = client.get("/api/v1/incidents", headers=auth_headers(volunteer["access_token"]))
        assert listed.status_code == 200
        assert len(listed.json()) >= 1


def test_monitoring_security_headers_rate_limit_and_websocket():
    with TestClient(app) as client:
        for path in ["/health", "/liveness", "/readiness", "/metrics"]:
            response = client.get(path)
            assert response.status_code == 200
            assert response.headers["X-Content-Type-Options"] == "nosniff"
            assert "X-Request-Duration-Ms" in response.headers
        with client.websocket_connect("/api/v1/realtime/ws") as websocket:
            assert websocket.receive_json()["type"] == "connected"
            websocket.send_json({"message": "hello"})
            assert websocket.receive_json()["type"] == "event"
