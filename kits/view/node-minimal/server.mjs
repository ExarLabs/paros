#!/usr/bin/env node
// PAROS minimal view: a zero-dependency local server for a markdown vault (Node.js 18+).
//
//   node server.mjs <vault-path> [--port 4747] [--tasks "TODO.md,00_TODO.md"] [--public <folder>]
//
// What it does (principle P02: the view reads markdown and writes back only into markdown):
//   GET  /                     the single-page view (public/)
//   GET  /api/notes            every markdown file with its frontmatter (title, description, status)
//   GET  /api/search?q=...     ranked search: title x10, description x5, body x1
//   GET  /api/note?path=...    one note: frontmatter and body
//   GET  /api/tasks            open and done tasks from the task files
//   POST /api/toggle           {path, line, text}: flips "- [ ]" and "- [x]" on that line, if the text still matches
//   GET  /api/events           server-sent events: "changed" whenever the vault changes (live view)
//
// Safety: listens on 127.0.0.1 only; reads and writes only .md files inside the vault; no other writes.
// It holds no knowledge of its own: delete it any time, nothing is lost (P01).

import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const args = process.argv.slice(2);
const VAULT = path.resolve(args.find((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--"))) || ".");
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : def; };
const PORT = Number(opt("--port", 4747));
const TASK_FILES = opt("--tasks", "TODO.md,00_TODO.md,Tasks.md").split(",").map((s) => s.trim());
const PUBLIC = path.resolve(opt("--public", path.join(path.dirname(fileURLToPath(import.meta.url)), "public")));
const SKIP = new Set([".git", ".obsidian", ".trash", "node_modules", ".smart-env", "venv", ".venv"]);
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8" };

let cache = null;
let cacheAt = 0;

function walk(dir, out = []) {
  let entries = [];
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (SKIP.has(e.name) || e.isSymbolicLink()) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.toLowerCase().endsWith(".md")) out.push(p);
  }
  return out;
}

function parse(text) {
  const m = text.match(/^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n/);
  const fm = {};
  if (m) {
    for (const line of m[1].split(/\r?\n/)) {
      const k = line.match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
      if (k) fm[k[1].toLowerCase()] = k[2].trim().replace(/^["']|["']$/g, "");
    }
  }
  return { fm, body: m ? text.slice(m[0].length) : text };
}

function notes() {
  if (cache && Date.now() - cacheAt < 30_000) return cache;
  cache = walk(VAULT).map((p) => {
    let text = "";
    try { text = fs.readFileSync(p, "utf8"); } catch {}
    const { fm, body } = parse(text);
    const rel = path.relative(VAULT, p).split(path.sep).join("/");
    return { path: rel, title: fm.title || path.basename(p, ".md"), description: fm.description || "",
             status: fm.status || "", mtime: fs.statSync(p).mtimeMs, body: body.toLowerCase() };
  });
  cacheAt = Date.now();
  return cache;
}

function safePath(rel) {
  const p = path.resolve(VAULT, rel || "");
  if (!p.startsWith(VAULT + path.sep) || !p.toLowerCase().endsWith(".md")) throw new Error("path outside vault or not markdown");
  return p;
}

function search(q) {
  const terms = q.toLowerCase().split(/\s+/).filter((t) => t.length > 1);
  if (!terms.length) return [];
  return notes().map((n) => {
    let score = 0;
    for (const t of terms) {
      if (n.title.toLowerCase().includes(t)) score += 10;
      if (n.description.toLowerCase().includes(t)) score += 5;
      if (n.body.includes(t)) score += 1;
    }
    return { ...n, score };
  }).filter((n) => n.score > 0).sort((a, b) => b.score - a.score || b.mtime - a.mtime).slice(0, 50)
    .map(({ body, ...n }) => n);
}

function tasks() {
  const out = [];
  for (const name of TASK_FILES) {
    const p = path.join(VAULT, name);
    if (!fs.existsSync(p)) continue;
    fs.readFileSync(p, "utf8").split(/\r?\n/).forEach((line, i) => {
      const m = line.match(/^\s*[-*] \[( |x|X)\] (.*)$/);
      if (m) out.push({ path: name, line: i, done: m[1] !== " ", text: m[2], raw: line });
    });
  }
  return out;
}

function toggle({ path: rel, line, text }) {
  const p = safePath(rel);
  const lines = fs.readFileSync(p, "utf8").split(/\r?\n/);
  const cur = lines[line];
  if (cur === undefined || cur !== text) throw new Error("the line changed since it was read; reload");
  if (/\[ \]/.test(cur)) lines[line] = cur.replace("[ ]", "[x]");
  else if (/\[[xX]\]/.test(cur)) lines[line] = cur.replace(/\[[xX]\]/, "[ ]");
  else throw new Error("not a task line");
  fs.writeFileSync(p, lines.join("\n"), "utf8");
  cache = null;
  return { ok: true, line: lines[line] };
}

const clients = new Set();
try {
  fs.watch(VAULT, { recursive: true }, (_e, file) => {
    if (!file || !String(file).toLowerCase().endsWith(".md")) return;
    cache = null;
    for (const res of clients) res.write(`data: changed ${String(file).split(path.sep).join("/")}\n\n`);
  });
} catch { /* recursive watch is not available everywhere; the view still works, without live refresh */ }

function send(res, code, body, type = "application/json; charset=utf-8") {
  res.writeHead(code, { "Content-Type": type, "Cache-Control": "no-store" });
  res.end(typeof body === "string" ? body : JSON.stringify(body));
}

http.createServer((req, res) => {
  const url = new URL(req.url, "http://localhost");
  try {
    if (url.pathname === "/api/notes") return send(res, 200, notes().map(({ body, ...n }) => n));
    if (url.pathname === "/api/search") return send(res, 200, search(url.searchParams.get("q") || ""));
    if (url.pathname === "/api/note") {
      const p = safePath(url.searchParams.get("path"));
      const { fm, body } = parse(fs.readFileSync(p, "utf8"));
      return send(res, 200, { path: url.searchParams.get("path"), frontmatter: fm, body });
    }
    if (url.pathname === "/api/tasks") return send(res, 200, tasks());
    if (url.pathname === "/api/toggle" && req.method === "POST") {
      let data = "";
      req.on("data", (c) => (data += c));
      req.on("end", () => { try { send(res, 200, toggle(JSON.parse(data))); } catch (e) { send(res, 409, { error: e.message }); } });
      return;
    }
    if (url.pathname === "/api/events") {
      res.writeHead(200, { "Content-Type": "text/event-stream", "Cache-Control": "no-store", Connection: "keep-alive" });
      res.write("data: hello\n\n");
      clients.add(res);
      req.on("close", () => clients.delete(res));
      return;
    }
    const file = path.join(PUBLIC, url.pathname === "/" ? "index.html" : path.normalize(url.pathname));
    if (!file.startsWith(PUBLIC) || !fs.existsSync(file)) return send(res, 404, "not found", "text/plain");
    return send(res, 200, fs.readFileSync(file, "utf8"), TYPES[path.extname(file)] || "text/plain");
  } catch (e) {
    return send(res, 400, { error: e.message });
  }
}).listen(PORT, "127.0.0.1", () => {
  console.log(`PAROS view: http://localhost:${PORT}  (vault: ${VAULT})`);
});
