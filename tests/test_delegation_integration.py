import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from database import connect_to_mongo, close_mongo_connection

@pytest_asyncio.fixture
async def mongo_connection():
    await connect_to_mongo()
    yield
    await close_mongo_connection()

@pytest_asyncio.fixture
async def clean_users(mongo_connection):
    from database import get_database
    db = get_database()
    await db.users.delete_many({})
    yield

@pytest_asyncio.fixture
async def async_client(mongo_connection):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_delegation_flow(async_client, clean_users):
    """Test complet du flow personne aidant : invitation, acceptation, révocation, accès Kanban."""
    # 1. Créer deux utilisateurs (user et aidant)
    user_data = {"username": "user1", "email": "user1@test.com", "password": "testpass", "full_name": "User One"}
    aidant_data = {"username": "aidant1", "email": "aidant1@test.com", "password": "testpass", "full_name": "Aidant One"}

    resp_user = await async_client.post("/api/auth/register", json=user_data)
    print("REGISTER USER RESPONSE:", resp_user.status_code, resp_user.json())
    assert resp_user.status_code == 200
    user_id = resp_user.json()["data"]["user"]["id"]
    resp_aidant = await async_client.post("/api/auth/register", json=aidant_data)
    assert resp_aidant.status_code == 200
    aidant_id = resp_aidant.json()["data"]["user"]["id"]

    # 2. Login pour récupérer les tokens
    resp_login_user = await async_client.post("/api/auth/login", json={"username": user_data["username"], "password": user_data["password"]})
    assert resp_login_user.status_code == 200
    token_user = resp_login_user.json()["data"]["access_token"]
    resp_login_aidant = await async_client.post("/api/auth/login", json={"username": aidant_data["username"], "password": aidant_data["password"]})
    assert resp_login_aidant.status_code == 200
    token_aidant = resp_login_aidant.json()["data"]["access_token"]

    # 3. User invite l'aidant
    resp_invite = await async_client.post(
        "/delegations/invite",
        params={"aidant_id": aidant_id},
        headers={"Authorization": f"Bearer {token_user}"}
    )
    assert resp_invite.status_code == 200
    print("RESPONSE INVITE:", resp_invite.json())
    delegation_id = resp_invite.json()["_id"]

    # 4. Aidant accepte la délégation
    resp_accept = await async_client.post(
        "/delegations/accept",
        params={"delegation_id": delegation_id},
        headers={"Authorization": f"Bearer {token_aidant}"}
    )
    assert resp_accept.status_code == 200
    assert resp_accept.json()["status"] == "accepted"

    # 5. User crée une tâche
    task_data = {"title": "Tâche aidée", "category": "personnel", "priority": "normale"}
    resp_task = await async_client.post("/api/tasks/", json=task_data, headers={"Authorization": f"Bearer {token_user}"})
    print("TASK CREATE RESPONSE:", resp_task.status_code, resp_task.json())
    assert resp_task.status_code in (200, 201)
    # 6. Aidant accède au Kanban de user
    resp_kanban = await async_client.get(
        "/delegations/kanban",
        params={"user_id": user_id},
        headers={"Authorization": f"Bearer {token_aidant}"}
    )
    assert resp_kanban.status_code == 200
    tasks = resp_kanban.json()
    assert any(t["title"] == "Tâche aidée" for t in tasks)

    # 7. User révoque la délégation
    resp_revoke = await async_client.post(
        "/delegations/revoke",
        params={"delegation_id": delegation_id},
        headers={"Authorization": f"Bearer {token_user}"}
    )
    assert resp_revoke.status_code == 200
    assert resp_revoke.json()["status"] == "revoked"

    # 8. Aidant ne peut plus accéder au Kanban
    resp_kanban2 = await async_client.get(
        "/delegations/kanban",
        params={"user_id": user_id},
        headers={"Authorization": f"Bearer {token_aidant}"}
    )
    assert resp_kanban2.status_code == 403 