"""Unit tests for classifier."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cli.classifier import classify, extract_cwe_refs, summarize
from cli.context_resolver import ROLE_SERVER, RoleConfig
from cli.mapping_loader import VERDICT_ALLOWED, VERDICT_REVIEW, load

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "tiny-cwe-mapping.json"
DEFAULT_VERDICTS = (VERDICT_ALLOWED, VERDICT_REVIEW)


def _role_config() -> RoleConfig:
    return RoleConfig(
        server_globs=("**/src/main/java/**", "**/api/**", "**/server/**"),
        client_globs=("**/*.tsx", "**/webapp/**"),
        default_role=ROLE_SERVER,
    )


def _issue(key: str, cwe: str, component: str, **overrides) -> dict:
    base = {
        "key": key,
        "rule": "test:rule",
        "severity": "MAJOR",
        "component": component,
        "project": "demo",
        "type": "VULNERABILITY",
        "message": "",
        "tags": [],
        "securityStandards": [cwe],
    }
    base.update(overrides)
    return base


class TestCweExtraction(unittest.TestCase):
    def test_from_security_standards(self) -> None:
        issue = {"securityStandards": ["cwe:79", "owaspTop10:a3"]}
        self.assertEqual(extract_cwe_refs(issue), ["CWE-79"])

    def test_from_tags(self) -> None:
        issue = {"tags": ["cwe-89", "sql"], "securityStandards": []}
        self.assertEqual(extract_cwe_refs(issue), ["CWE-89"])

    def test_no_duplicates(self) -> None:
        issue = {"tags": ["cwe:79"], "securityStandards": ["cwe:79"]}
        self.assertEqual(extract_cwe_refs(issue), ["CWE-79"])

    def test_no_cwe_present(self) -> None:
        issue = {"tags": ["sql"], "securityStandards": ["owaspTop10:a3"]}
        self.assertEqual(extract_cwe_refs(issue), [])


class TestClassifier(unittest.TestCase):
    def setUp(self) -> None:
        self.index = load(FIXTURE)
        self.role_config = _role_config()

    def test_single_cluster_mapping(self) -> None:
        issue = _issue("I1", "cwe:89", "demo:src/main/java/Repo.java")
        f = classify(issue, self.index, self.role_config, DEFAULT_VERDICTS)
        self.assertEqual(len(f.resolved), 1)
        self.assertEqual(f.primary_clusters[0].number, 2)
        self.assertEqual([c.tag for c in f.tag_clusters], ["tlctc-02"])

    def test_sequence_mapping_yields_two_tags(self) -> None:
        issue = _issue("I2", "cwe:829", "demo:pom.xml")
        f = classify(issue, self.index, self.role_config, DEFAULT_VERDICTS)
        self.assertEqual(f.primary_clusters[0].number, 10)
        self.assertEqual(sorted(c.tag for c in f.tag_clusters), ["tlctc-07", "tlctc-10"])

    def test_role_resolves_server_branch(self) -> None:
        issue = _issue("I3", "cwe:79", "demo:src/main/java/Renderer.java")
        f = classify(issue, self.index, self.role_config, DEFAULT_VERDICTS)
        self.assertEqual(f.primary_clusters[0].number, 2)
        self.assertEqual(sorted(c.tag for c in f.tag_clusters), ["tlctc-02", "tlctc-07"])

    def test_role_resolves_client_branch(self) -> None:
        issue = _issue("I4", "cwe:79", "demo:src/main/webapp/App.tsx")
        f = classify(issue, self.index, self.role_config, DEFAULT_VERDICTS)
        self.assertEqual(f.primary_clusters[0].number, 3)
        self.assertEqual([c.tag for c in f.tag_clusters], ["tlctc-03"])

    def test_discouraged_lands_in_low_confidence(self) -> None:
        issue = _issue("I5", "cwe:20", "demo:src/main/java/X.java")
        f = classify(issue, self.index, self.role_config, DEFAULT_VERDICTS)
        self.assertEqual(f.resolved, ())
        self.assertEqual(len(f.low_confidence), 1)
        self.assertEqual(f.low_confidence[0].entry.verdict, "Discouraged")

    def test_prohibited_silently_skipped(self) -> None:
        issue = _issue("I6", "cwe:1011", "demo:anywhere")
        f = classify(issue, self.index, self.role_config, DEFAULT_VERDICTS)
        self.assertEqual(f.resolved, ())
        self.assertEqual(f.low_confidence, ())
        self.assertEqual(f.skipped_prohibited, ("CWE-1011",))

    def test_review_verdict_included_by_default(self) -> None:
        issue = _issue("I7", "cwe:330", "demo:anywhere")
        f = classify(issue, self.index, self.role_config, DEFAULT_VERDICTS)
        self.assertEqual(len(f.resolved), 1)
        self.assertEqual(f.resolved[0].entry.verdict, "Allowed-with-Review")

    def test_review_verdict_filtered_when_strict(self) -> None:
        issue = _issue("I8", "cwe:330", "demo:anywhere")
        f = classify(issue, self.index, self.role_config, include_verdicts=(VERDICT_ALLOWED,))
        self.assertEqual(f.resolved, ())
        self.assertEqual(len(f.low_confidence), 1)

    def test_unknown_cwe_marked_unmapped(self) -> None:
        issue = _issue("I9", "cwe:99999", "demo:anywhere")
        f = classify(issue, self.index, self.role_config, DEFAULT_VERDICTS)
        self.assertEqual(f.unmapped_cwes, ("CWE-99999",))


class TestSummarize(unittest.TestCase):
    def setUp(self) -> None:
        self.index = load(FIXTURE)
        self.role_config = _role_config()

    def test_groups_by_primary_cluster(self) -> None:
        issues = [
            _issue("I1", "cwe:89", "demo:src/main/java/A.java"),
            _issue("I2", "cwe:79", "demo:src/main/java/B.java"),
            _issue("I3", "cwe:79", "demo:src/main/webapp/C.tsx"),
        ]
        findings = [classify(i, self.index, self.role_config, DEFAULT_VERDICTS) for i in issues]
        summary = summarize(findings)
        self.assertEqual(summary[2].count, 2)
        self.assertEqual(summary[3].count, 1)


if __name__ == "__main__":
    unittest.main()
