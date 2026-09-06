# Pinned upstream schemas

| File | Upstream | Commit | Pinned on |
|---|---|---|---|
| `taxonomies/schema.misp-taxonomy.json` | `MISP/misp-taxonomies` `schema.json` | `7b66073f68b1d7323542638b38c31442b38d366b` | 2026-09-06 |
| `objects/schema_objects.misp.json` | `MISP/misp-objects` `schema_objects.json` | `e8293d393fd4bfdb25e582dd36ae0262f8adbd04` | 2026-09-06 |

Both schemas use the draft-04 `id` keyword. `scripts/validate-misp.js` deletes
`$schema` and `id` before compiling with ajv (`strict: false`); the schema
semantics are otherwise unchanged. Refresh by re-running the two `curl` lines
in the implementation plan with a newer commit and updating this table.
