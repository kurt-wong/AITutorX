"""Task A — Resolver option content-span fix (minimal, options-line scoped).

Changes ONLY resolver.py _locate_options / _option_span content handling.
Does NOT touch Producer, Gate, Schema, Decomposition, P1.4-B.
"""
from pathlib import Path

p = Path(r"D:\Project\AITutors-v3\backend\app\domains\resolver\resolver.py")
s = p.read_text(encoding="utf-8")

# 1) Add content-span helper after _label_offsets
old_helper = '''def _label_offsets(text: str, label: str) -> list[int]:
    """Char offsets of option-label tokens for `label` in `text` (Rules A-C forms)."""
    offs: list[int] = []
    for m in _LABEL_RE.finditer(text):
        if m.group(1).upper() == label.upper():
            offs.append(m.start())
    for m in _LABEL_DIGIT_GLUE_RE.finditer(text):
        if m.group(2).upper() == label.upper():
            offs.append(m.start(2))
    if not _LABEL_SPACE_SEP_PROSE.search(text):
        for m in _LABEL_SPACE_SEP_RE.finditer(text):
            if m.group(1).upper() == label.upper():
                offs.append(m.start(1))
    return sorted(set(offs))
'''
new_helper = '''def _label_offsets(text: str, label: str) -> list[int]:
    """Char offsets of option-label tokens for `label` in `text` (Rules A-C forms)."""
    offs: list[int] = []
    for m in _LABEL_RE.finditer(text):
        if m.group(1).upper() == label.upper():
            offs.append(m.start())
    for m in _LABEL_DIGIT_GLUE_RE.finditer(text):
        if m.group(2).upper() == label.upper():
            offs.append(m.start(2))
    if not _LABEL_SPACE_SEP_PROSE.search(text):
        for m in _LABEL_SPACE_SEP_RE.finditer(text):
            if m.group(1).upper() == label.upper():
                offs.append(m.start(1))
    return sorted(set(offs))


def _all_label_token_spans(text: str) -> list[tuple[int, int, str]]:
    """All option-label token spans on a line: (start, end, letter) in source order.

    end = index AFTER the separator (start of option content).
    Used to slice content = after this label → before next label (Task A).
    """
    hits: list[tuple[int, int, str]] = []
    for m in _LABEL_RE.finditer(text):
        hits.append((m.start(), m.end(), m.group(1).upper()))
    for m in _LABEL_DIGIT_GLUE_RE.finditer(text):
        # token is `2D.` — content starts after glue+letter+sep
        hits.append((m.start(2), m.end(), m.group(2).upper()))
    if not _LABEL_SPACE_SEP_PROSE.search(text):
        for m in _LABEL_SPACE_SEP_RE.finditer(text):
            # `D 麦哲伦` — content starts after letter + spaces
            hits.append((m.start(1), m.end(), m.group(1).upper()))
    # stable by start offset; drop exact duplicates
    hits = sorted(set(hits), key=lambda x: (x[0], x[1]))
    return hits


def _option_content_bounds(text: str, label: str, prefer_offset: int | None = None):
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
if old_helper not in s:
    print("helper block not found")
else:
    s = s.replace(old_helper, new_helper, 1)
    print("added content-bounds helper")

# 2) Replace _locate_options to return content spans for multi-label lines
old_loc = '''    def _locate_options(self, out, unit_id, labels, start_ref, region_upper):
        """逐 label 定位：优先行首选项；否则前一个选项行上的 bounded inline（单行多选项）。

        返回 {label: ("ok", ref) | ("inline", ref, start, end) | ("ambiguous",) | ("incomplete",)}。
        重复→ambiguous；完全缺失→incomplete。
        """
        found: dict[str, tuple] = {}
        cursor_seq = self._idx.seq_of(start_ref)
        cursor_ref: str | None = None
        cursor_end = 0
        for lab in labels:
            starts = [
                l for l in self._idx.lines
                if l.seq > cursor_seq
                and (region_upper is None or l.seq < region_upper)
                and lab in option_tokens(normalize_text(l.text), (lab,))
            ]
            if len(starts) == 1:
                found[lab] = ("ok", starts[0].line_ref)
                cursor_seq = starts[0].seq
                cursor_ref = starts[0].line_ref
                cursor_end = 0  # 同行后续标签从行首后任意 offset 找（单行多选项）
                continue
            if len(starts) > 1:
                found[lab] = ("ambiguous",)
                continue
            # 无行首选项：尝试在前一个选项行（同物理行多选项）bounded inline。
            if cursor_ref is not None:
                line = self._idx.get(cursor_ref)
                offs = [o for o in _label_offsets(line.text, lab) if o >= cursor_end]
                if len(offs) == 1:
                    found[lab] = ("inline", cursor_ref, offs[0], offs[0] + len(lab))
                    cursor_end = offs[0] + len(lab)
                    continue
'''
new_loc = '''    def _locate_options(self, out, unit_id, labels, start_ref, region_upper):
        """逐 label 定位：优先行首选项；否则前一个选项行上的 bounded inline（单行多选项）。

        Task A: 多标签同行时返回 **内容区间**（标签后→下一标签前），不再整行吞并。
        返回 {label: ("content", ref, c_start, c_end) | ("ok", ref) |
                     ("inline", ref, start, end) | ("ambiguous",) | ("incomplete",)}。
        重复→ambiguous；完全缺失→incomplete。
        搜索范围不扩大：仍只在已命中的选项行 / cursor 行上切内容。
        """
        found: dict[str, tuple] = {}
        cursor_seq = self._idx.seq_of(start_ref)
        cursor_ref: str | None = None
        cursor_end = 0
        for lab in labels:
            starts = [
                l for l in self._idx.lines
                if l.seq > cursor_seq
                and (region_upper is None or l.seq < region_upper)
                and lab in option_tokens(normalize_text(l.text), (lab,))
            ]
            if len(starts) == 1:
                line = starts[0]
                bounds = _option_content_bounds(line.text, lab, prefer_offset=None)
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
                continue
            if len(starts) > 1:
                found[lab] = ("ambiguous",)
                continue
            # 无行首选项：尝试在前一个选项行（同物理行多选项）bounded inline。
            if cursor_ref is not None:
                line = self._idx.get(cursor_ref)
                bounds = _option_content_bounds(line.text, lab, prefer_offset=cursor_end)
                if bounds is not None and bounds[0] >= cursor_end:
                    found[lab] = ("content", cursor_ref, bounds[0], bounds[1])
                    cursor_end = bounds[1]
                    continue
                offs = [o for o in _label_offsets(line.text, lab) if o >= cursor_end]
                if len(offs) == 1:
                    found[lab] = ("inline", cursor_ref, offs[0], offs[0] + len(lab))
                    cursor_end = offs[0] + len(lab)
                    continue
'''
if old_loc not in s:
    print("locate block not found")
else:
    s = s.replace(old_loc, new_loc, 1)
    print("patched _locate_options")

# 3) _option_span handle "content"
old_span = '''    def _option_span(self, out, unit_id, t, option_hits):
        entry = option_hits.get(t.label or "", ("incomplete",))
        kind = entry[0]
        if kind == "ok":
            out.add_span(unit_id, t, [entry[1]], "exact", (f"option label={t.label}",))
            return
        if kind == "inline":
            out.add_char_span(unit_id, t, entry[1], entry[2], entry[3], "exact",
                              (f"option label={t.label} (inline, line_character)",))
            return
        out.add_unresolved(t, kind if kind in ("ambiguous", "incomplete") else "incomplete",
                           (f"option {t.label}",))
'''
new_span = '''    def _option_span(self, out, unit_id, t, option_hits):
        entry = option_hits.get(t.label or "", ("incomplete",))
        kind = entry[0]
        if kind == "ok":
            out.add_span(unit_id, t, [entry[1]], "exact", (f"option label={t.label}",))
            return
        if kind == "content":
            # Task A: content span = after label → before next label (line_character)
            out.add_char_span(unit_id, t, entry[1], entry[2], entry[3], "exact",
                              (f"option label={t.label} (content span, line_character)",))
            return
        if kind == "inline":
            out.add_char_span(unit_id, t, entry[1], entry[2], entry[3], "exact",
                              (f"option label={t.label} (inline, line_character)",))
            return
        out.add_unresolved(t, kind if kind in ("ambiguous", "incomplete") else "incomplete",
                           (f"option {t.label}",))
'''
if old_span not in s:
    print("option_span block not found")
else:
    s = s.replace(old_span, new_span, 1)
    print("patched _option_span")

p.write_text(s, encoding="utf-8")
print("wrote resolver.py")
