import pytest
import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInBhc3N3b3JkX2hhc2giOiIkMmIkMTIkQS9vRVBVNU5lc3hjM3ozbXJQcTg5dTM4N3RoMy5wOTRsb2trcFd6NS5Ba0ZTWmtpSFV6SUciLCJyb2xlcyI6ImFkbWluIn0.lc0oKbSZSIqTMSgIGy9uwFG-J4tWJVf4bDGU35eic80'
}

@pytest.fixture(scope='session')
def test_login_as_admin(): #access_token
    payload = {"username": "admin", "password": "admin"}
    response = requests.post(url="http://52.221.247.92:8080/auth/login", json=payload)
    token = response.json()["access_token"]
    return token
    
def test_get_health():
    response = requests.get(url="http://52.221.247.92:8080/health")
    assert response.ok

def test_get_comment():
    payload={}
    response = requests.get(url="http://52.221.247.92:8080/comments", headers=headers, data=payload)
    print(response.text)

def test_post_comments():
    url = "http://52.221.247.92:8080/comments"
    payload = "{\"comment_text\": \"Henlo!\", \"likes\": \"100000\"}"
    response = requests.post(url, headers=headers, data=payload)
    print(response.text)

def test_put_comments():
    url = "http://52.221.247.92:8080/comments"
    payload = "{\"comment_text\": \"Henlo!\", \"likes\": \"100000\"}"
    response = requests.put(url, headers=headers, data=payload)
    print(response.text)
    
def test_delete_comments():
    url = "http://52.221.247.92:8080/comments"
    payload={}
    response = requests.delete(url, headers=headers, data=payload)
    print(response.text)
    
def test_get_users():
    payload={}
    response = requests.get(url="http://52.221.247.92:8080/users", headers=headers, data=payload)
    print(response.text)

def test_post_users():
    url = "http://52.221.247.92:8080/users"
    payload = "{\"username\": \"ainamarie\", \"password_hash\": \"asdfasdfaewrwe\", \"roles\": \"user\"}"
    response = requests.post(url, headers=headers, data=payload)
    print(response.text)

def test_get_userme():
    payload={}
    response = requests.get(url="http://52.221.247.92:8080/users/me", headers=headers, data=payload)
    print(response.text)
    
def test_delete_users():
    url = "http://52.221.247.92:8080/users"
    payload={}
    response = requests.delete(url, headers=headers, data=payload)
    print(response.text)