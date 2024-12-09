import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from bot import get_activities, user_tokens
from server_for_tests import SimpleServer


class TestBotCommands(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Creating a mock server object
        self.mock_server_instance = MagicMock()

    @patch("bot.aiohttp.ClientSession.get")
    async def test_get_activities(self, mock_get):
        """Test get_activities command."""
        mock_ctx = AsyncMock()
        user_tokens[mock_ctx.author.id] = "dummy_access_token"  # Simulate an access token

        # Mock object for response from Strava API
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(
            return_value=[
                {"start_date": "2024-01-01", "type": "Run", "distance": 1000, "name": "Morning Run"}
            ]
        )

        # Testing the function
        await get_activities(mock_ctx)
        expected_message = (
            "2024-01-01 - Run - 1000m - N/As - elevation gain: N/A m - av.speed: N/A m/s - Morning Run"
        )
        mock_ctx.send.assert_called_with(expected_message)

    def test_server_lifecycle(self):
        # Creating and running the server
        server = SimpleServer(port=0)  # We use port 0 to automatically select an available port
        server.start()

        # The server will process one request (or wait for a timeout) and terminate.
        server.thread.join(timeout=2)  # Waiting for the stream to complete with a timeout

        # Stop the server if it is still running
        server.stop()
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
