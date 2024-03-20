from datetime import datetime, timedelta
import sqlalchemy as sa
import pytest
from api.app import db
from api.models import User, Post
from tests.base_test_case import BaseTestCase


class UserModelTests(BaseTestCase):
    def test_password_hashing(self):
        u = User(username='susan', password='cat')
        assert not u.verify_password('dog')
        assert u.verify_password('cat')
        with pytest.raises(AttributeError):
            u.password

    def test_url(self):
        u = User(username='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        assert u.url == 'http://localhost:5000/api/users/' + str(u.id)

    def test_get_users(self):
        rv = self.client.post('/api/users', json={
            'username': 'john',
            'email': 'john@example.com',
            'password': 'cat',
        })

        rv = self.client.get('/api/users')
        assert rv.status_code == 200
        assert rv.json['pagination']['total'] == 2
        assert rv.json['data'][1]['username'] == 'john'
        assert rv.json['data'][1]['email'] == 'john@example.com'
        assert 'password' not in rv.json['data'][1]

    