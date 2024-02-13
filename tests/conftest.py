import pytest
import main


@pytest.fixture()
def test_client():
    app = main.app
    return app.test_client()
