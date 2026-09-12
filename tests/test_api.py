from fastapi.testclient import TestClient

import src.app as app_module


client = TestClient(app_module.app)


def make_valid_transaction():
    return {
        feature: 0.0
        for feature in app_module.model_service.features
    }


def test_home_status_code():
    response = client.get("/")

    assert response.status_code == 200


def test_home_message():
    response = client.get("/")

    assert response.json() == {
        "message": "Fraud Detection API is running"
    }


def test_predict_status_code(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "save_prediction",
        lambda **kwargs: None #temporarily sets the save prediction function as nothing so that it doesnt store anything 
    )

    response = client.post(
        "/predict",
        json=make_valid_transaction()
    )

    assert response.status_code == 200


def test_predict_response_structure(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "save_prediction",
        lambda **kwargs: None
    )

    response = client.post(
        "/predict",
        json=make_valid_transaction()
    )

    result = response.json()

    assert "fraud_probability" in result
    assert "threshold" in result
    assert "prediction" in result
    assert "decision" in result


def test_predict_response_values(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "save_prediction",
        lambda **kwargs: None
    )

    response = client.post(
        "/predict",
        json=make_valid_transaction()
    )

    result = response.json()

    assert 0.0 <= result["fraud_probability"] <= 1.0
    assert result["prediction"] in [0, 1]
    assert result["decision"] in ["ALLOW", "FLAG"]

def test_threshold_in_response(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "save_prediction",
        lambda **kwargs: None
    )

def test_missing_feature_returns_422(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "save_prediction",
        lambda **kwargs: None
    )

    transaction = make_valid_transaction()
    transaction.pop("Amount")

    response = client.post(
        "/predict",
        json=transaction
    )

    assert response.status_code == 422

    detail = response.json()["detail"]

    missing_fields = {
        error["loc"][-1]
        for error in detail
    }

    assert "Amount" in missing_fields


def test_multiple_missing_features_return_422(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "save_prediction",
        lambda **kwargs: None
    )

    transaction = make_valid_transaction()
    transaction.pop("Amount")
    transaction.pop("V1")

    response = client.post(
        "/predict",
        json=transaction
    )

    assert response.status_code == 422

    detail = response.json()["detail"]

    missing_fields = {
        error["loc"][-1]
        for error in detail
    }

    assert "Amount" in missing_fields
    assert "V1" in missing_fields
#Checks if FastAPI behaves correctly for a nonexistent endpoint.
def test_unknown_endpoint_returns_404():
    response = client.get("/does-not-exist")

    assert response.status_code == 404

def test_non_numeric_input_returns_422():
    transaction = make_valid_transaction()
    transaction["Amount"] = "not-a-number"

    response = client.post(
        "/predict",
        json=transaction
    )

    assert response.status_code == 422


def test_extra_feature_returns_422():
    transaction = make_valid_transaction()
    transaction["unexpected_feature"] = 123.0

    response = client.post(
        "/predict",
        json=transaction
    )

    assert response.status_code == 422
def test_prediction_failure_returns_500_and_logs(monkeypatch, caplog):
    def fake_predict(transaction):
        raise RuntimeError("Simulated model failure")

    monkeypatch.setattr(
        app_module.model_service,
        "predict",
        fake_predict
    )

    transaction = make_valid_transaction()

    with caplog.at_level("ERROR"):
        response = client.post(
            "/predict",
            json=transaction
        )

    assert response.status_code == 500
    assert response.json()["detail"] == "Prediction service failed"

    assert "event=prediction_failed" in caplog.text