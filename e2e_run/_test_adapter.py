import json, sys
from pathlib import Path
sys.path.insert(0, '.')
from scripts.preprocessing_consumer.manifest_reader import load_manifest
from scripts.preprocessing_consumer.annotation_adapter import manifest_to_annotation_payload

mf = load_manifest(Path(r'D:\Project\AITutor-X\e2e_run\minimal-loop-manifest.json'))
print('units:', len(mf.units))
for u in mf.units[:3]:
    print(' ', u.unit_id, 'type=' + u.original_question_type, 'options=' + str([o.label for o in u.options]))
payload = manifest_to_annotation_payload(mf)
for su in payload['semantic_units'][:3]:
    opts = su.get('content', {}).get('options', [])
    print(' payload', su['unit_id'], 'options=' + str(opts))
gaps = payload.get('producer_boundary', {}).get('known_gaps', [])
print('known_gaps:', len(gaps))
for g in gaps[:3]:
    print(' ', g['code'], g['unit_id'])
