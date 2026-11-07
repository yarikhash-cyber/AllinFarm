import httpx
import pytest

from allinfarm_api.main import app


@pytest.fixture
async def client() -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.db
async def test_health_reports_database_and_postgis(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["engine"] == {"engine": "0.1.0", "units": "0.1.0"}
    assert body["database"]["status"] == "ok"
    assert body["database"]["postgres"].startswith("18")
    assert body["database"]["postgis"].startswith("3.6")


async def test_openapi_is_served_under_api(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "AllinFarm API"
