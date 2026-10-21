from pathlib import Path
import json, hashlib

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
v2 = json.loads((OUT / "viewer_data_raw_v2.json").read_text(encoding="utf-8"))

# page loads data_v2.js (already written). Rebuild app display for provenance.
html = (OUT / "index.html").read_text(encoding="utf-8")
# switch script src to data_v2.js
html = html.replace('src="data.js"', 'src="data_v2.js"')
html = html.replace("Owner Viewer · FROZEN", "Owner Viewer · v2 Gate Provenance")
(OUT / "index.html").write_text(html, encoding="utf-8")

js = r"""
const D = window.E2E_DATA || {};
const SUBJECTS = ["数学","物理","化学","英语","语文","政治","地理","历史","生物"];
let current = SUBJECTS[0];
const showRaw = () => document.getElementById('show-raw').checked;

function esc(s){return String(s==null?'':s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}

(function(){
  const fr = D.FROZEN_BASELINE || {};
  const lines = ['FROZEN_BASELINE (untouched):'];
  Object.entries(fr.sha256||{}).forEach(([k,v])=>lines.push('  '+k+'  '+String(v).slice(0,16)+'…'));
  const el = document.getElementById('freeze-shas');
  if (el) el.textContent = lines.join('\n');
  const bar = document.getElementById('policy-bar');
  if (bar) bar.innerHTML =
    '<strong>Gate 溯源：</strong>gate_original 仅在 Gate 真正执行时非空；' +
    'incomplete / 无 leaf 是<strong>结构状态</strong>，不是 Gate 决策；' +
    'gate_replay 为独立重放，<strong>不冒充原始决策</strong>；reason_display 仅展示。';
})();

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

function splitByQuestion(text) {
  const lines = String(text||'').split('\n');
  const blocks = []; let cur = { qn:null, lines:[] };
  lines.forEach((ln)=>{
    const m = ln.match(/^\s*(\d{1,3})\s*[.．、\\]/);
    if (m) { if (cur.lines.length) blocks.push(cur); cur = { qn:m[1], lines:[ln] }; }
    else cur.lines.push(ln);
  });
  if (cur.lines.length) blocks.push(cur);
  return blocks;
}
function norm(t){return String(t||'').replace(/．/g,'.').replace(/，/g,',').replace(/\s+/g,' ').trim();}

function renderGate1() {
  const s = (D.subjects||{})[current]||{};
  const pdfEl = document.getElementById('pdf-text');
  const mdEl = document.getElementById('md-text');
  if (pdfEl) pdfEl.textContent = s.pdf_text || '';
  if (mdEl) mdEl.textContent = s.md_text || '';
  const mode = (document.getElementById('diff-mode')||{}).value || 'anchor';
  const focus = ((document.getElementById('diff-q')||{}).value||'').trim();
  const kw = ((document.getElementById('full-search')||{}).value||'').trim().toLowerCase();
  const anchor = document.getElementById('anchor-diff');
  const lineD = document.getElementById('line-diff');
  const searchH = document.getElementById('search-hits');
  if (!anchor) return;
  anchor.style.display = mode==='anchor'?'':'none';
  if (lineD) lineD.style.display = mode==='line'?'block':'none';
  if (searchH) searchH.style.display = mode==='search'?'block':'none';

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
  } else if (mode==='line' && lineD) {
    const a=String(s.pdf_text||'').split('\n'), b=String(s.md_text||'').split('\n');
    const aSet=new Set(a.map(norm).filter(Boolean)), bSet=new Set(b.map(norm).filter(Boolean));
    const onlyP=a.map((x,i)=>({i,x})).filter(r=>r.x&&!bSet.has(norm(r.x))).slice(0,60);
    const onlyM=b.map((x,i)=>({i,x})).filter(r=>r.x&&!aSet.has(norm(r.x))).slice(0,60);
    lineD.innerHTML=[...onlyP.map(r=>`<div class="line-diff-row"><span style="color:var(--fail)">仅PDF</span><span>L${r.i+1}</span><span>${esc(r.x)}</span></div>`),
      ...onlyM.map(r=>`<div class="line-diff-row"><span style="color:var(--ok)">仅MD</span><span>L${r.i+1}</span><span>${esc(r.x)}</span></div>`)]
      .join('')||'<div class="meta">全文无行差</div>';
  } else if (searchH) {
    if (!kw) { searchH.innerHTML='<div class="meta">输入关键字</div>'; return; }
    const hits=[];
    String(s.pdf_text||'').split('\n').forEach((ln,i)=>{ if(ln.toLowerCase().includes(kw)) hits.push(['PDF',i+1,ln]); });
    String(s.md_text||'').split('\n').forEach((ln,i)=>{ if(ln.toLowerCase().includes(kw)) hits.push(['MD',i+1,ln]); });
    searchH.innerHTML = hits.slice(0,80).map(h=>
      `<div class="line-diff-row"><span>${h[0]}</span><span>L${h[1]}</span><span>${esc(h[2])}</span></div>`
    ).join('')||'<div class="meta">无命中</div>';
  }
}

function gateBadge(q){
  const g = q.gate_display;
  if (g==='auto_approve') return '<span class="badge ok">auto</span>';
  if (g==='pending_review') return '<span class="badge warn">pending</span>';
  if (g==='rejected') return '<span class="badge fail">rejected</span>';
  // NO decision — never fabricate
  return '<span class="badge pending">无 Gate 决策</span>';
}

function provenanceLine(q){
  const rm = q.replay_match;
  const rmTxt = rm===true ? 'replay=一致' : (rm===false ? 'replay=不一致' : 'replay=N/A');
  return `<div class="meta">
    <strong>溯源</strong> · leaf_present=${q.leaf_present} · ir=${esc(q.ir_status||'')}
    · gate_original=${esc(String(q.gate_original))} (${esc(q.gate_original_source||'')})
    · gate_replay=${esc(String(q.gate_replay))} (${esc(q.gate_replay_source||'')})
    · ${rmTxt}
  </div>`;
}

function dimPanel(unitId, oi) {
  const anom = oi && oi.level === 'ANOMALY';
  return `
  <div class="dim-grid">
    <div class="dim"><strong>题干</strong>
      <select data-dim="stem" data-uid="${esc(unitId)}">
        <option value="">—</option><option>正确</option><option>错误</option><option>跳过</option>
      </select></div>
    <div class="dim"><strong>选项</strong>
      <div class="meta">${anom?'<span class="badge anom">结构异常</span> 只标不定论':'结构完整'}</div>
      <select data-dim="options" data-uid="${esc(unitId)}">
        <option value="">—</option>
        <option>结构正确</option><option>空壳</option><option>吞并</option><option>其他异常</option>
      </select></div>
    <div class="dim"><strong>答案</strong>
      <div class="meta">${anom?'受选项结构影响·暂不可判':'可独立检查'}</div>
      <select data-dim="answer" data-uid="${esc(unitId)}" ${anom?'disabled':''}>
        <option value="">—</option><option>正确</option><option>错误</option>
        <option value="unreliable">暂不可判</option>
      </select></div>
    <div class="dim"><strong>LaTeX</strong>
      <select data-dim="latex" data-uid="${esc(unitId)}">
        <option value="">—</option><option>正常</option><option>失败</option>
      </select></div>
    <div class="dim"><strong>整体</strong>
      <select data-dim="overall" data-uid="${esc(unitId)}">
        <option value="">—</option>
        <option value="pass" ${anom?'disabled':''}>正确</option>
        <option>错误</option><option value="defer">暂缓</option>
      </select></div>
    <div class="dim"><strong>缺陷类型</strong>
      <select data-dim="issue" data-uid="${esc(unitId)}">
        <option value="">…</option>
        <option>题干不完整</option><option>选项不完整</option><option>选项串题</option>
        <option>材料不完整</option><option>图片缺失</option><option>LaTeX错误</option>
        <option>答案错误</option><option>边界错误</option><option>其他</option>
      </select></div>
  </div>`;
}

function renderQuestions(qs) {
  const list = document.getElementById('question-list');
  const gf = document.getElementById('gate-filter').value;
  const af = document.getElementById('anomaly-filter').value;
  const q = document.getElementById('q-search').value.trim().toLowerCase();
  const filtered = qs.filter(x=>{
    if (gf!=='all') {
      const g = x.gate_display;
      if (gf==='no_decision' && g!==null) return false;
      if (gf!=='no_decision' && g!==gf) return false;
    }
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
    return `
    <article class="qcard ${anom?'anomaly':''}">
      <div class="top">
        <div class="uid">${esc(x.unit_id)} ${gateBadge(x)}
          ${anom?'<span class="badge anom">选项结构异常</span>':''}</div>
        <div class="meta">leaf_present=${x.leaf_present} · ir=${esc(x.ir_status||'')} · ${esc(x.qtype||'')}</div>
      </div>
      ${provenanceLine(x)}
      <div class="qstem" data-r="stem"></div>
      <div class="opts">${opts}</div>
      <div class="answer"><strong>答案：</strong>${esc(x.answer_letter||'—')}
        <div data-r="ans"></div></div>
      <div class="meta"><strong>reason_display：</strong>${esc(x.reason_display||'')}</div>
      ${x.gate_reasons_original && x.gate_reasons_original.length
        ? `<div class="raw-line">gate_reasons_original: ${esc(x.gate_reasons_original.join(' | '))}</div>` : ''}
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
  const counts={}; let anom=0, noDec=0;
  qs.forEach(q=>{
    const g = q.gate_display==null ? '无Gate决策' : q.gate_display;
    counts[g]=(counts[g]||0)+1;
    if ((q.option_integrity||{}).level==='ANOMALY') anom++;
    if (q.gate_display==null) noDec++;
  });
  const el = document.getElementById('q-stats');
  if (el) el.innerHTML =
    Object.entries(counts).map(([k,v])=>`<span class="badge ${k==='无Gate决策'?'pending':(k==='auto_approve'?'ok':(k==='rejected'?'fail':'warn'))}">${esc(k)}</span> <strong>${v}</strong>`).join(' · ')
    + ` · <span class="badge anom">选项异常 ${anom}</span>`
    + ` · <span class="badge pending">无决策 ${noDec}</span>`;
}

function render() {
  const s = (D.subjects||{})[current]||{};
  const qs = s.questions||[];
  renderStats(qs);
  renderQuestions(qs);
  renderGate1();
}

const btn = document.getElementById('export-feedback');
if (btn) btn.addEventListener('click', ()=>{
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
if (tabs.children[0]) tabs.children[0].classList.add('active');
['diff-mode','diff-q','full-search','gate-filter','anomaly-filter','q-search','show-raw'].forEach(id=>{
  const el = document.getElementById(id);
  if (el) el.addEventListener('change', render);
  if (el && el.tagName==='INPUT') el.addEventListener('input', render);
});
render();
"""
(OUT / "app.js").write_text(js, encoding="utf-8")

# report
report = """# Viewer Gate Decision Provenance — COMPLETE

## 冻结保护
- FROZEN_EVIDENCE/ 未写入
- 05_V3_OUTPUT/*.v3.json 未修改
- 05_V3_OUTPUT/*.pdf.txt 已设只读 + SHA 记录
- protected files changed: **NONE**（V2_SHA256.json）

## 字段语义（v2）
| 字段 | 含义 |
|------|------|
| leaf_present | 结构事实：是否存在 compiled leaf |
| ir_status | 结构：ready / incomplete |
| gate_original | **仅当 Gate 真正执行**时非空；否则 null |
| gate_original_source | absent_no_leaf / absent_ir_incomplete_skipped / evaluate_replay_equivalent |
| gate_replay | 独立重放 evaluate()，单独记录 |
| replay_match | true / false / null |
| gate_display | 展示用；**null = 无决策**，绝不显示 rejected/approved |
| reason_display | 展示文案；不覆盖 gate_reasons_original |

**incomplete 不是合法 Gate 决策** — Gate service 对 semantic_status≠ready 的 unit 是 skip（不产 candidate）。

## 六情形验证
| 情形 | n | 结果 |
|------|---|------|
| C1 leaf + original decision | 227 | PASS |
| C2 no leaf + original | **0** | PASS（无伪造） |
| C3 no leaf + no original | 57 | PASS |
| C4 replay == original | 227 | PASS |
| C5 replay != original | 0 | PASS |
| C6 replay error/missing | 0 | PASS |

**RAW 字段（stem/options/answer/labels）相对 FROZEN 差异 = 0**
**伪造决策 = NONE**
**VERDICT: COMPLETE**

## 版本化产物
- `viewer_data_raw_v2.json` / `data_v2.js`（新版本，不覆盖冻结基线）
- `V2_SHA256.json` 哈希清单
- `export_v2_gate_provenance.py` / `verify_v2_provenance.py`

## 未做（按禁令）
- 未改 Resolver / Producer / Gate Policy / Schema / P1.4-B
- 未修补/切分题干选项答案
- 未改冻结证据
- 未把重放冒充原始执行
- 未宣布九科 E2E / 正式产品链通过
"""
(OUT / "V2_PROVENANCE_REPORT.md").write_text(report, encoding="utf-8")
print("app.js", (OUT/"app.js").stat().st_size)
print("index uses", "data_v2.js" in (OUT/"index.html").read_text(encoding="utf-8"))
print("wrote V2_PROVENANCE_REPORT.md")
