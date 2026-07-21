import unittest
from unittest.mock import MagicMock, patch


class FetchBacklinkAuditTests(unittest.TestCase):
    @patch("backlinks.rankparse_client.RankParseClient")
    def test_merges_backlinks_and_domain_authority(self, mock_client_cls):
        from backlinks.rankparse_client import fetch_backlink_audit

        mock_client = MagicMock()
        mock_client.backlinks.return_value = {"data": [{"from": "a.com"}], "total": 1}
        mock_client.domain_authority.return_value = {"data": {"domain": "example.com", "score": 42}}
        mock_client_cls.return_value.__enter__.return_value = mock_client

        result = fetch_backlink_audit("example.com", "rp_test")

        mock_client.backlinks.assert_called_once_with("example.com")
        mock_client.domain_authority.assert_called_once_with("example.com")
        self.assertEqual(result["backlinks"]["total"], 1)
        self.assertEqual(result["domain_authority"]["data"]["score"], 42)

    @patch("backlinks.rankparse_client.RankParseClient")
    def test_propagates_rankparse_errors(self, mock_client_cls):
        from backlinks.rankparse_client import fetch_backlink_audit
        from rankparse.errors import AuthError

        mock_client = MagicMock()
        mock_client.backlinks.side_effect = AuthError("Invalid API key", code="auth_error")
        mock_client_cls.return_value.__enter__.return_value = mock_client

        with self.assertRaises(AuthError):
            fetch_backlink_audit("example.com", "rp_bad")


if __name__ == "__main__":
    unittest.main()
