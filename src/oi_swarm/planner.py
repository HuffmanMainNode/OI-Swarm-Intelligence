"""Deterministic, policy-gated planning for heterogeneous OI resources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def plan_task(task: dict[str, Any], resources: list[dict[str, Any]], policy: dict[str, Any]) -> dict[str, Any]:
    """Rank declared capabilities; deny all resources unless an explicit allowlist is supplied."""
    required = set(task.get("required_capabilities", []))
    if not required or not all(isinstance(item, str) and item for item in required):
        raise ValueError("task.required_capabilities must contain non-empty strings")

    allowed_value = policy.get("allowed_resource_ids", [])
    if not isinstance(allowed_value, list) or not all(isinstance(item, str) and item for item in allowed_value):
        raise ValueError("policy.allowed_resource_ids must be an array of non-empty strings")
    allowed = set(allowed_value)
    approval_required = bool(policy.get("human_approval_required", True))
    eligible: list[tuple[int, str]] = []
    rejected: list[dict[str, str]] = []

    for resource in resources:
        if not isinstance(resource, dict):
            rejected.append({"resource_id": "<invalid>", "reason": "resource must be an object"})
            continue
        resource_id = resource.get("id")
        if not isinstance(resource_id, str) or not resource_id:
            rejected.append({"resource_id": "<missing>", "reason": "missing resource id"})
            continue
        if resource_id not in allowed:
            rejected.append({"resource_id": resource_id, "reason": "not allowlisted by policy"})
            continue
        capabilities = {
            item.get("id") for item in resource.get("capabilities", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        score = len(required & capabilities)
        if score == 0:
            rejected.append({"resource_id": resource_id, "reason": "no required capability match"})
            continue
        eligible.append((score, resource_id))

    eligible.sort(key=lambda item: (-item[0], item[1]))
    selected = [{"resource_id": rid, "matched_capabilities": score} for score, rid in eligible]
    return {
        "task_id": task.get("id", "unnamed-task"),
        "status": "approval_required" if approval_required and selected else ("planned" if selected else "no_candidate"),
        "human_approval_required": approval_required,
        "assignments": selected,
        "rejected": sorted(rejected, key=lambda item: item["resource_id"]),
        "execution_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a policy-gated OI swarm assignment plan.")
    parser.add_argument("input", type=Path, help="JSON file containing task, resources, and policy")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = plan_task(payload["task"], payload["resources"], payload.get("policy", {}))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
