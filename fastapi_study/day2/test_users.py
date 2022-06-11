
# pylint: disable=redefined-outer-name
import os
import tempfile
from random import randint
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from fastapi_study.day2.app import create_app
from fastapi_study.day2.schema import UserBase


@pytest.fixture(scope='function')
def fastapi_app():
    """yields fastapi app"""
    # sqlite_file = tempfile.NamedTemporaryFile(suffix='.db')
    with tempfile.NamedTemporaryFile(suffix='.db') as sqlite_file:
        # sqlite_file = './test.db'
        os.environ['DATABASE_DSN'] = f'sqlite:///{sqlite_file.name}'
        app = create_app()
        yield app
        # os.unlink(sqlite_file.name)


@pytest.fixture(scope='function')
def client(fastapi_app):
    """yields fastapi test_client for an app"""
    yield TestClient(fastapi_app)


fake = Faker()

def create_dummy_user():
    """더미 사용자 속성"""
    return {
        'name': fake.name(),
        'age': randint(16, 66)
    }


def test_user(client):
    """사용자 테스트"""

    # 예제 사용자 생성
    payload = UserBase.__config__.schema_extra.get('example')

    response = client.post('/user/', json=payload)
    assert response.status_code == 201, '올바르지 않은 상태코드입니다'
    result = response.json()
    assert result.get('message') == 'user added', '사용자가 생성되지 않았습니다'
    assert result.get('user') == payload, '생성된 사용자 속성이 다릅니다'

    user_id = result.get('item_id')

    # 사용자 변경
    new_name = fake.name()
    response = client.put(f'/user/{user_id}', json={'name': new_name})
    assert response.status_code == 200
    result = response.json()
    assert 'name' in result.get('changes'), 'name 속성이 변경되지 않았습니다'
    assert result.get('changes')['name'] == new_name, 'name 속성이 변경되지 않았습니다'

    # 사용자 삭제
    response = client.delete(f'/user/{user_id}')
    assert response.status_code == 204, '사용자가 정상적으로 삭제되지 않았습니다'


    # 벌크 생성, 목록 조회
    users = {}

    for _ in range(10):
        response = client.post('/user/', json=create_dummy_user())
        assert response.status_code == 201
        result = response.json()
        users[result.get('item_id')] = result.get('user')

    response = client.get('/user/')
    items = response.json().get('users')
    for user in items:
        user_id = user.get('id')
        assert users.get(user_id).get('name') == user.get('name')
        assert users.get(user_id).get('age') == user.get('age')
    assert len(items) == 10
