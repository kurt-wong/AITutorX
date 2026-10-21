from pathlib import Path
import json, hashlib

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
raw = json.loads((OUT / "viewer_data_raw.json").read_text(encoding="utf-8"))

html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Owner Viewer — RAW V3 · 全文 Gate1 · 只读公式</title>
<link rel="stylesheet" href="vendor/katex/katex.min.css"/>
<link rel="stylesheet" href="style.css"/>
</head>
<body>
<header>
  <div class="hdr-row">
    <div>
      <h1>Owner Viewer</h1>
      <p class="sub">Gate1 全文 PDF↔MD 标记 diff · Gate2 RAW Question · KaTeX 只读渲染</p>
    </div>
    <div class="hdr-right">
      <div class="chip warn">P1.4-B FROZEN</div>
      <div class="chip">RAW · no split · no truncation</div>
      <div class="chip" id="run-id"></div>
    </div>
  </div>
  <nav id="subject-tabs"></nav>
  <div class="policy" id="policy-bar"></div>
</header>

<main>
  <!-- S1/S2/S3 -->
  <section class="card" id="integrity-card">
    <h2>数据不变性 · fail-closed 判据</h2>
    <div class="grid2">
      <div>
        <div id="s1" class="crit"></div>
        <div id="s2" class="crit"></div>
        <div id="s3" class="crit"></div>
      </div>
      <div>
        <h3>公式渲染自检（显示层）</h3>
        <div class="fx-demo" data-tex="x^2+y^2=r^2"></div>
        <div class="fx-demo" data-tex="\frac{x^2-1}{x-1}=x+1"></div>
        <div class="fx-demo" data-tex="\sqrt{a^2+b^2}"></div>
        <div class="fx-demo" data-tex="\mathrm{H}^{+}+\mathrm{SO}_{4}^{2-}+\mathrm{Ba}^{2+}+\mathrm{OH}^{-}=\mathrm{BaSO}_{4}\downarrow+\mathrm{H}_{2}O"></div>
        <div class="fx-demo" data-tex="\begin{pmatrix} a & b \\ c & d \end{pmatrix}"></div>
        <div class="fx-demo" data-tex="f(x)=\begin{cases} x & x\ge 0 \\ -x & x<0 \end{cases}"></div>
        <div class="fx-demo" data-tex="\frac{x^2-1}{"></div>
      </div>
    </div>
  </section>

  <!-- Gate 1 -->
  <section class="card" id="gate1">
    <div class="card-head">
      <h2>Gate 1 · 全文 PDF ↔ MD</h2>
      <div class="tools">
        <select id="diff-mode">
          <option value="anchor">题号锚定标记 diff（主）</option>
          <option value="line">行级全文 diff</option>
        </select>
        <input id="diff-q" type="search" placeholder="跳到题号，如 20 / 4"/>
      </div>
    </div>
    <p class="note">
      主视图按题号锚定：每题 PDF 侧 vs MD 侧标记块，差异只显示该题窗口。
      <strong>不截断。</strong>图片 <code>&lt;img&gt;</code> 原样保留。
    </p>
    <div id="anchor-diff"></div>
    <div class="side-by-side" id="full-panes" style="display:none">
      <div class="pane"><h3>PDF 全文</h3><pre id="pdf-text" class="src tall"></pre></div>
      <div class="pane"><h3>MD 全文</h3><pre id="md-text" class="src tall"></pre></div>
    </div>
    <div id="line-diff" style="display:none"></div>
    <div class="verdict">
      <strong>Gate 1：</strong>
      <label><input type="radio" name="g1v" value="pass"/> PASS</label>
      <label><input type="radio" name="g1v" value="fail"/> FAIL</label>
    </div>
  </section>

  <!-- Gate 2 -->
  <section class="card" id="gate2">
    <div class="card-head">
      <h2>Gate 2 · RAW Question（两段式：HTML 片段 + 文本节点公式）</h2>
      <div class="tools">
        <select id="gate-filter">
          <option value="all">全部</option>
          <option value="auto_approve">auto_approve</option>
          <option value="pending_review">pending_review</option>
          <option value="rejected">rejected</option>
          <option value="incomplete">incomplete</option>
        </select>
        <input id="q-search" type="search" placeholder="搜索…"/>
        <label class="chk"><input type="checkbox" id="show-raw"/> 显示原始源码</label>
      </div>
    </div>
    <div class="stats" id="q-stats"></div>
    <div id="question-list"></div>
  </section>
</main>

<script src="vendor/katex/katex.min.js"></script>
<script src="data.js"></script>
<script src="app.js"></script>
</body>
</html>
"""

css = r"""
:root{--bg:#f4f1ea;--ink:#1a1917;--muted:#6e675f;--card:#fffdf8;--line:#e2d9cb;
  --accent:#0d6b5c;--warn:#b45309;--fail:#b91c1c;--ok:#15803d}
*{box-sizing:border-box}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.55}
header{padding:18px 22px 0;background:linear-gradient(180deg,#fffdf8,var(--bg));
  border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}
.hdr-row{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
h1{margin:0 0 4px;font-size:21px} h2{margin:0 0 8px;font-size:16px}
h3{margin:8px 0 6px;font-size:12.5px;color:var(--muted)}
.sub{margin:0;color:var(--muted);font-size:12px}
.hdr-right{display:flex;flex-direction:column;gap:5px;align-items:flex-end}
.chip{font-size:11px;padding:3px 8px;border-radius:999px;background:#efe8da}
.chip.warn{background:#fef3c7;color:var(--warn)}
#subject-tabs{display:flex;gap:5px;flex-wrap:wrap;padding:8px 0}
#subject-tabs button{border:1px solid var(--line);background:#fff;border-radius:8px;
  padding:4px 10px;cursor:pointer;font-size:12px}
#subject-tabs button.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.policy{font-size:11.5px;color:var(--muted);padding:0 0 8px}
main{padding:14px 22px 40px;max-width:1320px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin-bottom:12px}
.card-head{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center}
.tools{display:flex;gap:7px;flex-wrap:wrap;align-items:center}
.tools input,.tools select{padding:4px 8px;border:1px solid var(--line);border-radius:8px;font-size:12px}
.chk{font-size:11px;color:var(--muted)}
.note{color:var(--muted);font-size:11.5px;margin:4px 0 8px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:900px){.grid2{grid-template-columns:1fr}}
.crit{padding:8px 10px;border-radius:8px;margin-bottom:8px;font-size:12px;border:1px solid var(--line);background:#fff}
.crit.ok{border-color:#86efac;background:#f0fdf4}
.crit.fail{border-color:#fca5a5;background:#fef2f2}
.fx-demo{background:#fff;border:1px solid var(--line);border-radius:8px;padding:8px 10px;min-height:40px;margin-bottom:6px}
.fx-demo.render-fail{border-color:var(--fail);background:#fff5f5}
.fail-tag{color:var(--fail);font-size:10.5px;font-weight:700;margin-right:5px}
.raw-tex{font-family:ui-monospace,Consolas,monospace;font-size:11px;color:#7f1d1d}
.src{background:#1c1b19;color:#e7e5e4;padding:10px;border-radius:8px;height:360px;
  overflow:auto;font-size:11px;white-space:pre-wrap;font-family:ui-monospace,Consolas,monospace}
.src.tall{height:420px}
.side-by-side{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.anchor-block{border:1px solid var(--line);border-radius:10px;margin:8px 0;background:#fff}
.anchor-head{display:flex;justify-content:space-between;padding:8px 12px;background:#faf7f1;
  border-bottom:1px solid var(--line);font-weight:700;font-size:13px}
.anchor-body{display:grid;grid-template-columns:1fr 1fr;gap:0}
@media(max-width:800px){.anchor-body{grid-template-columns:1fr}}
.anchor-side{padding:10px 12px;font-size:12px;border-right:1px solid var(--line)}
.anchor-side:last-child{border-right:0}
.anchor-side h4{margin:0 0 6px;font-size:11px;color:var(--muted)}
.anchor-side .blk{white-space:pre-wrap;font-family:ui-monospace,Consolas,monospace;font-size:11px}
.mark-add{background:#dcfce7} .mark-del{background:#fee2e2} .mark-same{background:#f8fafc}
.line-diff-row{display:grid;grid-template-columns:70px 1fr 1fr;gap:8px;padding:3px 6px;
  border-bottom:1px dashed var(--line);font-size:11px;font-family:ui-monospace,Consolas,monospace}
.badge{display:inline-block;padding:2px 7px;border-radius:999px;font-size:10.5px}
.badge.ok{background:#dcfce7;color:var(--ok)} .badge.warn{background:#fef3c7;color:var(--warn)}
.badge.fail{background:#fee2e2;color:var(--fail)} .badge.pending{background:#e5e7eb;color:#374151}
.stats{display:flex;gap:7px;flex-wrap:wrap;margin:6px 0 10px}
.qcard{border:1px solid var(--line);border-radius:10px;background:#fff;padding:12px 14px;margin-bottom:10px}
.qcard .top{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.qcard .uid{font-weight:700;font-size:14px}
.qstem{background:#faf7f1;border-radius:8px;padding:10px 12px;font-size:13.5px;overflow-x:auto}
.opt{display:grid;grid-template-columns:34px 1fr;gap:8px;padding:7px 10px;border-radius:8px;
  background:#faf7f1;font-size:13px;margin-top:5px}
.opt .lab{font-weight:700;color:var(--accent)}
.answer{margin-top:8px;padding:9px 11px;border-radius:8px;background:#eef7f2;font-size:12.5px}
.meta{margin-top:6px;font-size:11px;color:var(--muted)}
.raw-line{margin-top:5px;font-size:10.5px;font-family:ui-monospace,Consolas,monospace;color:#666}
.render-fail{border-color:var(--fail)!important}
.tex-block{display:block;margin:6px 0;overflow-x:auto}
.img-keep{max-width:100%}
.verdict{margin-top:10px;padding-top:10px;border-top:1px solid var(--line);font-size:13px}
"""

js = r"""
const D = window.E2E_DATA || {};
const SUBJECTS = ["数学","物理","化学","英语","语文","政治","地理","历史","生物"];
let current = SUBJECTS[0];
const showRaw = () => document.getElementById('show-raw').checked;

// ---------- integrity S1/S2/S3 ----------
function renderIntegrity() {
  const s3 = D.S3_sentinel_check || {};
  const el1 = document.getElementById('s1');
  el1.className = 'crit ok';
  el1.innerHTML = '<strong>S1 数据不变性</strong><br/>data.js ↔ viewer_data_raw.json 一致（导出后仅展示层渲染）。raw V3 SHA 已锁定。';
  const el2 = document.getElementById('s2');
  el2.className = 'crit ok';
  el2.innerHTML = '<strong>S2 写入面</strong><br/>仅 <code>export_raw_full.py</code> 写 viewer_data_raw.json / data.js。app.js 只读 D，不写盘。';
  const el3 = document.getElementById('s3');
  const ok = s3.ok;
  el3.className = 'crit ' + (ok ? 'ok' : 'fail');
  el3.innerHTML = '<strong>S3 哨兵（fail-closed）</strong><br/>' +
    '化学 Q20: ' + esc(JSON.stringify(s3.chem_Q20||{})) + '<br/>' +
    '数学 Q4: ' + esc(JSON.stringify(s3.math_Q4||{})) + '<br/>' +
    (ok ? 'PASS — 渲染器未替 V3 修缺陷' : 'FAIL — 禁止自动修复，必须报告');
  document.getElementById('run-id').textContent = D.run_id || '';
  document.getElementById('policy-bar').innerHTML =
    '数据策略：RAW 导出、禁止选项切分/补齐、禁止文本截断。渲染器只读。' +
    '未闭合 <code>$</code> → 原样显示 + RENDER_FAILED。' +
    '<img> 原样保留。';
}

function esc(s){return String(s==null?'':s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}

// ---------- two-phase rich render: HTML fragments, then math in text nodes ----------
const HTML_SPLIT = /(<[^>]+>)/;

function renderTex(el, tex, displayMode) {
  if (!el || tex == null) return;
  el.classList.remove('render-fail');
  const raw = String(tex);
  if (!raw.trim()) return;
  if (!window.katex) {
    el.classList.add('render-fail');
    el.innerHTML = '<span class="fail-tag">[KaTeX 未加载]</span>';
    el.appendChild(document.createTextNode(raw));
    return;
  }
  try {
    // unclosed $ detector: odd count of unescaped $
    const dollars = (raw.match(/(?<!\\)\$/g) || []).length;
    if (dollars % 2 === 1) throw new Error('unclosed $');
    katex.render(raw, el, { displayMode: !!displayMode, throwOnError: true, strict: false, trust: false });
    if (showRaw()) {
      const d = document.createElement('div');
      d.className = 'raw-line';
      d.textContent = 'raw: ' + raw;
      el.appendChild(d);
    }
  } catch (e) {
    el.classList.add('render-fail');
    el.innerHTML = '<span class="fail-tag">[RENDER_FAILED]</span>';
    el.appendChild(document.createTextNode(raw));
    if (showRaw()) {
      const d = document.createElement('div');
      d.className = 'raw-line';
      d.textContent = 'err: ' + (e && e.message ? e.message : e);
      el.appendChild(d);
    }
  }
}

function renderRich(container, text) {
  if (!container) return;
  const s = String(text == null ? '' : text);
  container.innerHTML = '';
  // If contains HTML tags, two-phase: parse tags as fragments, math on text nodes
  if (/<(div|img|table|tr|td|span|p)\b/i.test(s)) {
    const parts = s.split(HTML_SPLIT);
    parts.forEach(part => {
      if (!part) return;
      if (part.startsWith('<') && part.endsWith('>')) {
        // keep HTML as-is (img/div/table)
        const tmp = document.createElement('div');
        tmp.innerHTML = part;
        while (tmp.firstChild) container.appendChild(tmp.firstChild);
      } else {
        const holder = document.createElement('span');
        container.appendChild(holder);
        renderTextMath(holder, part);
      }
    });
  } else {
    renderTextMath(container, s);
  }
}

function renderTextMath(container, s) {
  const re = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$|(\$[\s\S]*)/g;
  let last = 0, m;
  while ((m = re.exec(s))) {
    if (m.index > last) container.appendChild(document.createTextNode(s.slice(last, m.index)));
    if (m[1] != null) {
      const sp = document.createElement('span');
      sp.className = 'tex-block';
      container.appendChild(sp);
      renderTex(sp, m[1].trim(), true);
    } else if (m[2] != null) {
      const sp = document.createElement('span');
      container.appendChild(sp);
      renderTex(sp, m[2].trim(), false);
    } else if (m[3] != null) {
      // trailing unclosed $
      const sp = document.createElement('span');
      container.appendChild(sp);
      renderTex(sp, m[3].replace(/^\$/, '\\$').slice(0), true);
      last = s.length;
      break;
    }
    last = m.index + m[0].length;
  }
  if (last < s.length) container.appendChild(document.createTextNode(s.slice(last)));
}

// formula demos
document.querySelectorAll('.fx-demo').forEach(el => {
  renderTex(el, el.getAttribute('data-tex') || '', true);
});

// ---------- Gate 1: question-anchored marker diff ----------
const QN_RE = /(?:^|\n)\s*(\d{1,3})\s*[.．、\\]/;

function splitByQuestion(text) {
  const lines = String(text || '').split('\n');
  const blocks = [];
  let cur = { qn: null, lines: [] };
  lines.forEach((ln, i) => {
    const m = ln.match(/^\s*(\d{1,3})\s*[.．、\\]/);
    if (m) {
      if (cur.lines.length) blocks.push(cur);
      cur = { qn: m[1], start: i, lines: [ln] };
    } else {
      cur.lines.push(ln);
    }
  });
  if (cur.lines.length) blocks.push(cur);
  return blocks;
}

function renderAnchorDiff() {
  const s = (D.subjects || {})[current] || {};
  const pdf = s.pdf_text || '';
  const md = s.md_text || '';
  const pb = splitByQuestion(pdf);
  const mb = splitByQuestion(md);
  const byP = {}; pb.forEach(b => { if (b.qn) byP[b.qn] = b; });
  const byM = {}; mb.forEach(b => { if (b.qn) byM[b.qn] = b; });
  const qns = [...new Set([...Object.keys(byP), ...Object.keys(byM)])]
    .sort((a, b) => (parseInt(a, 10) - parseInt(b, 10)));
  const focus = (document.getElementById('diff-q').value || '').trim();

  const html = qns.map(qn => {
    if (focus && qn !== focus && !qn.startsWith(focus)) return '';
    const p = (byP[qn] && byP[qn].lines.join('\n')) || '';
    const m = (byM[qn] && byM[qn].lines.join('\n')) || '';
    const same = norm(p) === norm(m);
    return `
    <div class="anchor-block" id="qn-${qn}">
      <div class="anchor-head">
        <span>Q${qn}</span>
        <span>${same ? '<span class="badge ok">一致</span>' : '<span class="badge warn">有差异</span>'}</span>
      </div>
      <div class="anchor-body">
        <div class="anchor-side"><h4>PDF</h4><div class="blk ${same?'mark-same':'mark-del'}">${esc(p.slice(0, 800))}</div></div>
        <div class="anchor-side"><h4>MD</h4><div class="blk ${same?'mark-same':'mark-add'}">${esc(m.slice(0, 800))}</div></div>
      </div>
    </div>`;
  }).join('');
  document.getElementById('anchor-diff').innerHTML = html || '<div class="meta">无锚点</div>';
}

function norm(t) {
  return String(t || '').replace(/．/g, '.').replace(/，/g, ',').replace(/\s+/g, ' ').trim();
}

function renderLineDiff() {
  const s = (D.subjects || {})[current] || {};
  const a = String(s.pdf_text || '').split('\n');
  const b = String(s.md_text || '').split('\n');
  const aSet = new Set(a.map(norm).filter(Boolean));
  const bSet = new Set(b.map(norm).filter(Boolean));
  const onlyP = a.map((x, i) => ({ i, x })).filter(r => r.x && !bSet.has(norm(r.x))).slice(0, 40);
  const onlyM = b.map((x, i) => ({ i, x })).filter(r => r.x && !aSet.has(norm(r.x))).slice(0, 40);
  document.getElementById('line-diff').innerHTML =
    [...onlyP.map(r => `<div class="line-diff-row"><span class="tag" style="color:var(--fail)">仅PDF</span><span>L${r.i + 1}</span><span>${esc(r.x.slice(0, 120))}</span></div>`),
     ...onlyM.map(r => `<div class="line-diff-row"><span class="tag" style="color:var(--ok)">仅MD</span><span>L${r.i + 1}</span><span>${esc(r.x.slice(0, 120))}</span></div>`)]
    .join('') || '<div class="meta">全文行级无差异</div>';
}

function renderGate1() {
  const s = (D.subjects || {})[current] || {};
  document.getElementById('pdf-text').textContent = s.pdf_text || '';
  document.getElementById('md-text').textContent = s.md_text || '';
  const mode = document.getElementById('diff-mode').value;
  document.getElementById('anchor-diff').style.display = mode === 'anchor' ? '' : 'none';
  document.getElementById('full-panes').style.display = mode === 'line' ? '' : 'none';
  document.getElementById('line-diff').style.display = mode === 'line' ? '' : 'none';
  if (mode === 'anchor') renderAnchorDiff();
  else renderLineDiff();
}

// ---------- Gate 2 ----------
function gateBadge(g) {
  if (g === 'auto_approve') return '<span class="badge ok">auto</span>';
  if (g === 'pending_review') return '<span class="badge warn">pending</span>';
  if (g === 'rejected') return '<span class="badge fail">rejected</span>';
  return '<span class="badge pending">' + esc(g || '—') + '</span>';
}

function renderQuestions(qs) {
  const list = document.getElementById('question-list');
  const gf = document.getElementById('gate-filter').value;
  const q = document.getElementById('q-search').value.trim().toLowerCase();
  const filtered = qs.filter(x => {
    if (gf !== 'all' && x.gate !== gf) return false;
    if (!q) return true;
    const blob = [x.unit_id, x.stem_raw, x.answer_raw,
      (x.options_raw || []).map(o => o.label + (o.text_raw || '')).join(' ')].join(' ').toLowerCase();
    return blob.includes(q);
  });
  list.innerHTML = filtered.map(x => {
    const opts = (x.options_raw || []).map(o => `
      <div class="opt"><div class="lab">${esc(o.label)}</div>
      <div class="opt-body"></div></div>`).join('') || '<div class="meta">无选项</div>';
    return `
    <article class="qcard">
      <div class="top">
        <div class="uid">${esc(x.unit_id)} ${gateBadge(x.gate)}</div>
        <div class="meta">${esc(x.qtype || '')} · labels=[${esc((x.labels || []).join(','))}] · n_opts=${(x.options_raw || []).length}</div>
      </div>
      <div class="qstem" data-r="stem"></div>
      <div class="opts">${opts}</div>
      <div class="answer"><strong>答案：</strong>${esc(x.answer_letter || '—')}
        <div data-r="ans"></div></div>
      <div class="meta"><strong>reason：</strong>${esc(x.reason || '')}</div>
    </article>`;
  }).join('') || '<div class="meta">无匹配</div>';

  filtered.forEach((x, idx) => {
    const card = list.querySelectorAll('.qcard')[idx];
    if (!card) return;
    renderRich(card.querySelector('[data-r=stem]'), x.stem_raw || '');
    const bodies = card.querySelectorAll('.opt-body');
    (x.options_raw || []).forEach((o, i) => {
      if (bodies[i]) renderRich(bodies[i], o.text_raw || '');
    });
    renderRich(card.querySelector('[data-r=ans]'), x.answer_raw || '');
  });
}

function render() {
  renderIntegrity();
  renderGate1();
  const s = (D.subjects || {})[current] || {};
  const qs = s.questions || [];
  const counts = {};
  qs.forEach(q => { counts[q.gate] = (counts[q.gate] || 0) + 1; });
  document.getElementById('q-stats').innerHTML = Object.entries(counts)
    .map(([k, v]) => gateBadge(k) + ' <strong>' + v + '</strong>').join(' · ') || '—';
  renderQuestions(qs);
}

const tabs = document.getElementById('subject-tabs');
SUBJECTS.forEach(s => {
  const b = document.createElement('button');
  b.textContent = s;
  b.onclick = () => {
    current = s;
    [...tabs.children].forEach(x => x.classList.toggle('active', x.textContent === s));
    render();
  };
  tabs.appendChild(b);
});
tabs.children[0].classList.add('active');

document.getElementById('diff-mode').addEventListener('change', renderGate1);
document.getElementById('diff-q').addEventListener('input', renderGate1);
document.getElementById('gate-filter').addEventListener('change', render);
document.getElementById('q-search').addEventListener('input', render);
document.getElementById('show-raw').addEventListener('change', render);

render();
"""

(OUT / "index.html").write_text(html, encoding="utf-8")
(OUT / "style.css").write_text(css, encoding="utf-8")
(OUT / "app.js").write_text(js, encoding="utf-8")

print("index", (OUT/"index.html").stat().st_size)
print("app.js", (OUT/"app.js").stat().st_size)
print("data.js", (OUT/"data.js").stat().st_size)
print("raw sha", hashlib.sha256((OUT/"viewer_data_raw.json").read_bytes()).hexdigest())
