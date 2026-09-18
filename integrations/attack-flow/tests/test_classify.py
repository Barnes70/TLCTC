import unittest

from cli.classify import classify_flow, derive_path, render_notation, summarize, transitions
from cli.flow import Action, Condition, Edge, Flow, Operator
from cli.mapping import load_attack_mapping

M = load_attack_mapping()


def linear(*techs, starts=None, ts=None):
    f = Flow(name="t", scope="incident")
    ids = []
    for i, t in enumerate(techs):
        aid = f"a{i}"
        f.actions[aid] = Action(id=aid, name=f"A{i}", technique_id=t, execution_start=(ts[i] if ts else None))
        ids.append(aid)
    for a, b in zip(ids, ids[1:]):
        f.edges.append(Edge(a, b))
    if starts:
        f.start_ids = starts
    return f


class DerivePathTests(unittest.TestCase):
    def test_linear_resolved(self):
        f = linear("T1566.001", "T1204.002", "T1078")  # phishing → user execution → valid accounts
        r = classify_flow(f, M)
        self.assertEqual(r["action_status"].get("resolved", 0) + r["action_status"].get("rule_dependent", 0), 3)
        self.assertTrue(r["notation_compressed"].startswith("#9"))
        self.assertEqual(r["entry_cluster"], "#9")
        self.assertTrue(r["entry_is_first_step"])

    def test_preparation_excluded(self):
        f = linear("T1583.002", "T1566.001")  # acquire domain (N/A) → phishing
        r = classify_flow(f, M)
        self.assertEqual(r["action_status"]["preparation"], 1)
        self.assertEqual(r["path"]["raw"][0]["cluster"], "#9")
        self.assertEqual(r["steps_raw"], len(r["path"]["raw"]))

    def test_sequence_mapping_expands(self):
        f = linear("T1195.002")
        r = classify_flow(f, M)
        self.assertEqual([s["cluster"] for s in r["path"]["raw"]], ["#10", "#7"])
        self.assertTrue(r["path"]["raw"][1]["implied"])
        self.assertEqual(r["notation_compressed"], "#10 → #7")

    def test_rule_dependent_becomes_unresolved(self):
        f = linear("T1190")  # exploit public-facing application: #2 | ... depending on mapping
        r = classify_flow(f, M)
        s = r["path"]["compressed"][0]
        if r["actions"][0]["status"] == "rule_dependent":
            self.assertEqual(s["kind"], "unresolved")
            self.assertTrue(s["candidates"])
            self.assertEqual(r["notation_compressed"], "?")
        else:
            self.assertEqual(s["kind"], "classified")

    def test_no_technique_is_unresolved(self):
        f = linear(None, "T1078")
        r = classify_flow(f, M)
        self.assertEqual(r["action_status"]["no_technique"], 1)
        self.assertEqual(r["path"]["raw"][0]["kind"], "unresolved")
        self.assertEqual(r["path"]["raw"][0]["reason"], "no_technique")
        self.assertFalse(r["entry_is_first_step"])
        self.assertEqual(r["entry_cluster"], "#4")

    def test_compression(self):
        f = linear("T1082", "T1083", "T1057")  # three discovery techniques
        r = classify_flow(f, M)
        clusters = {s["cluster"] for s in r["path"]["raw"]}
        if clusters == {"#1"}:
            self.assertEqual(r["steps_compressed"], 1)
            self.assertEqual(r["path"]["compressed"][0]["count"], 3)

    def test_condition_true_branch_followed_false_noted(self):
        f = Flow(name="c")
        f.actions["a"] = Action(id="a", name="a", technique_id="T1566.001")
        f.conditions["c"] = Condition(id="c", description="user clicked?")
        f.actions["b"] = Action(id="b", name="b", technique_id="T1204.002")
        f.actions["d"] = Action(id="d", name="d", technique_id="T1598")
        f.edges += [Edge("a", "c"), Edge("c", "b", "true"), Edge("c", "d", "false")]
        r = classify_flow(f, M)
        self.assertTrue(any("false branch" in n for n in r["path"]["notes"]))
        self.assertEqual(r["counts"]["conditions"], 1)

    def test_and_operator_marks_parallel(self):
        f = Flow(name="p")
        f.actions["a"] = Action(id="a", name="a", technique_id="T1566.001")
        f.operators["op"] = Operator(id="op", operator="AND")
        f.actions["b"] = Action(id="b", name="b", technique_id="T1204.002")
        f.actions["c"] = Action(id="c", name="c", technique_id="T1078")
        f.edges += [Edge("a", "op"), Edge("op", "b"), Edge("op", "c")]
        r = classify_flow(f, M)
        hinted = {s["action_id"] for s in r["path"]["raw"] if s.get("parallel_hint")}
        self.assertEqual(hinted, {"b", "c"})

    def test_delta_t_from_timestamps(self):
        f = linear("T1566.001", "T1204.002", ts=["2024-01-01T00:00:00Z", "2024-01-01T02:00:00Z"])
        r = classify_flow(f, M)
        self.assertEqual([s.get("delta_t_to_next") for s in r["path"]["raw"] if s.get("delta_t_to_next")], ["2h"])
        self.assertIn("Δt=2h", r["notation_raw"])
        self.assertEqual(r["delta_t_edges"], 1)

    def test_summary_shapes(self):
        rs = [classify_flow(linear("T1566.001", "T1204.002", "T1078"), M), classify_flow(linear("T1583.002"), M)]
        s = summarize(rs)
        self.assertEqual(s["flows"], 2)
        self.assertEqual(s["profile"]["actions"]["n"], 4)
        self.assertEqual(sum(v["n"] for v in s["action_status"].values()), 4)
        self.assertEqual(len(s["per_flow"]), 2)
        self.assertIn("#9", s["frequency"])
        self.assertIsInstance(transitions(rs[0]), list)
        self.assertEqual(render_notation([]), "")


if __name__ == "__main__":
    unittest.main()
