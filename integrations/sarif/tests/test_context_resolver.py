import unittest

from cli.context_resolver import resolve_role


class TestContextResolver(unittest.TestCase):
    def setUp(self):
        self.globs = {"server": ["**/api/**", "**/server/**"], "client": ["**/ui/**", "**/*.html"]}

    def test_server_path_picks_2(self):
        cluster, reason = resolve_role("src/api/users.py", self.globs)
        self.assertEqual(cluster, "#2")
        self.assertIn("server", reason)

    def test_client_path_picks_3(self):
        cluster, reason = resolve_role("web/ui/login.html", self.globs)
        self.assertEqual(cluster, "#3")

    def test_no_match_returns_none(self):
        cluster, reason = resolve_role("misc/readme.txt", self.globs)
        self.assertIsNone(cluster)
        self.assertIn("unresolved", reason)


if __name__ == "__main__":
    unittest.main()
