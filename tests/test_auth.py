import pytest
import os
import requests_mock
from dotenv import load_dotenv
from pyavrio_scheduler.auth import Authentication, AuthenticationError
from pyavrio_scheduler.endpoints import SchedulerEndpoints

load_dotenv()

HOST = os.getenv("HOST")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
EMAIL = os.getenv("EMAIL")
USER_ID = int(os.getenv("USER_ID"))

@pytest.fixture
def auth_instance():
    return Authentication()

def test_authenticate_password_method(auth_instance):
    with requests_mock.Mocker() as m:
        # Mock the token endpoint response
        token_endpoint = HOST + SchedulerEndpoints.TOKEN_ENDPOINT
        m.post(token_endpoint, json={"accessToken": ACCESS_TOKEN})
        
        # Mock the user details endpoint response
        user_details_endpoint = HOST + SchedulerEndpoints.USER_DETAILS
        m.post(user_details_endpoint, json={"userId": USER_ID})
        
        # Define authentication parameters
        auth_params = {
            "host": HOST,
            "method": "password",
            "username": USERNAME,
            "password": PASSWORD
        }
        
        # Authenticate
        session = auth_instance.authenticate(auth_params)
        
        # Assertions
        assert session.user_state.access_token == ACCESS_TOKEN
        assert session.user_state.email == EMAIL
        assert session.user_state.user_id == USER_ID
        assert session._host == HOST

def test_authenticate_access_token_method(auth_instance):
    with requests_mock.Mocker() as m:
        # Mock the user details endpoint response
        user_details_endpoint = HOST + SchedulerEndpoints.USER_DETAILS
        m.post(user_details_endpoint, json={"userId": USER_ID})
        
        # Define authentication parameters
        auth_params = {
            "host": HOST,
            "method": "access_token",
            "access_token": ACCESS_TOKEN
        }
        
        # Authenticate
        session = auth_instance.authenticate(auth_params)
        
        # Assertions
        assert session.user_state.access_token == ACCESS_TOKEN
        assert session.user_state.email == EMAIL
        assert session.user_state.user_id == USER_ID
        assert session._host == HOST

def test_authenticate_missing_host(auth_instance):
    auth_params = {
        "method": "password",
        "username": USERNAME,
        "password": PASSWORD
    }
    with pytest.raises(AuthenticationError, match="Host must be specified."):
        auth_instance.authenticate(auth_params)

def test_authenticate_missing_method(auth_instance):
    auth_params = {
        "host": HOST,
        "username": USERNAME,
        "password": PASSWORD
    }
    with pytest.raises(AuthenticationError, match="Authentication method must be specified."):
        auth_instance.authenticate(auth_params)

def test_authenticate_invalid_method(auth_instance):
    auth_params = {
        "host": HOST,
        "method": "invalid_method",
        "username": USERNAME,
        "password": PASSWORD
    }
    with pytest.raises(AuthenticationError, match="Unsupported authentication method: invalid_method"):
        auth_instance.authenticate(auth_params)

def test_extract_email_from_jwt(auth_instance):
    jwt_token = ACCESS_TOKEN  
    email = auth_instance.extract_email_from_jwt(jwt_token)
    assert email == EMAIL  

def test_update_user_details(auth_instance):
    with requests_mock.Mocker() as m:
        # Mock the user details endpoint response
        user_details_endpoint = HOST + SchedulerEndpoints.USER_DETAILS
        m.post(user_details_endpoint, json={"userId": USER_ID})
        
        auth_instance.user_state.email = EMAIL
        auth_instance.update_user_details(HOST, ACCESS_TOKEN)
        
        assert auth_instance.user_state.user_id == USER_ID
