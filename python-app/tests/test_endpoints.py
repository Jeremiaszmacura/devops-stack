import unittest

from fastapi.testclient import TestClient

from main import app


class TestEndpoints(unittest.TestCase):
    """Tests for the FastAPI routes defined in endpoints.py."""

    def setUp(self):
        self.client = TestClient(app)

    def test_root_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_health_returns_200(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_error_returns_500(self):
        response = self.client.get("/error")
        self.assertEqual(response.status_code, 500)

    def test_redirect_returns_302(self):
        response = self.client.get("/redirect", follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_metrics_returns_200(self):
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
