# TLCTC Operational Enumeration (Sub-Clusters)

**Companion to:** *A Cause-Oriented Cyber Threat Taxonomy: The TLCTC Framework* (the core paper)
**Layer:** Operational (the `TLCTC-XX.YY` sub-cluster catalogue)
**Status:** Living document — community-extensible, **not** frozen with the core's DOI.
**Author:** Bernhard Kreinz · License: CC BY 4.0
**Machine-readable twin:** `json-schemas/operational/tlctc-operational-enumeration.json` (validated by `tlctc-operational-enumeration.schema.json`; sub-cluster IDs use the same `TLCTC-XX.YY` shape that Layer-3 and Layer-4 already reference).

> **Why this is separate from the core.** The ten strategic clusters (`#1`–`#10`) are derived
> axiomatically and frozen as the citable core. The operational layer below them is the
> *extensible* part of the framework: sub-clusters are refinements, proposed and validated over
> time with community input. Keeping the enumeration here lets it evolve without re-minting the
> core's version/DOI, and keeps the core's "complete and mutually exclusive by construction"
> claim attached only to the strategic layer.

## 1. Naming and the governing principle

- **Strategic:** `#X` (and shorthand `#X.Y`). **Operational:** `TLCTC-XX.YY`.
- `TLCTC-XX.00` is the top-level cluster (reserved). `TLCTC-XX.Y0` (tens digit) is a **sub-cluster**
  — a *vector class*. `TLCTC-XX.YZ` (ones digit ≠ 0) is a **refinement** within a sub-cluster.
  This yields up to 81 operational positions per cluster (9 sub-clusters × 9 refinements).
  Strategic shorthand: `#X.Y` = `TLCTC-XX.Y0` (e.g. `#2.1` = `TLCTC-02.10`).
- **Governing principle (R-SUBCLUSTER):** every sub-cluster MUST reach the *same generic
  vulnerability* as its parent cluster, through a different vector (architectural path or physical
  mechanism). *If a candidate requires a different generic vulnerability, it is a different
  cluster, not a sub-cluster.* Sub-clusters never change the top-level meaning of cluster `XX`.

**Status legend:** **Reference** = decomposition published in the core as a method demonstration ·
**Proposed** = candidate awaiting community review / empirical validation · **Open** = no
decomposition yet; proposals welcome.

---

## 2. Reference decompositions (established in the core)

### #2 Exploiting Server — *generic vulnerability: code imperfection in server-side software*

The vectors decompose *where in the server's software architecture* the flaw resides.

| Operational ID | Strategic | Vector | Description |
|---|---|---|---|
| `TLCTC-02.10` | `#2.1` | Protocol vector | Server-side protocol-handling flaws |
| `TLCTC-02.20` | `#2.2` | Core function vector | Internal processing / parsing flaws |
| `TLCTC-02.30` | `#2.3` | External handler vector | Delegated processing flaws |

*Examples:* Heartbleed (server TLS) → `#2.1`; SQL injection via the query parser → `#2.2`; a flaw in a server-side PHP engine or Apache module → `#2.3`. Status: **Reference**.

### #3 Exploiting Client — *generic vulnerability: code imperfection in client-side software*

Mirrors `#2` (Axiom II), decomposing the same architectural layers on the client side.

| Operational ID | Strategic | Vector | Description |
|---|---|---|---|
| `TLCTC-03.10` | `#3.1` | Protocol vector | Client-side protocol-handling flaws |
| `TLCTC-03.20` | `#3.2` | Core function vector | Internal processing / parsing flaws |
| `TLCTC-03.30` | `#3.3` | External handler vector | Delegated processing flaws |

The `#2`/`#3` symmetry gives a complete 2×3 matrix (server/client × protocol/core/handler). Status: **Reference**.

### #8 Physical Attack — *generic vulnerability: physical accessibility of IT assets*

The vectors decompose the *physical mechanism of interaction*.

| Operational ID | Strategic | Vector | Description |
|---|---|---|---|
| `TLCTC-08.10` | `#8.1` | Mechanical vector | Physical contact with matter (tamper, theft, intrusion) |
| `TLCTC-08.20` | `#8.2` | Signal vector | Energy propagation, no contact (TEMPEST, acoustic, environmental) |

The mechanical/signal split is falsifiable physics, mapping to different control regimes (physical access control vs. emission/shielding). Status: **Reference**.

### #10 Supply Chain Attack — *generic vulnerability: necessary trust in third parties*

The vectors decompose the *temporal phase and medium* through which the trust link is exploited.

| Operational ID | Strategic | Vector | Description |
|---|---|---|---|
| `TLCTC-10.10` | `#10.1` | Update vector | Post-deployment, active delivery channel |
| `TLCTC-10.20` | `#10.2` | Development vector | Pre-deployment, silent insertion |
| `TLCTC-10.30` | `#10.3` | Hardware vector | Physical component supply chain |

*Examples:* compromised update → `#10.1`; malicious build-pipeline/dependency insertion → `#10.2`; manufacturing implant → `#10.3`. Status: **Reference**.

---

## 3. Open clusters — proposals welcome

The following six clusters have analytically feasible decompositions but no published reference set.
Proposed sub-clusters go here; each must satisfy R-SUBCLUSTER (same generic vulnerability, different vector).

### #1 Abuse of Functions — *generic vulnerability: inherent trust/scope/complexity of designed functionality*
Status: **Open**. *(Proposals to be added.)*

### #4 Identity Theft — *generic vulnerability: insufficient identity-artifact binding at point of use*
Status: **Open**. *(Proposals to be added.)*

### #5 Man in the Middle — *generic vulnerability: insufficient end-to-end protection of the channel*
Status: **Open**. *(Proposals to be added.)*

### #6 Flooding Attack — *generic vulnerability: finite capacity*
Status: **Open**. *(Proposals to be added.)*

### #7 Malware — *generic vulnerability: the environment's designed capability to execute foreign code*
Status: **Open**. *(Proposals to be added.)*

### #9 Social Engineering — *generic vulnerability: human susceptibility to manipulation*
Status: **Open**. *(Proposals to be added.)*

---

## 4. Contributing a sub-cluster

A proposal should provide, per sub-cluster: the operational ID (`TLCTC-XX.Y0`), strategic shorthand
(`#X.Y`), a vector name, a one-line description, and a short justification that it reaches the *same*
generic vulnerability as cluster `XX` through a distinct vector. Refinements (`TLCTC-XX.YZ`, `Z ≠ 0`)
may specialize a sub-cluster. Promotion from **Proposed** to **Reference** follows community review
and, where applicable, empirical validation against classified attack-path instances.
