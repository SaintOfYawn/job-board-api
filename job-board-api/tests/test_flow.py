import pytest


@pytest.mark.asyncio
async def test_register_login_and_flow(client, random_company_payload, random_user_payload):
    r = await client.post("/auth/register-company", json=random_company_payload)
    assert r.status_code == 200, r.text
    company_token = r.json()["access_token"]

    r = await client.post(
        "/companies/me",
        json={"name": "TestCo", "description": "desc", "website": "https://test.co"},
        headers={"Authorization": f"Bearer {company_token}"},
    )
    assert r.status_code == 200, r.text

    r = await client.post(
        "/vacancies",
        json={
            "title": "Junior Python",
            "description": "FastAPI + Postgres",
            "city": "Remote",
            "min_salary": 1000,
            "max_salary": 2000,
            "employment_type": "full_time",
        },
        headers={"Authorization": f"Bearer {company_token}"},
    )
    assert r.status_code == 200, r.text
    vacancy_id = r.json()["id"]

    r = await client.get("/vacancies?limit=10&offset=0")
    assert r.status_code == 200, r.text
    assert r.json()["total"] >= 1

    r = await client.post("/auth/register", json=random_user_payload)
    assert r.status_code == 200, r.text
    user_token = r.json()["access_token"]

    r = await client.post(
        f"/applications/vacancy/{vacancy_id}",
        json={"cover_letter": "Hello!"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert r.status_code == 200, r.text
    app_id = r.json()["id"]

    r = await client.post(
        f"/applications/vacancy/{vacancy_id}",
        json={"cover_letter": "Again"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert r.status_code in (400, 409), r.text

    r = await client.get("/applications/me", headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 200, r.text
    assert any(x["id"] == app_id for x in r.json())

    r = await client.get(f"/applications/vacancy/{vacancy_id}", headers={"Authorization": f"Bearer {company_token}"})
    assert r.status_code == 200, r.text
    assert len(r.json()) >= 1
