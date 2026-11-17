import unittest

from oi_swarm.planner import plan_task


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.task = {"id": "t1", "required_capabilities": ["a", "b"]}
        self.resources = [
            {"id": "both", "capabilities": [{"id": "a"}, {"id": "b"}]},
            {"id": "one", "capabilities": [{"id": "a"}]},
            {"id": "none", "capabilities": [{"id": "z"}]},
        ]

    def test_ranks_by_coverage_then_id(self):
        policy = {"allowed_resource_ids": ["both", "one", "none"], "human_approval_required": False}
        result = plan_task(self.task, self.resources, policy)
        self.assertEqual([x["resource_id"] for x in result["assignments"]], ["both", "one"])
        self.assertEqual(result["status"], "planned")

    def test_policy_allowlist_is_enforced(self):
        result = plan_task(self.task, self.resources, {"allowed_resource_ids": ["one"]})
        self.assertEqual([x["resource_id"] for x in result["assignments"]], ["one"])
        self.assertIn("not allowlisted by policy", [x["reason"] for x in result["rejected"]])

    def test_missing_allowlist_denies_all(self):
        result = plan_task(self.task, self.resources, {})
        self.assertEqual(result["assignments"], [])
        self.assertEqual(result["status"], "no_candidate")

    def test_empty_requirements_rejected(self):
        with self.assertRaises(ValueError):
            plan_task({"required_capabilities": []}, self.resources, {})

    def test_plan_never_executes(self):
        result = plan_task(self.task, self.resources, {"allowed_resource_ids": ["both"]})
        self.assertFalse(result["execution_performed"])
        self.assertTrue(result["human_approval_required"])


if __name__ == "__main__":
    unittest.main()
