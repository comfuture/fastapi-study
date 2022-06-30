
import os
import sys
import pytest
from unittest import TestCase
from fastapi.testclient import TestClient
from fastapi_study.day5.app import app, PostPayload

project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)


@pytest.fixture(scope='session')
def client():
    """yields fastapi test_client for an app"""
    yield TestClient(app)


def test_normal_request(client):
    """보통 요청"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0].get('title') == 'hello'


def test_schema_request(client):
    """스키마 요청"""
    response = client.get('/', headers={'Accept': 'application/schema+json'})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    TestCase().assertDictEqual(data, PostPayload.schema())


    response = client.get('/?type=schema')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    TestCase().assertDictEqual(data, PostPayload.schema())
