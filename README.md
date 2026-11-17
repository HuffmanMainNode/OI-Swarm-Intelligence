# OI Swarm Intelligence

**A local-first reference implementation for coordinating independent intelligence resources.**

This repository implements the coordination layer of an Open Intelligence (OI) swarm. It is deliberately narrower than a general-purpose autonomous-agent platform: it ranks declared capabilities against a task, applies an explicit permission policy, and produces a deterministic assignment plan. It does not execute agents, grant permissions, or claim that a selected resource is trustworthy.

## What is implemented

- Capability-based candidate matching with deterministic ranking.
- Mission policy gates for allowed resource IDs and required human approval.
- Explicit rejection reasons for unavailable or unauthorized candidates.
- A JSON task/resource example and a small Python library.
- Unit tests for ranking, policy denial, and empty candidate sets.

## Install and run

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
oi-swarm-plan examples/mission.json
```

No network access, hosted service, API key, or third-party runtime dependency is required.

## Coordination model

1. A caller supplies a task with required capability identifiers.
2. The planner scores declared resources by capability coverage.
3. Policy filters candidates before assignment.
4. The result records selected IDs and rejected candidates with reasons.
5. A human or separately authorized runtime decides whether to invoke anything.

The planner uses declarations, not empirical performance. Capability claims must be independently tested. This project does not provide distributed consensus, secure transport, agent execution, or a trust oracle.

## Safety boundary

Resource discovery is not authorization. A resource manifest never grants tool, filesystem, network, or secret access. Keep execution in a separately sandboxed runtime with least privilege. See [SECURITY.md](SECURITY.md).

## Relationship to the OI ecosystem

The shared resource vocabulary and manifest contract are maintained by [Open-Intelligence-Fabric](https://github.com/HuffmanMainNode/Open-Intelligence-Fabric). This repository owns swarm task planning and policy-gated resource assignment.

## Project status

Version 0.1.0 is an initial reference implementation. Distributed transport, durable state, fault-tolerant consensus, and measured scheduling remain future work. No performance claims are implied.
