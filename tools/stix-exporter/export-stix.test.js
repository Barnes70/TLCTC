// Round-trip smoke test for export-stix.js.
// Run: node export-stix.test.js

const path = require('path');
const fs = require('fs');
const assert = require('assert');
const { exportPath, extractAttackTechniqueIds, strategicCluster, clusterDisplayName } = require('./export-stix');

const repoRoot = path.resolve(__dirname, '..', '..');
const solarPath = path.join(repoRoot, 'json-schemas', 'layer-3', 'examples', 'solarwinds-2020.json');
const adPath = path.join(repoRoot, 'attack-paths', 'ad-domain-admin-cascade-2025.json');

function loadJson(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }

function findStepSDO(bundle, stepId) {
  return bundle.objects.find(o => o.x_tlctc_step_id === stepId);
}

function findReport(bundle) {
  return bundle.objects.find(o => o.type === 'report');
}

function findRelationships(bundle) {
  return bundle.objects.filter(o => o.type === 'relationship');
}

function findPrecedesEdges(bundle) {
  return findRelationships(bundle).filter(r => r.x_tlctc_relation === 'precedes');
}

function run() {
  let passed = 0;
  let failed = 0;
  const cases = [];

  function test(name, fn) {
    try {
      fn();
      console.log(`  ok  ${name}`);
      passed++;
    } catch (e) {
      console.log(`  FAIL ${name}: ${e.message}`);
      failed++;
      cases.push({ name, err: e });
    }
  }

  // --- pure helpers ---
  console.log('helpers:');
  test('strategicCluster maps #X', () => {
    assert.strictEqual(strategicCluster('#7'), '#7');
  });
  test('strategicCluster maps TLCTC-XX.YY', () => {
    assert.strictEqual(strategicCluster('TLCTC-07.03'), '#7');
  });
  test('extractAttackTechniqueIds finds Txxxx and Txxxx.NNN', () => {
    const ids = extractAttackTechniqueIds({
      notes: 'See T1078 and T1059.001 for details.',
      evidence_refs: ['T1003']
    });
    assert.deepStrictEqual([...ids].sort(), ['T1003', 'T1059.001', 'T1078']);
  });
  test('clusterDisplayName labels strategic clusters', () => {
    assert.ok(clusterDisplayName('#7').includes('Malware'));
  });

  // --- SolarWinds bundle ---
  console.log('solarwinds:');
  const solar = loadJson(solarPath);
  const solarBundle = exportPath(solar);

  test('bundle is STIX 2.1 bundle shape', () => {
    assert.strictEqual(solarBundle.type, 'bundle');
    assert.ok(solarBundle.id.startsWith('bundle--'));
    assert.ok(Array.isArray(solarBundle.objects));
  });

  test('report SDO references all other objects', () => {
    const report = findReport(solarBundle);
    assert.ok(report);
    const others = solarBundle.objects.filter(o => o.type !== 'report');
    assert.strictEqual(report.object_refs.length, others.length);
    assert.strictEqual(report.x_tlctc_incident_id, 'SOLARWINDS-SUNBURST-2020');
  });

  test('s1-supply-chain step retains cluster + boundary', () => {
    const s1 = findStepSDO(solarBundle, 's1-supply-chain');
    assert.ok(s1, 's1 step missing');
    assert.strictEqual(s1.x_tlctc_cluster, '#10');
    assert.deepStrictEqual(s1.x_tlctc_boundary, {
      context: 'update',
      source_sphere: '@Vendor',
      target_sphere: '@Org'
    });
  });

  test('s2 retains fec_executed', () => {
    const s2 = findStepSDO(solarBundle, 's2-sunburst-execution');
    assert.strictEqual(s2.x_tlctc_cluster, '#7');
    assert.strictEqual(s2.x_tlctc_fec, true);
  });

  test('s3 retains DRE outcomes', () => {
    const s3 = findStepSDO(solarBundle, 's3-credential-forgery');
    assert.deepStrictEqual(s3.x_tlctc_dre, ['C']);
  });

  test('precedes edges match step count - 1', () => {
    const edges = findPrecedesEdges(solarBundle);
    assert.strictEqual(edges.length, solar.path_sequence.length - 1);
  });

  test('first precedes edge carries Δt = instant', () => {
    const edges = findPrecedesEdges(solarBundle);
    assert.strictEqual(edges[0].x_tlctc_delta_t, 'instant');
  });

  test('cluster ID surfaces as external_reference for tlctc source', () => {
    const s1 = findStepSDO(solarBundle, 's1-supply-chain');
    const ref = s1.external_references.find(r => r.source_name === 'tlctc');
    assert.ok(ref);
    assert.strictEqual(ref.external_id, '#10');
  });

  // --- AD cascade bundle ---
  console.log('ad-domain-admin-cascade:');
  const ad = loadJson(adPath);
  const adBundle = exportPath(ad);

  test('unresolved gap step is emitted with x_tlctc_status=unresolved', () => {
    const s0 = findStepSDO(adBundle, 's0-acquisition-prefix');
    assert.ok(s0);
    assert.strictEqual(s0.x_tlctc_status, 'unresolved');
    assert.strictEqual(s0.x_tlctc_unresolved_type, 'gap');
    assert.ok(!s0.x_tlctc_cluster, 'unresolved step must not carry x_tlctc_cluster');
    assert.ok(!s0.x_tlctc_dre, 'unresolved step must not carry x_tlctc_dre (R-UNRES-5)');
    assert.ok(Array.isArray(s0.x_tlctc_candidates));
  });

  test('s1 RDP foothold preserves topology boundary', () => {
    const s1 = findStepSDO(adBundle, 's1-rdp-foothold');
    assert.deepStrictEqual(s1.x_tlctc_boundary, {
      context: 'prod',
      source_sphere: '@Attacker',
      target_sphere: '@Org'
    });
  });

  test('s6b acquisition retains DRE:C', () => {
    const s6b = findStepSDO(adBundle, 's6b-credential-harvest');
    assert.deepStrictEqual(s6b.x_tlctc_dre, ['C']);
  });

  test('s6c application has no DRE (R-CRED)', () => {
    const s6c = findStepSDO(adBundle, 's6c-harvested-cred-application');
    assert.ok(!s6c.x_tlctc_dre, 's6c must not carry DRE per R-CRED');
  });

  test('s8 exfil step preserves fec_executed and DRE:C', () => {
    const s8 = findStepSDO(adBundle, 's8-exfil-tool-exec');
    assert.strictEqual(s8.x_tlctc_fec, true);
    assert.deepStrictEqual(s8.x_tlctc_dre, ['C']);
  });

  test('precedes edge count matches sequence length - 1', () => {
    const edges = findPrecedesEdges(adBundle);
    assert.strictEqual(edges.length, ad.path_sequence.length - 1);
  });

  test('every SDO has a STIX 2.1 spec_version', () => {
    for (const o of adBundle.objects) {
      if (o.type === 'bundle') continue;
      assert.strictEqual(o.spec_version, '2.1', `${o.type} ${o.id} missing spec_version`);
    }
  });

  console.log(`\n${passed} passed, ${failed} failed`);
  if (failed > 0) {
    process.exit(1);
  }
}

run();
