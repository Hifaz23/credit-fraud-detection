from src.model_service import FraudModelService


service = FraudModelService()


def test_feature_count():
    assert len(service.features) == 30


def test_threshold():
    assert service.threshold == 0.7900000000000001


def test_prediction_output():
    transaction = {
        feature: 0.0
        for feature in service.features
    }

    result = service.predict(transaction)

    assert "fraud_probability" in result
    assert "threshold" in result
    assert "prediction" in result
    assert "decision" in result

    assert 0.0 <= result["fraud_probability"] <= 1.0
    assert result["prediction"] in [0, 1]
    assert result["decision"] in ["ALLOW", "FLAG"]