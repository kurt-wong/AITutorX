from pathlib import Path
import json, hashlib

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
raw = json.loads((OUT / "viewer_data_raw.json").read_text(encoding="utf-8"))

# data.js embeds RAW only
data_js = "window.E2E_DATA = " + json.dumps(raw, ensure_ascii=False) + ";\n"
(OUT / "data.js").write_text(data_js, encoding="utf-8")
print("data.js sha", hashlib.sha256((OUT/"data.js").read_bytes()).hexdigest())
print("raw json sha", hashlib.sha256((OUT/"viewer_data_raw.json").read_bytes()).hexdigest())

html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Owner Viewer — RAW V3 + 公式只读渲染</title>
<link rel="stylesheet" href="vendor/katex/katex.min.css"/>
<link rel="stylesheet" href="style.css"/>
</head>
<body>
<header>
  <div class="hdr-row">
    <div>
      <h1>Owner Viewer</h1>
      <p class="sub">Gate 1：PDF ↔ MD · Gate 2：RAW Question · 公式只读渲染（不改数据）</p>
    </div>
    <div class="hdr-right">
      <div class="chip warn">P1.4-B FROZEN</div>
      <div class="chip">RAW export · no option split</div>
      <div class="chip" id="run-id"></div>
    </div>
  </div>
  <nav id="subject-tabs"></nav>
  <div class="policy">
    <strong>数据策略：</strong>本页只展示真实管线输出。渲染器<strong>不得</strong>改写题干/选项/答案。
    渲染失败时显示原始 LaTeX 并标记失败。auto/pending/rejected 是机器状态，不是正确性结论。
    <span id="sha-status" class="mono"></span>
  </div>
</header>

<main>
  <!-- formula self-test -->
  <section class="card" id="formula-test">
    <h2>公式渲染自检（显示层 only）</h2>
    <div class="grid2">
      <div>
        <h3>行内</h3>
        <div class="fx-demo" data-tex="x^2+y^2=r^2"></div>
        <h3>分数 / 根号</h3>
        <div class="fx-demo" data-tex="\frac{x^2-1}{x-1}=x+1"></div>
        <div class="fx-demo" data-tex="\sqrt{a^2+b^2}"></div>
        <h3>化学</h3>
        <div class="fx-demo" data-tex="\mathrm{H}^{+} + \mathrm{SO}_{4}^{2-} + \mathrm{Ba}^{2+} + \mathrm{OH}^{-} = \mathrm{BaSO}_{4}\downarrow + \mathrm{H}_{2}O"></div>
      </div>
      <div>
        <h3>矩阵</h3>
        <div class="fx-demo" data-tex="\begin{pmatrix} a & b \\ c & d \end{pmatrix}"></div>
        <h3>分段</h3>
        <div class="fx-demo" data-tex="f(x)=\begin{cases} x & x\ge 0 \\ -x & x<0 \end{cases}"></div>
        <h3>非法 LaTeX（必须可见失败）</h3>
        <div class="fx-demo" data-tex="\frac{x^2-1}{"></div>
      </div>
    </div>
  </section>

  <section class="card" id="gate1">
    <div class="card-head">
      <h2>Gate 1 · PDF 文本 ↔ MD</h2>
      <div class="tools">
        <input id="diff-filter" type="search" placeholder="过滤…"/>
      </div>
    </div>
    <div class="side-by-side">
      <div class="pane"><h3>PDF 文本层</h3><pre id="pdf-text" class="src"></pre></div>
      <div class="pane"><h3>MD <span class="badge pending" id="g1-status">AWAITING_OWNER</span></h3><pre id="md-text" class="src"></pre></div>
    </div>
    <div class="diff-box"><h3>行级差异</h3><div id="diff-list"></div></div>
  </section>

  <section class="card" id="gate2">
    <div class="card-head">
      <h2>Gate 2 · RAW Question（渲染仅作用于显示）</h2>
      <div class="tools">
        <select id="gate-filter">
          <option value="all">全部</option>
          <option value="auto_approve">auto_approve</option>
          <option value="pending_review">pending_review</option>
          <option value="rejected">rejected</option>
          <option value="incomplete">incomplete</option>
        </select>
        <input id="q-search" type="search" placeholder="搜索…"/>
        <label class="chk"><input type="checkbox" id="show-raw-tex"/> 显示原始 LaTeX</label>
      </div>
    </div>
    <div class="stats" id="q-stats"></div>
    <div id="question-list"></div>
  </section>

  <section class="card">
    <h2>数据不变性</h2>
    <pre id="integrity" class="src"></pre>
  </section>
</main>

<script src="vendor/katex/katex.min.js"></script>
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
header{padding:20px 24px 0;background:linear-gradient(180deg,#fffdf8,var(--bg));
  border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}
.hdr-row{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
h1{margin:0 0 4px;font-size:22px} h2{margin:0 0 8px;font-size:16px}
h3{margin:10px 0 6px;font-size:13px;color:var(--muted)}
.sub{margin:0;color:var(--muted);font-size:12.5px}
.hdr-right{display:flex;flex-direction:column;gap:6px;align-items:flex-end}
.chip{font-size:11.5px;padding:3px 9px;border-radius:999px;background:#efe8da}
.chip.warn{background:#fef3c7;color:var(--warn)}
#subject-tabs{display:flex;gap:6px;flex-wrap:wrap;padding:10px 0}
#subject-tabs button{border:1px solid var(--line);background:#fff;border-radius:8px;
  padding:5px 11px;cursor:pointer;font-size:12.5px}
#subject-tabs button.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.policy{font-size:12px;color:var(--muted);padding:0 0 10px}
.policy .mono{margin-left:8px;font-family:ui-monospace,Consolas,monospace;font-size:11px}
main{padding:16px 24px 40px;max-width:1280px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:14px 16px;margin-bottom:14px}
.card-head{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center}
.tools{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.tools input,.tools select{padding:5px 9px;border:1px solid var(--line);border-radius:8px;font-size:12.5px}
.chk{font-size:11.5px;color:var(--muted)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:800px){.grid2{grid-template-columns:1fr}}
.fx-demo{background:#fff;border:1px solid var(--line);border-radius:8px;padding:10px 12px;min-height:44px}
.fx-demo.render-fail{border-color:var(--fail);background:#fff5f5}
.fx-demo .fail-tag{color:var(--fail);font-size:11px;font-weight:700;margin-right:6px}
.fx-demo .raw-tex{font-family:ui-monospace,Consolas,monospace;font-size:12px;color:#7f1d1d}
.side-by-side{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:900px){.side-by-side{grid-template-columns:1fr}}
.src{background:#1c1b19;color:#e7e5e4;padding:10px;border-radius:8px;height:280px;
  overflow:auto;font-size:11.5px;white-space:pre-wrap;font-family:ui-monospace,Consolas,monospace}
#integrity{height:auto;min-height:120px}
.diff-row{display:grid;grid-template-columns:56px 1fr 1fr;gap:8px;padding:3px 0;
  border-bottom:1px dashed var(--line);font-size:12px}
.tag{font-size:11px;font-weight:700}
.tag.add{color:var(--ok)} .tag.del{color:var(--fail)}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 10px}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px}
.badge.ok{background:#dcfce7;color:var(--ok)}
.badge.warn{background:#fef3c7;color:var(--warn)}
.badge.fail{background:#fee2e2;color:var(--fail)}
.badge.pending{background:#e5e7eb;color:#374151}
.qcard{border:1px solid var(--line);border-radius:10px;background:#fff;padding:12px 14px;margin-bottom:10px}
.qcard .uid{font-weight:700}
.qcard .top{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.qstem{background:#faf7f1;border-radius:8px;padding:10px 12px;font-size:14px}
.opt{display:grid;grid-template-columns:36px 1fr;gap:8px;padding:7px 10px;border-radius:8px;
  background:#faf7f1;font-size:13.5px;margin-top:5px}
.opt .lab{font-weight:700;color:var(--accent)}
.answer{margin-top:8px;padding:9px 11px;border-radius:8px;background:#eef7f2;font-size:13px}
.meta{margin-top:6px;font-size:11.5px;color:var(--muted)}
.raw-line{margin-top:6px;font-size:11px;font-family:ui-monospace,Consolas,monospace;color:#666}
.render-fail{border-color:var(--fail) !important}
"""

js = r"""
const D = window.E2E_DATA || {};
const SUBJECTS = ["数学","物理","化学","英语","语文","政治","地理","历史","生物"];
let current = SUBJECTS[0];
const showRaw = () => document.getElementById('show-raw-tex').checked;

// ---- read-only KaTeX render helper (NEVER mutates D) ----
function renderTex(el, tex, displayMode) {
  if (el.dataset.rendered === '1' && el.dataset.tex === tex && el.dataset.mode === String(!!displayMode)) return;
  el.dataset.tex = tex;
  el.dataset.mode = String(!!displayMode);
  el.dataset.rendered = '1';
  el.classList.remove('render-fail');
  el.innerHTML = '';
  const raw = document.createElement('span');
  raw.className = 'raw-tex';
  raw.textContent = tex;
  if (!window.katex) {
    el.classList.add('render-fail');
    el.innerHTML = '<span class="fail-tag">[KaTeX 未加载]</span>';
    el.appendChild(raw);
    return;
  }
  try {
    katex.render(tex, el, {
      displayMode: !!displayMode,
      throwOnError: true,
      strict: false,
      trust: false,
    });
    if (showRaw()) {
      const s = document.createElement('div');
      s.className = 'raw-line';
      s.textContent = 'raw: ' + tex;
      el.appendChild(s);
    }
  } catch (err) {
    el.classList.add('render-fail');
    el.innerHTML = '<span class="fail-tag">[渲染失败]</span>';
    el.appendChild(raw);
  }
}

// Split text into plain + $...$ / $$...$$ segments and render formulas
function renderRich(container, text, displayBlock) {
  const s = String(text == null ? '' : text);
  // do not mutate source; build display DOM only
  const re = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;
  let last = 0, m;
  container.textContent = '';
  while ((m = re.exec(s))) {
    if (m.index > last) {
      container.appendChild(document.createTextNode(s.slice(last, m.index)));
    }
    const isBlock = !!m[1];
    const tex = (m[1] || m[2] || '').trim();
    const span = document.createElement('span');
    span.className = isBlock ? 'tex-block' : 'tex-inline';
    container.appendChild(span);
    renderTex(span, tex, isBlock && displayBlock !== false);
    last = m.index + m[0].length;
  }
  if (last < s.length) container.appendChild(document.createTextNode(s.slice(last)));
}

// formula self-test
document.querySelectorAll('.fx-demo').forEach(el=>{
  renderTex(el, el.getAttribute('data-tex')||'', true);
});

document.getElementById('show-raw-tex').addEventListener('change', ()=>{
  document.querySelectorAll('.fx-demo').forEach(el=>{ el.dataset.rendered=''; });
  document.querySelectorAll('.fx-demo').forEach(el=>{
    renderTex(el, el.getAttribute('data-tex')||'', true);
  });
  render();
});

document.getElementById('run-id').textContent = D.run_id || '';
document.getElementById('sha-status').textContent =
  'raw_v3_sha_locked=' + (D.data_policy && D.data_policy.raw_only ? 'YES' : 'NO');

function esc(s){return String(s==null?'':s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
function gateBadge(g){
  if(g==='auto_approve') return '<span class="badge ok">auto</span>';
  if(g==='pending_review') return '<span class="badge warn">pending</span>';
  if(g==='rejected') return '<span class="badge fail">rejected</span>';
  return '<span class="badge pending">'+esc(g||'—')+'</span>';
}

const tabs=document.getElementById('subject-tabs');
SUBJECTS.forEach(s=>{
  const b=document.createElement('button');
  b.textContent=s;
  b.onclick=()=>{current=s;render();};
  tabs.appendChild(b);
});

function simpleDiff(pdfText, mdText){
  const norm=t=>String(t||'').replace(/．/g,'.').replace(/，/g,',').replace(/\r/g,'')
    .replace(/[ \t　]+/g,' ').trim();
  const a=norm(pdfText).split('\n'), b=norm(mdText).split('\n');
  const aSet=new Set(a.filter(Boolean)), bSet=new Set(b.filter(Boolean));
  return {
    onlyPdf: a.map((x,i)=>({i,x})).filter(r=>r.x&&!bSet.has(r.x)).slice(0,25),
    onlyMd: b.map((x,i)=>({i,x})).filter(r=>r.x&&!aSet.has(r.x)).slice(0,25),
  };
}

function render(){
  [...tabs.children].forEach(b=>b.classList.toggle('active', b.textContent===current));
  const s=(D.subjects||{})[current]||{};
  document.getElementById('pdf-text').textContent=(s.pdf_text_preview||'')+
    (s.pdf_text_len>4000?'\n…（完整见 05_V3_OUTPUT/'+current+'.pdf.txt）':'');
  document.getElementById('md-text').textContent=(s.md_text_preview||'')+
    (s.md_text_len>4000?'\n…（完整见 02_PREPROCESSING_OUTPUT）':'');
  const d=simpleDiff(s.pdf_text_preview||'', s.md_text_preview||'');
  document.getElementById('diff-list').innerHTML=
    [...d.onlyPdf.map(r=>`<div class="diff-row"><span class="tag del">仅PDF</span><span>L${r.i+1}</span><span>${esc(r.x.slice(0,110))}</span></div>`),
     ...d.onlyMd.map(r=>`<div class="diff-row"><span class="tag add">仅MD</span><span>L${r.i+1}</span><span>${esc(r.x.slice(0,110))}</span></div>`)]
    .join('')||'<div class="meta">预览范围内无明显行差</div>';
  document.getElementById('g1-status').textContent=(s.status&&s.status.gate1_owner)||'AWAITING_OWNER';

  const qs=s.questions||[];
  const counts={};
  qs.forEach(q=>{counts[q.gate]=(counts[q.gate]||0)+1;});
  document.getElementById('q-stats').innerHTML=Object.entries(counts)
    .map(([k,v])=>gateBadge(k)+' <strong>'+v+'</strong>').join(' · ')||'—';

  renderQuestions(qs);
  renderIntegrity();
}

function renderQuestions(qs){
  const list=document.getElementById('question-list');
  const gf=document.getElementById('gate-filter').value;
  const q=document.getElementById('q-search').value.trim().toLowerCase();
  const filtered=qs.filter(x=>{
    if(gf!=='all'&&x.gate!==gf) return false;
    if(!q) return true;
    const blob=[x.unit_id,x.stem_raw,x.answer_raw,(x.options_raw||[]).map(o=>o.label+(o.text_raw||'')).join(' ')].join(' ').toLowerCase();
    return blob.includes(q);
  });

  list.innerHTML=filtered.map(x=>{
    const opts=(x.options_raw||[]).map(o=>`
      <div class="opt"><div class="lab">${esc(o.label)}</div>
      <div class="opt-body" data-role="opt-text"></div></div>`).join('')||'<div class="meta">无选项</div>';
    return `
    <article class="qcard" data-uid="${esc(x.unit_id)}">
      <div class="top">
        <div class="uid">${esc(x.unit_id)} ${gateBadge(x.gate)}</div>
        <div class="meta">${esc(x.qtype||'')} · labels=[${esc((x.labels||[]).join(','))}]</div>
      </div>
      <div class="qstem" data-role="stem"></div>
      <div class="opts">${opts}</div>
      <div class="answer"><strong>答案：</strong>${esc(x.answer_letter||'—')}
        <div class="meta" data-role="ans"></div></div>
      <div class="meta"><strong>reason：</strong>${esc(x.reason||'')}</div>
      <div class="raw-line">RAW stem/options/answer 未做任何切分或补齐</div>
    </article>`;
  }).join('')||'<div class="meta">无匹配</div>';

  // then hydrate with formula rendering (display-only)
  filtered.forEach((x, idx)=>{
    const card=list.querySelectorAll('.qcard')[idx];
    if(!card) return;
    renderRich(card.querySelector('[data-role=stem]'), x.stem_raw||'', true);
    const bodies=card.querySelectorAll('[data-role=opt-text]');
    (x.options_raw||[]).forEach((o,i)=>{
      if(bodies[i]) renderRich(bodies[i], o.text_raw||'', true);
    });
    renderRich(card.querySelector('[data-role=ans]'), 'raw: '+(x.answer_raw||''), true);
  });
}

function renderIntegrity(){
  const lines=[
    'viewer_data_raw.json = RAW V3 export (options_raw[].text_raw untouched)',
    'data.js mirrors viewer_data_raw.json',
    'renderer = display-only KaTeX; no write to D',
    '',
    'raw V3 output SHA256 (locked):'
  ];
  const h=D.raw_v3_output_sha256||{};
  Object.entries(h).forEach(([k,v])=>lines.push('  '+k+'  '+v));
  lines.push('', 'data_policy: '+JSON.stringify(D.data_policy||{}));
  document.getElementById('integrity').textContent=lines.join('\n');
}

document.getElementById('gate-filter').addEventListener('change', render);
document.getElementById('q-search').addEventListener('input', render);
render();
"""

(OUT / "index.html").write_text(html, encoding="utf-8")
(OUT / "style.css").write_text(css, encoding="utf-8")
(OUT / "app.js").write_text(js, encoding="utf-8")

# integrity note
print("data.js bytes", (OUT/"data.js").stat().st_size)
print("index bytes", (OUT/"index.html").stat().st_size)
# verify math Q4 raw options unchanged
d = json.loads((OUT/"viewer_data_raw.json").read_text(encoding="utf-8"))
for q in d["subjects"]["数学"]["questions"]:
    if q["unit_id"]=="Q4":
        print("Math Q4 RAW options:")
        for o in q["options_raw"]:
            print(" ", o["label"], repr((o.get("text_raw") or "")[:70]))
        break
print("chem Q7 RAW:")
for q in d["subjects"]["化学"]["questions"]:
    if q["unit_id"]=="Q7":
        for o in q["options_raw"]:
            print(" ", o["label"], repr((o.get("text_raw") or "")[:70]))
        break
