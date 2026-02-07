import asyncio
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def _rand_email(prefix: str) -> str:
    import uuid
    return f"{prefix}-{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def random_user_payload():
    return {"email": _rand_email("user"), "password": "pass12345"}


@pytest.fixture
def random_company_payload():
    return {"email": _rand_email("company"), "password": "pass12345"}


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
