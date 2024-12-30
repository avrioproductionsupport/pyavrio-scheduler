"""
Authentication module for PyAvrio Scheduler
"""
import requests
import base64
import json
from .endpoints import SchedulerEndpoints
from typing import Dict
from .state import UserState
from .session import Session

class AuthenticationError(Exception):
    """Custom exception for authentication errors"""
    pass

class Authentication:
    def __init__(self):
        """
        Initialize the Authentication class with default values.
        """
        self.user_state = UserState()  # Store user authentication state
        self.token_endpoint = SchedulerEndpoints.TOKEN_ENDPOINT # Endpoint for obtaining a token
        self.user_details_endpoint = SchedulerEndpoints.USER_DETAILS  # Endpoint for fetching user details

    def authenticate(self, auth_params: Dict) -> Session:
        """
        Authenticate the user using either the password or access token method.

        Args:
            auth_params (dict): Dictionary containing authentication parameters.
                Required keys based on method:
                - `method`: 'password' or 'access_token'.
                - For the 'password' method:
                    - `username`: str
                    - `password`: str
                - For the 'access_token' method:
                    - `access_token`: str
                    
        Returns:
            Session: A session object containing the user's authentication state and host information.
        
        Raises:
            AuthenticationError: If required parameters are missing, invalid, or if authentication fails.
        """
        # Extract host from authentication parameters
        host = auth_params.get('host')
        if not host:
            raise AuthenticationError("Host must be specified.")

        # Determine authentication method
        method = auth_params.get('method')
        if not method:
            raise AuthenticationError("Authentication method must be specified.")
        
        if method == 'password':
            # Extract username and password for password-based authentication
            username = auth_params.get('username')
            password = auth_params.get('password')
            
            if not username or not password:
                raise AuthenticationError("Username and password are required for password authentication.")
                
            # Prepare payload and headers for API request
            payload = {"email": username, "password": password}
            headers = {"Content-Type": "application/json"}
            
            try:
                # Send API request to obtain the access token
                response = requests.post(host + self.token_endpoint, json=payload, headers=headers)
                response.raise_for_status()  # Raise an error if the response status is not 200
                data = response.json()
                
                # Update user state with obtained access token
                self.user_state.username = username
                self.user_state.access_token = data.get("accessToken")
            except requests.exceptions.RequestException as e:
                # Handle request failures
                raise AuthenticationError(f"Failed to obtain access token: {str(e)}")
        
        elif method == 'access_token':
            # Extract access token for token-based authentication
            access_token = auth_params.get('access_token')
            if not access_token:
                raise AuthenticationError("Access token is required for token authentication.")
                
            # Update user state with provided access token
            self.user_state.access_token = access_token
        else:
            # Raise an error for unsupported authentication methods
            raise AuthenticationError(f"Unsupported authentication method: {method}")
        
        # Extract user email from the JWT token for additional validation
        email = self.extract_email_from_jwt(self.user_state.access_token)
        self.user_state.email = email

        # Fetch and update user details using the user details endpoint
        self.update_user_details(host, self.user_state.access_token)

        # Return a session object containing the authenticated user's state
        return Session(host, self.user_state)
    
    def update_user_details(self, host,  access_token: str):
        """
        Get user details using the access token and user email.

        Args:
            access_token: The access token to use for authentication

        Returns:
            Dictionary containing user details if successful, None otherwise
        """
        try:
            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
            payload = {"emailId": self.user_state.email}
            # Make a request to the user details endpoint
            response = requests.post(host+self.user_details_endpoint, json=payload, headers=headers)
            response.raise_for_status()
           # Extract JSON data
            response_data = response.json()

            # Safely extract 'userId' from the response dictionary
            user_id = response_data.get('userId')

            # Assign it to the user_state attribute
            self.user_state.user_id = user_id

        except requests.exceptions.RequestException:
            return None

    @staticmethod
    def extract_email_from_jwt(jwt_token):
        """
        Extracts the 'email' field from the payload of a JWT.

        Args:
            jwt_token (str): The JWT token.

        Returns:
            str: The email address if present in the payload.
        """
        try:
            # Split the JWT into its components
            parts = jwt_token.split('.')
            if len(parts) != 3:
                raise ValueError("Invalid JWT token format.")
            
            # The payload is the second part
            payload_base64 = parts[1]
            
            # Add padding if necessary
            payload_base64 += '=' * ((4 - len(payload_base64) % 4) % 4)
            
            # Decode the Base64 payload
            payload_json = base64.urlsafe_b64decode(payload_base64).decode('utf-8')
            
            # Parse the JSON payload
            payload_data = json.loads(payload_json)
            
            # Extract the email field
            email = payload_data.get('email')
            if not email:
                raise KeyError("Email key not found in the JWT payload.")
            
            return email
        except Exception as e:
            raise ValueError(f"Error extracting email: {e}")