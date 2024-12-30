from .state import UserState

class Session:
    """
    The Session class stores the user state and host information for the current session.

    Attributes:
        _user_state (UserState): The state of the current user, holding information such as access tokens and user details.
        _host (str): The host URL or server address for the session.
    """
    
    def __init__(self, host: str, user_state: UserState):
        """
        Initialize the Session object with host and user state information.

        Args:
            host (str): The host URL or address for the session.
            user_state (UserState): An instance of the UserState class holding user-specific data.
        """
        self._user_state = user_state  # Store the user state instance in the session
        self._host = host  # Store the host URL for the session

    def get_host(self) -> str:
        """
        Get the host URL for the current session.

        Returns:
            str: The host URL of the session.
        """
        return self._host 

    @property
    def user_state(self) -> UserState:
        """
        Retrieve the current user's state information.

        Returns:
            UserState: The user state object that holds the user's information and session data.
        """
        return self._user_state 
    
    def get_scheduler(self):
        """
        Retrieve the scheduler instance associated with the current session.

        This method imports the Scheduler class and returns an instance of it, passing the current session as an argument.

        Returns:
            Scheduler: An instance of the Scheduler class associated with this session.
        """
        from .scheduler import Scheduler  
        return Scheduler(self)  
