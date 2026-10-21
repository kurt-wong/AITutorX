from pathlib import Path
p = Path(r"D:\Project\AITutors-v3\backend\app\domains\resolver\resolver.py")
s = p.read_text(encoding="utf-8")

old = '''def _option_content_bounds(text: str, label: str, prefer_offset: int | None = None):
    """Return (content_start, content_end) for `label` on `text`, or None.

    Content = characters after this label's separator up to the next label token
    (or end of line). NEVER includes the label token itself.
    Task A assertion: `A. 1 B. 2` → A content='1', B content='2'.
    """
    tokens = _all_label_token_spans(text)
    if not tokens:
        return None
    lab_u = label.upper()
    idxs = [i for i, t in enumerate(tokens) if t[2] == lab_u]
    if not idxs:
        return None
    # pick the occurrence at/after prefer_offset when given (inline cursor)
    pick = idxs[0]
    if prefer_offset is not None:
        for i in idxs:
            if tokens[i][0] >= prefer_offset:
                pick = i
                break
    start = tokens[pick][1]  # after separator
    if pick + 1 < len(tokens):
        end = tokens[pick + 1][0]  # before next label token start
    else:
        end = len(text)
    # trim trailing whitespace from content
    while end > start and text[end - 1] in " \\t\\u3000":
        end -= 1
    if start > end:
        return None
    return (start, end)
'''
new = '''def _option_content_bounds(
    text: str,
    label: str,
    prefer_offset: int | None = None,
    boundary_labels: frozenset | set | None = None,
):
    """Return (content_start, content_end) for `label` on `text`, or None.

    Content = characters after this label's separator up to the next **declared**
    option-label token (or end of line). NEVER includes the label token itself.
    Task A: `A. 1 B. 2` → A content='1', B content='2'.
    `boundary_labels` limits which tokens may end content — prevents chemical
    `H:` in `B. H: O: H` from slicing B to empty when H is not a declared option.
    """
    tokens = _all_label_token_spans(text)
    if not tokens:
        return None
    lab_u = label.upper()
    idxs = [i for i, t in enumerate(tokens) if t[2] == lab_u]
    if not idxs:
        return None
    pick = idxs[0]
    if prefer_offset is not None:
        for i in idxs:
            if tokens[i][0] >= prefer_offset:
                pick = i
                break
    start = tokens[pick][1]  # after separator
    # next boundary: first later token whose letter is a declared option label
    end = len(text)
    for i in range(pick + 1, len(tokens)):
        letter = tokens[i][2]
        if boundary_labels is None or letter in boundary_labels:
            end = tokens[i][0]
            break
    while end > start and text[end - 1] in " \\t\\u3000":
        end -= 1
    if start > end:
        return None
    return (start, end)
'''
if old not in s:
    print("content bounds fn not found")
else:
    s = s.replace(old, new, 1)
    print("patched content bounds with boundary_labels")

# pass boundary_labels from _locate_options
s = s.replace(
    "bounds = _option_content_bounds(line.text, lab, prefer_offset=None)",
    "bounds = _option_content_bounds(line.text, lab, prefer_offset=None, boundary_labels=set(labels))",
)
s = s.replace(
    "bounds = _option_content_bounds(line.text, lab, prefer_offset=cursor_end)",
    "bounds = _option_content_bounds(line.text, lab, prefer_offset=cursor_end, boundary_labels=set(labels))",
)
p.write_text(s, encoding="utf-8")
print("locate callers pass boundary_labels")
