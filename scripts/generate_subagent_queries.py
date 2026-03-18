from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"


MODES = [
    {
        "id": "audit",
        "title": "Audit",
        "verb": "audit",
        "difficulty": "medium",
        "apply_scope": "Apply only low-risk fixes directly; report larger issues rather than forcing a broad rewrite.",
        "expected_output": [
            "Top findings or opportunities ranked by impact.",
            "Low-risk improvements applied directly where they materially help.",
            "Residual risks, unknowns, and follow-up actions."
        ]
    },
    {
        "id": "implement",
        "title": "Implement",
        "verb": "implement",
        "difficulty": "high",
        "apply_scope": "Implement the smallest coherent improvement that materially advances the target area.",
        "expected_output": [
            "A scoped implementation plan with bounded ownership across subagents.",
            "Direct code or doc changes that complete the smallest useful version of the work.",
            "Validation performed plus any follow-up needed for full rollout."
        ]
    },
    {
        "id": "fix",
        "title": "Fix",
        "verb": "fix",
        "difficulty": "medium",
        "apply_scope": "Prioritize reproducible defects, patch the highest-leverage issues, and avoid unrelated cleanup.",
        "expected_output": [
            "Most likely defect sources with evidence.",
            "Concrete fixes applied directly with supporting validation.",
            "Remaining edge cases or failure paths still needing attention."
        ]
    },
    {
        "id": "refactor",
        "title": "Refactor",
        "verb": "refactor",
        "difficulty": "high",
        "apply_scope": "Preserve behavior while reducing complexity, duplication, or coupling.",
        "expected_output": [
            "Refactor targets ranked by readability and maintenance payoff.",
            "Behavior-preserving structural changes kept reviewable and scoped.",
            "Coverage or regression checks that protect the refactor."
        ]
    },
    {
        "id": "harden",
        "title": "Harden",
        "verb": "harden",
        "difficulty": "high",
        "apply_scope": "Prioritize resilience, safety, and edge-case handling without bloating the design.",
        "expected_output": [
            "Key safety or resilience gaps with severity-oriented reasoning.",
            "Defensive improvements applied directly where safe.",
            "Residual risk and any remaining approval-worthy changes."
        ]
    },
    {
        "id": "optimize",
        "title": "Optimize",
        "verb": "optimize",
        "difficulty": "high",
        "apply_scope": "Target measurable latency, throughput, or clarity wins rather than speculative micro-optimization.",
        "expected_output": [
            "Likely bottlenecks or waste ranked by impact.",
            "Small, testable optimizations applied directly.",
            "What still requires profiling, benchmarking, or production verification."
        ]
    },
    {
        "id": "migrate",
        "title": "Migrate",
        "verb": "migrate",
        "difficulty": "high",
        "apply_scope": "Preserve compatibility where possible and call out irreversible or rollout-sensitive changes.",
        "expected_output": [
            "Migration plan with dependencies, ordering, and compatibility concerns.",
            "Safe migration steps applied directly where feasible.",
            "Remaining rollout, cleanup, or cutover steps."
        ]
    },
    {
        "id": "review",
        "title": "Review",
        "verb": "review",
        "difficulty": "medium",
        "apply_scope": "Keep the focus on findings, risks, regressions, and missing coverage rather than broad improvement work.",
        "expected_output": [
            "Top findings ranked by severity and confidence.",
            "Evidence for each finding mapped to concrete code or docs.",
            "Minimal recommended fixes or mitigations."
        ]
    },
    {
        "id": "validate",
        "title": "Validate",
        "verb": "validate",
        "difficulty": "medium",
        "apply_scope": "Verify that the target area is internally consistent and add missing checks only when they raise confidence.",
        "expected_output": [
            "What was validated and how.",
            "Any missing checks, tests, or docs added directly.",
            "Remaining assumptions that need runtime or human verification."
        ]
    },
    {
        "id": "productionize",
        "title": "Productionize",
        "verb": "productionize",
        "difficulty": "high",
        "apply_scope": "Raise readiness through tests, docs, observability, and rollout guardrails without overengineering.",
        "expected_output": [
            "Readiness gaps ranked by operational impact.",
            "Direct improvements to tests, docs, configs, and safeguards.",
            "What still blocks confident rollout."
        ]
    }
]


DOMAINS = [
    {
        "id": "architecture",
        "label": "architecture and system boundaries",
        "recommended_subagents": ["architect-reviewer", "code-mapper", "reviewer"],
        "scenarios": [
            {"slug": "service-boundaries", "title": "service boundaries and ownership", "focus": "coupling, ownership seams, and cross-module responsibilities"},
            {"slug": "api-versioning", "title": "API versioning and compatibility", "focus": "contract drift, callers, and migration safety"},
            {"slug": "event-workflows", "title": "event-driven workflows", "focus": "message flow, idempotency, and failure recovery"},
            {"slug": "composition-root", "title": "composition root and dependency wiring", "focus": "construction logic, inversion of control, and lifecycle boundaries"},
            {"slug": "config-separation", "title": "configuration and environment separation", "focus": "environment isolation, defaults, and config sprawl"},
            {"slug": "caching-architecture", "title": "caching and state invalidation architecture", "focus": "staleness, coherence, and invalidation boundaries"},
            {"slug": "background-systems", "title": "background jobs and schedulers", "focus": "ownership, retry rules, and operational boundaries"},
            {"slug": "multi-tenant", "title": "multi-tenant design", "focus": "tenant boundaries, shared services, and risk of cross-tenant bleed"},
            {"slug": "observability-boundaries", "title": "observability and operational boundaries", "focus": "signals, runbooks, and responsibility split between code and ops"},
            {"slug": "rollout-architecture", "title": "migration and rollout architecture", "focus": "backward compatibility, cutovers, and sequencing risk"}
        ]
    },
    {
        "id": "backend",
        "label": "backend services and APIs",
        "recommended_subagents": ["backend-developer", "debugger", "reviewer"],
        "scenarios": [
            {"slug": "auth-session", "title": "auth and session flow", "focus": "identity, session lifecycle, and correctness under failure"},
            {"slug": "request-lifecycle", "title": "input validation and request lifecycle", "focus": "guardrails, parsing, and request-to-response integrity"},
            {"slug": "data-transactions", "title": "data access patterns and transactions", "focus": "query correctness, consistency, and transaction boundaries"},
            {"slug": "queue-handlers", "title": "background jobs and queue handlers", "focus": "retries, idempotency, and job-level failure handling"},
            {"slug": "webhooks", "title": "webhook ingestion and retries", "focus": "verification, retries, and duplicate event behavior"},
            {"slug": "cache-idempotency", "title": "caching and idempotency", "focus": "cache coherence, duplicate suppression, and correctness"},
            {"slug": "error-status", "title": "error handling and status codes", "focus": "predictable failure contracts and caller-facing semantics"},
            {"slug": "config-secrets", "title": "config and secrets loading", "focus": "sane defaults, secret boundaries, and runtime safety"},
            {"slug": "rate-abuse", "title": "rate limiting and abuse handling", "focus": "throttling, fairness, and failure behavior under load"},
            {"slug": "schema-compatibility", "title": "API schema compatibility", "focus": "response shape stability and caller breakage risk"}
        ]
    },
    {
        "id": "frontend",
        "label": "frontend product flows",
        "recommended_subagents": ["frontend-developer", "accessibility-tester", "reviewer"],
        "scenarios": [
            {"slug": "routing-state", "title": "routing and page-state ownership", "focus": "state boundaries, route transitions, and persistence behavior"},
            {"slug": "forms-validation", "title": "forms and validation UX", "focus": "input handling, validation feedback, and submission behavior"},
            {"slug": "async-data", "title": "async data fetching and stale state", "focus": "loading races, stale data, and conditional render edges"},
            {"slug": "component-contracts", "title": "component composition and prop contracts", "focus": "clarity, reuse boundaries, and hidden coupling"},
            {"slug": "accessibility", "title": "accessibility and keyboard support", "focus": "focus order, semantics, and interaction fallbacks"},
            {"slug": "large-lists", "title": "table, list, and rendering performance", "focus": "rerender pressure, virtualization, and UI responsiveness"},
            {"slug": "optimistic-updates", "title": "optimistic updates and error recovery", "focus": "state rollback, retries, and user trust"},
            {"slug": "design-system", "title": "design system consistency", "focus": "shared patterns, token usage, and UI drift"},
            {"slug": "responsive-mobile", "title": "mobile responsiveness", "focus": "layout behavior, touch ergonomics, and content hierarchy"},
            {"slug": "search-filter-sort", "title": "search, filter, and sort interactions", "focus": "state clarity, user control, and result consistency"}
        ]
    },
    {
        "id": "fullstack",
        "label": "end-to-end product flows",
        "recommended_subagents": ["fullstack-developer", "api-designer", "qa-expert"],
        "scenarios": [
            {"slug": "onboarding", "title": "user onboarding flow", "focus": "handoffs between UI, API, and persistence layers"},
            {"slug": "protected-workflow", "title": "auth-protected workflow", "focus": "permission boundaries and end-to-end failure handling"},
            {"slug": "crud-slice", "title": "CRUD feature vertical slice", "focus": "state flow, validation, and backend consistency"},
            {"slug": "billing", "title": "billing or checkout flow", "focus": "transaction boundaries, user feedback, and reconciliation risk"},
            {"slug": "file-processing", "title": "file upload and processing", "focus": "UI expectations, backend processing, and retry behavior"},
            {"slug": "notifications", "title": "notifications and realtime updates", "focus": "delivery guarantees, UI sync, and stale state"},
            {"slug": "admin-dashboard", "title": "admin dashboard flows", "focus": "privileged operations, data freshness, and usability"},
            {"slug": "search-platform", "title": "cross-stack search and filtering", "focus": "query semantics, UI control, and performance tradeoffs"},
            {"slug": "background-ui", "title": "background processing surfaced in UI", "focus": "progress states, polling or push updates, and user trust"},
            {"slug": "feature-flags", "title": "feature flags and rollout path", "focus": "consistency, toggles, and safe cross-stack rollout"}
        ]
    },
    {
        "id": "performance",
        "label": "performance-sensitive paths",
        "recommended_subagents": ["performance-engineer", "code-mapper", "reviewer"],
        "scenarios": [
            {"slug": "slow-endpoints", "title": "slow API endpoints", "focus": "request latency, query behavior, and hot call chains"},
            {"slug": "n-plus-one", "title": "N+1 and hot query patterns", "focus": "query amplification and wasted backend work"},
            {"slug": "render-thrash", "title": "frontend rerender pressure", "focus": "render loops, stale derived state, and unnecessary work"},
            {"slug": "cache-strategy", "title": "caching strategy", "focus": "hit rate, invalidation, and avoiding needless recomputation"},
            {"slug": "job-throughput", "title": "background job throughput", "focus": "queue pressure, concurrency limits, and retries"},
            {"slug": "bundle-assets", "title": "bundle size and asset loading", "focus": "startup cost, asset strategy, and user-perceived latency"},
            {"slug": "memory-leaks", "title": "memory leaks and resource lifecycle", "focus": "retained resources, cleanup, and long-running pressure"},
            {"slug": "concurrency", "title": "concurrency bottlenecks", "focus": "locks, serialization, and underused parallelism"},
            {"slug": "startup-time", "title": "startup and cold start time", "focus": "initialization cost and first-request readiness"},
            {"slug": "telemetry-overhead", "title": "telemetry overhead", "focus": "instrumentation cost, noise, and signal quality"}
        ]
    },
    {
        "id": "security",
        "label": "security-critical paths",
        "recommended_subagents": ["security-auditor", "penetration-tester", "reviewer"],
        "scenarios": [
            {"slug": "authz-boundaries", "title": "auth and authorization boundaries", "focus": "identity checks, policy enforcement, and bypass risk"},
            {"slug": "secrets", "title": "secrets handling", "focus": "storage, loading, exposure, and logging risk"},
            {"slug": "file-upload", "title": "file upload and parsing", "focus": "input abuse, content validation, and downstream execution risk"},
            {"slug": "external-fetch", "title": "external fetch and SSRF risk", "focus": "network boundaries, URL handling, and privileged fetch behavior"},
            {"slug": "injection", "title": "injection and input validation", "focus": "query safety, escaping, and parser trust boundaries"},
            {"slug": "sessions-csrf", "title": "session management and CSRF", "focus": "cookie policy, request origin checks, and replay behavior"},
            {"slug": "webhook-verification", "title": "webhook verification", "focus": "signature validation, retries, and replay handling"},
            {"slug": "tenant-isolation", "title": "tenant isolation", "focus": "cross-tenant access risk and shared-state exposure"},
            {"slug": "dependencies", "title": "dependency and supply-chain exposure", "focus": "third-party trust boundaries and update risk"},
            {"slug": "audit-logging", "title": "audit logging and incident response readiness", "focus": "forensics, detection coverage, and safe signal handling"}
        ]
    },
    {
        "id": "testing",
        "label": "test strategy and quality",
        "recommended_subagents": ["qa-expert", "test-automator", "reviewer"],
        "scenarios": [
            {"slug": "unit-gaps", "title": "unit coverage gaps", "focus": "logic branches, helper behavior, and isolated correctness"},
            {"slug": "integration-boundaries", "title": "integration test boundaries", "focus": "real interfaces, contracts, and meaningful test seams"},
            {"slug": "flaky-tests", "title": "flaky test triage", "focus": "nondeterminism, timing assumptions, and environment coupling"},
            {"slug": "fixtures", "title": "test data and fixtures", "focus": "clarity, reuse, realism, and brittleness"},
            {"slug": "e2e-critical-paths", "title": "end-to-end critical path coverage", "focus": "user-visible workflows and regression confidence"},
            {"slug": "failure-paths", "title": "failure path coverage", "focus": "error states, retries, and degraded mode behavior"},
            {"slug": "contract-tests", "title": "contract tests for APIs", "focus": "compatibility, drift detection, and caller safety"},
            {"slug": "regression-harness", "title": "regression harness for bug fixes", "focus": "pinning behavior and preventing reintroductions"},
            {"slug": "perf-tests", "title": "performance test scaffolding", "focus": "repeatability, representative load, and signal quality"},
            {"slug": "ci-reliability", "title": "test runtime and CI reliability", "focus": "feedback speed, consistency, and signal-to-noise ratio"}
        ]
    },
    {
        "id": "data",
        "label": "data systems and pipelines",
        "recommended_subagents": ["data-engineer", "data-analyst", "reviewer"],
        "scenarios": [
            {"slug": "ingestion", "title": "ingestion pipeline correctness", "focus": "data arrival guarantees, parsing, and loss prevention"},
            {"slug": "transformations", "title": "transformations and schema drift", "focus": "shape changes, mapping logic, and downstream breakage"},
            {"slug": "warehouse-models", "title": "warehouse model organization", "focus": "layering, naming, and dependency clarity"},
            {"slug": "backfills", "title": "backfills and replay jobs", "focus": "reprocessing safety, idempotency, and operational cost"},
            {"slug": "data-quality", "title": "data quality assertions", "focus": "coverage, failure thresholds, and noisy checks"},
            {"slug": "metrics", "title": "metric definition consistency", "focus": "semantic drift, duplication, and stakeholder trust"},
            {"slug": "feature-prep", "title": "feature store and ML data prep", "focus": "training-serving consistency and feature lineage"},
            {"slug": "streaming-batch", "title": "streaming versus batch boundaries", "focus": "latency tradeoffs, correctness, and duplicated logic"},
            {"slug": "pii-access", "title": "PII handling and access control", "focus": "sensitivity boundaries, masking, and analyst safety"},
            {"slug": "analyst-docs", "title": "analyst-facing docs and examples", "focus": "discoverability, trustworthy examples, and semantic clarity"}
        ]
    },
    {
        "id": "docs",
        "label": "documentation and examples",
        "recommended_subagents": ["documentation-engineer", "docs-researcher", "reviewer"],
        "scenarios": [
            {"slug": "getting-started", "title": "getting started onboarding", "focus": "time to first success and setup ambiguity"},
            {"slug": "api-reference", "title": "API reference accuracy", "focus": "drift from implementation and missing edge cases"},
            {"slug": "architecture-docs", "title": "architecture docs versus code drift", "focus": "fidelity, stale diagrams, and conceptual gaps"},
            {"slug": "runbooks", "title": "runbook completeness", "focus": "operational steps, failure handling, and missing decision points"},
            {"slug": "examples", "title": "examples and sample requests", "focus": "copy-paste value, realism, and coverage of common tasks"},
            {"slug": "migration-guides", "title": "migration guides", "focus": "upgrade sequencing, compatibility notes, and rollback awareness"},
            {"slug": "troubleshooting", "title": "troubleshooting docs", "focus": "diagnostic clarity, real symptoms, and operator confidence"},
            {"slug": "release-notes", "title": "changelog and release notes", "focus": "signal density, user impact, and upgrade clarity"},
            {"slug": "contributor-docs", "title": "contributor docs", "focus": "repo conventions, setup friction, and review readiness"},
            {"slug": "glossary", "title": "internal glossary and naming consistency", "focus": "terminology drift and reader confusion"}
        ]
    },
    {
        "id": "release-platform",
        "label": "release engineering and platform operations",
        "recommended_subagents": ["devops-engineer", "sre-engineer", "reviewer"],
        "scenarios": [
            {"slug": "ci-reliability", "title": "CI pipeline reliability", "focus": "failure modes, feedback speed, and wasted reruns"},
            {"slug": "cd-safety", "title": "CD rollout safety", "focus": "progressive delivery, gating, and blast-radius control"},
            {"slug": "infra-drift", "title": "infrastructure config drift", "focus": "environment consistency and declarative ownership"},
            {"slug": "env-secrets", "title": "environment and secrets management", "focus": "config distribution, secret hygiene, and operator safety"},
            {"slug": "incident-hooks", "title": "incident response hooks", "focus": "alert routing, escalation, and actionable runbooks"},
            {"slug": "monitoring-alerting", "title": "monitoring and alerting", "focus": "signal quality, SLO alignment, and false positives"},
            {"slug": "backup-restore", "title": "backup and restore readiness", "focus": "recovery confidence, restoration steps, and verification"},
            {"slug": "staging-parity", "title": "staging and production parity", "focus": "configuration skew, seed data, and rollout surprises"},
            {"slug": "build-repro", "title": "container and build reproducibility", "focus": "determinism, caching, and dependency stability"},
            {"slug": "rollback-safety", "title": "rollback and migration safety", "focus": "reversibility, data compatibility, and operator confidence"}
        ]
    }
]


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            ordered.append(item)
            seen.add(item)
    return ordered


def build_recommended_subagents(domain: dict, mode: dict) -> list[str]:
    mode_specific = {
        "audit": ["search-specialist"],
        "implement": ["reviewer"],
        "fix": ["debugger"],
        "refactor": ["refactoring-specialist"],
        "harden": ["security-auditor"],
        "optimize": ["performance-engineer"],
        "migrate": ["architect-reviewer"],
        "review": ["reviewer"],
        "validate": ["qa-expert"],
        "productionize": ["sre-engineer"],
    }
    return dedupe(domain["recommended_subagents"] + mode_specific[mode["id"]])


def build_prompt(domain: dict, scenario: dict, mode: dict) -> str:
    scenario_title = scenario["title"]
    domain_label = domain["label"]
    expected = "\n".join(
        f"{idx}. {line}" for idx, line in enumerate(mode["expected_output"], start=1)
    )

    return (
        f"Use subagents in parallel to {mode['verb']} the {scenario_title} in this repo's {domain_label}.\n\n"
        f"Target focus:\n"
        f"- {scenario_title}\n"
        f"- Emphasize {scenario['focus']}\n\n"
        f"Suggested split:\n"
        f"1. Map the relevant files, call paths, contracts, and dependencies around {scenario_title}.\n"
        f"2. Go deep on {scenario['focus']} inside the target area.\n"
        f"3. Validate likely regressions across tests, docs, integration edges, and failure handling.\n\n"
        f"Expected output:\n"
        f"{expected}\n\n"
        f"Constraints:\n"
        f"- Keep diffs scoped and reviewable.\n"
        f"- {mode['apply_scope']}\n"
        f"- Prefer evidence over guesses.\n"
        f"- Preserve backward compatibility unless the migration itself is the goal.\n"
        f"- Update tests or docs only when they materially improve confidence."
    )


def build_entry(index: int, domain: dict, scenario: dict, mode: dict) -> dict:
    slug = f"{domain['id']}-{scenario['slug']}-{mode['id']}"
    return {
        "id": f"sq-{index:04d}",
        "slug": slug,
        "title": f"{mode['title']} {scenario['title']} ({domain['id']})",
        "domain": domain["id"],
        "scenario": scenario["title"],
        "mode": mode["id"],
        "difficulty": mode["difficulty"],
        "recommended_subagents": build_recommended_subagents(domain, mode),
        "prompt": build_prompt(domain, scenario, mode),
        "expected_output": mode["expected_output"],
        "tags": [
            "codex",
            "subagents",
            domain["id"],
            mode["id"],
            scenario["slug"],
        ],
    }


def generate_entries() -> list[dict]:
    entries: list[dict] = []
    index = 1
    for domain in DOMAINS:
        for scenario in domain["scenarios"]:
            for mode in MODES:
                entries.append(build_entry(index, domain, scenario, mode))
                index += 1
    return entries


def build_catalog(entries: list[dict]) -> dict:
    domain_counts: dict[str, int] = {}
    mode_counts: dict[str, int] = {}

    catalog_entries = []
    for entry in entries:
        domain_counts[entry["domain"]] = domain_counts.get(entry["domain"], 0) + 1
        mode_counts[entry["mode"]] = mode_counts.get(entry["mode"], 0) + 1
        catalog_entries.append(
            {
                "id": entry["id"],
                "slug": entry["slug"],
                "title": entry["title"],
                "domain": entry["domain"],
                "scenario": entry["scenario"],
                "mode": entry["mode"],
                "difficulty": entry["difficulty"],
                "recommended_subagents": entry["recommended_subagents"],
                "tags": entry["tags"],
            }
        )

    return {
        "version": 1,
        "query_count": len(entries),
        "domain_counts": domain_counts,
        "mode_counts": mode_counts,
        "entries": catalog_entries,
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    entries = generate_entries()
    full_payload = {
        "version": 1,
        "query_count": len(entries),
        "entries": entries,
    }
    write_json(DATA_DIR / "subagent-queries.json", full_payload)
    write_json(DATA_DIR / "subagent-query-catalog.json", build_catalog(entries))


if __name__ == "__main__":
    main()
