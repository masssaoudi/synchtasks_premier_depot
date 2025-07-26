import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "ok"}

@pytest.mark.asyncio
async def test_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/")
        assert resp.status_code == 200