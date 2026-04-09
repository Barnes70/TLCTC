#!/usr/bin/env python3
"""Generate ISO 27001:2022 Annex A control-matrix starter JSON for the TLCTC Control Matrix tool."""
import json
import os
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(SCRIPT_DIR, "control-matrix-starter-iso27001.json")

# ── factory ──────────────────────────────────────────────────────────────────

_id = 0

def ctl(iso_ref, iso_title, desc, kind):
    """Return a control object matching the control-matrix tool schema."""
    global _id
    _id += 1
    return {
        "id": f"iso-{_id}",
        "name": f"{iso_ref} \u2014 {iso_title}",
        "description": desc,
        "linkMore": "",
        "ownerName": "",
        "ownerOrgChart": "",
        "kind": kind,
        "maturity": 0,
        "linkJira": "",
        "role": "",
        "cde_max": {"value": None, "rationale": "", "set_by": "", "last_reviewed": "", "review_trigger": ""},
        "cde_fitness": {"target_velocity_class": "", "fit": None, "factor": None, "rationale": ""},
        "coe": {"metrics": [], "aggregation_method": "weighted_mean", "weights": {}, "composite_coe": None},
        "ecr": None,
    }

def cell(local, umbrella):
    return {
        "local": local,
        "umbrella": umbrella,
        "velocity_context": {"primary_velocity_class": "", "delta_t": "", "delta_t_source": "", "delta_t_confidence": ""},
        "controls_meta": {"expected_count": None},
    }

# ── mapping helpers ──────────────────────────────────────────────────────────
# Each cell is built by calling cell([ctl(...),...], [ctl(...),...])
# kind: "org" = A.5/A.6 organizational, "tech" = A.7/A.8 technological

def build_cells():
    """Build all 60 cells (10 clusters × 6 CSF functions)."""
    cells = {}

    # ═══════════════════════════════════════════════════════════════════════════
    # CLUSTER 1 — Abuse of Functions (AoF)
    # ═══════════════════════════════════════════════════════════════════════════

    cells["1-GV"] = cell(
        local=[
            ctl("A.5.10", "Acceptable use of information and other associated assets",
                "Define acceptable use boundaries for administrative and privileged functions", "org"),
            ctl("A.5.37", "Documented operating procedures",
                "Document authorized procedures for critical system functions to detect deviations", "org"),
        ],
        umbrella=[
            ctl("A.5.1", "Policies for information security",
                "Define acceptable-use policies addressing misuse of legitimate system functions", "org"),
            ctl("A.5.2", "Information security roles and responsibilities",
                "Assign ownership for monitoring and controlling function abuse risk", "org"),
            ctl("A.5.3", "Segregation of duties",
                "Enforce separation of duties to prevent single-actor function abuse", "org"),
        ],
    )

    cells["1-ID"] = cell(
        local=[
            ctl("A.8.9", "Configuration management",
                "Identify and document all configurable functions and their security-relevant settings", "tech"),
            ctl("A.8.2", "Privileged access rights",
                "Identify all accounts with elevated privileges that enable function abuse", "tech"),
        ],
        umbrella=[
            ctl("A.5.9", "Inventory of information and other associated assets",
                "Inventory all systems with privileged functions that could be abused", "org"),
            ctl("A.5.7", "Threat intelligence",
                "Monitor threat intelligence for function-abuse TTPs targeting deployed systems", "org"),
        ],
    )

    cells["1-PR"] = cell(
        local=[
            ctl("A.8.2", "Privileged access rights",
                "Enforce time-limited, just-in-time privileged access to reduce function abuse window", "tech"),
            ctl("A.8.18", "Use of privileged utility programs",
                "Restrict and audit use of system utilities that bypass normal controls", "tech"),
            ctl("A.8.9", "Configuration management",
                "Lock down system configurations to prevent unauthorized function enablement", "tech"),
        ],
        umbrella=[
            ctl("A.5.15", "Access control",
                "Restrict function access to authorized use patterns; enforce least privilege for admin functions", "org"),
            ctl("A.5.18", "Access rights",
                "Provision and review access rights to prevent unauthorized function use", "org"),
        ],
    )

    cells["1-DE"] = cell(
        local=[
            ctl("A.8.15", "Logging",
                "Log all privileged function invocations, configuration changes, and admin actions", "tech"),
            ctl("A.8.16", "Monitoring activities",
                "Monitor for anomalous function usage patterns (volume, timing, scope)", "tech"),
            ctl("A.8.17", "Clock synchronization",
                "Synchronize system clocks to ensure accurate correlation of function-abuse timelines", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Integrate function-abuse indicators into detection rules", "org"),
        ],
    )

    cells["1-RS"] = cell(
        local=[
            ctl("A.5.28", "Collection of evidence",
                "Preserve logs and session data as evidence of function abuse", "org"),
            ctl("A.5.25", "Assessment and decision on information security events",
                "Triage function-abuse alerts and classify severity", "org"),
        ],
        umbrella=[
            ctl("A.5.24", "Information security incident management planning and preparation",
                "Prepare response procedures for function-abuse incidents", "org"),
            ctl("A.5.26", "Response to information security incidents",
                "Execute containment for active function abuse (revoke access, disable function)", "org"),
        ],
    )

    cells["1-RC"] = cell(
        local=[
            ctl("A.5.30", "ICT readiness for business continuity",
                "Ensure function-abuse recovery is included in continuity plans", "org"),
            ctl("A.8.9", "Configuration management",
                "Restore verified baseline configurations after function-abuse compromise", "tech"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Maintain security controls during recovery from function-abuse incidents", "org"),
            ctl("A.5.27", "Learning from information security incidents",
                "Conduct post-incident reviews of function-abuse events to refine controls", "org"),
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # CLUSTER 2 — Exploiting Server (ExS)
    # ═══════════════════════════════════════════════════════════════════════════

    cells["2-GV"] = cell(
        local=[
            ctl("A.5.31", "Legal, statutory, regulatory and contractual requirements",
                "Identify compliance requirements for server-hosted data and services", "org"),
            ctl("A.5.37", "Documented operating procedures",
                "Document server hardening and patch management procedures", "org"),
        ],
        umbrella=[
            ctl("A.5.1", "Policies for information security",
                "Define policies for server hardening, patching, and vulnerability management", "org"),
            ctl("A.5.2", "Information security roles and responsibilities",
                "Assign ownership for server security and vulnerability remediation", "org"),
            ctl("A.5.8", "Information security in project management",
                "Require security assessment of server components in all projects", "org"),
        ],
    )

    cells["2-ID"] = cell(
        local=[
            ctl("A.8.8", "Management of technical vulnerabilities",
                "Scan servers for known vulnerabilities and prioritize by exploitability", "tech"),
            ctl("A.8.9", "Configuration management",
                "Identify server misconfigurations and deviations from hardening baselines", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Monitor threat feeds for server-side exploit campaigns targeting deployed technologies", "org"),
            ctl("A.5.9", "Inventory of information and other associated assets",
                "Maintain inventory of all server assets, OS versions, and exposed services", "org"),
        ],
    )

    cells["2-PR"] = cell(
        local=[
            ctl("A.8.8", "Management of technical vulnerabilities",
                "Apply patches and mitigations for server-side vulnerabilities within defined SLAs", "tech"),
            ctl("A.8.27", "Secure system architecture and engineering principles",
                "Design server architecture with defense-in-depth against exploitation", "tech"),
            ctl("A.8.26", "Application security requirements",
                "Define security requirements for server-side applications", "tech"),
            ctl("A.8.22", "Segregation of networks",
                "Segment server networks to limit lateral movement after exploitation", "tech"),
        ],
        umbrella=[
            ctl("A.5.23", "Information security for use of cloud services",
                "Secure cloud-hosted server instances with provider-specific hardening", "org"),
        ],
    )

    cells["2-DE"] = cell(
        local=[
            ctl("A.8.15", "Logging",
                "Log server access, error conditions, and authentication events for exploit detection", "tech"),
            ctl("A.8.16", "Monitoring activities",
                "Monitor servers for exploitation indicators (unexpected processes, file changes, outbound connections)", "tech"),
            ctl("A.8.20", "Networks security",
                "Deploy network-based intrusion detection for server exploitation attempts", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Integrate server exploit signatures and IOCs into detection systems", "org"),
        ],
    )

    cells["2-RS"] = cell(
        local=[
            ctl("A.5.28", "Collection of evidence",
                "Capture server forensic images and logs for exploitation analysis", "org"),
            ctl("A.5.25", "Assessment and decision on information security events",
                "Triage server security alerts and determine exploitation scope", "org"),
        ],
        umbrella=[
            ctl("A.5.24", "Information security incident management planning and preparation",
                "Prepare response playbooks for server compromise scenarios", "org"),
            ctl("A.5.26", "Response to information security incidents",
                "Contain server exploitation (isolate, patch, rotate credentials)", "org"),
        ],
    )

    cells["2-RC"] = cell(
        local=[
            ctl("A.5.30", "ICT readiness for business continuity",
                "Include server compromise recovery in business continuity plans", "org"),
            ctl("A.8.13", "Information backup",
                "Restore server systems and data from verified clean backups", "tech"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Maintain server security controls during recovery operations", "org"),
            ctl("A.5.27", "Learning from information security incidents",
                "Analyze server exploitation root cause to prevent recurrence", "org"),
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # CLUSTER 3 — Exploiting Client (ExC)
    # ═══════════════════════════════════════════════════════════════════════════

    cells["3-GV"] = cell(
        local=[
            ctl("A.6.7", "Remote working",
                "Establish security requirements for remote client devices and home networks", "org"),
            ctl("A.5.37", "Documented operating procedures",
                "Document client hardening procedures and approved application lists", "org"),
        ],
        umbrella=[
            ctl("A.5.1", "Policies for information security",
                "Define policies for client device hardening, browser security, and application controls", "org"),
            ctl("A.5.2", "Information security roles and responsibilities",
                "Assign ownership for endpoint security program", "org"),
        ],
    )

    cells["3-ID"] = cell(
        local=[
            ctl("A.8.8", "Management of technical vulnerabilities",
                "Scan client applications for known vulnerabilities", "tech"),
            ctl("A.8.1", "User endpoint devices",
                "Identify all endpoint device types and their security posture", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Monitor threat intelligence for client-side exploit campaigns (browser, document, plugin)", "org"),
            ctl("A.5.9", "Inventory of information and other associated assets",
                "Maintain inventory of all client devices, software versions, and browser extensions", "org"),
        ],
    )

    cells["3-PR"] = cell(
        local=[
            ctl("A.8.1", "User endpoint devices",
                "Harden endpoint configurations (disable macros, restrict plugins, enable sandboxing)", "tech"),
            ctl("A.8.19", "Installation of software on operational systems",
                "Restrict software installation to approved applications only", "tech"),
            ctl("A.8.23", "Web filtering",
                "Filter web content to block known exploit delivery sites", "tech"),
            ctl("A.8.8", "Management of technical vulnerabilities",
                "Patch client applications (browsers, office, media) within defined SLAs", "tech"),
        ],
        umbrella=[
            ctl("A.6.3", "Information security awareness, education and training",
                "Train users on client-side risks (malicious documents, drive-by downloads)", "org"),
        ],
    )

    cells["3-DE"] = cell(
        local=[
            ctl("A.8.15", "Logging",
                "Log client application events, process execution, and file downloads for exploitation detection", "tech"),
            ctl("A.8.16", "Monitoring activities",
                "Monitor endpoints for client-side exploitation indicators (unexpected child processes, shellcode)", "tech"),
            ctl("A.8.7", "Protection against malware",
                "Detect exploitation payloads delivered through client-side vectors", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Integrate client exploit IOCs into endpoint detection rules", "org"),
        ],
    )

    cells["3-RS"] = cell(
        local=[
            ctl("A.5.28", "Collection of evidence",
                "Collect endpoint forensic artifacts from exploited client systems", "org"),
            ctl("A.5.25", "Assessment and decision on information security events",
                "Triage client exploitation alerts and assess lateral movement risk", "org"),
        ],
        umbrella=[
            ctl("A.5.24", "Information security incident management planning and preparation",
                "Prepare response procedures for client-side exploitation incidents", "org"),
            ctl("A.5.26", "Response to information security incidents",
                "Contain client exploitation (isolate endpoint, kill processes, block C2)", "org"),
        ],
    )

    cells["3-RC"] = cell(
        local=[
            ctl("A.5.30", "ICT readiness for business continuity",
                "Include client system rebuild in continuity plans", "org"),
            ctl("A.8.1", "User endpoint devices",
                "Reimage or restore client devices to verified clean state", "tech"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Maintain endpoint security during client system recovery", "org"),
            ctl("A.5.27", "Learning from information security incidents",
                "Review client exploitation incidents to improve endpoint controls", "org"),
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # CLUSTER 4 — Identity Theft (IdT)
    # ═══════════════════════════════════════════════════════════════════════════

    cells["4-GV"] = cell(
        local=[
            ctl("A.5.17", "Authentication information",
                "Define requirements for credential strength, rotation, and protection", "org"),
            ctl("A.5.37", "Documented operating procedures",
                "Document credential management and identity verification procedures", "org"),
        ],
        umbrella=[
            ctl("A.5.1", "Policies for information security",
                "Define identity and access management policies including MFA requirements", "org"),
            ctl("A.5.16", "Identity management",
                "Govern identity lifecycle from provisioning through decommissioning", "org"),
            ctl("A.5.3", "Segregation of duties",
                "Enforce duty separation to limit impact of single compromised identity", "org"),
        ],
    )

    cells["4-ID"] = cell(
        local=[
            ctl("A.8.2", "Privileged access rights",
                "Identify all privileged accounts and their access scope", "tech"),
            ctl("A.5.18", "Access rights",
                "Review access rights to identify excessive or orphaned permissions", "org"),
        ],
        umbrella=[
            ctl("A.5.9", "Inventory of information and other associated assets",
                "Inventory all identity stores, directories, and authentication systems", "org"),
            ctl("A.5.7", "Threat intelligence",
                "Monitor for credential dump campaigns, password spray attacks, and identity theft TTPs", "org"),
        ],
    )

    cells["4-PR"] = cell(
        local=[
            ctl("A.8.5", "Secure authentication",
                "Enforce MFA and strong authentication to prevent credential abuse", "tech"),
            ctl("A.8.3", "Information access restriction",
                "Implement role-based access to limit impact of stolen credentials", "tech"),
            ctl("A.8.2", "Privileged access rights",
                "Restrict and time-limit elevated access to reduce identity theft impact", "tech"),
        ],
        umbrella=[
            ctl("A.5.15", "Access control",
                "Enforce access control policies preventing unauthorized identity assumption", "org"),
            ctl("A.6.5", "Responsibilities after termination or change of employment",
                "Revoke access promptly upon role changes or termination", "org"),
        ],
    )

    cells["4-DE"] = cell(
        local=[
            ctl("A.8.15", "Logging",
                "Log authentication events, failed attempts, and access anomalies", "tech"),
            ctl("A.8.16", "Monitoring activities",
                "Monitor for credential abuse indicators (impossible travel, unusual hours, brute force)", "tech"),
            ctl("A.8.5", "Secure authentication",
                "Detect authentication anomalies (token replay, session hijack, MFA bypass attempts)", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Integrate credential theft indicators (leaked credentials, dark web monitoring) into detection", "org"),
        ],
    )

    cells["4-RS"] = cell(
        local=[
            ctl("A.5.28", "Collection of evidence",
                "Preserve authentication logs and session data for identity theft forensics", "org"),
            ctl("A.5.25", "Assessment and decision on information security events",
                "Triage identity alerts and assess scope of compromised access", "org"),
        ],
        umbrella=[
            ctl("A.5.24", "Information security incident management planning and preparation",
                "Prepare response playbooks for credential compromise", "org"),
            ctl("A.5.26", "Response to information security incidents",
                "Contain identity theft (force password reset, revoke sessions, disable accounts)", "org"),
        ],
    )

    cells["4-RC"] = cell(
        local=[
            ctl("A.5.30", "ICT readiness for business continuity",
                "Include identity system recovery in continuity plans", "org"),
            ctl("A.5.16", "Identity management",
                "Re-establish verified identity states and clean up compromised accounts", "org"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Maintain access controls during identity recovery operations", "org"),
            ctl("A.5.27", "Learning from information security incidents",
                "Analyze identity theft incidents to strengthen authentication controls", "org"),
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # CLUSTER 5 — Man in the Middle (MitM)
    # ═══════════════════════════════════════════════════════════════════════════

    cells["5-GV"] = cell(
        local=[
            ctl("A.5.31", "Legal, statutory, regulatory and contractual requirements",
                "Identify regulatory requirements for data-in-transit protection", "org"),
            ctl("A.5.37", "Documented operating procedures",
                "Document certificate management and secure channel configuration procedures", "org"),
        ],
        umbrella=[
            ctl("A.5.1", "Policies for information security",
                "Define policies for encryption standards, certificate management, and secure communications", "org"),
            ctl("A.5.14", "Information transfer",
                "Define rules and agreements for secure information transfer between parties", "org"),
            ctl("A.5.2", "Information security roles and responsibilities",
                "Assign ownership for network security and encryption program", "org"),
        ],
    )

    cells["5-ID"] = cell(
        local=[
            ctl("A.8.20", "Networks security",
                "Identify all network segments and their encryption status", "tech"),
            ctl("A.7.12", "Cabling security",
                "Identify physical network cabling vulnerable to tapping", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Monitor for MitM campaign intelligence (rogue APs, certificate abuse, BGP hijacks)", "org"),
            ctl("A.5.9", "Inventory of information and other associated assets",
                "Inventory all network paths, certificates, and trust anchors", "org"),
        ],
    )

    cells["5-PR"] = cell(
        local=[
            ctl("A.8.24", "Use of cryptography",
                "Implement strong encryption (TLS 1.3, IPsec) for all data in transit", "tech"),
            ctl("A.8.20", "Networks security",
                "Enforce network security controls (802.1X, WPA3) preventing unauthorized access", "tech"),
            ctl("A.8.21", "Security of network services",
                "Secure network services with mutual authentication and encryption", "tech"),
            ctl("A.8.22", "Segregation of networks",
                "Segregate networks to limit interception scope", "tech"),
        ],
        umbrella=[
            ctl("A.5.14", "Information transfer",
                "Enforce encrypted channels for all sensitive information transfers", "org"),
        ],
    )

    cells["5-DE"] = cell(
        local=[
            ctl("A.8.15", "Logging",
                "Log certificate events, connection downgrades, and network anomalies", "tech"),
            ctl("A.8.16", "Monitoring activities",
                "Monitor for MitM indicators (certificate mismatches, ARP spoofing, DNS hijacking)", "tech"),
            ctl("A.8.17", "Clock synchronization",
                "Ensure accurate timestamps for correlating network interception events", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Integrate MitM indicators (rogue certificates, ARP anomalies) into detection", "org"),
        ],
    )

    cells["5-RS"] = cell(
        local=[
            ctl("A.5.28", "Collection of evidence",
                "Capture network traffic and certificate data for interception forensics", "org"),
            ctl("A.5.25", "Assessment and decision on information security events",
                "Triage network anomaly alerts for potential interception", "org"),
        ],
        umbrella=[
            ctl("A.5.24", "Information security incident management planning and preparation",
                "Prepare response procedures for interception incidents", "org"),
            ctl("A.5.26", "Response to information security incidents",
                "Contain MitM attacks (revoke compromised certificates, isolate network segments)", "org"),
        ],
    )

    cells["5-RC"] = cell(
        local=[
            ctl("A.5.30", "ICT readiness for business continuity",
                "Include network infrastructure recovery in continuity plans", "org"),
            ctl("A.8.24", "Use of cryptography",
                "Reissue certificates and re-establish secure channels after compromise", "tech"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Maintain encrypted communications during network recovery", "org"),
            ctl("A.5.27", "Learning from information security incidents",
                "Review interception incidents to strengthen transport security", "org"),
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # CLUSTER 6 — Flooding Attack (Fld)
    # ═══════════════════════════════════════════════════════════════════════════

    cells["6-GV"] = cell(
        local=[
            ctl("A.5.23", "Information security for use of cloud services",
                "Define cloud service availability SLAs and DDoS protection requirements", "org"),
            ctl("A.5.37", "Documented operating procedures",
                "Document DDoS response and traffic management procedures", "org"),
        ],
        umbrella=[
            ctl("A.5.1", "Policies for information security",
                "Define availability requirements and DoS protection policies", "org"),
            ctl("A.5.2", "Information security roles and responsibilities",
                "Assign ownership for availability management and DDoS defense", "org"),
            ctl("A.5.31", "Legal, statutory, regulatory and contractual requirements",
                "Identify regulatory availability requirements (SLA, uptime)", "org"),
        ],
    )

    cells["6-ID"] = cell(
        local=[
            ctl("A.8.6", "Capacity management",
                "Assess capacity limits and identify single points of failure for resource exhaustion", "tech"),
            ctl("A.8.14", "Redundancy of information processing facilities",
                "Identify redundancy gaps that increase flooding attack impact", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Monitor for flooding attack campaigns targeting organization's sector or infrastructure", "org"),
            ctl("A.5.9", "Inventory of information and other associated assets",
                "Inventory public-facing assets and their bandwidth/capacity profiles", "org"),
        ],
    )

    cells["6-PR"] = cell(
        local=[
            ctl("A.8.6", "Capacity management",
                "Provision capacity headroom and auto-scaling to absorb traffic spikes", "tech"),
            ctl("A.8.14", "Redundancy of information processing facilities",
                "Deploy redundant processing to maintain availability during flooding", "tech"),
            ctl("A.8.20", "Networks security",
                "Deploy rate limiting, traffic shaping, and DDoS mitigation at network level", "tech"),
            ctl("A.8.22", "Segregation of networks",
                "Segregate critical services to contain flooding impact", "tech"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Ensure availability controls remain functional during flooding attacks", "org"),
        ],
    )

    cells["6-DE"] = cell(
        local=[
            ctl("A.8.15", "Logging",
                "Log traffic volumes, connection rates, and resource utilization for flooding detection", "tech"),
            ctl("A.8.16", "Monitoring activities",
                "Monitor for flooding indicators (traffic spikes, resource exhaustion, latency increases)", "tech"),
            ctl("A.8.6", "Capacity management",
                "Alert when resource utilization approaches capacity thresholds", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Integrate DDoS botnet indicators and attack signatures into detection", "org"),
        ],
    )

    cells["6-RS"] = cell(
        local=[
            ctl("A.5.25", "Assessment and decision on information security events",
                "Assess flooding attack scope and identify targeted services", "org"),
        ],
        umbrella=[
            ctl("A.5.24", "Information security incident management planning and preparation",
                "Prepare DDoS response runbooks with ISP and CDN escalation procedures", "org"),
            ctl("A.5.26", "Response to information security incidents",
                "Activate DDoS mitigation (upstream filtering, traffic scrubbing, failover)", "org"),
            ctl("A.5.5", "Contact with authorities",
                "Coordinate with ISPs and authorities during large-scale flooding attacks", "org"),
        ],
    )

    cells["6-RC"] = cell(
        local=[
            ctl("A.5.30", "ICT readiness for business continuity",
                "Test and update business continuity plans for extended DDoS scenarios", "org"),
            ctl("A.8.14", "Redundancy of information processing facilities",
                "Validate and restore redundancy after flooding-induced failover", "tech"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Restore service availability with security controls active", "org"),
            ctl("A.5.27", "Learning from information security incidents",
                "Analyze flooding attacks to improve capacity planning and mitigation", "org"),
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # CLUSTER 7 — Malware (Mlw)
    # ═══════════════════════════════════════════════════════════════════════════

    cells["7-GV"] = cell(
        local=[
            ctl("A.5.37", "Documented operating procedures",
                "Document malware prevention, detection, and response procedures", "org"),
            ctl("A.5.10", "Acceptable use of information and other associated assets",
                "Prohibit unauthorized software installation and removable media use", "org"),
        ],
        umbrella=[
            ctl("A.5.1", "Policies for information security",
                "Define anti-malware policies including allowed software, execution controls, and media handling", "org"),
            ctl("A.5.2", "Information security roles and responsibilities",
                "Assign ownership for malware defense program and incident handling", "org"),
        ],
    )

    cells["7-ID"] = cell(
        local=[
            ctl("A.8.8", "Management of technical vulnerabilities",
                "Identify vulnerabilities exploited by current malware campaigns for prioritized patching", "tech"),
            ctl("A.8.19", "Installation of software on operational systems",
                "Audit installed software against approved baseline to detect unauthorized additions", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Monitor malware threat intelligence (campaigns, families, IOCs targeting deployed platforms)", "org"),
            ctl("A.5.9", "Inventory of information and other associated assets",
                "Inventory all endpoints and their anti-malware coverage status", "org"),
        ],
    )

    cells["7-PR"] = cell(
        local=[
            ctl("A.8.7", "Protection against malware",
                "Deploy and maintain anti-malware controls (AV, EDR, application whitelisting)", "tech"),
            ctl("A.8.1", "User endpoint devices",
                "Harden endpoints against malware (disable autorun, restrict macros, enable application control)", "tech"),
            ctl("A.8.19", "Installation of software on operational systems",
                "Enforce application whitelisting and code signing requirements", "tech"),
            ctl("A.7.10", "Storage media",
                "Control removable storage media to prevent malware introduction", "tech"),
        ],
        umbrella=[
            ctl("A.6.3", "Information security awareness, education and training",
                "Train users to recognize malware delivery vectors (phishing, drive-by, USB)", "org"),
        ],
    )

    cells["7-DE"] = cell(
        local=[
            ctl("A.8.7", "Protection against malware",
                "Configure real-time malware detection with behavioral and signature-based engines", "tech"),
            ctl("A.8.15", "Logging",
                "Log process execution, file system changes, and network connections for malware activity detection", "tech"),
            ctl("A.8.16", "Monitoring activities",
                "Monitor endpoints for malware behavioral indicators (encryption activity, C2 beacons, lateral movement)", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Integrate malware IOC feeds into detection systems (hashes, domains, behaviors)", "org"),
        ],
    )

    cells["7-RS"] = cell(
        local=[
            ctl("A.5.28", "Collection of evidence",
                "Collect malware samples and forensic artifacts for analysis and attribution", "org"),
            ctl("A.5.25", "Assessment and decision on information security events",
                "Triage malware alerts and determine infection scope and impact", "org"),
        ],
        umbrella=[
            ctl("A.5.24", "Information security incident management planning and preparation",
                "Prepare malware incident playbooks (containment, eradication, recovery)", "org"),
            ctl("A.5.26", "Response to information security incidents",
                "Contain malware spread (isolate host, block C2, quarantine files)", "org"),
        ],
    )

    cells["7-RC"] = cell(
        local=[
            ctl("A.8.13", "Information backup",
                "Restore data from verified clean backups after malware eradication", "tech"),
            ctl("A.8.1", "User endpoint devices",
                "Reimage or restore infected endpoints to verified clean state", "tech"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Maintain security monitoring during malware cleanup and recovery", "org"),
            ctl("A.5.27", "Learning from information security incidents",
                "Conduct post-incident malware analysis to improve preventive controls", "org"),
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # CLUSTER 8 — Physical Attack (Phy)
    # ═══════════════════════════════════════════════════════════════════════════

    cells["8-GV"] = cell(
        local=[
            ctl("A.7.6", "Working in secure areas",
                "Establish rules for working in secure areas (no photography, escort requirements)", "tech"),
            ctl("A.5.37", "Documented operating procedures",
                "Document physical access procedures, visitor management, and emergency protocols", "org"),
        ],
        umbrella=[
            ctl("A.5.1", "Policies for information security",
                "Define physical security policies including perimeters, access control, and environmental protection", "org"),
            ctl("A.5.2", "Information security roles and responsibilities",
                "Assign ownership for physical security program", "org"),
        ],
    )

    cells["8-ID"] = cell(
        local=[
            ctl("A.7.1", "Physical security perimeters",
                "Assess physical perimeter adequacy and identify boundary weaknesses", "tech"),
            ctl("A.7.3", "Securing offices, rooms and facilities",
                "Identify sensitive areas requiring enhanced physical protection", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Monitor physical threat intelligence (local crime, targeted break-ins, insider threats)", "org"),
            ctl("A.5.9", "Inventory of information and other associated assets",
                "Inventory all physical locations, server rooms, and high-value asset locations", "org"),
        ],
    )

    cells["8-PR"] = cell(
        local=[
            ctl("A.7.2", "Physical entry",
                "Implement physical access controls (badges, biometrics, mantraps)", "tech"),
            ctl("A.7.8", "Equipment siting and protection",
                "Position equipment to minimize physical attack exposure", "tech"),
            ctl("A.7.5", "Protecting against physical and environmental threats",
                "Protect against environmental threats (fire, flood, power loss)", "tech"),
            ctl("A.7.7", "Clear desk and clear screen",
                "Enforce clear desk/screen policy to prevent physical information disclosure", "tech"),
        ],
        umbrella=[
            ctl("A.6.1", "Screening",
                "Screen personnel with physical access to sensitive areas", "org"),
            ctl("A.6.3", "Information security awareness, education and training",
                "Train staff on physical security awareness (tailgating, unauthorized access)", "org"),
        ],
    )

    cells["8-DE"] = cell(
        local=[
            ctl("A.7.4", "Physical security monitoring",
                "Monitor physical access points with CCTV, sensors, and alarms", "tech"),
            ctl("A.8.15", "Logging",
                "Log physical access events (badge reads, door opens, visitor entries)", "tech"),
            ctl("A.8.16", "Monitoring activities",
                "Monitor for physical security anomalies (after-hours access, repeated denied attempts)", "tech"),
        ],
        umbrella=[
            ctl("A.6.8", "Information security event reporting",
                "Enable staff to report physical security anomalies", "org"),
        ],
    )

    cells["8-RS"] = cell(
        local=[
            ctl("A.5.28", "Collection of evidence",
                "Preserve CCTV footage and access logs as evidence of physical breach", "org"),
        ],
        umbrella=[
            ctl("A.5.24", "Information security incident management planning and preparation",
                "Prepare response procedures for physical security breaches", "org"),
            ctl("A.5.26", "Response to information security incidents",
                "Contain physical breaches (lock down, isolate area, alert authorities)", "org"),
            ctl("A.5.5", "Contact with authorities",
                "Coordinate with law enforcement for physical security incidents", "org"),
        ],
    )

    cells["8-RC"] = cell(
        local=[
            ctl("A.7.13", "Equipment maintenance",
                "Repair and verify physical security equipment after incidents", "tech"),
            ctl("A.7.14", "Secure disposal or re-use of equipment",
                "Securely dispose of equipment compromised by physical attack", "tech"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Maintain security during physical facility recovery", "org"),
            ctl("A.5.27", "Learning from information security incidents",
                "Review physical security incidents to improve controls", "org"),
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # CLUSTER 9 — Social Engineering (SE)
    # ═══════════════════════════════════════════════════════════════════════════

    cells["9-GV"] = cell(
        local=[
            ctl("A.5.14", "Information transfer",
                "Define verification rules for information requests received via any channel", "org"),
            ctl("A.5.37", "Documented operating procedures",
                "Document verification procedures for unusual or high-risk requests", "org"),
        ],
        umbrella=[
            ctl("A.5.1", "Policies for information security",
                "Define policies addressing social engineering risks (phishing, pretexting, baiting)", "org"),
            ctl("A.5.2", "Information security roles and responsibilities",
                "Assign ownership for security awareness and anti-social-engineering program", "org"),
        ],
    )

    cells["9-ID"] = cell(
        local=[
            ctl("A.5.12", "Classification of information",
                "Classify information to define what must never be shared in response to unsolicited requests", "org"),
            ctl("A.6.8", "Information security event reporting",
                "Track social engineering attempt frequency and success rates", "org"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Monitor for social engineering campaigns targeting the organization or sector", "org"),
            ctl("A.5.9", "Inventory of information and other associated assets",
                "Identify high-value targets (executives, finance, IT admins) for social engineering", "org"),
        ],
    )

    cells["9-PR"] = cell(
        local=[
            ctl("A.8.23", "Web filtering",
                "Block access to known phishing and social engineering domains", "tech"),
            ctl("A.8.7", "Protection against malware",
                "Scan email attachments and links from social engineering vectors", "tech"),
            ctl("A.5.10", "Acceptable use of information and other associated assets",
                "Prohibit sharing credentials or sensitive information via social channels", "org"),
        ],
        umbrella=[
            ctl("A.6.3", "Information security awareness, education and training",
                "Train staff to recognize and resist social engineering (phishing simulations, pretexting drills)", "org"),
            ctl("A.6.6", "Confidentiality or non-disclosure agreements",
                "Enforce NDAs limiting what staff may disclose to external parties", "org"),
        ],
    )

    cells["9-DE"] = cell(
        local=[
            ctl("A.8.15", "Logging",
                "Log email security events (blocked phishing, URL detonation, attachment analysis)", "tech"),
            ctl("A.8.16", "Monitoring activities",
                "Monitor for social engineering indicators (email anomalies, impersonation, urgency patterns)", "tech"),
        ],
        umbrella=[
            ctl("A.6.8", "Information security event reporting",
                "Enable and encourage staff to report suspicious communications", "org"),
            ctl("A.5.7", "Threat intelligence",
                "Integrate social engineering IOCs (phishing domains, spoofed senders) into detection", "org"),
        ],
    )

    cells["9-RS"] = cell(
        local=[
            ctl("A.5.28", "Collection of evidence",
                "Preserve social engineering artifacts (emails, call logs, chat transcripts) as evidence", "org"),
            ctl("A.5.25", "Assessment and decision on information security events",
                "Assess social engineering incident scope and potential data exposure", "org"),
        ],
        umbrella=[
            ctl("A.5.24", "Information security incident management planning and preparation",
                "Prepare response playbooks for social engineering incidents (BEC, phishing, vishing)", "org"),
            ctl("A.5.26", "Response to information security incidents",
                "Contain social engineering incidents (block sender, reset credentials, warn staff)", "org"),
        ],
    )

    cells["9-RC"] = cell(
        local=[
            ctl("A.6.4", "Disciplinary process",
                "Address policy violations resulting from social engineering susceptibility", "org"),
            ctl("A.5.30", "ICT readiness for business continuity",
                "Include social engineering compromise recovery in continuity plans", "org"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Maintain awareness controls during recovery from social engineering incidents", "org"),
            ctl("A.5.27", "Learning from information security incidents",
                "Analyze social engineering incidents to improve training effectiveness", "org"),
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # CLUSTER 10 — Supply Chain Attack (SCA)
    # ═══════════════════════════════════════════════════════════════════════════

    cells["10-GV"] = cell(
        local=[
            ctl("A.5.21", "Managing information security in the ICT supply chain",
                "Define requirements for ICT supply chain integrity (signing, verification)", "org"),
            ctl("A.5.37", "Documented operating procedures",
                "Document vendor onboarding, assessment, and monitoring procedures", "org"),
        ],
        umbrella=[
            ctl("A.5.1", "Policies for information security",
                "Define supply chain security policies including vendor requirements and trust boundaries", "org"),
            ctl("A.5.19", "Information security in supplier relationships",
                "Establish information security requirements for supplier relationships", "org"),
            ctl("A.5.20", "Addressing information security within supplier agreements",
                "Include security clauses in all supplier contracts", "org"),
        ],
    )

    cells["10-ID"] = cell(
        local=[
            ctl("A.5.9", "Inventory of information and other associated assets",
                "Inventory all third-party components, libraries, and services in use", "org"),
            ctl("A.8.4", "Access to source code",
                "Identify all dependencies on external source code and assess supply chain risk", "tech"),
        ],
        umbrella=[
            ctl("A.5.7", "Threat intelligence",
                "Monitor for supply chain compromise campaigns (SolarWinds-type, dependency confusion)", "org"),
            ctl("A.5.22", "Monitoring, review and change management of supplier services",
                "Track changes in supplier services that could indicate compromise", "org"),
        ],
    )

    cells["10-PR"] = cell(
        local=[
            ctl("A.8.25", "Secure development life cycle",
                "Integrate supply chain security checks (dependency scanning, SBOM) into SDLC", "tech"),
            ctl("A.8.30", "Outsourced development",
                "Enforce security requirements for outsourced development (code review, integrity verification)", "tech"),
            ctl("A.8.19", "Installation of software on operational systems",
                "Verify integrity of software before installation (signatures, hashes)", "tech"),
        ],
        umbrella=[
            ctl("A.5.19", "Information security in supplier relationships",
                "Enforce supplier security requirements through contracts and assessments", "org"),
            ctl("A.5.23", "Information security for use of cloud services",
                "Secure cloud service supply chain (provider due diligence, exit plans)", "org"),
        ],
    )

    cells["10-DE"] = cell(
        local=[
            ctl("A.8.15", "Logging",
                "Log software update events, package installations, and third-party API calls", "tech"),
            ctl("A.8.16", "Monitoring activities",
                "Monitor for supply chain compromise indicators (unexpected update behavior, new network connections)", "tech"),
        ],
        umbrella=[
            ctl("A.5.22", "Monitoring, review and change management of supplier services",
                "Monitor supplier service changes for anomalous behavior indicating compromise", "org"),
            ctl("A.5.7", "Threat intelligence",
                "Integrate supply chain compromise IOCs into detection (malicious updates, backdoored packages)", "org"),
        ],
    )

    cells["10-RS"] = cell(
        local=[
            ctl("A.5.28", "Collection of evidence",
                "Preserve supply chain artifacts (package versions, update logs, integrity checksums) as evidence", "org"),
            ctl("A.5.25", "Assessment and decision on information security events",
                "Triage supply chain alerts and assess trust chain impact", "org"),
        ],
        umbrella=[
            ctl("A.5.24", "Information security incident management planning and preparation",
                "Prepare response procedures for supply chain compromise incidents", "org"),
            ctl("A.5.26", "Response to information security incidents",
                "Contain supply chain compromise (isolate affected components, halt updates, notify affected parties)", "org"),
        ],
    )

    cells["10-RC"] = cell(
        local=[
            ctl("A.5.30", "ICT readiness for business continuity",
                "Include supply chain compromise recovery (vendor switching, redeployment) in continuity plans", "org"),
            ctl("A.8.25", "Secure development life cycle",
                "Rebuild and verify supply chain integrity (re-audit dependencies, update SBOMs)", "tech"),
        ],
        umbrella=[
            ctl("A.5.29", "Information security during disruption",
                "Maintain security during supply chain incident recovery", "org"),
            ctl("A.5.27", "Learning from information security incidents",
                "Review supply chain incidents to strengthen vendor management and verification", "org"),
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # SUPPLEMENTARY — remaining Annex A controls placed in best-fit cells
    # ═══════════════════════════════════════════════════════════════════════════

    cells["7-GV"]["umbrella"].append(
        ctl("A.5.4", "Management responsibilities",
            "Ensure management enforces anti-malware controls and supports security investment", "org"))

    cells["2-ID"]["umbrella"].append(
        ctl("A.5.6", "Contact with special interest groups",
            "Engage ISACs and security communities for server vulnerability intelligence", "org"))

    cells["4-RC"]["local"].append(
        ctl("A.5.11", "Return of assets",
            "Ensure return of all access tokens, devices, and credentials upon separation", "org"))

    cells["9-PR"]["local"].append(
        ctl("A.5.13", "Labelling of information",
            "Label information classification visibly to prevent disclosure under social pressure", "org"))

    cells["10-GV"]["local"].append(
        ctl("A.5.32", "Intellectual property rights",
            "Ensure supply chain agreements address intellectual property rights and code ownership", "org"))

    cells["1-GV"]["local"].append(
        ctl("A.5.33", "Protection of records",
            "Protect audit records and logs from tampering via function abuse", "org"))

    cells["4-PR"]["local"].append(
        ctl("A.5.34", "Privacy and protection of PII",
            "Protect personally identifiable information to reduce identity theft impact", "org"))

    cells["2-GV"]["umbrella"].append(
        ctl("A.5.35", "Independent review of information security",
            "Commission independent security reviews of server infrastructure and controls", "org"))

    cells["8-GV"]["umbrella"].append(
        ctl("A.5.36", "Compliance with policies, rules and standards for information security",
            "Verify compliance with physical security policies and regulatory standards", "org"))

    cells["9-GV"]["umbrella"].append(
        ctl("A.6.2", "Terms and conditions of employment",
            "Include security responsibilities in employment terms addressing social engineering risks", "org"))

    cells["8-PR"]["local"].append(
        ctl("A.7.9", "Security of assets off-premises",
            "Secure assets during transport, at remote work locations, and while traveling", "tech"))

    cells["6-PR"]["local"].append(
        ctl("A.7.11", "Supporting utilities",
            "Protect supporting utilities (power, cooling, comms) to maintain availability", "tech"))

    cells["1-RC"]["local"].append(
        ctl("A.8.10", "Information deletion",
            "Ensure secure deletion of data exposed or compromised during function-abuse incidents", "tech"))

    cells["4-PR"]["local"].append(
        ctl("A.8.11", "Data masking",
            "Apply data masking to reduce exposure of sensitive identifiers in non-production contexts", "tech"))

    cells["1-DE"]["local"].append(
        ctl("A.8.12", "Data leakage prevention",
            "Deploy DLP controls to detect unauthorized data exfiltration via legitimate function abuse", "tech"))

    cells["2-PR"]["local"].append(
        ctl("A.8.28", "Secure coding",
            "Apply secure coding practices to prevent introduction of server-side vulnerabilities", "tech"))

    cells["2-ID"]["local"].append(
        ctl("A.8.29", "Security testing in development and acceptance",
            "Conduct security testing of server applications before deployment", "tech"))

    cells["2-PR"]["local"].append(
        ctl("A.8.31", "Separation of development, test and production environments",
            "Separate development, test, and production server environments to prevent cross-contamination", "tech"))

    cells["10-GV"]["local"].append(
        ctl("A.8.32", "Change management",
            "Manage changes to supply chain components with mandatory security review", "tech"))

    cells["2-GV"]["local"].append(
        ctl("A.8.33", "Test information",
            "Protect test information and ensure production data is not used without safeguards", "tech"))

    cells["1-GV"]["local"].append(
        ctl("A.8.34", "Protection of information systems during audit testing",
            "Protect systems during audit testing to prevent function abuse via test access", "tech"))

    return cells


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    cells = build_cells()

    data = {
        "version": "1.0.0",
        "tool": "TLCTC Control Matrix Manager",
        "exportDate": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "orgName": "ISO 27001:2022 Annex A Starter",
        "targetMaturity": 3,
        "environments": [
            {
                "id": "env-iso27001",
                "name": "ISO 27001:2022 Annex A",
                "cells": cells,
            }
        ],
        "sharedControls": [],
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # summary
    total = sum(
        len(c["local"]) + len(c["umbrella"])
        for c in cells.values()
    )
    print(f"Wrote {OUTPUT}")
    print(f"  Cells: {len(cells)}")
    print(f"  Controls: {total}")
    print(f"  Last ID: iso-{_id}")


if __name__ == "__main__":
    main()
