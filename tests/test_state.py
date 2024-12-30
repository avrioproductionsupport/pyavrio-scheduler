import unittest
from pyavrio_scheduler.state import UserState


class TestUserState(unittest.TestCase):
    def setUp(self):
        """
        Ensure the singleton instance is reset before each test.
        """
        UserState._instance = None  # Reset the singleton instance for clean tests

    def test_singleton_behavior(self):
        """
        Test that the UserState class follows the Singleton pattern.
        """
        user_state_1 = UserState()
        user_state_2 = UserState()
        self.assertIs(user_state_1, user_state_2, "UserState does not follow Singleton pattern")

    def test_access_token_property(self):
        """
        Test the `access_token` property for getting and setting.
        """
        user_state = UserState()
        user_state.access_token = "mock_access_token"
        self.assertEqual(user_state.access_token, "mock_access_token")

    def test_username_property(self):
        """
        Test the `username` property for getting and setting.
        """
        user_state = UserState()
        user_state.username = "mock_user"
        self.assertEqual(user_state.username, "mock_user")

    def test_email_property(self):
        """
        Test the `email` property for getting and setting.
        """
        user_state = UserState()
        user_state.email = "mock_email@example.com"
        self.assertEqual(user_state.email, "mock_email@example.com")

    def test_user_id_property(self):
        """
        Test the `user_id` property for getting and setting.
        """
        user_state = UserState()
        user_state.user_id = 12345
        self.assertEqual(user_state.user_id, 12345)

    def test_clear_method(self):
        """
        Test the `clear` method to ensure it resets all attributes.
        """
        user_state = UserState()
        user_state.access_token = "mock_access_token"
        user_state.username = "mock_user"
        user_state.email = "mock_email@example.com"
        user_state.user_id = 12345

        user_state.clear()

        self.assertIsNone(user_state.access_token)
        self.assertIsNone(user_state.username)
        self.assertIsNone(user_state.email)
        self.assertIsNone(user_state.user_id)


if __name__ == "__main__":
    unittest.main()
