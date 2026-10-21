from pathlib import Path
import json

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
meta = json.loads((OUT / "MANIFEST.json").read_text(encoding="utf-8"))

# embed data
data = {
    "run_id": meta.get("run_id"),
    "purpose": meta.get("purpose"),
    "frozen": meta.get("frozen"),
    "preprocessing_note": meta.get("preprocessing_note"),
    "git": meta.get("git"),
    "subjects": meta.get("subjects"),
}

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>9 科正式 E2E Acceptance Run</title>
<link rel="stylesheet" href="style.css"/>
</head>
<body>
<header>
  <h1>9 科正式 E2E Acceptance Run</h1>
  <p class="sub">PDF → Preprocessing → Owner Gate1 → V3 → Question → Owner Gate2</p>
  <div class="chips">
    <span class="chip warn">P1.4-B FROZEN</span>
    <span class="chip">no code fix this run</span>
    <span class="chip" id="run-id"></span>
  </div>
</header>

<main>
  <section class="card">
    <h2>链路与责任</h2>
    <div class="flow">
      <div class="node">01 原始 PDF</div>
      <div class="arrow">→</div>
      <div class="node">02 Preprocessing MD</div>
      <div class="arrow">→</div>
      <div class="node gate">Gate1 Owner</div>
      <div class="arrow">→</div>
      <div class="node">03 Sealed Accepted</div>
      <div class="arrow">→</div>
      <div class="node">04 V3 Input</div>
      <div class="arrow">→</div>
      <div class="node">05 Question</div>
      <div class="arrow">→</div>
      <div class="node gate">Gate2 Owner</div>
    </div>
    <p class="note">发现问题时做差分：Preproc 错→Preprocessing；Preproc 对 V3 错→V3/Integration；数据对前端错→Frontend。</p>
    <p class="note" id="preproc-note"></p>
  </section>

  <section class="card">
    <h2>Round 1 总表</h2>
    <table id="summary">
      <thead>
        <tr>
          <th>科目</th><th>试卷</th>
          <th>PDF SHA</th><th>MD SHA</th>
          <th>IR ready/inc</th><th>auto/pending/rej</th>
          <th>Gate1</th><th>Gate2 machine</th><th>Gate2 Owner</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  </section>

  <section class="card">
    <h2>人工验收 · Gate 1（Preprocessing）</h2>
    <p class="note">对每科检查：题目边界 / 题干 / 选项完整与串题 / 跨行误拆 / 答案 / 材料题。通过后产物封存，禁止再改。</p>
    <div id="gate1"></div>
  </section>

  <section class="card">
    <h2>人工验收 · Gate 2（V3 → Question）</h2>
    <p class="note">看最终用户看到的题目，不看内部 manifest 是否“漂亮”。不对时再展开 stem/options/answer 定位首次变坏层。</p>
    <div id="gate2"></div>
  </section>

  <section class="card">
    <h2>归因矩阵（Round 1 机器观测）</h2>
    <table id="attribution">
      <thead>
        <tr><th>科目</th><th>Preproc 产物</th><th>V3 输入哈希一致</th><th>V3 首次表现</th><th>可能责任层</th></tr>
      </thead>
      <tbody></tbody>
    </table>
  </section>

  <section class="card">
    <h2>目录与血缘</h2>
    <pre id="tree"></pre>
  </section>
</main>

<footer>
  <p>验收顺序：L1 数据正确 → L2 产品正确 → L3 治理正确。本页只做 L1/L2 观测与人工门禁。</p>
</footer>

<script src="data.js"></script>
<script src="app.js"></script>
</body>
</html>
"""

css = """
:root {
  --bg: #f6f4ef;
  --ink: #1c1b19;
  --muted: #6b6560;
  --card: #fffdf8;
  --line: #e4ddd2;
  --accent: #0b6e4f;
  --warn: #b45309;
  --fail: #b91c1c;
  --ok: #15803d;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.55;
}
header {
  padding: 28px 32px 12px;
  border-bottom: 1px solid var(--line);
  background: linear-gradient(180deg, #fffdf8, var(--bg));
}
h1 { margin: 0 0 6px; font-size: 26px; letter-spacing: 0.02em; }
h2 { margin: 0 0 12px; font-size: 18px; }
.sub { margin: 0; color: var(--muted); }
.chips { margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; }
.chip {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 999px;
  background: #efe9dc;
  color: var(--ink);
}
.chip.warn { background: #fef3c7; color: var(--warn); }
main { padding: 24px 32px 48px; max-width: 1200px; }
.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 18px;
}
.flow {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-bottom: 10px;
}
.node {
  padding: 8px 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fff;
  font-size: 13px;
}
.node.gate { border-color: var(--accent); color: var(--accent); font-weight: 600; }
.arrow { color: var(--muted); }
.note { color: var(--muted); font-size: 13px; margin: 6px 0; }
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
th, td {
  border-bottom: 1px solid var(--line);
  padding: 8px 10px;
  text-align: left;
  vertical-align: top;
}
th { color: var(--muted); font-weight: 600; background: #faf7f1; }
.mono { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; }
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 12px;
}
.badge.ok { background: #dcfce7; color: var(--ok); }
.badge.warn { background: #fef3c7; color: var(--warn); }
.badge.fail { background: #fee2e2; color: var(--fail); }
.badge.pending { background: #e5e7eb; color: #374151; }
.checklist {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 10px;
  margin-top: 8px;
}
.check {
  border: 1px dashed var(--line);
  border-radius: 8px;
  padding: 10px 12px;
  background: #fff;
}
.check h3 { margin: 0 0 6px; font-size: 14px; }
.check label {
  display: block;
  font-size: 12px;
  color: var(--muted);
  margin: 3px 0;
}
.qprev {
  border-left: 3px solid var(--accent);
  padding: 6px 10px;
  margin: 8px 0;
  background: #fff;
  font-size: 12px;
}
pre#tree {
  background: #1c1b19;
  color: #f5f5f4;
  padding: 14px;
  border-radius: 8px;
  overflow: auto;
  font-size: 12px;
}
footer {
  padding: 16px 32px 32px;
  color: var(--muted);
  font-size: 12px;
}
"""

# data.js
data_js = "window.E2E_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n"

js = r"""
const D = window.E2E_DATA || {};
document.getElementById('run-id').textContent = D.run_id || '';
document.getElementById('preproc-note').textContent = D.preprocessing_note || '';

const subjects = D.subjects || {};
const order = ["数学","物理","化学","英语","语文","政治","地理","历史","生物"];

function shortSha(s) {
  return s ? s.slice(0, 10) + '…' : '—';
}
function badge(text, cls) {
  return `<span class="badge ${cls}">${text}</span>`;
}

const tbody = document.querySelector('#summary tbody');
const g1 = document.getElementById('gate1');
const g2 = document.getElementById('gate2');
const attr = document.querySelector('#attribution tbody');

order.forEach(name => {
  const s = subjects[name] || {};
  const v = s.v3 || {};
  const st = s.status || {};
  const row = document.createElement('tr');
  row.innerHTML = `
    <td><strong>${name}</strong></td>
    <td>${s.paper_label || '—'}</td>
    <td class="mono">${shortSha(s.pdf && s.pdf.sha256)}</td>
    <td class="mono">${shortSha(s.preproc_md && s.preproc_md.sha256)}</td>
    <td>${v.ir_ready ?? '—'} / ${v.ir_incomplete ?? '—'}</td>
    <td>${v.gate_auto ?? '—'} / ${v.gate_pending ?? '—'} / ${v.gate_rejected ?? '—'}</td>
    <td>${badge(st.gate1_owner || '—', st.gate1_owner === 'AWAITING_OWNER' ? 'pending' : 'pending')}</td>
    <td>${badge(st.gate2_machine || '—', (st.gate2_machine||'').startsWith('PASS') ? 'ok' : 'fail')}</td>
    <td>${badge(st.gate2_owner || '—', 'pending')}</td>
  `;
  tbody.appendChild(row);

  // Gate1 checklist card
  const c1 = document.createElement('div');
  c1.className = 'check';
  c1.innerHTML = `
    <h3>${name} · ${s.paper_label || ''}</h3>
    <div class="mono">MD ${shortSha(s.preproc_md && s.preproc_md.sha256)}</div>
    <label><input type="radio" name="g1-${name}" value="pass"> 题目边界正确</label>
    <label><input type="radio" name="g1-${name}" value="pass"> 题干/公式/图片完整</label>
    <label><input type="radio" name="g1-${name}" value="pass"> 选项完整且不串题</label>
    <label><input type="radio" name="g1-${name}" value="pass"> 无跨行误拆选项</label>
    <label><input type="radio" name="g1-${name}" value="pass"> 答案存在且不错位</label>
    <label><input type="radio" name="g1-${name}" value="fail"> 发现问题 → FAIL</label>
  `;
  g1.appendChild(c1);

  // Gate2 preview
  const c2 = document.createElement('div');
  c2.className = 'check';
  const qs = (s.v3 && s.v3.questions) || [];
  const preview = qs.slice(0, 3).map(q =>
    `<div class="qprev"><strong>${q.unit_id}</strong> labels=[${(q.labels||[]).join(',')}]
     ans=${q.answer_letter || '—'} gate=${q.gate}<br/>
     <span class="mono">${(q.stem_preview||'').slice(0,80)}</span></div>`
  ).join('');
  c2.innerHTML = `
    <h3>${name}</h3>
    <div>${badge('auto ' + (v.gate_auto ?? 0), 'ok')} ${badge('pending ' + (v.gate_pending ?? 0), 'warn')} ${badge('rej ' + (v.gate_rejected ?? 0), 'fail')}</div>
    ${preview || '<div class="note">无题目预览</div>'}
    <label><input type="radio" name="g2-${name}" value="pass"> 最终题目正确</label>
    <label><input type="radio" name="g2-${name}" value="fail"> 发现问题 → FAIL</label>
  `;
  g2.appendChild(c2);

  // attribution
  const ident = s.owner_accepted && s.owner_accepted.identical_to_preproc;
  let layer = '待人工';
  if ((st.gate2_machine||'').startsWith('FAIL')) layer = 'Integration / V3 runtime';
  else if (v.gate_auto === 0 && (v.gate_pending||0) > 0) layer = 'Answer-side / S0 family (see math)';
  else layer = 'No machine-level block observed';
  const ar = document.createElement('tr');
  ar.innerHTML = `
    <td>${name}</td>
    <td>${s.preproc_md ? 'OK ' + shortSha(s.preproc_md.sha256) : 'MISSING'}</td>
    <td>${ident ? badge('YES', 'ok') : badge('?', 'warn')}</td>
    <td>auto=${v.gate_auto ?? '—'} pending=${v.gate_pending ?? '—'} rej=${v.gate_rejected ?? '—'}</td>
    <td>${layer}</td>
  `;
  attr.appendChild(ar);
});

document.getElementById('tree').textContent = [
  'E2E_ACCEPTANCE/',
  '  MANIFEST.json          # lineage: pdf/md/manifest/output SHA256 + git heads',
  '  01_INPUT_PDF/          # 9 original PDFs',
  '  02_PREPROCESSING_OUTPUT/  # machine MD (official Ocr-markdown)',
  '  03_OWNER_ACCEPTED/     # sealed after Gate1 PASS (identical bytes)',
  '  04_V3_INPUT/           # manifest + accepted MD',
  '  05_V3_OUTPUT/          # question-level JSON',
  '  index.html style.css app.js data.js',
  '',
  'git: ' + JSON.stringify(D.git || {}),
  'frozen: ' + JSON.stringify(D.frozen || {}),
].join('\n');
"""

(OUT / "index.html").write_text(html, encoding="utf-8")
(OUT / "style.css").write_text(css, encoding="utf-8")
(OUT / "app.js").write_text(js, encoding="utf-8")
(OUT / "data.js").write_text(data_js, encoding="utf-8")
print("wrote index.html / style.css / app.js / data.js")
# print summary counts
total_auto = sum((s.get("v3") or {}).get("gate_auto", 0) for s in meta["subjects"].values())
total_pend = sum((s.get("v3") or {}).get("gate_pending", 0) for s in meta["subjects"].values())
total_rej = sum((s.get("v3") or {}).get("gate_rejected", 0) for s in meta["subjects"].values())
print(f"TOTALS auto={total_auto} pending={total_pend} rejected={total_rej}")
for n in order:
    s = meta["subjects"].get(n, {})
    v = s.get("v3") or {}
    print(f"  {n}: {s.get('status',{}).get('gate2_machine')} "
          f"auto={v.get('gate_auto')} pend={v.get('gate_pending')} rej={v.get('gate_rejected')} "
          f"units={v.get('n_units')}")
