"""Unit tests for context_resolver."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cli.context_resolver import ROLE_CLIENT, ROLE_SERVER, RoleConfig, resolve
from cli.path_parser import Cluster, Sequence, parse


def _config() -> RoleConfig:
    return RoleConfig(
        server_globs=("**/src/main/java/**", "**/api/**"),
        client_globs=("**/*.tsx", "**/webapp/**"),
        default_role=ROLE_SERVER,
    )


class TestContextResolver(unittest.TestCase):
    def test_non_alternation_passes_through(self) -> None:
        ast = parse("#2")
        result = resolve("anywhere", ast, _config())
        self.assertEqual(result.resolved, ast)
        self.assertIsNone(result.role)

    def test_alternation_resolves_to_server(self) -> None:
        ast = parse("#2 | #3")
        result = resolve("src/main/java/X.java", ast, _config())
        self.assertEqual(result.resolved, Cluster(2))
        self.assertEqual(result.role, ROLE_SERVER)

    def test_alternation_resolves_to_client(self) -> None:
        ast = parse("#2 | #3")
        result = resolve("ui/App.tsx", ast, _config())
        self.assertEqual(result.resolved, Cluster(3))
        self.assertEqual(result.role, ROLE_CLIENT)

    def test_alternation_with_sequences(self) -> None:
        ast = parse("#2 → #7 | #3 → #7")
        result = resolve("src/main/java/X.java", ast, _config())
        self.assertEqual(result.resolved, Sequence((Cluster(2), Cluster(7))))
        self.assertEqual(result.role, ROLE_SERVER)

    def test_sonar_component_prefix_stripped(self) -> None:
        ast = parse("#2 → #7 | #3")
        result = resolve("project-key:src/main/java/X.java", ast, _config())
        self.assertEqual(result.role, ROLE_SERVER)

    def test_client_glob_more_specific_than_server(self) -> None:
        ast = parse("#2 | #3")
        # Path matches both: '**/src/main/java/**' (server, in TOML)
        # and '**/*.tsx' (client). Client should win.
        result = resolve("src/main/java/page.tsx", ast, _config())
        self.assertEqual(result.role, ROLE_CLIENT)

    def test_no_match_falls_back_to_default_role(self) -> None:
        ast = parse("#2 | #3")
        result = resolve("unknown/path.ext", ast, _config())
        self.assertEqual(result.role, ROLE_SERVER)
        self.assertIsNone(result.matched_glob)

    def test_alternation_without_server_or_client_branches(self) -> None:
        ast = parse("#1 | #4")
        result = resolve("anywhere", ast, _config())
        self.assertEqual(result.resolved, Cluster(1))
        self.assertIsNone(result.role)


if __name__ == "__main__":
    unittest.main()
