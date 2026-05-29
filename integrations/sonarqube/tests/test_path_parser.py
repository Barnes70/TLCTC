"""Unit tests for path_parser."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cli.path_parser import (
    Alternation,
    Cluster,
    PathParseError,
    Sequence,
    Unmapped,
    all_clusters,
    parse,
    primary_cluster,
)


class TestPathParser(unittest.TestCase):
    def test_single_cluster(self) -> None:
        self.assertEqual(parse("#2"), Cluster(2))
        self.assertEqual(parse("#10"), Cluster(10))

    def test_sequence_unicode_arrow(self) -> None:
        node = parse("#2 → #7")
        self.assertEqual(node, Sequence((Cluster(2), Cluster(7))))

    def test_sequence_ascii_arrow(self) -> None:
        node = parse("#2 -> #7")
        self.assertEqual(node, Sequence((Cluster(2), Cluster(7))))

    def test_alternation_two_clusters(self) -> None:
        node = parse("#2 | #3")
        self.assertEqual(node, Alternation((Cluster(2), Cluster(3))))

    def test_alternation_with_sequences(self) -> None:
        node = parse("#2 → #7 | #3 → #7")
        self.assertEqual(node, Alternation((
            Sequence((Cluster(2), Cluster(7))),
            Sequence((Cluster(3), Cluster(7))),
        )))

    def test_mixed_alternation(self) -> None:
        node = parse("#2 → #7 | #3")
        self.assertEqual(node, Alternation((
            Sequence((Cluster(2), Cluster(7))),
            Cluster(3),
        )))

    def test_unmapped(self) -> None:
        self.assertIsInstance(parse("N/A"), Unmapped)

    def test_cluster_tag_format(self) -> None:
        self.assertEqual(Cluster(2).tag, "tlctc-02")
        self.assertEqual(Cluster(10).tag, "tlctc-10")

    def test_cluster_out_of_range(self) -> None:
        with self.assertRaises(PathParseError):
            parse("#11")
        with self.assertRaises(PathParseError):
            parse("#0")

    def test_missing_hash(self) -> None:
        with self.assertRaises(PathParseError):
            parse("2 → #7")

    def test_empty_branch(self) -> None:
        with self.assertRaises(PathParseError):
            parse("#2 | ")

    def test_empty_input(self) -> None:
        with self.assertRaises(PathParseError):
            parse("")

    def test_all_clusters_deduped(self) -> None:
        node = parse("#2 → #7 | #3 → #7")
        clusters = all_clusters(node)
        self.assertEqual([c.number for c in clusters], [2, 7, 3])

    def test_primary_cluster_first_branch_first_step(self) -> None:
        node = parse("#2 → #7 | #3")
        self.assertEqual(primary_cluster(node), Cluster(2))

    def test_primary_cluster_of_unmapped(self) -> None:
        self.assertIsNone(primary_cluster(parse("N/A")))


if __name__ == "__main__":
    unittest.main()
