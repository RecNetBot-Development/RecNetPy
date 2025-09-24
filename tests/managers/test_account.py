import pytest
from typing import Dict, Any
from src.recnetpy.client import Client
from src.recnetpy.rest.response import Response
from src.recnetpy.dataclasses.account import Account, PLATFORM_LIST, PERSONAL_PRONOUNS_LIST, IDENTITY_FLAGS_LIST

pytestmark = pytest.mark.asyncio

ALL_PLATFORMS = 511
ALL_PERSONAL_PRONOUNS = 63
ALL_IDENTITY_FLAGS = 1023

def return_sample_account(account_id: int = 1) -> Dict[str, Any]:
    return {
        "accountId": account_id, "username": "Jegarde", "displayName": "Jesse", 
        "profileImage": "img.rec.net/pfp", "bannerImage": "img.rec.net/banner",
        "isJunior": False,
        "platforms": ALL_PLATFORMS,
        "personalPronouns": ALL_PERSONAL_PRONOUNS,
        "identityFlags": ALL_IDENTITY_FLAGS,
        "createdAt":"2024-06-10T00:00:00+00:00"
    }

def return_sample_client() -> Client:
    return Client(api_key="dummy")

def validate_account_except_id(account: Account) -> None:
    sample_account: Account = return_sample_account()
    assert account.username == sample_account["username"]
    assert account.display_name == sample_account["displayName"]
    assert account.profile_image == sample_account["profileImage"]
    assert account.banner_image == sample_account["bannerImage"]
    assert account.is_junior == sample_account["isJunior"]
    assert account.platforms == PLATFORM_LIST
    assert account.personal_pronouns == PERSONAL_PRONOUNS_LIST
    assert account.identity_flags == IDENTITY_FLAGS_LIST
    assert account.created_at == 1717977600


def return_empty_404_response() -> Response:
    return Response(
        url="empty404", status=404, success=False, headers={}, data={})


async def test_accounts_get_valid(monkeypatch):
    sample_account_data = return_sample_account()
    client = return_sample_client()
    
    async def fake_make_request(_self, method, params=None, body=None, headers=None) -> Response:
        return Response(
            url="bleh", status=200, success=True, headers={}, data=sample_account_data)
    
    monkeypatch.setattr(type(client.rec_net.accounts), "make_request", fake_make_request, raising=False)

    account = await client.accounts.get("valid")
    validate_account_except_id(account)

    await client.close()


async def test_accounts_get_invalid(monkeypatch):
    client = return_sample_client()
    
    async def fake_make_request(_self, method, params=None, body=None, headers=None) -> Response:
        return return_empty_404_response()
    
    monkeypatch.setattr(type(client.rec_net.accounts), "make_request", fake_make_request, raising=False)

    account = await client.accounts.get("invalid")
    assert account == None

    await client.close()


async def test_accounts_fetch_valid(monkeypatch):
    FETCH_ID = 1

    sample_account_data = return_sample_account(account_id=FETCH_ID)
    client = return_sample_client()
    
    async def fake_make_request(_self, method, params=None, body=None, headers=None) -> Response:
        return Response(
            url="bleh", status=200, success=True, headers={}, data=sample_account_data)
    
    monkeypatch.setattr(type(client.rec_net.accounts), "make_request", fake_make_request, raising=False)

    account = await client.accounts.fetch(FETCH_ID)
    assert account.id == FETCH_ID
    validate_account_except_id(account)

    await client.close()


async def test_accounts_fetch_invalid(monkeypatch):
    client = return_sample_client()
    
    async def fake_make_request(_self, method, params=None, body=None, headers=None) -> Response:
        return return_empty_404_response()
    
    monkeypatch.setattr(type(client.rec_net.accounts), "make_request", fake_make_request, raising=False)

    account = await client.accounts.fetch(-1)
    assert account == None

    await client.close()


async def test_accounts_get_many_valid(monkeypatch):
    FETCH_NAMES = ["1", "2", "3"]

    sample_account_data = []
    for i in FETCH_NAMES:
        sample_account_data.append(return_sample_account())

    client = return_sample_client()
    
    async def fake_make_request(_self, method, params=None, body=None, headers=None) -> Response:
        return Response(
            url="bleh", status=200, success=True, headers={}, data=sample_account_data)
    
    monkeypatch.setattr(type(client.rec_net.accounts), "make_request", fake_make_request, raising=False)

    accounts = await client.accounts.get_many(FETCH_NAMES)
    assert len(accounts) == len(FETCH_NAMES)

    for i, acc in enumerate(accounts):
        validate_account_except_id(acc)

    await client.close()


async def test_accounts_get_many_invalid(monkeypatch):
    FETCH_NAMES = []

    client = return_sample_client()
    
    async def fake_make_request(_self, method, params=None, body=None, headers=None) -> Response:
        return Response(url="bleh", status=200, success=True, headers={}, data=[])
    
    monkeypatch.setattr(type(client.rec_net.accounts), "make_request", fake_make_request, raising=False)

    accounts = await client.accounts.get_many(FETCH_NAMES)
    assert accounts == []

    await client.close()


async def test_accounts_fetch_many_valid(monkeypatch):
    FETCH_IDS = [1, 2, 3]

    sample_account_data = []
    for i in FETCH_IDS:
        sample_account_data.append(return_sample_account(account_id=i))

    client = return_sample_client()
    
    async def fake_make_request(_self, method, params=None, body=None, headers=None) -> Response:
        return Response(
            url="bleh", status=200, success=True, headers={}, data=sample_account_data)
    
    monkeypatch.setattr(type(client.rec_net.accounts), "make_request", fake_make_request, raising=False)

    accounts = await client.accounts.fetch_many(FETCH_IDS)
    assert len(accounts) == len(FETCH_IDS)

    for i, acc in enumerate(accounts):
        assert acc.id == FETCH_IDS[i]
        validate_account_except_id(acc)

    await client.close()


async def test_accounts_fetch_many_invalid(monkeypatch):
    FETCH_IDS = []

    client = return_sample_client()
    
    async def fake_make_request(_self, method, params=None, body=None, headers=None) -> Response:
        return Response(url="bleh", status=200, success=True, headers={}, data=[])
    
    monkeypatch.setattr(type(client.rec_net.accounts), "make_request", fake_make_request, raising=False)

    accounts = await client.accounts.fetch_many(FETCH_IDS)
    assert accounts == []

    await client.close()
    

async def test_accounts_search_valid(monkeypatch):
    search_result = [return_sample_account()]

    client = return_sample_client()
    
    async def fake_make_request(_self, method, params=None, body=None, headers=None) -> Response:
        return Response(
            url="bleh", status=200, success=True, headers={}, data=search_result)
    
    monkeypatch.setattr(type(client.rec_net.accounts), "make_request", fake_make_request, raising=False)

    accounts = await client.accounts.search("something")
    assert len(accounts) == 1

    await client.close()


async def test_accounts_search_invalid(monkeypatch):
    client = return_sample_client()
    
    async def fake_make_request(_self, method, params=None, body=None, headers=None) -> Response:
        return Response(url="bleh", status=200, success=True, headers={}, data=[])
    
    monkeypatch.setattr(type(client.rec_net.accounts), "make_request", fake_make_request, raising=False)

    accounts = await client.accounts.search("")
    assert accounts == []

    await client.close()


async def test_create_dataclass():
    client = return_sample_client()

    ACCOUNT_ID = 42
    sample_account_data = return_sample_account(ACCOUNT_ID)
    account = client.accounts.create_dataclass(ACCOUNT_ID, sample_account_data)
    
    assert account.id == ACCOUNT_ID
    validate_account_except_id(account)

    await client.close()


async def test_create_from_data_list():
    client = return_sample_client()

    ACCOUNT_IDS = [1, 2, 3]

    sample_account_data = []
    for i in ACCOUNT_IDS:
        sample_account_data.append(return_sample_account(account_id=i))

    accounts = client.accounts.create_from_data_list(sample_account_data)

    for i, acc in enumerate(accounts):
        assert acc.id == ACCOUNT_IDS[i]
        validate_account_except_id(acc)
    

    await client.close()
