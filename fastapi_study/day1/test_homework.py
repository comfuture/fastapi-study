
import os
import sys
import pytest
from fastapi.testclient import TestClient
from fastapi_study.day1.homework import app

project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)


@pytest.fixture
def client():
    """yields fastapi test_client for an app"""
    yield TestClient(app)


def test_raw_querystrings(client):
    """미정형 쿼리스트링 테스트"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'queries': {}}, '아무 쿼리 파라메터를 넘기지 않음'

    response = client.get('/?a=1&b=2')
    assert response.status_code == 200
    assert response.json() == {'queries': {'a': '1', 'b': '2'}}, '쿼리 파라메터를 모두 참조함'


def test_modeled_querystrings(client):
    """모델을 정의한 쿼리스트링 테스트"""
    response = client.get('/with-models')
    assert response.status_code == 200
    assert response.json() == {'name': None, 'age': 0}, '아무 쿼리 파라메터를 넘기지 않음'

    response = client.get('/with-models?name=maroo&age=20')
    assert response.status_code == 200
    assert response.json() == {'name': 'maroo', 'age': 20}, '쿼리 파라메터를 모두 참조함'
    assert type(response.json().get('age')) == int, '자동 형 변환이 일어남'

    response = client.get('/with-models?name=maroo&age=twenty')
    assert response.status_code == 200
    assert response.json() == {'name': 'maroo', 'age': 0}, '잘못된 파라메터 타잎을 validator가 보정함'
