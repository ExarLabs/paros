// PAROS starter dashboard. Plain JavaScript, no build step, no dependencies.
// Talks only to the server's /api/* endpoints (the same API as kits/view/node-minimal).
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const getJSON = async (url) => { const r = await fetch(url); if (!r.ok) throw new Error((await r.json()).error || r.status); return r.json(); };
const DAY = 86_400_000;
const STALE_DAYS = 90;
let notes = [];
let current = null; // { kind: "note" | "agent", id }

// Used when an agent definition is not (yet) present next to starter/.
const FALLBACK = {
  librarian: "Keeps the vault findable: ranked search, content descriptions, links, and the archive. Reads first, changes only with a yes.",
  maestro: "Turns corrections into lessons: reviews learning packets with evidence and routes work to the right viewpoint.",
  alfred: "The owner's chief of staff: sorts the task inbox, prepares the daily briefing, drafts but never sends.",
};

// ---------- markdown (small on purpose) ----------
function inline(s) {
  return esc(s)
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/(^|\W)\*(.+?)\*(?=\W|$)/g, "$1<i>$2</i>")
    .replace(/`(.+?)`/g, "<code>$1</code>")
    .replace(/\[\[(.+?)\]\]/g, (_m, t) => `<a href="#" data-title="${t}">${t}</a>`)
    .replace(/\[(.+?)\]\((https?:[^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
}

function md(src) {
  const out = [];
  let code = false, table = null;
  const flush = () => { if (table) { out.push(`<table>${table.join("")}</table>`); table = null; } };
  for (const line of src.split(/\r?\n/)) {
    if (line.startsWith("```")) { flush(); out.push(code ? "</pre>" : "<pre>"); code = !code; continue; }
    if (code) { out.push(esc(line)); continue; }
    if (/^\s*\|.*\|\s*$/.test(line)) {
      if (/^\s*\|[\s:|-]+\|\s*$/.test(line)) continue; // separator row
      const cells = line.trim().slice(1, -1).split("|").map((c) => inline(c.trim()));
      const tag = table ? "td" : "th";
      table = table || [];
      table.push(`<tr>${cells.map((c) => `<${tag}>${c}</${tag}>`).join("")}</tr>`);
      continue;
    }
    flush();
    const h = line.match(/^(#{1,6}) (.*)$/);
    if (h) { const n = Math.min(h[1].length + 1, 3); out.push(`<h${n}>${inline(h[2])}</h${n}>`); continue; }
    const task = line.match(/^\s*[-*] \[( |x|X)\] (.*)$/);
    if (task) { out.push(`<div class="li">${task[1] === " " ? "&#9744;" : "&#9745;"} ${inline(task[2])}</div>`); continue; }
    const li = line.match(/^\s*(?:[-*]|\d+\.) (.*)$/);
    if (li) { out.push(`<div class="li">&#8226; ${inline(li[1])}</div>`); continue; }
    const q = line.match(/^> ?(.*)$/);
    if (q) { out.push(`<blockquote>${inline(q[1])}</blockquote>`); continue; }
    if (line.trim()) out.push(`<p>${inline(line)}</p>`);
  }
  flush();
  return out.join("\n");
}

// ---------- drawer ----------
function show(title, meta, path, body) {
  $("#note").innerHTML = `<h1>${esc(title)}</h1>` +
    `<p class="meta">${meta ? esc(meta) + "<br>" : ""}<small>${esc(path)}</small></p>` + md(body || "");
  $("#drawer").hidden = false;
  $("#drawer").scrollTop = 0;
}

async function openNote(path) {
  try {
    const n = await getJSON("/api/note?path=" + encodeURIComponent(path));
    const fm = n.frontmatter || {};
    current = { kind: "note", id: path };
    show(fm.title || path, fm.description, path, n.body);
  } catch (e) { alert(e.message); }
}

async function openAgent(name) {
  try {
    const a = await getJSON("/api/agent?name=" + encodeURIComponent(name));
    current = { kind: "agent", id: name };
    show(a.frontmatter.title || name, a.frontmatter.description, a.path, a.body);
  } catch (e) { alert(e.message); }
}

function closeDrawer() { $("#drawer").hidden = true; current = null; }

// ---------- agents ----------
async function loadAgents() {
  let rows = [];
  try { rows = await getJSON("/api/agents"); } catch { $("#agents").innerHTML = '<div class="empty">The server is not reachable. Start it: node dashboard/server.mjs</div>'; return; }
  $("#agents").innerHTML = rows.map((a) => `
    <div class="agent">
      <div class="nm">${esc(a.title)}</div>
      <div class="role">${esc(a.role)}${a.version ? " · v" + esc(a.version) : ""}</div>
      <div class="desc">${esc(a.description || FALLBACK[a.name] || "")}</div>
      <div class="path">${esc(a.link)}</div>
      <div class="row">
        ${a.found
          ? `<button data-agent="${esc(a.name)}">Read definition</button><span class="state ok">found</span>`
          : `<a class="btn ghost" href="${esc(a.url)}" target="_blank" rel="noopener">On GitHub</a><span class="state no">not found locally</span>`}
      </div>
    </div>`).join("");
}

// ---------- search ----------
async function search() {
  const q = $("#q").value.trim();
  if (q.length < 2) { $("#results").innerHTML = ""; return; }
  const rows = await getJSON("/api/search?q=" + encodeURIComponent(q));
  $("#results").innerHTML = rows.length ? rows.slice(0, 12).map((r) => `
    <div class="res" tabindex="0" data-path="${esc(r.path)}">
      <span class="score">${r.score}</span>
      <div class="rt">${esc(r.title)}</div>
      <div class="rp">${esc(r.path)}</div>
      <div class="rx">${esc(r.description || "No description: this note is hard to find. Add one (P01).")}</div>
    </div>`).join("")
    : '<div class="empty">Nothing found. Try fewer, more characteristic words.</div>';
}

// ---------- tasks ----------
async function loadTasks() {
  const [rows, todo] = await Promise.all([getJSON("/api/tasks"), getJSON("/api/note?path=TODO.md").catch(() => null)]);
  // Give each task the heading above it (Inbox, Now, Waiting), found by matching its raw line in the note body.
  if (todo) {
    const lines = (todo.body || "").split(/\r?\n/);
    const used = new Set();
    for (const t of rows) {
      const i = lines.findIndex((l, k) => l === t.raw && !used.has(k));
      if (i < 0) continue;
      used.add(i);
      for (let k = i; k >= 0; k--) { const h = lines[k].match(/^#{2,6} (.*)$/); if (h) { t.sec = h[1]; break; } }
    }
  }
  const open = rows.filter((t) => !t.done);
  $("#sTasks").textContent = open.length;
  $("#tasks").innerHTML = open.length ? open.map((t, i) => `
    <li><input type="checkbox" id="t${i}" data-i="${i}"><label for="t${i}">${t.sec ? `<span class="sec">${esc(t.sec)}</span>` : ""}${esc(t.text)}</label></li>`).join("")
    : '<li class="empty">No open tasks. Everything in TODO.md is ticked.</li>';
  $("#tasks").querySelectorAll("input").forEach((box) => box.addEventListener("change", async () => {
    const t = open[box.dataset.i];
    const r = await fetch("/api/toggle", { method: "POST", body: JSON.stringify({ path: t.path, line: t.line, text: t.raw }) });
    if (!r.ok) alert((await r.json()).error);
    loadTasks();
  }));
}

// ---------- freshness ----------
function noteDate(n) {
  const d = n.date && /^\d{4}-\d{2}-\d{2}/.test(n.date) ? Date.parse(n.date.slice(0, 10)) : NaN;
  return Number.isNaN(d) ? n.mtime : d;
}
const ago = (t) => { const d = Math.floor((Date.now() - t) / DAY); return d <= 0 ? "today" : d === 1 ? "1 day" : d + " days"; };

async function loadNotes() {
  notes = await getJSON("/api/notes");
  const inVault = notes.filter((n) => !n.path.startsWith("dashboard/"));
  $("#sNotes").textContent = inVault.length;

  const areas = {};
  for (const n of inVault) {
    const m = n.path.match(/^(Areas\/[^/]+|Archive|PAROS)\//);
    const key = m ? m[1].replace(/^Areas\//, "") : "Vault root";
    (areas[key] ||= []).push(n);
  }
  const stale = inVault.filter((n) => n.status === "active" && Date.now() - noteDate(n) > STALE_DAYS * DAY)
    .sort((a, b) => noteDate(a) - noteDate(b));
  $("#sStale").textContent = stale.length;

  $("#areas").innerHTML = Object.keys(areas).sort().map((k) => {
    const list = areas[k];
    const newest = Math.max(...list.map(noteDate));
    const oldActive = list.filter((n) => n.status === "active" && Date.now() - noteDate(n) > STALE_DAYS * DAY).length;
    return `<div class="area ${oldActive ? "warn" : ""}">
      <div class="an">${esc(k)}</div>
      <div class="am">${list.length} note${list.length === 1 ? "" : "s"} · newest ${ago(newest)}${oldActive ? ` · ${oldActive} stale` : ""}</div>
    </div>`;
  }).join("");

  const recent = [...inVault].sort((a, b) => b.mtime - a.mtime).slice(0, 6);
  $("#recent").innerHTML = recent.map((n) =>
    `<li data-path="${esc(n.path)}"><span>${esc(n.title)}</span><span class="age">${ago(n.mtime)}</span></li>`).join("");
  $("#stale").innerHTML = stale.length ? stale.map((n) =>
    `<li data-path="${esc(n.path)}"><span>${esc(n.title)}</span><span class="age old">${ago(noteDate(n))}</span></li>`).join("")
    : '<li class="empty">Nothing stale. Every active note was touched in the last 90 days.</li>';
  $("#fresh").textContent = "read " + new Date().toLocaleTimeString();
}

// ---------- wiring ----------
let timer;
$("#q").addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(search, 180); });
document.addEventListener("click", (e) => {
  const agent = e.target.closest("[data-agent]");
  if (agent) return openAgent(agent.dataset.agent);
  const link = e.target.closest("a[data-title]");
  if (link) {
    e.preventDefault();
    const hit = notes.find((n) => n.title.toLowerCase() === link.dataset.title.toLowerCase());
    return hit ? openNote(hit.path) : alert("No note titled " + link.dataset.title);
  }
  const row = e.target.closest("[data-path]");
  if (row && !e.target.closest("#drawer")) openNote(row.dataset.path);
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeDrawer();
  const row = e.target.closest && e.target.closest(".res[data-path]");
  if (row && e.key === "Enter") openNote(row.dataset.path);
});
$("#close").addEventListener("click", closeDrawer);

function refresh() {
  loadTasks(); loadNotes();
  if (current && current.kind === "note") openNote(current.id);
}
new EventSource("/api/events").onmessage = (e) => { if (e.data !== "hello") refresh(); };
loadAgents(); loadTasks(); loadNotes();
