#!/usr/bin/env python3
"""
ETDA Threat Group Cards → TLCTC Actor Profile Scoring Engine

Scores 514 ETDA actors against TLCTC clusters using:
  - Tool arsenal analysis (type/category mapping)
  - Description text mining (keyword signals)
  - Calibrated against 20 expert-scored Mandiant/CrowdStrike actors

Output: JSON dataset ready for embedding in actor-profile-designer.html
"""
import json, re, sys
from collections import Counter

# ── Load data ──────────────────────────────────────────────────────
with open('../input4new/tgc-actors.json', encoding='utf-8') as f:
    etda = json.load(f)
with open('../input4new/tgc-tools.json', encoding='utf-8') as f:
    tools_data = json.load(f)

tool_map = {t['uuid']: t for t in tools_data['values']}

# ── Country code → name mapping ────────────────────────────────────
COUNTRY_MAP = {
    'CN': 'China', 'RU': 'Russia', 'KP': 'North Korea', 'IR': 'Iran',
    'PK': 'Pakistan', 'VN': 'Vietnam', 'IN': 'India', 'US': 'USA',
    'IL': 'Israel', 'KR': 'South Korea', 'TR': 'Turkey', 'UA': 'Ukraine',
    'BY': 'Belarus', 'SY': 'Syria', 'LB': 'Lebanon', 'NG': 'Nigeria',
    'BR': 'Brazil', 'TN': 'Tunisia', 'EG': 'Egypt', 'SA': 'Saudi Arabia',
    'PS': 'Palestine', 'GB': 'UK', 'DE': 'Germany', 'FR': 'France',
    'TW': 'Taiwan', 'MM': 'Myanmar', 'PH': 'Philippines', 'MX': 'Mexico',
    'CO': 'Colombia', 'DZ': 'Algeria', 'MA': 'Morocco', 'ET': 'Ethiopia',
    'UZ': 'Uzbekistan', 'AZ': 'Azerbaijan', 'KZ': 'Kazakhstan',
    'AE': 'UAE', 'JP': 'Japan', 'ES': 'Spain', 'NL': 'Netherlands',
    'SE': 'Sweden', 'HK': 'Hong Kong',
}

# Map ETDA origins to the app's ORIGINS list for filtering
ORIGIN_NORMALIZE = {
    'China': 'China', 'Russia': 'Russia', 'North Korea': 'North Korea',
    'Iran': 'Iran', 'Pakistan': 'Pakistan', 'Vietnam': 'Vietnam',
    'Belarus': 'Russia',
}

# Map ETDA cfr-target-category to app's TARGET_SECTORS
SECTOR_MAP = {
    'Aerospace': 'Aerospace & Defense', 'Defense': 'Aerospace & Defense',
    'Aviation': 'Aerospace & Defense',
    'Financial': 'Financial Services', 'Banking': 'Financial Services',
    'Government': 'Government', 'Embassies': 'Government',
    'Think Tanks': 'Civil Society & NGOs', 'NGOs': 'Civil Society & NGOs',
    'Civil society': 'Civil Society & NGOs', 'Dissidents': 'Civil Society & NGOs',
    'Technology': 'Technology', 'IT': 'Technology', 'Software': 'Technology',
    'Electronics': 'Technology', 'Telecommunications': 'Telecommunications',
    'Healthcare': 'Healthcare', 'Pharmaceutical': 'Pharma & Biotech',
    'Pharma': 'Pharma & Biotech', 'Chemical': 'Pharma & Biotech',
    'Education': 'Education', 'Academia': 'Education', 'Research': 'Education',
    'Energy': 'Energy & Utilities', 'Oil and gas': 'Energy & Utilities',
    'Utilities': 'Energy & Utilities',
    'Manufacturing': 'Manufacturing', 'Industrial': 'Manufacturing',
    'Construction': 'Manufacturing', 'Engineering': 'Manufacturing',
    'Automotive': 'Manufacturing',
    'Media': 'Media & Entertainment', 'Entertainment': 'Media & Entertainment',
    'Journalism': 'Media & Entertainment',
    'Shipping and Logistics': 'Transportation & Logistics',
    'Transportation': 'Transportation & Logistics',
    'Legal': 'Legal & Professional Services',
    'Hospitality': 'Retail & Hospitality', 'Retail': 'Retail & Hospitality',
    'Gaming': 'Gaming', 'Maritime': 'Maritime', 'Nuclear': 'Nuclear',
    'Mining': 'Critical Infrastructure', 'Water': 'Critical Infrastructure',
    'Food and Agriculture': 'Critical Infrastructure',
    'Critical infrastructure': 'Critical Infrastructure',
}

# Map ETDA motivation to app's MOTIVATIONS
MOTIVATION_MAP = {
    'Information theft and espionage': 'Espionage',
    'Espionage': 'Espionage',
    'Cyber espionage': 'Espionage',
    'Financial crime': 'Financial Gain',
    'Financial gain': 'Financial Gain',
    'Sabotage and destruction': 'Sabotage / Destruction',
    'Sabotage': 'Sabotage / Destruction',
    'Destruction': 'Sabotage / Destruction',
    'Ideology': 'Information Operations',
    'Hacktivism': 'Information Operations',
    'Information operations': 'Information Operations',
    'Surveillance': 'Surveillance',
}

VALID_MOTIVATIONS = {'Espionage', 'Financial Gain', 'IP Theft', 'Information Operations', 'Sabotage / Destruction', 'Surveillance'}

# ── Build tool profile per actor ───────────────────────────────────
def get_tool_profile(actor):
    types = Counter()
    cats = Counter()
    tool_names = []
    for r in actor.get('related', []):
        if r['type'] == 'uses' and r['dest-uuid'] in tool_map:
            t = tool_map[r['dest-uuid']]
            tool_names.append(t['value'])
            cat = t.get('meta', {}).get('category', '')
            if cat:
                cats[cat] += 1
            for tp in t.get('meta', {}).get('type', []):
                types[tp] += 1
    # Only count DDoS tools where DDoS is a primary purpose (<=3 types)
    ddos_dedicated = 0
    for r in actor.get('related', []):
        if r['type'] == 'uses' and r['dest-uuid'] in tool_map:
            t = tool_map[r['dest-uuid']]
            ttypes = t.get('meta', {}).get('type', [])
            if 'DDoS' in ttypes and len(ttypes) <= 3:
                ddos_dedicated += 1

    return {
        'total': len(tool_names),
        'names': tool_names,
        'cats': dict(cats),
        'types': dict(types),
        'malware': cats.get('Malware', 0),
        'dual_use': cats.get('Tools', 0),
        'exploits': cats.get('Exploits', 0),
        'cred': types.get('Credential stealer', 0) + types.get('Keylogger', 0),
        'info_stealer': types.get('Info stealer', 0),
        'backdoor': types.get('Backdoor', 0),
        'ransomware': types.get('Ransomware', 0),
        'wiper': types.get('Wiper', 0),
        'ddos': ddos_dedicated,
        'rootkit': types.get('Rootkit', 0),
        'vuln_scanner': types.get('Vulnerability scanner', 0),
        'tunneling': types.get('Tunneling', 0),
        'botnet': types.get('Botnet', 0),
        'loader': types.get('Loader', 0),
        'worm': types.get('Worm', 0),
    }

# ── Text signal detection ──────────────────────────────────────────
def text_signals(desc):
    d = desc if desc else ''
    return {
        'phishing': bool(re.search(r'phish|spear.?phish|smishing|vishing|lure|pretexting|impersonat|social.engineer', d, re.I)),
        'phishing_weak': bool(re.search(r'email.*campaign|malicious.*email|targeted.*email|deliver.*attachment|email.*attachment|email.*link', d, re.I)),
        'server_exploit': bool(re.search(r'web.?shell|sql.inject|remote code execution|RCE|server.?side|exploit.*vuln|CVE-\d|zero.?day|0.?day', d, re.I)),
        'client_exploit': bool(re.search(r'browser.exploit|drive.by|document.exploit|macro|\.rtf|\.doc.*exploit|flash.exploit|java.exploit|client.side', d, re.I)),
        'credential': bool(re.search(r'credential|brute.force|password|pass.the.hash|stolen.*account|compromised.*account|credential.dump', d, re.I)),
        'mitm': bool(re.search(r'man.in.the.middle|intercept|eavesdrop|DNS.spoof|ARP.spoof|MITM|network.sniff', d, re.I)),
        'ddos': bool(re.search(r'\bDDoS\b|denial.of.service|\bflood(?:ing)?\s+attack', d, re.I)),
        'physical': bool(re.search(r'physical|USB|removable|air.gap|hardware.implant', d, re.I)),
        'supply_chain': bool(re.search(r'supply.chain|trojaniz|compromise.*update|trusted.relationship|software.update.*compromise', d, re.I)),
        'abuse_functions': bool(re.search(r'legitimate.tool|living.off.the.land|LOLBin|powershell|lateral.movement|WMI|psexec|misuse', d, re.I)),
        'ransomware': bool(re.search(r'ransomware|ransom|encrypt.*file|big.game.hunting', d, re.I)),
        'wiper': bool(re.search(r'wiper|destruct|sabotag', d, re.I)),
        'watering_hole': bool(re.search(r'watering.hole|strategic.web.compromise', d, re.I)),
    }

# ── SCORING FUNCTION ───────────────────────────────────────────────
def score_actor(actor, tp, ts):
    s = [1,1,1,1,1,1,1,1,1,1]

    # #7 Malware (index 6)
    m = tp['malware']
    if m >= 30 or (m >= 20 and tp['total'] >= 45):
        s[6] = 4
    elif m >= 9:
        s[6] = 3
    elif m >= 3:
        s[6] = 2
    if ts['ransomware'] and s[6] < 3:
        s[6] = max(s[6], 2)
    if tp['rootkit'] >= 2:
        s[6] = min(s[6] + 1, 4)
    if tp['worm'] >= 2:
        s[6] = min(s[6] + 1, 4)

    # #4 Identity Theft (index 3)
    c = tp['cred']
    if c >= 9:
        s[3] = 3
    elif c >= 4:
        s[3] = 2
    if ts['credential'] and s[3] < 3:
        s[3] = min(s[3] + 1, 3)

    # #1 Abuse of Functions (index 0)
    d = tp['dual_use']
    if d >= 12:
        s[0] = 3
    elif d >= 4:
        s[0] = 2
    if ts['abuse_functions'] and s[0] < 3:
        s[0] = min(s[0] + 1, 3)
    if tp['total'] >= 40 and s[0] < 3:
        s[0] = max(s[0], 2)

    # #2 Exploiting Server (index 1)
    e = tp['exploits'] + tp['vuln_scanner']
    if e >= 3:
        s[1] = 3
    elif e >= 1:
        s[1] = 2
    if ts['server_exploit'] and s[1] < 3:
        s[1] = min(s[1] + 1, 3)
    if ts['watering_hole'] and s[1] < 3:
        s[1] = min(s[1] + 1, 3)

    # #3 Exploiting Client (index 2)
    if ts['client_exploit']:
        s[2] = max(s[2], 2)
    if ts['watering_hole']:
        s[2] = max(s[2], 2)
    zero_days = sum(1 for r in actor.get('related', [])
                    if r['type'] == 'uses' and r['dest-uuid'] in tool_map
                    and '0-day' in tool_map[r['dest-uuid']].get('meta',{}).get('type',[]))
    if zero_days >= 2:
        s[2] = max(s[2], 3)
    elif zero_days >= 1:
        s[2] = max(s[2], 2)

    # #9 Social Engineering (index 8)
    if ts['phishing']:
        s[8] = max(s[8], 3)
    elif ts['phishing_weak']:
        s[8] = max(s[8], 2)
    # Espionage-motivated APTs with significant arsenals almost always use SE
    motiv = [m.lower() for m in actor.get('meta', {}).get('motivation', [])]
    is_espionage = any('espionage' in m for m in motiv)
    if is_espionage and tp['total'] >= 10 and s[8] < 2:
        s[8] = 2

    # #5 Man in the Middle (index 4)
    if ts['mitm']:
        s[4] = max(s[4], 2)
    if tp['tunneling'] >= 5:
        s[4] = max(s[4], 2)

    # #6 Flooding (index 5)
    if tp['ddos'] >= 2:
        s[5] = 3
    elif tp['ddos'] >= 1 or ts['ddos']:
        s[5] = 2
    if tp['botnet'] >= 2:
        s[5] = max(s[5], 2)

    # #8 Physical (index 7)
    if ts['physical']:
        s[7] = max(s[7], 2)

    # #10 Supply Chain (index 9)
    if ts['supply_chain']:
        s[9] = max(s[9], 2)

    return s

# ── Expert actors for calibration ─────────────────────────────────
EXPERTS = {
    'apt 41':          [3,2,3,3,1,1,4,1,3,1],
    'leviathan':       [2,1,1,2,1,1,4,1,3,1],
    'zirconium':       [1,2,3,1,1,1,2,1,1,1],
    'naikon':          [2,1,1,1,1,1,3,2,1,1],
    'emissary panda':  [2,3,2,2,1,1,2,1,3,1],
    'cozy bear':       [3,3,1,3,1,1,4,1,3,2],
    'fancy bear':      [2,3,2,3,1,1,4,1,3,1],
    'sandworm':        [3,3,2,2,1,1,4,1,2,2],
    'kimsuky':         [2,1,1,3,1,1,3,1,4,1],
    'reaper':          [1,2,3,1,1,1,3,1,3,1],
    'charming kitten': [2,1,1,3,1,1,3,1,4,1],
    'elfin':           [2,2,1,2,1,1,3,1,3,1],
    'oilrig':          [2,2,1,2,1,1,3,1,3,1],
    'comment crew':    [2,2,1,2,1,1,3,1,3,1],
    'gothic panda':    [1,1,3,1,1,1,3,1,1,1],
    'menupass':        [2,2,1,2,1,1,3,1,3,2],
    'turla':           [3,2,1,2,2,1,4,1,2,2],
    'fin7':            [3,1,1,2,1,1,3,1,3,1],
    'fin11':           [2,2,1,2,1,1,3,1,2,1],
    'chafer':          [2,1,1,2,1,1,2,1,3,1],
}

# Build ETDA lookup by name/synonym
etda_lookup = {}
for a in etda['values']:
    names = [a['value'].lower().strip()]
    for s in a.get('meta', {}).get('synonyms', []):
        names.append(s.lower().strip())
    for part in a['value'].split(','):
        names.append(part.strip().lower())
    for n in names:
        etda_lookup[n] = a

# ── Calibration run ───────────────────────────────────────────────
LABELS = ['#1 AoF','#2 Srv','#3 Cli','#4 IdT','#5 MitM','#6 Fld','#7 Mal','#8 Phy','#9 SE','#10 SC']
total_correct = 0
total_cells = 0
total_off_by_1 = 0

print("=== CALIBRATION: Heuristic vs Expert ===")
for expert_name, expert_scores in EXPERTS.items():
    if expert_name not in etda_lookup:
        print(f"  SKIP: {expert_name} not in ETDA")
        continue
    actor = etda_lookup[expert_name]
    tp = get_tool_profile(actor)
    ts = text_signals(actor.get('description', ''))
    heuristic = score_actor(actor, tp, ts)

    match = sum(1 for h, e in zip(heuristic, expert_scores) if h == e)
    off1 = sum(1 for h, e in zip(heuristic, expert_scores) if abs(h - e) <= 1)
    total_correct += match
    total_cells += 10
    total_off_by_1 += off1

    diffs = []
    for i, (h, e) in enumerate(zip(heuristic, expert_scores)):
        if h != e:
            diffs.append(f"{LABELS[i]}:h{h}/e{e}")
    diff_str = ', '.join(diffs) if diffs else 'PERFECT'
    print(f"  {expert_name:20s} exact={match}/10  ±1={off1}/10  | {diff_str}")

print(f"\n  TOTAL: exact={total_correct}/{total_cells} ({100*total_correct/total_cells:.0f}%)  ±1={total_off_by_1}/{total_cells} ({100*total_off_by_1/total_cells:.0f}%)")

# ── Generate full dataset ──────────────────────────────────────────
output_actors = []
for actor in etda['values']:
    tp = get_tool_profile(actor)
    ts = text_signals(actor.get('description', ''))
    scores = score_actor(actor, tp, ts)

    # Name: use value, include synonyms
    name_parts = [p.strip() for p in actor['value'].split(',')]
    synonyms = actor.get('meta', {}).get('synonyms', [])
    all_names = list(dict.fromkeys(name_parts + synonyms))
    if len(all_names) > 3:
        display_name = ', '.join(all_names[:3])
    else:
        display_name = ', '.join(all_names)

    # Country
    cc = actor.get('meta', {}).get('country', '')
    country_name = COUNTRY_MAP.get(cc, '')
    origin = ORIGIN_NORMALIZE.get(country_name, 'Unknown') if country_name else 'Unknown'

    # Motivation
    raw_motiv = actor.get('meta', {}).get('motivation', [])
    motivations = list(dict.fromkeys(
        MOTIVATION_MAP.get(m, m) for m in raw_motiv
        if MOTIVATION_MAP.get(m, m) in VALID_MOTIVATIONS
    ))

    # Target sectors
    raw_targets = actor.get('meta', {}).get('cfr-target-category', [])
    sectors = list(dict.fromkeys(
        SECTOR_MAP[t] for t in raw_targets if t in SECTOR_MAP
    ))

    # Sequence
    scored_clusters = [(scores[i], i+1) for i in range(10) if scores[i] > 1]
    scored_clusters.sort(key=lambda x: -x[0])
    sequence = ' \u2192 '.join(f'#{c:02d}' for _, c in scored_clusters) if scored_clusters else ''

    # Notes
    notes_parts = []
    desc = actor.get('description', '').strip()
    if desc and 'mentioned in a summary report only' not in desc.lower():
        first_sent = desc.split('.')[0] + '.'
        if len(first_sent) > 250:
            first_sent = desc[:247] + '...'
        notes_parts.append(first_sent)

    rationale = []
    if tp['total'] > 0:
        rationale.append(f"Arsenal: {tp['total']} tools ({tp['malware']} malware, {tp['dual_use']} dual-use)")
    if tp['cred'] > 0:
        rationale.append(f"{tp['cred']} credential/keylogger tools")
    if ts['phishing']:
        rationale.append("phishing/SE signals in description")
    if ts['server_exploit']:
        rationale.append("server exploitation signals")
    if ts['supply_chain']:
        rationale.append("supply chain signals")
    if rationale:
        notes_parts.append('Scoring: ' + '; '.join(rationale) + '.')

    notes_parts.append('Heuristic-scored from ETDA Threat Group Cards.')

    # Cross-reference with expert data
    lookup_names = [p.strip().lower() for p in actor['value'].split(',')]
    lookup_names.extend(s.lower().strip() for s in synonyms)
    expert_match = None
    for ln in lookup_names:
        if ln in EXPERTS:
            expert_match = ln
            break
    if expert_match:
        expert_s = EXPERTS[expert_match]
        notes_parts.append(f'Cross-ref: Mandiant/CrowdStrike expert scores {expert_s}.')

    # Sources
    refs = actor.get('meta', {}).get('refs', [])
    sources = ['ETDA ThaiCERT Threat Group Cards v' + etda.get('version', '')]

    # Victims
    victims = actor.get('meta', {}).get('cfr-suspected-victims', [])
    if victims:
        notes_parts.append(f"Known victims: {', '.join(victims[:8])}.")

    sponsor = actor.get('meta', {}).get('cfr-suspected-state-sponsor', '')
    if sponsor:
        notes_parts.append(f"Suspected sponsor: {sponsor}.")

    # Top tools
    if tp['names']:
        top = tp['names'][:10]
        notes_parts.append(f"Key tools: {', '.join(top)}{'...' if len(tp['names'])>10 else ''}.")

    actor_obj = {
        'threat_actor': display_name,
        'tlctc_scores': scores,
        'origin_country': origin,
        'motivation': motivations,
        'target_sectors': sectors,
        'notes': ' '.join(notes_parts),
        'sequence': sequence,
        'sources': sources + refs[:3],
        'last_updated': '2026-04-08',
    }
    output_actors.append(actor_obj)

output_actors.sort(key=lambda a: a['threat_actor'].lower())

print(f"\n=== OUTPUT: {len(output_actors)} actors generated ===")

for i, label in enumerate(LABELS):
    dist = Counter(a['tlctc_scores'][i] for a in output_actors)
    print(f"  {label}: " + ', '.join(f"{k}={v}" for k, v in sorted(dist.items())))

with open('etda-dataset.json', 'w', encoding='utf-8') as f:
    json.dump({'schema_version': 'tlctc-actor-profile.v2', 'actors': output_actors}, f, ensure_ascii=False)

print(f"\n  Written to etda-dataset.json ({len(output_actors)} actors)")
