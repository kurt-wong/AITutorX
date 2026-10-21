from pathlib import Path
p = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-B-SIM\b_label_repair_simulation.py")
s = p.read_text(encoding="utf-8")
s = s.replace(
    "from app.domains.compile.snapshot import CompiledOption  # noqa: E402",
    "from app.domains.compile.snapshot import CompiledRole  # noqa: E402",
)
old = '''        opt = CompiledOption(
            label=new_label.upper(),
            span_id=SIM_SPAN,
            text=source_text,
            text_hash="sim",  # simulation-only; provenance layer will see this
            line_refs=(f"SIM@L{source_line}",) if source_line else (),
        )
        # CompiledOption signature may differ — fall back to simple namespace
        try:
            leaf.options = list(leaf.options) + [opt]
        except Exception:
            from types import SimpleNamespace
            leaf.options = list(leaf.options) + [SimpleNamespace(
                label=new_label.upper(), span_id=SIM_SPAN, text=source_text,
                text_hash="sim", line_refs=(),
            )]
    return compiled2, leaf'''
new = '''        opt = CompiledRole(
            role="option",
            span_id=SIM_SPAN,
            line_refs=(f"SIM@L{source_line}",) if source_line else (),
            text=source_text,
            text_hash="sim",
            label=new_label.upper(),
        )
        import dataclasses
        new_opts = tuple(leaf.options) + (opt,)
        new_leaf = dataclasses.replace(leaf, options=new_opts)
        new_leaves = tuple(
            new_leaf if l.unit_id == leaf.unit_id else l for l in compiled2.leaves
        )
        compiled2 = dataclasses.replace(compiled2, leaves=new_leaves)
        leaf = new_leaf
    return compiled2, leaf'''
if old not in s:
    print("OLD BLOCK NOT FOUND")
else:
    s = s.replace(old, new, 1)
    print("patched simulate_labels")
# also fix call site: simulate_labels currently mutates then evaluates
# compiled2 is rebuilt via replace — ok
p.write_text(s, encoding="utf-8")
