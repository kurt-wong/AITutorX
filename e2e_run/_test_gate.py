import asyncio, json, sys, uuid
from pathlib import Path
sys.path.insert(0, '.')

from scripts.preprocessing_consumer.manifest_reader import load_manifest
from scripts.preprocessing_consumer.annotation_adapter import manifest_to_annotation_payload
from scripts.preprocessing_consumer.resolved_span_adapter import manifest_to_resolved_spans
from scripts.preprocessing_consumer.source_loader import load_source_lines

from app.domains.resolver.span import ResolvedRun, ResolvedSpan
from app.domains.compile.ir import IRBuilder, validate_ir

mf = load_manifest(Path(r'D:\Project\AITutor-X\e2e_run\minimal-loop-manifest.json'))
src = Path(mf.source_file)
lines = load_source_lines(src)
sv_id = uuid.uuid4()
ann_id = uuid.uuid4()

resolved_dicts, unresolved = manifest_to_resolved_spans(mf, lines, sv_id)
spans = tuple(ResolvedSpan(**d) for d in resolved_dicts)
run = ResolvedRun(source_version_id=sv_id, resolved_spans=spans, unresolved_references=tuple())

payload = manifest_to_annotation_payload(mf)
ir = IRBuilder.build(run, payload, sv_id, ann_id)
ir = validate_ir(ir)

# Count IR leaves (ready units produce leaves)
leaves = [u for u in ir.units if u.semantic_status == 'ready']
print('Ready for Gate:', len(leaves))
print('Option content sample:')
for u in ir.units[:2]:
    for c in u.content:
        if c.role == 'option':
            print(' ', u.unit_id, c.role, c.label, 'span_id:', c.span_id)
