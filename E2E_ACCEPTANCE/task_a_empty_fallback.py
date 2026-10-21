from pathlib import Path
p = Path(r"D:\Project\AITutors-v3\backend\app\domains\resolver\resolver.py")
s = p.read_text(encoding="utf-8")
old = '''                bounds = _option_content_bounds(line.text, lab, prefer_offset=None, boundary_labels=set(labels))
                if bounds is not None:
                    # content span (may be multi-label line: A='1' B='2' …)
                    found[lab] = ("content", line.line_ref, bounds[0], bounds[1])
                    cursor_seq = line.seq
                    cursor_ref = line.line_ref
                    cursor_end = bounds[1]
                else:
                    # fallback: whole line (single unlabeled-style hit)
                    found[lab] = ("ok", line.line_ref)
                    cursor_seq = line.seq
                    cursor_ref = line.line_ref
                    cursor_end = 0
                continue'''
new = '''                bounds = _option_content_bounds(line.text, lab, prefer_offset=None, boundary_labels=set(labels))
                # Task A: empty/invalid content (e.g. false-positive declared label
                # `H` in `B. H: O: H` used as boundary) → fallback whole-line OK
                # so we do not turn previously-resolved options into incomplete.
                if bounds is not None and bounds[1] > bounds[0]:
                    found[lab] = ("content", line.line_ref, bounds[0], bounds[1])
                    cursor_seq = line.seq
                    cursor_ref = line.line_ref
                    cursor_end = bounds[1]
                else:
                    found[lab] = ("ok", line.line_ref)
                    cursor_seq = line.seq
                    cursor_ref = line.line_ref
                    cursor_end = 0
                continue'''
if old not in s:
    print("locate ok/content block not found")
else:
    s = s.replace(old, new, 1)
    print("patched empty-content fallback")

old2 = '''                bounds = _option_content_bounds(line.text, lab, prefer_offset=cursor_end, boundary_labels=set(labels))
                if bounds is not None and bounds[0] >= cursor_end:
                    found[lab] = ("content", cursor_ref, bounds[0], bounds[1])
                    cursor_end = bounds[1]
                    continue
                offs = [o for o in _label_offsets(line.text, lab) if o >= cursor_end]
                if len(offs) == 1:
                    found[lab] = ("inline", cursor_ref, offs[0], offs[0] + len(lab))
                    cursor_end = offs[0] + len(lab)
                    continue'''
new2 = '''                bounds = _option_content_bounds(line.text, lab, prefer_offset=cursor_end, boundary_labels=set(labels))
                if bounds is not None and bounds[1] > bounds[0] and bounds[0] >= cursor_end:
                    found[lab] = ("content", cursor_ref, bounds[0], bounds[1])
                    cursor_end = bounds[1]
                    continue
                offs = [o for o in _label_offsets(line.text, lab) if o >= cursor_end]
                if len(offs) == 1:
                    # content after this label if non-empty, else label-only inline
                    cb = _option_content_bounds(line.text, lab, prefer_offset=offs[0], boundary_labels=set(labels))
                    if cb is not None and cb[1] > cb[0] and cb[0] >= cursor_end:
                        found[lab] = ("content", cursor_ref, cb[0], cb[1])
                        cursor_end = cb[1]
                        continue
                    found[lab] = ("inline", cursor_ref, offs[0], offs[0] + len(lab))
                    cursor_end = offs[0] + len(lab)
                    continue'''
if old2 not in s:
    print("inline block not found")
else:
    s = s.replace(old2, new2, 1)
    print("patched inline empty-content fallback")
p.write_text(s, encoding="utf-8")
