import json, sys, uuid
from pathlib import Path
sys.path.insert(0, '.')
from scripts.preprocessing_consumer.manifest_reader import load_manifest
from scripts.preprocessing_consumer.resolved_span_adapter import manifest_to_resolved_spans
from scripts.preprocessing_consumer.source_loader import load_source_lines

mf = load_manifest(Path(r'D:\Project\AITutor-X\e2e_run\minimal-loop-manifest.json'))
src = Path(mf.source_file)
lines = load_source_lines(src)
sv_id = uuid.uuid4()
resolved, unresolved = manifest_to_resolved_spans(mf, lines, sv_id)
opt_spans = [s for s in resolved if '.option.' in s['span_id']]
print('total spans:', len(resolved), 'unresolved:', len(unresolved))
print('option spans:', len(opt_spans))
for s in opt_spans[:4]:
    print(' ', s['span_id'], s['start_line_ref'] + '-' + s['end_line_ref'])
