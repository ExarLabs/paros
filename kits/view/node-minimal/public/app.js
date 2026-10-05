// PAROS minimal view, plain JavaScript, no build step.
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
let current = null;

function md(src) {
  // A deliberately small markdown renderer: headings, lists, tasks, code, bold, italics, links.
  const out = [];
  let code = false;
  src.split(/\r?\n/).forEach((line) => {
    if (line.startsWith("```")) { out.push(code ? "</pre>" : "<pre>"); code = !code; return; }
    if (code) { out.push(esc(line)); return; }
    let h = esc(line)
      .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
      .replace(/(^|\W)\*(.+?)\*(?=\W|$)/g, "$1<i>$2</i>")
      .replace(/`(.+?)`/g, "<code>$1</code>")
      .replace(/\[(.+?)\]\((https?:[^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    const hd = h.match(/^(#{1,6}) (.*)$/);
    if (hd) return out.push(`<h${hd[1].length}>${hd[2]}</h${hd[1].length}>`);
    const task = h.match(/^\s*[-*] \[( |x|X)\] (.*)$/);
    if (task) return out.push(`<div>${task[1] === " " ? "☐" : "☑"} ${task[2]}</div>`);
    const li = h.match(/^\s*[-*] (.*)$/);
    if (li) return out.push(`<div>• ${li[1]}</div>`);
    out.push(h ? `<p>${h}</p>` : "");
  });
  return out.join("\n");
}

async function open(path) {
  const n = await (await fetch("/api/note?path=" + encodeURIComponent(path))).json();
  current = path;
  const fm = n.frontmatter || {};
  $("#note").innerHTML = `<h1>${esc(fm.title || path)}</h1>` +
    (fm.description ? `<p class="meta">${esc(fm.description)}<br><small>${esc(path)}</small></p>` : `<p class="meta"><small>${esc(path)}</small></p>`) +
    md(n.body || "");
}

async function search() {
  const q = $("#q").value.trim();
  if (q.length < 2) return;
  const rows = await (await fetch("/api/search?q=" + encodeURIComponent(q))).json();
  $("#results").innerHTML = rows.length ? rows.map((r) =>
    `<li data-path="${esc(r.path)}"><b>${esc(r.title)}</b><small>${esc(r.description || r.path)}</small></li>`).join("")
    : '<li class="muted">Nothing found. Try fewer, more characteristic words.</li>';
}

async function loadTasks() {
  const rows = await (await fetch("/api/tasks")).json();
  const open = rows.filter((t) => !t.done).slice(0, 30);
  $("#tasks").innerHTML = open.length ? open.map((t, i) =>
    `<li><label><input type="checkbox" data-i="${i}"> ${esc(t.text)}</label></li>`).join("")
    : '<li class="muted">No open tasks found in the task files.</li>';
  $("#tasks").querySelectorAll("input").forEach((box) => box.addEventListener("change", async () => {
    const t = open[box.dataset.i];
    const r = await fetch("/api/toggle", { method: "POST", body: JSON.stringify({ path: t.path, line: t.line, text: t.raw }) });
    if (!r.ok) alert((await r.json()).error);
    loadTasks();
  }));
  $("#fresh").textContent = "read " + new Date().toLocaleTimeString();
}

let timer;
$("#q").addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(search, 200); });
$("#results").addEventListener("click", (e) => { const li = e.target.closest("li[data-path]"); if (li) open(li.dataset.path); });
new EventSource("/api/events").onmessage = () => { loadTasks(); if (current) open(current); };
loadTasks();
