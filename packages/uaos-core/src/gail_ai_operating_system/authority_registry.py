"""Read-only R0-R5 authority posture for GAIL OS."""

from __future__ import annotations

from typing import Any


AUTHORITY_LEVELS: tuple[dict[str, str], ...] = (
    {
        "level": "R0",
        "name": "Observe",
        "meaning": "Read-only, no external effect",
        "agent_boundary": "Allowed for local dry-run observation.",
    },
    {
        "level": "R1",
        "name": "Propose",
        "meaning": "Draft, recommend, prepare - no external effect",
        "agent_boundary": "Allowed for proposal work only.",
    },
    {
        "level": "R2",
        "name": "Internal approved action",
        "meaning": "Reversible internal write with named approval",
        "agent_boundary": "Requires GAIL OS policy validation and evidence.",
    },
    {
        "level": "R3",
        "name": "Restricted action",
        "meaning": "External send, production release, irreversible change",
        "agent_boundary": "Requires explicit approval before execution.",
    },
    {
        "level": "R4",
        "name": "Delegated autonomous restricted action",
        "meaning": "Inside a valid pre-approved authority charter",
        "agent_boundary": "Owner-gated; requires a signed AuthorityEnvelope.",
    },
    {
        "level": "R5",
        "name": "Blocked / human-only",
        "meaning": "Agent may analyze only; human decides",
        "agent_boundary": "Human-only. No agent execution.",
    },
)


def authority_registry_payload() -> dict[str, Any]:
    return {
        "registry_valid": True,
        "source": "docs/governance/authority-ladders.md",
        "boundary": "A1 local no-network",
        "autonomy_level": "A1",
        "live_execution_enabled": False,
        "r4_requires_authority_envelope": True,
        "r5_human_only": True,
        "authority_levels": [dict(level) for level in AUTHORITY_LEVELS],
    }


__all__ = ["AUTHORITY_LEVELS", "authority_registry_payload"]
