# Security Policy

This project plans assignments; it does not execute resources or provide a security boundary.

- Treat resource manifests and capability claims as untrusted input.
- Do not pass secrets or unrestricted tool permissions to a planner.
- Enforce authorization again at the execution boundary.
- Run agents in isolated processes or containers with least privilege.
- Do not treat a high capability score as a trust or safety rating.

Report vulnerabilities privately to the repository maintainers before public disclosure. Include affected revision, reproduction steps, and impact. Do not include live credentials or personal data in reports.
