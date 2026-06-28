"""Agent registry — registered CNS agents with purpose, authority, and capability profiles."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AgentProfile:
    agent_id: str
    display_name: str
    purpose: str
    cns_layer: str
    owner: str
    maturity: str
    max_authority_level: str
    action_kinds: List[str] = field(default_factory=list)
    live_access_enabled: bool = False
    performance_notes: Optional[str] = None


@dataclass
class AgentRegistryReport:
    valid: bool
    agent_count: int
    issues: List[str] = field(default_factory=list)


class AgentRegistry:
    """Read-only registry of known CNS agents. Phase 1: in-memory seed data, no live access."""

    def __init__(self) -> None:
        self.profiles: List[AgentProfile] = list(_SEED_AGENTS)

    def validate(self) -> AgentRegistryReport:
        issues: List[str] = []
        agent_ids = [p.agent_id for p in self.profiles]
        if len(agent_ids) != len(set(agent_ids)):
            issues.append("Duplicate agent IDs detected in registry.")
        for p in self.profiles:
            if not p.agent_id or not p.display_name:
                issues.append(f"Agent profile missing required fields: {p.agent_id!r}")
        return AgentRegistryReport(
            valid=len(issues) == 0,
            agent_count=len(self.profiles),
            issues=issues,
        )

    def by_id(self, agent_id: str) -> Optional[AgentProfile]:
        for p in self.profiles:
            if p.agent_id == agent_id:
                return p
        return None

    def by_action_kind(self, action_kind: str) -> List[AgentProfile]:
        return [p for p in self.profiles if action_kind in p.action_kinds]


_SEED_AGENTS: List[AgentProfile] = [
    AgentProfile(
        agent_id="freedom-executive",
        display_name="Freedom Executive Cognition",
        purpose="Executive AI business partner — mission reasoning, decision briefing, authority escalation, and context synthesis",
        cns_layer="freedom",
        owner="Adam Goodwin",
        maturity="active",
        max_authority_level="R2_INTERNAL_WRITE",
        action_kinds=["research", "memory", "system", "general"],
        live_access_enabled=False,
    ),
    AgentProfile(
        agent_id="freedom-gateway",
        display_name="Freedom Gateway",
        purpose="API and webhook integration gateway — routes external signals into the CNS event bus",
        cns_layer="freedom",
        owner="Adam Goodwin",
        maturity="prototype",
        max_authority_level="R1_PROPOSE",
        action_kinds=["research", "general"],
        live_access_enabled=False,
    ),
    AgentProfile(
        agent_id="freedom-desktop",
        display_name="Freedom Desktop Host",
        purpose="Desktop application host — app control, file operations, and device management on Windows and Linux",
        cns_layer="freedom",
        owner="Adam Goodwin",
        maturity="prototype",
        max_authority_level="R2_INTERNAL_WRITE",
        action_kinds=["app_control", "file_open", "file_search", "device_control", "system", "build", "media"],
        live_access_enabled=False,
    ),
    AgentProfile(
        agent_id="freedom-mobile",
        display_name="Freedom Mobile Companion",
        purpose="Mobile companion — voice, messaging, and on-the-go capability extension",
        cns_layer="freedom",
        owner="Adam Goodwin",
        maturity="prototype",
        max_authority_level="R1_PROPOSE",
        action_kinds=["message", "general", "research"],
        live_access_enabled=False,
    ),
    AgentProfile(
        agent_id="gail-os-policy",
        display_name="GAIL OS Policy Authority Engine",
        purpose="Autonomic policy authority — validates actions, manages authority envelopes, records evidence, and tracks mission state",
        cns_layer="gail_os",
        owner="Adam Goodwin",
        maturity="active",
        max_authority_level="R3_EXECUTE",
        action_kinds=["system", "general"],
        live_access_enabled=False,
    ),
    AgentProfile(
        agent_id="graphify-cockpit",
        display_name="Graphify Relationship Intelligence",
        purpose="Cognitive infrastructure — entity context, mission history, research claims, and graph relationship queries",
        cns_layer="graphify",
        owner="Adam Goodwin",
        maturity="active",
        max_authority_level="R0_OBSERVE",
        action_kinds=["research", "general"],
        live_access_enabled=False,
    ),
]
