"""
Global user state management for PyAvrio Scheduler

This class manages the global state of the user within the PyAvrio Scheduler application.
It follows the Singleton pattern to ensure there is only one instance of the user state.
The state includes information like access token, username, email, and user ID.
"""

class UserState:
    """
    A Singleton class to manage the user state across the application.

    Attributes:
        _instance (UserState): The single instance of the UserState class.
        _access_token (str): The access token for authentication.
        _username (str): The username of the currently authenticated user.
        _email (str): The email address of the currently authenticated user.
        _user_id (int): The unique ID of the currently authenticated user.
    """
    
    _instance = None  # Holds the instance of the UserState class (for Singleton pattern)
    _access_token = None  # Stores the access token
    _username = None  # Stores the username
    _email = None  # Stores the user's email address
    _user_id = None  # Stores the user's ID

    def __new__(cls):
        """
        Ensure that only one instance of the UserState class is created.

        The method implements the Singleton pattern. If the instance already exists,
        it returns the existing instance; otherwise, it creates a new one.

        Returns:
            UserState: The single instance of the UserState class.
        """
        if cls._instance is None:
            # If instance does not exist, create a new one
            cls._instance = super(UserState, cls).__new__(cls)
        return cls._instance

    @property
    def access_token(self):
        """Get the current access token."""
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        """Set the access token."""
        self._access_token = value

    @property
    def username(self):
        """Get the current username."""
        return self._username

    @username.setter
    def username(self, value):
        """Set the username."""
        self._username = value

    @property
    def email(self):
        """Get the current email address."""
        return self._email

    @email.setter
    def email(self, value):
        """Set the email address."""
        self._email = value

    @property
    def user_id(self):
        """Get the current user ID."""
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        """Set the user ID."""
        self._user_id = value

    def clear(self):
        """Clear all stored state data."""
        self._access_token = None
        self._username = None
        self._email = None
        self._user_id = None
