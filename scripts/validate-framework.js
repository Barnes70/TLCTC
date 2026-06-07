// Validates a TLCTC framework JSON against the Layer-1 schema.
// Usage: node scripts/validate-framework.js <schema.json> <data.json>
const fs = require("fs");
const Ajv = require("ajv");
const addFormats = require("ajv-formats");

const [, , schemaPath, dataPath] = process.argv;
const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
const data = JSON.parse(fs.readFileSync(dataPath, "utf8"));

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);

const validate = ajv.compile(schema);
if (validate(data)) {
  console.log("VALID");
} else {
  console.log("INVALID");
  console.log(JSON.stringify(validate.errors, null, 2));
  process.exit(1);
}
