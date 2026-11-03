# Pinned upstream file

| Item | Value |
|---|---|
| Repository | [enisaeu/Reference-Security-Incident-Taxonomy-Task-Force](https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force) |
| Commit | `b9ad1f843025bb3e8aefa308cdaf0cc22d4f4b77` (2026-05-13, master) |
| File | `working_copy/machinev1` → `pinned/machinev1` |
| RSIT version | 1003 (39 values in 11 predicates) |
| sha256 (LF bytes as served by GitHub) | `bfaa07dd3d578ffa628170c49cdaa04b6fea8f27d8b80b2850569503fb0a53d6` |
| Licence | CC0 1.0 (RSIT repository) |

`machinev1` is the master file of RSIT; the MISP taxonomy `rsit/machinetag.json` is generated from
it and was also at version 1003 with 39 values on 2026-11-03. The validator hashes the file after
normalising CRLF to LF, because a Windows checkout with `core.autocrlf=true` rewrites line endings.

## Refresh recipe

```bash
C=<new master commit>
gh api "repos/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force/contents/working_copy/machinev1?ref=$C" \
  -H "Accept: application/vnd.github.raw" > mappings/rsit/pinned/machinev1
sha256sum mappings/rsit/pinned/machinev1      # update the table above and metadata.rsit_source in tlctc-rsit.json
npm run validate-rsit                         # names every RSIT value added, renamed or removed
```

Map any new value in `tlctc-rsit.json`, then `npm run build-rsit` to regenerate `upstream/`.
