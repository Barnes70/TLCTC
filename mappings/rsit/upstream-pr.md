# Upstream runbook: RSIT repository

Target: [enisaeu/Reference-Security-Incident-Taxonomy-Task-Force](https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force) (CC0, default branch `master`).
Route: **issue first, pull request second.** The session prepares the fork branch on request; the
owner opens the issue and the pull request (identity and the CC0 dedication are the owner's).

Context on the repository as of 2026-11-03:

- Issue [#70](https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/issues/70) (2019) asks to link RSIT to the ENISA threat taxonomy; the WG agreed in 2020 to sync "with upcoming version"; not done.
- Issue [#128](https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/issues/128): a maintainer (sebix) wrote that RSIT is "about the current state of an incident … not about how it came to be", and that a mapping to a related taxonomy "would be surely great to have".
- Issue [#126](https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/issues/126): governance under discussion (open consensus-based GitHub model proposed); contributions procedure in the README is marked deprecated.

## 1. Issue (owner opens)

**Title:** Proposal: rsit2tlctc — link RSIT values to a cause taxonomy (TLCTC), in the rsit2attck shape

**Body:**

```markdown
RSIT records the state of an incident; it deliberately does not say how the incident came to be
(as noted in #128). Issue #70 asked to link RSIT to the ENISA threat taxonomy. This proposal is
related but different: a link from RSIT to a cause taxonomy, as a crosswalk that changes nothing
in RSIT.

TLCTC (Top Level Cyber Threat Clusters) is an openly licensed, cause-oriented taxonomy: ten
non-overlapping clusters, each defined by the generic vulnerability an attacker exploits
(#1 Abuse of Functions … #10 Supply Chain Attack). For every RSIT value of machinev1 (version 1003),
the mapping states what the value already proves about the cause, and which question decides
where it does not. Some examples:

- Malicious Code / Infected System → #7 (the code ran); open question: how did it arrive?
- Intrusions / Unprivileged Account Compromise → #4 (a credential was used); open question: how was it obtained?
- Availability / Denial of Service → #6 (capacity) or #2/#3 (a defect crashes the component)
- Intrusion Attempts → the cluster of the attempted step; when blocked, a near miss (no successful step)
- Vulnerable → the cluster the exposure enables; no event
- Availability / Outage → no attacker, no cluster

The contribution would mirror working_copy/rsit2attck: a machinetag.json with one extra field,
`tlctc`, per value (ignored by MISP taxonomy processing), a generated rsit_2_tlctc.md table and a
small stdlib Python script to regenerate it. Only the seven values whose RSIT state proves the step
carry a TLCTC MISP machine tag; the others carry candidate clusters and the deciding question.

The mapping and its rationales:
https://github.com/Barnes70/TLCTC/tree/main/mappings/rsit
Rendered table: https://github.com/Barnes70/TLCTC/blob/main/mappings/rsit/upstream/rsit_2_tlctc.md
TLCTC core specification: https://doi.org/10.5281/zenodo.23437984

If this is welcome, I would open a pull request adding working_copy/rsit2tlctc/. The files would be
contributed under CC0 1.0, like the rest of this repository. Feedback on any individual value is
very welcome.
```

The links to `mappings/rsit` on `main` work only after the branch is merged and pushed in the TLCTC
repository. Open the issue after that push.

## 2. Fork branch (session, on the owner's request)

```bash
gh repo fork enisaeu/Reference-Security-Incident-Taxonomy-Task-Force --clone=false
git clone -c core.autocrlf=false https://github.com/Barnes70/Reference-Security-Incident-Taxonomy-Task-Force.git C:/Users/bkrei/Downloads/rsit
cd C:/Users/bkrei/Downloads/rsit
git remote add upstream https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force.git
git fetch upstream && git switch -c rsit2tlctc upstream/master
test "$(git rev-parse upstream/master)" = b9ad1f843025bb3e8aefa308cdaf0cc22d4f4b77 || echo "upstream moved: re-pin (PINNED.md) before continuing"
mkdir -p working_copy/rsit2tlctc
for f in machinetag.json rsit_2_tlctc.md machinetag2tlctc.py README.md; do    # committed LF bytes, never the CRLF working tree
  git -C ../tlctc show main:mappings/rsit/upstream/$f > working_copy/rsit2tlctc/$f
done
python3 working_copy/rsit2tlctc/machinetag2tlctc.py working_copy/rsit2tlctc/machinetag.json /tmp/check.md \
  && diff /tmp/check.md working_copy/rsit2tlctc/rsit_2_tlctc.md \
  && ! grep -lU $'\r' working_copy/rsit2tlctc/* \
  && git add working_copy/rsit2tlctc \
  && git commit -m "Add rsit2tlctc: RSIT → TLCTC crosswalk (tlctc field per value, generated table)" \
  && git push -u origin rsit2tlctc
```

The chain stops before `git add` if the table does not regenerate identically or any file has a CR.
The copies come from the committed blobs on `main` (LF), so the TLCTC branch must be merged first.

## 3. Pull request (owner runs)

```bash
cd C:/Users/bkrei/Downloads/rsit
gh pr create --repo enisaeu/Reference-Security-Incident-Taxonomy-Task-Force --base master --head Barnes70:rsit2tlctc \
  --title "Add rsit2tlctc: RSIT → TLCTC crosswalk" \
  --body "As proposed in #<issue>: adds working_copy/rsit2tlctc/ in the shape of rsit2attck — machinetag.json (machinev1 1003 + a tlctc field per value, ignored by MISP), the generated rsit_2_tlctc.md and machinetag2tlctc.py to regenerate it. No change to any RSIT class or description. Contributed under CC0 1.0. Rationales per value: https://github.com/Barnes70/TLCTC/tree/main/mappings/rsit"
```

## 4. If maintainers ask for changes

Edit `tlctc-rsit.json` in the TLCTC repository, `npm run build-rsit && npm run validate-rsit`, copy
`upstream/*` into the clone (LF), commit, push to the same branch; the pull request updates itself.
If RSIT's `machinev1` changes first, follow the refresh recipe in `PINNED.md`.
