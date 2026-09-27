# Agent Skills discovery endpoint — tlctc.net/.well-known/skills/

tlctc.net publishes the `tlctc-classify` agent skill at an Agent Skills discovery endpoint:

```
https://www.tlctc.net/.well-known/skills/index.json
https://www.tlctc.net/.well-known/skills/tlctc-classify/SKILL.md
```

This is the **CC BY 4.0 web edition** of the skill: the complete TLCTC v2.6 analysis system
(10 axioms, 10 clusters, 17 R-* rules, SRE doctrine, DRE refinement tree, attack-path notation),
with `license: CC-BY-4.0`, `author` and an attribution line. The ClawHub edition in
[`../clawhub/`](../clawhub/) carries the same text under ClawHub's MIT-0 terms.

```
integrations/well-known/
├── README.md                     this file (not published)
└── skills/                       mirrored to the site's /.well-known/skills/
    ├── index.json                generated
    └── tlctc-classify/
        └── SKILL.md              generated
```

## Installing

| Harness | Command | Copy |
|---|---|---|
| Hermes Agent (Nous Research) | `hermes skills install well-known:https://www.tlctc.net/.well-known/skills/tlctc-classify` | this CC BY edition, from tlctc.net |
| Hermes Agent | `hermes skills install Barnes70/TLCTC/plugins/tlctc/skills/tlctc-classify` | the plugin skill (CC BY), straight from GitHub |
| Hermes Agent | `hermes skills install clawhub/@barnes70/tlctc-classify` | the ClawHub edition (MIT-0) |
| OpenClaw | `openclaw skills install @barnes70/tlctc-classify` | the ClawHub edition (MIT-0) |

Hermes treats all three sources as community trust and scans every skill before installing;
community skills rated "caution" or worse are blocked unless forced. The skill scans **SAFE**
(checked 2026-09-27 with Hermes' own `tools/skills_guard.py`; one LOW finding for the
`CLAUDE.md` mention). Rescan after changing the skill's preamble.

## How the edition is made and published

Never edit the generated files. `scripts/build-skill-editions.js` renders both editions from
[`plugins/tlctc/skills/tlctc-classify/SKILL.md`](../../plugins/tlctc/skills/tlctc-classify/SKILL.md);
`scripts/validate-skill-editions.js` (part of `npm run validate`) checks them, including that
`index.json` lists the skill with the same name and description and `files: ["SKILL.md"]`.

```
npm run build-skills && npm run validate-skills
npm run site            # step 8c mirrors skills/ into the site tree's .well-known/skills/
```

The site's `deploy-changed.ps1` deploys the `.md` files that `.well-known/skills/index.json`
lists (unlinked Markdown is otherwise held back) and verifies `.well-known/` over HTTPS.
