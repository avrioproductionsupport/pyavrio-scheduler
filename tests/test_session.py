import unittest
from unittest.mock import MagicMock, patch
from pyavrio_scheduler.session import Session
from pyavrio_scheduler.state import UserState


class TestSession(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by creating mock objects for UserState and initializing Session.
        """
        self.mock_user_state = MagicMock(spec=UserState)
        self.mock_host = "https://mock-host.com"
        self.session = Session(host=self.mock_host, user_state=self.mock_user_state)

    def test_get_host(self):
        """
        Test the `get_host` method to ensure it returns the correct host URL.
        """
        self.assertEqual(self.session.get_host(), self.mock_host)

    def test_user_state_property(self):
        """
        Test the `user_state` property to ensure it returns the correct UserState instance.
        """
        self.assertEqual(self.session.user_state, self.mock_user_state)

    @patch("pyavrio_scheduler.scheduler.Scheduler")
    def test_get_scheduler(self, mock_scheduler_class):
        """
        Test the `get_scheduler` method to ensure it returns an instance of the Scheduler class.
        """
        mock_scheduler_instance = MagicMock()
        mock_scheduler_class.return_value = mock_scheduler_instance

        scheduler_instance = self.session.get_scheduler()

        # Assert that the Scheduler class was called with the session instance
        mock_scheduler_class.assert_called_once_with(self.session)

        # Assert that the returned instance is correct
        self.assertEqual(scheduler_instance, mock_scheduler_instance)


if __name__ == "__main__":
    unittest.main()
