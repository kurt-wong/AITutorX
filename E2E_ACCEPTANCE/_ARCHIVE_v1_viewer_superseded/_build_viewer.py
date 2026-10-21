from pathlib import Path
import json

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
viewer = json.loads((OUT / "viewer_data.json").read_text(encoding="utf-8"))

# slim pdf/md previews to keep data.js reasonable — full text loaded on demand via fetch
# For offline preview, embed moderate previews (3k) + keep full files on disk
def slim(v):
    if not isinstance(v, dict):
        return v
    out = dict(v)
    if out.get("pdf_text_preview"):
        out["pdf_text_preview"] = out["pdf_text_preview"][:3000]
    if out.get("md_text_preview"):
        out["md_text_preview"] = out["md_text_preview"][:3000]
    # keep all questions
    return out

data = {
    "run_id": viewer.get("run_id"),
    "purpose": viewer.get("purpose"),
    "frozen": viewer.get("frozen"),
    "note": viewer.get("note"),
    "git": viewer.get("git"),
    "subjects": {k: slim(v) for k, v in viewer.get("subjects", {}).items()},
}

html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Owner Viewer — 9科 E2E Acceptance</title>
<link rel="stylesheet" href="style.css"/>
</head>
<body>
<header>
  <div class="hdr-row">
    <div>
      <h1>Owner Viewer</h1>
      <p class="sub">Gate 1：PDF ↔ Preprocessing MD 对照 · Gate 2：最终 Question 人工验收</p>
    </div>
    <div class="hdr-right">
      <div class="chip warn">P1.4-B FROZEN · 不修生产代码</div>
      <div class="chip" id="run-id"></div>
    </div>
  </div>
  <nav id="subject-tabs"></nav>
</header>

<main>
  <!-- ===== Gate 1 ===== -->
  <section class="card" id="gate1">
    <div class="card-head">
      <h2>Gate 1 · Preprocessing（PDF 文本 ↔ MD）</h2>
      <div class="tools">
        <input id="diff-filter" type="search" placeholder="过滤差异 / 搜索文本…"/>
        <label class="chk"><input type="checkbox" id="show-full"/> 显示完整开头文本</label>
      </div>
    </div>
    <p class="note">
      机器先标出差异行；你只判断差异是否合理（全半角/标点/空格属正常，缺字/串行/标签丢失属异常）。
      <strong>auto/pending/rejected 是机器状态，不是正确性结论。</strong>
    </p>
    <div class="side-by-side">
      <div class="pane">
        <h3>PDF 文本层</h3>
        <pre id="pdf-text" class="src"></pre>
      </div>
      <div class="pane">
        <h3>Preprocessing MD <span class="badge pending" id="g1-status">AWAITING_OWNER</span></h3>
        <pre id="md-text" class="src"></pre>
      </div>
    </div>
    <div class="diff-box">
      <h3>行级差异摘要</h3>
      <div id="diff-list"></div>
    </div>
    <div class="verdict">
      <strong>Gate 1 裁决：</strong>
      <label><input type="radio" name="g1-verdict" value="pass"/> PASS（封存 03_OWNER_ACCEPTED）</label>
      <label><input type="radio" name="g1-verdict" value="fail"/> FAIL（记 issue，不改产物）</label>
      <textarea id="g1-note" rows="2" placeholder="备注：哪些题/行有问题…"></textarea>
    </div>
  </section>

  <!-- ===== Gate 2 ===== -->
  <section class="card" id="gate2">
    <div class="card-head">
      <h2>Gate 2 · V3 Question 人工验收</h2>
      <div class="tools">
        <select id="gate-filter">
          <option value="all">全部状态</option>
          <option value="auto_approve">auto_approve</option>
          <option value="pending_review">pending_review</option>
          <option value="rejected">rejected</option>
          <option value="incomplete">incomplete</option>
        </select>
        <input id="q-search" type="search" placeholder="搜题号/题干/选项…"/>
      </div>
    </div>
    <div class="stats" id="q-stats"></div>
    <p class="note">
      看的是最终用户会看到的题目是否正确。pending 的原因常是
      <code>answer_not_expressible</code>（答案侧/S0），<strong>不等于题目损坏</strong>。
    </p>
    <div id="question-list"></div>
    <div class="verdict">
      <strong>Gate 2 裁决：</strong>
      <label><input type="radio" name="g2-verdict" value="pass"/> PASS</label>
      <label><input type="radio" name="g2-verdict" value="fail"/> FAIL</label>
      <textarea id="g2-note" rows="2" placeholder="失败题号 + 错误类型：题干/选项/串题/材料/图片/LaTeX/答案/边界…"></textarea>
    </div>
  </section>

  <!-- ===== Attribution ===== -->
  <section class="card">
    <h2>归因辅助（机器观测，不替代 Owner）</h2>
    <table id="attr-table">
      <thead>
        <tr><th>科目</th><th>题量</th><th>机器状态</th><th>常见 reason</th><th>首次可疑层</th></tr>
      </thead>
      <tbody></tbody>
    </table>
    <p class="note">
      差分规则：Preproc 错 → Preprocessing；Preproc 对而 Question 错 → V3/Integration；
      Question 对而前端错 → Frontend。仅 FAIL 题进入逐层定位。
    </p>
  </section>
</main>

<footer>
  <p>目录：E2E_ACCEPTANCE/{01_INPUT_PDF, 02_PREPROCESSING_OUTPUT, 03_OWNER_ACCEPTED, 04_V3_INPUT, 05_V3_OUTPUT} · 详见 MANIFEST.json</p>
</footer>

<script src="data.js"></script>
<script src="app.js"></script>
</body>
</html>
"""

css = r"""
:root{
  --bg:#f4f1ea; --ink:#1a1917; --muted:#6e675f; --card:#fffdf8;
  --line:#e2d9cb; --accent:#0d6b5c; --warn:#b45309; --fail:#b91c1c; --ok:#15803d;
}
*{box-sizing:border-box}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.55}
header{padding:22px 28px 0;background:linear-gradient(180deg,#fffdf8,var(--bg));
  border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}
.hdr-row{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;flex-wrap:wrap}
h1{margin:0 0 4px;font-size:24px}
h2{margin:0 0 8px;font-size:17px}
h3{margin:0 0 8px;font-size:14px;color:var(--muted)}
.sub{margin:0;color:var(--muted);font-size:13px}
.hdr-right{display:flex;flex-direction:column;gap:6px;align-items:flex-end}
.chip{font-size:12px;padding:4px 10px;border-radius:999px;background:#efe8da}
.chip.warn{background:#fef3c7;color:var(--warn)}
#subject-tabs{display:flex;gap:6px;flex-wrap:wrap;padding:12px 0 10px}
#subject-tabs button{
  border:1px solid var(--line);background:#fff;border-radius:8px;
  padding:6px 12px;cursor:pointer;font-size:13px}
#subject-tabs button.active{background:var(--accent);color:#fff;border-color:var(--accent)}
main{padding:20px 28px 48px;max-width:1280px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:16px 18px;margin-bottom:16px}
.card-head{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center}
.tools{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.tools input,.tools select{padding:6px 10px;border:1px solid var(--line);border-radius:8px;font-size:13px}
.chk{font-size:12px;color:var(--muted)}
.note{color:var(--muted);font-size:12.5px;margin:6px 0 12px}
.side-by-side{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:900px){.side-by-side{grid-template-columns:1fr}}
.pane{min-width:0}
.src{
  background:#1c1b19;color:#e7e5e4;padding:12px;border-radius:8px;
  height:320px;overflow:auto;font-size:12px;white-space:pre-wrap;
  font-family:ui-monospace,SFMono-Regular,Consolas,monospace}
.diff-box{margin-top:12px;border-top:1px solid var(--line);padding-top:10px}
#diff-list{max-height:220px;overflow:auto;font-size:12px}
.diff-row{display:grid;grid-template-columns:56px 1fr 1fr;gap:8px;padding:4px 0;border-bottom:1px dashed var(--line)}
.diff-row .tag{font-size:11px;font-weight:600}
.tag.add{color:var(--ok)} .tag.del{color:var(--fail)} .tag.mod{color:var(--warn)}
.verdict{margin-top:14px;padding-top:12px;border-top:1px solid var(--line)}
.verdict label{margin-right:14px;font-size:13px}
.verdict textarea{width:100%;margin-top:8px;padding:8px;border:1px solid var(--line);border-radius:8px;font-size:13px}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 12px}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11.5px}
.badge.ok{background:#dcfce7;color:var(--ok)}
.badge.warn{background:#fef3c7;color:var(--warn)}
.badge.fail{background:#fee2e2;color:var(--fail)}
.badge.pending{background:#e5e7eb;color:#374151}
.qcard{
  border:1px solid var(--line);border-radius:10px;background:#fff;
  padding:14px 16px;margin-bottom:12px}
.qcard header{position:static;background:none;border:0;padding:0;margin:0 0 8px;
  display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}
.qcard .uid{font-weight:700;font-size:15px}
.qstem{background:#faf7f1;border-radius:8px;padding:10px 12px;font-size:14px;white-space:pre-wrap}
.opts{margin-top:10px;display:grid;gap:6px}
.opt{display:grid;grid-template-columns:36px 1fr;gap:8px;padding:8px 10px;
  border-radius:8px;background:#faf7f1;font-size:13.5px}
.opt .lab{font-weight:700;color:var(--accent)}
.answer{margin-top:10px;padding:10px 12px;border-radius:8px;background:#eef7f2;font-size:13.5px}
.meta{margin-top:8px;font-size:12px;color:var(--muted)}
.qverdict{margin-top:10px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.qverdict select{padding:4px 8px;border-radius:6px;border:1px solid var(--line)}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th,td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{color:var(--muted);background:#faf7f1}
code{background:#efe8da;padding:1px 5px;border-radius:4px;font-size:12px}
footer{padding:12px 28px 28px;color:var(--muted);font-size:12px}
"""

js = r"""
const D = window.E2E_DATA || {};
const SUBJECTS = ["数学","物理","化学","英语","语文","政治","地理","历史","生物"];
let current = SUBJECTS[0];

document.getElementById('run-id').textContent = D.run_id || '';

function esc(s){
  return String(s==null?'':s).replace(/[&<>]/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;' }[c]));
}
function gateBadge(g){
  if (g==='auto_approve') return '<span class="badge ok">auto</span>';
  if (g==='pending_review') return '<span class="badge warn">pending</span>';
  if (g==='rejected') return '<span class="badge fail">rejected</span>';
  return '<span class="badge pending">'+esc(g||'—')+'</span>';
}

// tabs
const tabs = document.getElementById('subject-tabs');
SUBJECTS.forEach(s=>{
  const b = document.createElement('button');
  b.textContent = s;
  b.onclick = ()=>{ current=s; render(); };
  tabs.appendChild(b);
});

function simpleDiff(pdfText, mdText){
  // normalize for comparison: fullwidth→halfwidth-ish, collapse spaces
  const norm = t => String(t||'')
    .replace(/．/g,'.')
    .replace(/，/g,',')
    .replace(/\r/g,'')
    .replace(/[ \t　]+/g,' ')
    .trim();
  const a = norm(pdfText).split('\n').map((x,i)=>({i,x}));
  const b = norm(mdText).split('\n').map((x,i)=>({i,x}));
  // crude line-set diff: lines in md not in pdf and vice versa (first 40)
  const aSet = new Set(a.map(r=>r.x).filter(Boolean));
  const bSet = new Set(b.map(r=>r.x).filter(Boolean));
  const onlyPdf = a.filter(r=>r.x && !bSet.has(r.x)).slice(0,25);
  const onlyMd  = b.filter(r=>r.x && !aSet.has(r.x)).slice(0,25);
  return {onlyPdf, onlyMd};
}

function render(){
  [...tabs.children].forEach(b=>b.classList.toggle('active', b.textContent===current));
  const s = (D.subjects||{})[current] || {};
  const pdfPrev = s.pdf_text_preview || '';
  const mdPrev = s.md_text_preview || '';
  document.getElementById('pdf-text').textContent = pdfPrev + (s.pdf_text_len>3000 ? '\n…（完整文本见 05_V3_OUTPUT/'+current+'.pdf.txt）' : '');
  document.getElementById('md-text').textContent = mdPrev + (s.md_text_len>3000 ? '\n…（完整 MD 见 02_PREPROCESSING_OUTPUT）' : '');

  const d = simpleDiff(pdfPrev, mdPrev);
  const box = document.getElementById('diff-list');
  box.innerHTML = [
    ...d.onlyPdf.map(r=>`<div class="diff-row"><span class="tag del">仅PDF</span><span class="mono">L${r.i+1}</span><span>${esc(r.x.slice(0,120))}</span></div>`),
    ...d.onlyMd.map(r=>`<div class="diff-row"><span class="tag add">仅MD</span><span class="mono">L${r.i+1}</span><span>${esc(r.x.slice(0,120))}</span></div>`),
  ].join('') || '<div class="note">预览范围内未发现明显行级差异（仍需人工扫一眼全文）</div>';

  // stats
  const qs = s.questions || [];
  const counts = {};
  qs.forEach(q=>{ counts[q.gate]=(counts[q.gate]||0)+1; });
  document.getElementById('q-stats').innerHTML = Object.entries(counts)
    .map(([k,v])=>gateBadge(k)+' <strong>'+v+'</strong>').join(' · ') || '—';
  document.getElementById('g1-status').textContent = (s.status&&s.status.gate1_owner) || 'AWAITING_OWNER';

  renderQuestions(qs);
  renderAttr();
}

function renderQuestions(qs){
  const list = document.getElementById('question-list');
  const gf = document.getElementById('gate-filter').value;
  const q = document.getElementById('q-search').value.trim().toLowerCase();
  const filtered = qs.filter(x=>{
    if (gf!=='all' && x.gate!==gf) return false;
    if (!q) return true;
    const blob = [x.unit_id,x.stem,(x.answer_text||''),(x.options||[]).map(o=>o.label+o.text).join(' ')]
      .join(' ').toLowerCase();
    return blob.includes(q);
  });
  list.innerHTML = filtered.map(x=>{
    const opts = (x.options||[]).map(o=>
      `<div class="opt"><div class="lab">${esc(o.label)}</div><div>${esc(o.text)}</div></div>`
    ).join('') || '<div class="note">无选项</div>';
    return `
    <article class="qcard" data-uid="${esc(x.unit_id)}">
      <header>
        <div class="uid">${esc(x.unit_id)} ${gateBadge(x.gate)}</div>
        <div class="meta">${esc(x.qtype||'')} · labels=[${esc((x.labels||[]).join(','))}] · verify=${esc(x.verify)}</div>
      </header>
      <div class="qstem">${esc(x.stem||'(无题干)')}</div>
      <div class="opts">${opts}</div>
      <div class="answer">
        <strong>答案：</strong>${esc(x.answer_letter||'—')}
        <span class="meta"> raw: ${esc((x.answer_text||'').slice(0,120))}</span>
      </div>
      <div class="meta"><strong>机器 reason：</strong>${esc(x.reason||'')}
        ${(x.gate_reasons||[]).length? ' · '+esc((x.gate_reasons||[]).join(' | ')) : ''}</div>
      <div class="qverdict">
        <strong>Owner：</strong>
        <select data-role="owner" data-uid="${esc(x.unit_id)}">
          <option value="">—</option>
          <option value="pass">正确</option>
          <option value="fail">错误</option>
          <option value="skip">跳过</option>
        </select>
        <select data-role="issuetype" data-uid="${esc(x.unit_id)}">
          <option value="">错误类型…</option>
          <option>题干不完整</option>
          <option>选项不完整</option>
          <option>选项串题</option>
          <option>材料不完整</option>
          <option>图片缺失</option>
          <option>LaTeX错误</option>
          <option>答案错误</option>
          <option>题目边界错误</option>
          <option>其他</option>
        </select>
      </div>
    </article>`;
  }).join('') || '<div class="note">无匹配题目</div>';
}

function renderAttr(){
  const tb = document.querySelector('#attr-table tbody');
  tb.innerHTML = SUBJECTS.map(name=>{
    const s = (D.subjects||{})[name]||{};
    const qs = s.questions||[];
    const counts = {};
    const reasons = {};
    qs.forEach(q=>{
      counts[q.gate]=(counts[q.gate]||0)+1;
      const r=(q.reason||'').split('(')[0].trim();
      if(r) reasons[r]=(reasons[r]||0)+1;
    });
    const topReason = Object.entries(reasons).sort((a,b)=>b[1]-a[1])[0];
    let layer='待 Owner Gate';
    const inc = counts.incomplete||0, pend=counts.pending_review||0;
    if (inc>0 && pend>0) layer='IR incomplete + answer-side';
    else if (pend>0 && !inc) layer='answer-side / S0 family（题目可能完好）';
    else if (counts.rejected) layer='Gate rejected — 需逐题看';
    else if (counts.auto_approve) layer='机器全过 — 抽查即可';
    return `<tr>
      <td>${name}</td>
      <td>${qs.length}</td>
      <td>${Object.entries(counts).map(([k,v])=>esc(k)+':'+v).join('<br/>')}</td>
      <td>${topReason?esc(topReason[0])+' ('+topReason[1]+')':'—'}</td>
      <td>${esc(layer)}</td>
    </tr>`;
  }).join('');
}

document.getElementById('gate-filter').addEventListener('change', ()=>{
  const s=(D.subjects||{})[current]||{};
  renderQuestions(s.questions||[]);
});
document.getElementById('q-search').addEventListener('input', ()=>{
  const s=(D.subjects||{})[current]||{};
  renderQuestions(s.questions||[]);
});

render();
"""

data_js = "window.E2E_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n"

(OUT / "index.html").write_text(html, encoding="utf-8")
(OUT / "style.css").write_text(css, encoding="utf-8")
(OUT / "app.js").write_text(js, encoding="utf-8")
(OUT / "data.js").write_text(data_js, encoding="utf-8")
print("index", (OUT/"index.html").stat().st_size)
print("data.js", (OUT/"data.js").stat().st_size)
print("app.js", (OUT/"app.js").stat().st_size)
# sanity: questions present
d = json.loads((OUT/"viewer_data.json").read_text(encoding="utf-8"))
for k,v in d["subjects"].items():
    print(k, "questions", len(v.get("questions") or []), "pdf_len", v.get("pdf_text_len"), "md_len", v.get("md_text_len"))
