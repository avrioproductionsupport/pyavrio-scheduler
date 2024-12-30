import unittest
from unittest.mock import patch, MagicMock
from pyavrio_scheduler.scheduler import Scheduler
from pyavrio_scheduler.session import Session
from pyavrio_scheduler.state import UserState



class TestScheduler(unittest.TestCase):

    def setUp(self):
        user_state = UserState()
        user_state.access_token = "mock_access_token"
        user_state.user_id = "mock_user_id"
        session = Session("https://mock-host.com", user_state)
        self.scheduler = Scheduler(session)

    @patch("requests.post")
    def test_list_all_invalid_topic(self, mock_post):
        """Test `list_all` with an invalid topic name."""
        result = self.scheduler.list_all("invalid_topic")
        self.assertIsNone(result)
        mock_post.assert_not_called()

    @patch("requests.post")
    def test_list_all_invalid_topic(self, mock_post):
        """Test `list_all` with an invalid topic name."""
        mock_post.return_value = MagicMock()
        result = self.scheduler.list_all("invalid_topic")

        self.assertIsNone(result)
        mock_post.assert_not_called()