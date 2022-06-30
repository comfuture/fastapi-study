import os
import pytest
from fastapi.testclient import TestClient
from fastapi_study.day3.standalone_tasks import app


@pytest.fixture
def client():
    """yields fastapi test_client for an app"""
    yield TestClient(app)


def test_standalone_tasks(client):
    """스탠드얼론 `BackgroundTasks` 테스트"""
    response = client.get('/')
    assert response.status_code == 202
    filename = response.json().get('filename')
    assert os.path.exists(filename)
    os.unlink(filename)

@pytest.mark.skip('fastapi는 background 를 리턴하지 않아도 태스크를 실행합니다')
def test_returning_background_tasks(client):
    """실행되지 않는 스탠드얼론 `BackgroundTasks` 테스트"""
    response = client.get('/without-return')
    assert response.status_code == 202
    filename = response.json().get('filename')
    assert os.path.exists(filename)
    os.unlink(filename)
