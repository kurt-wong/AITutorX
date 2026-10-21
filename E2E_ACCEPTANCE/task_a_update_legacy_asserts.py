from pathlib import Path

# test_resolver.py — content span contract
p = Path(r"D:\Project\AITutors-v3\backend\tests\test_resolver.py")
s = p.read_text(encoding="utf-8")
old = '''async def test_option_shared_line_line_character():
    """单行多选项 'A. 苹果 B. 香蕉' → B 以 line_character 定位（有界 label，非 first-match）。"""
    lines = mk("1. 哪个是水果", "A. 苹果  B. 香蕉")
    payload = {"semantic_units": [{"unit_id": "Q1", "content": {
        "stem": {"question_label": "1"}, "options": [{"label": "A"}, {"label": "B"}]}}]}
    run = resolver(lines).resolve(payload)
    b = next(s for s in run.resolved_spans if s.span_id == "sp-Q1.option.B")
    assert b.granularity == "line_character"
    assert b.line_refs == ("P1L002",)
    assert lines[1].text[b.start_offset:b.end_offset] == "B"
    assert not any(u.reference_id == "Q1.option.B" for u in run.unresolved_references)
'''
new = '''async def test_option_shared_line_line_character():
    """单行多选项 'A. 苹果 B. 香蕉' → Task A 内容区间（标签后→下一标签前），非 label-only。"""
    lines = mk("1. 哪个是水果", "A. 苹果  B. 香蕉")
    payload = {"semantic_units": [{"unit_id": "Q1", "content": {
        "stem": {"question_label": "1"}, "options": [{"label": "A"}, {"label": "B"}]}}]}
    run = resolver(lines).resolve(payload)
    a = next(s for s in run.resolved_spans if s.span_id == "sp-Q1.option.A")
    b = next(s for s in run.resolved_spans if s.span_id == "sp-Q1.option.B")
    assert b.granularity == "line_character"
    assert b.line_refs == ("P1L002",)
    # Task A: content span, not the label letter
    assert lines[1].text[b.start_offset:b.end_offset].strip() == "香蕉"
    assert lines[1].text[a.start_offset:a.end_offset].strip() == "苹果"
    assert not any(u.reference_id == "Q1.option.B" for u in run.unresolved_references)
'''
if old not in s:
    print("resolver test block not found")
else:
    s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")
    print("updated test_option_shared_line_line_character")

# fullwidth test — content span
p2 = Path(r"D:\Project\AITutors-v3\backend\tests\test_option_fullwidth_comma.py")
s2 = p2.read_text(encoding="utf-8")
old2 = '''        assert opts["D"].line_refs[0] == "P1L003"
        assert lines[2].text[opts["D"].start_offset:opts["D"].end_offset] == "D"
        for lab in "ABC":
            assert lab in opts, f"{lab} must stay resolved"
'''
new2 = '''        assert opts["D"].line_refs[0] == "P1L003"
        # Task A content span: after `D，` → content, not the label letter
        d_txt = lines[2].text[opts["D"].start_offset:opts["D"].end_offset]
        assert d_txt.strip() == "物种减少", d_txt
        assert "A" in opts and "B" in opts
        a_txt = lines[1].text[opts["A"].start_offset:opts["A"].end_offset]
        assert a_txt.strip() == "全球变暖", a_txt
        for lab in "ABC":
            assert lab in opts, f"{lab} must stay resolved"
'''
if old2 not in s2:
    print("fullwidth assert block not found")
else:
    s2 = s2.replace(old2, new2, 1)
    p2.write_text(s2, encoding="utf-8")
    print("updated test_u44_pattern_q44_options_resolved")
