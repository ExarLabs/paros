# Kit: a view on your vault (P02)

The view is the least important layer of PAROS: the markdown is the system. Most people need **no app at all** at the start; the notes editor (Obsidian, for example) is the interface. When you want more, choose one of three levels. You can move between them at any time, because none of them holds knowledge (P01).

| Level | What you get | Needs | Choose it when |
|---|---|---|---|
| **0. No app** | Your notes editor | nothing | You are starting. This is enough for weeks. |
| **1. Minimal view** ([`node-minimal/`](node-minimal/README.md)) | A local web page: ranked search, note preview, open tasks you can tick off (written back into markdown), live refresh when files change | Node.js 18+, nothing else: no `npm install`, no build step | You want a dashboard-like overview, or to share the screen in a workshop. **The recommended first view.** |
| **2. React app** ([`react/INSTRUCTIONS.md`](react/INSTRUCTIONS.md)) | A full interactive application (boards, graphs, timelines, forms) on top of the same API | Node.js, npm, a build tool (Vite) | You need rich interaction and you are comfortable maintaining a frontend project. |

## The rule that keeps both paths open

Level 1 and level 2 use **the same API** (the minimal server's `/api/*` endpoints). A React app is a different front on the same back. So:
- start with level 1;
- if you outgrow it, build level 2 against the same server;
- if the React app ever breaks or becomes a burden, level 1 still works.

## Where it lives

- **Outside the vault** if it has dependencies (`node_modules` must never sync with your notes).
- The minimal view has no dependencies, so it can live anywhere; a good place is next to this repository or in a tools folder outside the vault.

## Ask your agent

> Set up the PAROS minimal view for my vault (kits/view/node-minimal). Run it, open it, and show me my open tasks.

> I want a React view on my vault. Follow kits/view/react/INSTRUCTIONS.md and build it against the minimal server's API.
