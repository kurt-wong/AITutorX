"""Viewer assist: option integrity badges + per-dimension owner feedback + Gate1 full text.

Does NOT write viewer_data_raw.json / data.js (FROZEN).
Does NOT touch production Resolver/Producer/Gate.
"""
from pathlib import Path
import json, hashlib

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")

# load from FROZEN copy for display (read-only)
frozen = json.loads((OUT / "FROZEN_EVIDENCE" / "viewer_data_raw.json").read_text(encoding="utf-8"))

html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Owner Viewer — FROZEN RAW · 分维度验收</title>
<link rel="stylesheet" href="vendor/katex/katex.min.css"/>
<link rel="stylesheet" href="style.css"/>
</head>
<body>
<header>
  <div class="hdr-row">
    <div>
      <h1>Owner Viewer · FROZEN</h1>
      <p class="sub">Gate1 全文 PDF↔MD · Gate2 分维度反馈 · 公式只读渲染 · 选项结构异常只标不定论</p>
    </div>
    <div class="hdr-right">
      <div class="chip warn">RAW FROZEN</div>
      <div class="chip">Resolver 修复另立项</div>
      <div class="chip">E2E 尚未通过</div>
    </div>
  </div>
  <nav id="subject-tabs"></nav>
  <div class="policy" id="policy-bar"></div>
</header>

<main>
  <section class="card" id="facts">
    <h2>冻结事实与口径（本轮只记录，不实施 Resolver 修复）</h2>
    <ul class="facts">
      <li><strong>正式产品链</strong>：<code>TaskExecutor document_ingest → Seal → Annotation → Compile</code>；Annotation 为 V3 自有 LLM 提示词。<strong>不消费 Papers manifest。</strong></li>
      <li><strong>实验路径</strong>：<code>preprocessing_consumer</code>（<code>backend/scripts/</code>，task_type=<code>preprocessing_consumer_phase0</code>）——本 Viewer 数据来源，<strong>不能代替正式 E2E</strong>。</li>
      <li><strong>Resolver 缺陷形态</strong>（待独立立项）：<code>resolver.py::_locate_options</code> L588–611 多标签同 <code>start_line</code> 时 <code>len(starts)==1</code> 提前成功；<code>inline</code> 只定位<strong>标签字符区间</strong>，不定位内容。最小断言应为：每个选项 text =「该标签后至下一标签前」（如数学 Q1: A='1' B='2' C='\pi' D='2\pi'），而非「空壳数下降」。</li>
      <li><strong>可证明上限</strong>：S1 仅内部一致；更强证据 = <code>viewer_data_raw.json</code> ↔ 独立重放逐选项比对（待 DSH 执行，不改文件）。</li>
      <li><strong>冻结后禁止</strong>再跑 <code>export_raw_full.py</code> 覆盖证据；FROZEN_EVIDENCE/ 与 05_V3_OUTPUT/*.v3.json 已只读。</li>
    </ul>
    <div id="freeze-shas" class="mono"></div>
  </section>

  <section class="card" id="gate1">
    <div class="card-head">
      <h2>Gate 1 · 全文 PDF ↔ MD（可检索、可定位）</h2>
      <div class="tools">
        <select id="diff-mode">
          <option value="anchor">题号锚定（主）</option>
          <option value="line">行级全文</option>
          <option value="search">全文检索</option>
        </select>
        <input id="diff-q" type="search" placeholder="题号 20 / 4 …"/>
        <input id="full-search" type="search" placeholder="全文关键字…"/>
      </div>
    </div>
    <div id="anchor-diff"></div>
    <div id="line-diff" class="block"></div>
    <div id="search-hits" class="block"></div>
    <div class="side-by-side" id="full-panes">
      <div class="pane"><h3>PDF 全文（未切片）</h3>
        <pre id="pdf-text" class="src xtall"></pre></div>
      <div class="pane"><h3>MD 全文（未切片）</h3>
        <pre id="md-text" class="src xtall"></pre></div>
    </div>
  </section>

  <section class="card" id="gate2">
    <div class="card-head">
      <h2>Gate 2 · 分维度人工反馈（不整题跳过）</h2>
      <div class="tools">
        <select id="gate-filter">
          <option value="all">全部</option>
          <option value="auto_approve">auto</option>
          <option value="pending_review">pending</option>
          <option value="rejected">rejected</option>
          <option value="incomplete">incomplete</option>
        </select>
        <select id="anomaly-filter">
          <option value="all">选项结构全部</option>
          <option value="ANOMALY">仅选项异常</option>
          <option value="OK">仅选项完整</option>
        </select>
        <input id="q-search" type="search" placeholder="搜索…"/>
        <label class="chk"><input type="checkbox" id="show-raw"/> 源码</label>
      </div>
    </div>
    <div class="stats" id="q-stats"></div>
    <div id="question-list"></div>
    <div class="verdict">
      <button id="export-feedback">导出反馈 JSON（本地下载，不写盘到证据区）</button>
    </div>
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
.facts{font-size:12.5px;line-height:1.6;padding-left:18px}
.facts code{background:#efe8da;padding:1px 4px;border-radius:4px;font-size:11px}
.mono{font-family:ui-monospace,Consolas,monospace;font-size:10.5px;color:var(--muted);margin-top:8px;white-space:pre-wrap}
.src{background:#1c1b19;color:#e7e5e4;padding:10px;border-radius:8px;height:320px;
  overflow:auto;font-size:11px;white-space:pre-wrap;font-family:ui-monospace,Consolas,monospace}
.src.xtall{height:480px}
.side-by-side{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:900px){.side-by-side{grid-template-columns:1fr}}
.anchor-block{border:1px solid var(--line);border-radius:10px;margin:8px 0;background:#fff}
.anchor-head{display:flex;justify-content:space-between;padding:8px 12px;background:#faf7f1;
  border-bottom:1px solid var(--line);font-weight:700;font-size:13px}
.anchor-body{display:grid;grid-template-columns:1fr 1fr}
@media(max-width:800px){.anchor-body{grid-template-columns:1fr}}
.anchor-side{padding:10px 12px;font-size:12px;border-right:1px solid var(--line)}
.anchor-side:last-child{border-right:0}
.anchor-side h4{margin:0 0 6px;font-size:11px;color:var(--muted)}
.anchor-side .blk{white-space:pre-wrap;font-family:ui-monospace,Consolas,monospace;font-size:11px}
.mark-add{background:#dcfce7} .mark-del{background:#fee2e2} .mark-same{background:#f8fafc}
.line-diff-row{display:grid;grid-template-columns:70px 1fr 1fr;gap:8px;padding:3px 6px;
  border-bottom:1px dashed var(--line);font-size:11px;font-family:ui-monospace,Consolas,monospace}
.block{margin:8px 0;display:none}
.badge{display:inline-block;padding:2px 7px;border-radius:999px;font-size:10.5px}
.badge.ok{background:#dcfce7;color:var(--ok)} .badge.warn{background:#fef3c7;color:var(--warn)}
.badge.fail{background:#fee2e2;color:var(--fail)} .badge.pending{background:#e5e7eb;color:#374151}
.badge.anom{background:#fee2e2;color:var(--fail);font-weight:700}
.stats{display:flex;gap:7px;flex-wrap:wrap;margin:6px 0 10px}
.qcard{border:1px solid var(--line);border-radius:10px;background:#fff;padding:12px 14px;margin-bottom:10px}
.qcard.anomaly{border-color:#fca5a5}
.qcard .top{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.qcard .uid{font-weight:700;font-size:14px}
.qstem{background:#faf7f1;border-radius:8px;padding:10px 12px;font-size:13.5px;overflow-x:auto}
.opt{display:grid;grid-template-columns:34px 1fr auto;gap:8px;padding:7px 10px;border-radius:8px;
  background:#faf7f1;font-size:13px;margin-top:5px}
.opt .lab{font-weight:700;color:var(--accent)}
.opt.shell{background:#fef2f2}
.opt.multi{background:#fff7ed}
.answer{margin-top:8px;padding:9px 11px;border-radius:8px;background:#eef7f2;font-size:12.5px}
.answer.unreliable{background:#fef3c7}
.meta{margin-top:6px;font-size:11px;color:var(--muted)}
.raw-line{margin-top:5px;font-size:10.5px;font-family:ui-monospace,Consolas,monospace;color:#666}
.dim-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px;margin-top:10px}
.dim{border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:#fafafa;font-size:12px}
.dim label{display:block;margin:3px 0;font-size:11.5px}
.dim select{width:100%;padding:3px 6px;border-radius:6px;border:1px solid var(--line);font-size:12px}
.verdict{margin-top:12px;padding-top:10px;border-top:1px solid var(--line)}
button{padding:8px 14px;border-radius:8px;border:1px solid var(--accent);background:var(--accent);color:#fff;cursor:pointer;font-size:13px}
.render-fail{border-color:var(--fail)!important}
.fail-tag{color:var(--fail);font-size:10.5px;font-weight:700;margin-right:5px}
.tex-block{display:block;margin:6px 0;overflow-x:auto}
"""

js = r"""
const D = window.E2E_DATA || {};
const SUBJECTS = ["数学","物理","化学","英语","语文","政治","地理","历史","生物"];
let current = SUBJECTS[0];
const showRaw = () => document.getElementById('show-raw').checked;

function esc(s){return String(s==null?'':s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}

// freeze shas
(function(){
  const fr = D.FROZEN_BASELINE || {};
  const lines = ['FROZEN_BASELINE:'];
  Object.entries(fr.sha256||{}).forEach(([k,v])=>lines.push('  '+k+'  '+v.slice(0,16)+'…'));
  document.getElementById('freeze-shas').textContent = lines.join('\n');
})();

// KaTeX (read-only)
function renderTex(el, tex, displayMode) {
  if (!el || tex == null) return;
  el.classList.remove('render-fail');
  const raw = String(tex);
  if (!raw.trim()) return;
  if (!window.katex) {
    el.classList.add('render-fail');
    el.innerHTML = '<span class="fail-tag">[KaTeX 未加载]</span>' + esc(raw);
    return;
  }
  try {
    const dollars = (raw.match(/(?<!\\)\$/g) || []).length;
    if (dollars % 2 === 1) throw new Error('unclosed $');
    katex.render(raw, el, { displayMode: !!displayMode, throwOnError: true, strict: false, trust: false });
    if (showRaw()) {
      const d = document.createElement('div'); d.className='raw-line';
      d.textContent = 'raw: ' + raw; el.appendChild(d);
    }
  } catch (e) {
    el.classList.add('render-fail');
    el.innerHTML = '<span class="fail-tag">[RENDER_FAILED]</span>';
    el.appendChild(document.createTextNode(raw));
  }
}

function renderRich(container, text) {
  if (!container) return;
  const s = String(text == null ? '' : text);
  container.innerHTML = '';
  if (/<(div|img|table|tr|td|span|p)\b/i.test(s)) {
    const parts = s.split(/(<[^>]+>)/);
    parts.forEach(part => {
      if (!part) return;
      if (part.startsWith('<') && part.endsWith('>')) {
        const tmp = document.createElement('div'); tmp.innerHTML = part;
        while (tmp.firstChild) container.appendChild(tmp.firstChild);
      } else {
        const holder = document.createElement('span');
        container.appendChild(holder);
        renderTextMath(holder, part);
      }
    });
  } else renderTextMath(container, s);
}

function renderTextMath(container, s) {
  const re = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$|(\$[\s\S]*)/g;
  let last = 0, m;
  while ((m = re.exec(s))) {
    if (m.index > last) container.appendChild(document.createTextNode(s.slice(last, m.index)));
    if (m[1] != null) {
      const sp = document.createElement('span'); sp.className='tex-block';
      container.appendChild(sp); renderTex(sp, m[1].trim(), true);
    } else if (m[2] != null) {
      const sp = document.createElement('span');
      container.appendChild(sp); renderTex(sp, m[2].trim(), false);
    } else if (m[3] != null) {
      const sp = document.createElement('span');
      container.appendChild(sp); renderTex(sp, m[3], true);
      last = s.length; break;
    }
    last = m.index + m[0].length;
  }
  if (last < s.length) container.appendChild(document.createTextNode(s.slice(last)));
}

// ---------- Gate1 ----------
function splitByQuestion(text) {
  const lines = String(text||'').split('\n');
  const blocks = []; let cur = { qn:null, lines:[] };
  lines.forEach((ln,i)=>{
    const m = ln.match(/^\s*(\d{1,3})\s*[.．、\\]/);
    if (m) { if (cur.lines.length) blocks.push(cur); cur = { qn:m[1], start:i, lines:[ln] }; }
    else cur.lines.push(ln);
  });
  if (cur.lines.length) blocks.push(cur);
  return blocks;
}
function norm(t){return String(t||'').replace(/．/g,'.').replace(/，/g,',').replace(/\s+/g,' ').trim();}

function renderGate1() {
  const s = (D.subjects||{})[current]||{};
  // FULL text — no slice
  document.getElementById('pdf-text').textContent = s.pdf_text || '';
  document.getElementById('md-text').textContent = s.md_text || '';
  const mode = document.getElementById('diff-mode').value;
  const focus = (document.getElementById('diff-q').value||'').trim();
  const kw = (document.getElementById('full-search').value||'').trim().toLowerCase();

  const anchor = document.getElementById('anchor-diff');
  const lineD = document.getElementById('line-diff');
  const searchH = document.getElementById('search-hits');

  anchor.style.display = mode==='anchor'?'':'none';
  lineD.style.display = mode==='line'?'block':'none';
  searchH.style.display = mode==='search'?'block':'none';

  if (mode==='anchor') {
    const pb = splitByQuestion(s.pdf_text||'');
    const mb = splitByQuestion(s.md_text||'');
    const byP={}, byM={};
    pb.forEach(b=>{if(b.qn)byP[b.qn]=b;});
    mb.forEach(b=>{if(b.qn)byM[b.qn]=b;});
    const qns=[...new Set([...Object.keys(byP),...Object.keys(byM)])]
      .sort((a,b)=>parseInt(a,10)-parseInt(b,10));
    anchor.innerHTML = qns.map(qn=>{
      if (focus && !(qn===focus || qn.startsWith(focus))) return '';
      const p=(byP[qn]&&byP[qn].lines.join('\n'))||'';
      const m=(byM[qn]&&byM[qn].lines.join('\n'))||'';
      const same = norm(p)===norm(m);
      return `<div class="anchor-block">
        <div class="anchor-head"><span>Q${qn}</span>
        <span>${same?'<span class="badge ok">一致</span>':'<span class="badge warn">有差异</span>'}</span></div>
        <div class="anchor-body">
          <div class="anchor-side"><h4>PDF</h4><div class="blk ${same?'mark-same':'mark-del'}">${esc(p)}</div></div>
          <div class="anchor-side"><h4>MD</h4><div class="blk ${same?'mark-same':'mark-add'}">${esc(m)}</div></div>
        </div></div>`;
    }).join('')||'<div class="meta">无锚点</div>';
  } else if (mode==='line') {
    const a=String(s.pdf_text||'').split('\n'), b=String(s.md_text||'').split('\n');
    const aSet=new Set(a.map(norm).filter(Boolean)), bSet=new Set(b.map(norm).filter(Boolean));
    const onlyP=a.map((x,i)=>({i,x})).filter(r=>r.x&&!bSet.has(norm(r.x))).slice(0,60);
    const onlyM=b.map((x,i)=>({i,x})).filter(r=>r.x&&!aSet.has(norm(r.x))).slice(0,60);
    lineD.innerHTML=[...onlyP.map(r=>`<div class="line-diff-row"><span style="color:var(--fail)">仅PDF</span><span>L${r.i+1}</span><span>${esc(r.x)}</span></div>`),
      ...onlyM.map(r=>`<div class="line-diff-row"><span style="color:var(--ok)">仅MD</span><span>L${r.i+1}</span><span>${esc(r.x)}</span></div>`)]
      .join('')||'<div class="meta">全文无行差</div>';
  } else {
    if (!kw) { searchH.innerHTML='<div class="meta">输入关键字检索 PDF/MD 全文</div>'; return; }
    const hits=[];
    String(s.pdf_text||'').split('\n').forEach((ln,i)=>{ if(ln.toLowerCase().includes(kw)) hits.push(['PDF',i+1,ln]); });
    String(s.md_text||'').split('\n').forEach((ln,i)=>{ if(ln.toLowerCase().includes(kw)) hits.push(['MD',i+1,ln]); });
    searchH.innerHTML = hits.slice(0,80).map(h=>
      `<div class="line-diff-row"><span>${h[0]}</span><span>L${h[1]}</span><span>${esc(h[2])}</span></div>`
    ).join('')||'<div class="meta">无命中</div>';
  }
}

// ---------- Gate2 ----------
function gateBadge(g){
  if(g==='auto_approve') return '<span class="badge ok">auto</span>';
  if(g==='pending_review') return '<span class="badge warn">pending</span>';
  if(g==='rejected') return '<span class="badge fail">rejected</span>';
  return '<span class="badge pending">'+esc(g||'—')+'</span>';
}

function dimPanel(unitId, oi) {
  const anom = oi && oi.level === 'ANOMALY';
  const answerNote = anom
    ? '受选项结构影响，暂不可判（answer↔labels 一致性依赖 options）'
    : '答案字段可见时可独立检查';
  return `
  <div class="dim-grid">
    <div class="dim"><strong>题干完整性</strong>
      <select data-dim="stem" data-uid="${esc(unitId)}">
        <option value="">—</option><option>正确</option><option>错误</option><option>跳过</option>
      </select></div>
    <div class="dim"><strong>选项完整性</strong>
      <div class="meta">${anom?'<span class="badge anom">选项结构异常</span> 只标异常，不判内容对错':'结构完整'}</div>
      <select data-dim="options" data-uid="${esc(unitId)}">
        <option value="">—</option>
        <option>结构正确</option>
        <option>结构异常-空壳</option>
        <option>结构异常-吞并</option>
        <option>结构异常-其他</option>
      </select></div>
    <div class="dim"><strong>答案完整性</strong>
      <div class="meta">${anom?esc(answerNote):'可独立检查'}</div>
      <select data-dim="answer" data-uid="${esc(unitId)}" ${anom?'disabled':''}>
        <option value="">—</option><option>正确</option><option>错误</option>
        <option value="unreliable">受选项结构影响·暂不可判</option>
      </select></div>
    <div class="dim"><strong>LaTeX 渲染</strong>
      <select data-dim="latex" data-uid="${esc(unitId)}">
        <option value="">—</option><option>渲染正常</option><option>渲染失败</option>
      </select></div>
    <div class="dim"><strong>题目整体</strong>
      <div class="meta">${anom?'选项损坏时暂缓整体结论':'可给出整体结论'}</div>
      <select data-dim="overall" data-uid="${esc(unitId)}">
        <option value="">—</option>
        <option value="pass" ${anom?'disabled':''}>正确</option>
        <option>错误</option>
        <option value="defer">暂缓（选项结构）</option>
      </select></div>
    <div class="dim"><strong>缺陷反馈</strong>
      <select data-dim="issue" data-uid="${esc(unitId)}">
        <option value="">错误类型…</option>
        <option>题干不完整</option><option>选项不完整</option><option>选项串题</option>
        <option>材料不完整</option><option>图片缺失</option><option>LaTeX错误</option>
        <option>答案错误</option><option>题目边界错误</option><option>其他</option>
      </select></div>
  </div>`;
}

function renderQuestions(qs) {
  const list = document.getElementById('question-list');
  const gf = document.getElementById('gate-filter').value;
  const af = document.getElementById('anomaly-filter').value;
  const q = document.getElementById('q-search').value.trim().toLowerCase();
  const filtered = qs.filter(x=>{
    if (gf!=='all' && x.gate!==gf) return false;
    const anom = (x.option_integrity||{}).level==='ANOMALY';
    if (af==='ANOMALY' && !anom) return false;
    if (af==='OK' && anom) return false;
    if (!q) return true;
    const blob=[x.unit_id,x.stem_raw,x.answer_raw,(x.options_raw||[]).map(o=>o.label+(o.text_raw||'')).join(' ')].join(' ').toLowerCase();
    return blob.includes(q);
  });

  list.innerHTML = filtered.map(x=>{
    const oi = x.option_integrity || {level:'OK', options:[]};
    const anom = oi.level==='ANOMALY';
    const flags = {};
    (oi.options||[]).forEach(f=>{ flags[f.label]=f; });
    const opts = (x.options_raw||[]).map(o=>{
      const f = flags[o.label] || {};
      const cls = f.is_shell ? 'shell' : (f.is_multilabel_line ? 'multi' : '');
      const mark = f.is_shell ? '<span class="badge fail">空壳</span>'
        : (f.is_multilabel_line ? '<span class="badge warn">吞并</span>' : '');
      return `<div class="opt ${cls}"><div class="lab">${esc(o.label)}</div>
        <div class="opt-body"></div><div>${mark}</div></div>`;
    }).join('') || '<div class="meta">无选项</div>';
    const ansUnreliable = anom;
    return `
    <article class="qcard ${anom?'anomaly':''}">
      <div class="top">
        <div class="uid">${esc(x.unit_id)} ${gateBadge(x.gate)}
          ${anom?'<span class="badge anom">选项结构异常</span>':''}</div>
        <div class="meta">${esc(x.qtype||'')} · labels=[${esc((x.labels||[]).join(','))}]
          · n=${(x.options_raw||[]).length} · shell=${oi.n_shell||0} · multi=${oi.n_multilabel_line||0}</div>
      </div>
      <div class="qstem" data-r="stem"></div>
      <div class="opts">${opts}</div>
      <div class="answer ${ansUnreliable?'unreliable':''}">
        <strong>答案：</strong>${esc(x.answer_letter||'—')}
        ${ansUnreliable?'<span class="badge warn">一致性暂不可判</span>':''}
        <div data-r="ans"></div>
      </div>
      <div class="meta"><strong>reason：</strong>${esc(x.reason||'')}</div>
      ${dimPanel(x.unit_id, oi)}
    </article>`;
  }).join('') || '<div class="meta">无匹配</div>';

  filtered.forEach((x, idx)=>{
    const card = list.querySelectorAll('.qcard')[idx];
    if (!card) return;
    renderRich(card.querySelector('[data-r=stem]'), x.stem_raw||'');
    const bodies = card.querySelectorAll('.opt-body');
    (x.options_raw||[]).forEach((o,i)=>{ if (bodies[i]) renderRich(bodies[i], o.text_raw||''); });
    renderRich(card.querySelector('[data-r=ans]'), x.answer_raw||'');
  });
}

function renderStats(qs) {
  const counts={}; let anom=0;
  qs.forEach(q=>{
    counts[q.gate]=(counts[q.gate]||0)+1;
    if ((q.option_integrity||{}).level==='ANOMALY') anom++;
  });
  document.getElementById('q-stats').innerHTML =
    Object.entries(counts).map(([k,v])=>gateBadge(k)+' <strong>'+v+'</strong>').join(' · ')
    + ' · <span class="badge anom">选项异常 '+anom+'</span>';
}

function render() {
  const s = (D.subjects||{})[current]||{};
  const qs = s.questions||[];
  renderStats(qs);
  renderQuestions(qs);
  renderGate1();
}

// feedback export (download only — never write evidence area)
document.getElementById('export-feedback').addEventListener('click', ()=>{
  const out = {subject: current, dims: []};
  document.querySelectorAll('#question-list select[data-dim]').forEach(sel=>{
    if (sel.value) out.dims.push({uid: sel.getAttribute('data-uid'), dim: sel.getAttribute('data-dim'), value: sel.value});
  });
  const blob = new Blob([JSON.stringify(out, null, 2)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'owner-feedback-'+current+'.json';
  a.click();
});

const tabs = document.getElementById('subject-tabs');
SUBJECTS.forEach(s=>{
  const b=document.createElement('button');
  b.textContent=s;
  b.onclick=()=>{ current=s; [...tabs.children].forEach(x=>x.classList.toggle('active', x.textContent===s)); render(); };
  tabs.appendChild(b);
});
tabs.children[0].classList.add('active');
document.getElementById('diff-mode').addEventListener('change', renderGate1);
document.getElementById('diff-q').addEventListener('input', renderGate1);
document.getElementById('full-search').addEventListener('input', renderGate1);
document.getElementById('gate-filter').addEventListener('change', render);
document.getElementById('anomaly-filter').addEventListener('change', render);
document.getElementById('q-search').addEventListener('input', render);
document.getElementById('show-raw').addEventListener('change', render);
render();
"""

# data.js = frozen evidence (display only)
# Keep FROZEN_EVIDENCE/data.js as source of truth; page data.js is a copy for load
# Do not modify FROZEN_EVIDENCE/*
(OUT / "index.html").write_text(html, encoding="utf-8")
(OUT / "style.css").write_text(css, encoding="utf-8")
(OUT / "app.js").write_text(js, encoding="utf-8")

# ensure page data.js matches frozen (without writing frozen)
frozen_js = (OUT / "FROZEN_EVIDENCE" / "data.js").read_text(encoding="utf-8")
(OUT / "data.js").write_text(frozen_js, encoding="utf-8")

print("index", (OUT/"index.html").stat().st_size)
print("app.js", (OUT/"app.js").stat().st_size)
print("data.js sha", hashlib.sha256((OUT/"data.js").read_bytes()).hexdigest())
print("frozen data.js sha", hashlib.sha256((OUT/"FROZEN_EVIDENCE"/"data.js").read_bytes()).hexdigest())
print("match", hashlib.sha256((OUT/"data.js").read_bytes()).hexdigest()
       == hashlib.sha256((OUT/"FROZEN_EVIDENCE"/"data.js").read_bytes()).hexdigest())
