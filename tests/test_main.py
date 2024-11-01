import pytest

from fastapi.testclient import TestClient
from app.main import app
from app.database import Session
from app.models import Wallet

client = TestClient(app)

WALLET_UUID = "1"
balance = 100
operation_type = "DEPOSIT"
amount = 50


def setup():
    session = Session()
    wallet = Wallet(id=WALLET_UUID, balance=balance)
    session.merge(wallet)
    session.commit()


def teardown():
    session = Session()
    wallet = session.query(Wallet).get(WALLET_UUID)
    if wallet:
        session.delete(wallet)
        session.commit()


def test_get_balance():
    setup()
    response = client.get(f"/api/v1/wallets/{WALLET_UUID}")
    assert response.status_code == 200
    assert response.json()["balance"] == balance
    teardown()


def test_get_balance_invalid_WALLET_UUID():
    response = client.get("/api/v1/wallets/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Wallet not found"


def test_perform_operation_invalid_WALLET_UUID():
    response = client.post(
        "/api/v1/wallets/999/operation",
        json={"operation_type": operation_type, "amount": amount},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Wallet not found"


def test_perform_operation_deposit():
    setup()
    response = client.post(
        f"/api/v1/wallets/{WALLET_UUID}/operation",
        json={"operation_type": operation_type, "amount": amount},
    )
    assert response.status_code == 200
    assert response.json()["balance"] == balance + amount
    teardown()


def test_perform_operation_withdraw():
    setup()
    response = client.post(
        f"/api/v1/wallets/{WALLET_UUID}/operation",
        json={"operation_type": "WITHDRAW", "amount": amount},
    )
    assert response.status_code == 200
    assert response.json()["balance"] == balance - amount
    teardown()


def test_perform_operation_invalid_operation_type():
    setup()
    response = client.post(
        f"/api/v1/wallets/{WALLET_UUID}/operation",
        json={"operation_type": "INVALID", "amount": amount},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid operation type"
    teardown()


def test_perform_operation_insufficient_funds():
    setup()
    response = client.post(
        f"/api/v1/wallets/{WALLET_UUID}/operation",
        json={"operation_type": "WITHDRAW", "amount": balance + 1},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds"
    teardown()


def test_perform_operation_concurrent_updates():
    setup()
    import threading

    def perform_operation():
        response = client.post(
            f"/api/v1/wallets/{WALLET_UUID}/operation",
            json={"operation_type": operation_type, "amount": amount},
        )
        assert response.status_code == 200

    threads = []
    for _ in range(2):
        thread = threading.Thread(target=perform_operation)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    response = client.get(f"/api/v1/wallets/{WALLET_UUID}")
    assert response.status_code == 200
    assert response.json()["balance"] == balance + 2 * amount
    teardown()


@pytest.mark.benchmark
def test_perform_operation_1000_rps(benchmark):
    setup()

    def perform_operation():
        response = client.post(
            f"/api/v1/wallets/{WALLET_UUID}/operation",
            json={"operation_type": operation_type, "amount": amount},
        )
        assert response.status_code == 200

    benchmark.pedantic(perform_operation, rounds=1000, iterations=1)
    teardown()
