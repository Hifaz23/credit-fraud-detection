import sqlite3

import src.database as database


def test_initialize_database_creates_predictions_table(tmp_path, monkeypatch):
    test_db = tmp_path / "test_predictions.db"
#redirect database operations to a temporary test file
    monkeypatch.setattr(database, "DATABASE", test_db)

    database.initialize_database()

    with sqlite3.connect(test_db) as conn:
        result = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name='predictions'
            """
        ).fetchone()#fecth single row

    assert result is not None


def test_save_prediction_inserts_row(tmp_path, monkeypatch):
    test_db = tmp_path / "test_predictions.db"

    monkeypatch.setattr(database, "DATABASE", test_db)

    database.initialize_database()

    transaction = {"Amount": 100.0}

    database.save_prediction(
        transaction=transaction,
        fraud_probability=0.85,
        prediction=1,
        decision="FLAG"
    )

    with sqlite3.connect(test_db) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM predictions"
        ).fetchone()[0]

    assert count == 1


def test_saved_prediction_values(tmp_path, monkeypatch):
    test_db = tmp_path / "test_predictions.db"

    monkeypatch.setattr(database, "DATABASE", test_db)

    database.initialize_database()

    database.save_prediction(
        transaction={"Amount": 50.0},
        fraud_probability=0.10,
        prediction=0,
        decision="ALLOW"
    )

    with sqlite3.connect(test_db) as conn:
        row = conn.execute(
            """
            SELECT fraud_probability, prediction, decision
            FROM predictions
            LIMIT 1
            """
        ).fetchone()

    assert row[0] == 0.10
    assert row[1] == 0
    assert row[2] == "ALLOW"
