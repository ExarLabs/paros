# React view: step-by-step instructions for an agent

These are instructions, not a template: the agent builds the app for the person's vault, so it fits their areas and habits. The back end is the **minimal server** (`../node-minimal/server.mjs`); the React app is only a front on its API. If the React app ever becomes a burden, the minimal view keeps working.

## 0. Decide first

Ask the person:
- What do you want to **see** that the minimal view does not show? (a board by status, a timeline, a graph of links, a page per area, forms for quick capture)
- Are you comfortable with a project that needs `npm install` and occasional updates?

If the answers are vague, do not build it yet: extend the minimal view instead.

## 1. Where

Create the project **outside the vault**, for example next to it: `<parent-of-vault>/paros-view/`. `node_modules` must never sync with the notes.

## 2. Scaffold

```bash
npm create vite@latest paros-view -- --template react-ts
cd paros-view
npm install
```

In `vite.config.ts`, proxy the API to the minimal server so the app and the server share one origin during development:

```ts
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/api": "http://localhost:4747" } },
});
```

Run both: `node ../path/to/node-minimal/server.mjs <vault>` and `npm run dev`.

## 3. Build in this order

1. **A typed API client** (`src/api.ts`) for the six endpoints in `node-minimal/README.md`. Nothing else talks to the server.
2. **Search and note preview** first, so the app is immediately useful.
3. **Tasks with write-back** through `/api/toggle` only, sending the `raw` line you read (the server refuses stale writes).
4. **Live refresh** from `/api/events` (an `EventSource` in one hook).
5. Only then the person's own views (board, timeline, area pages). Each new view that needs data the API does not give: **add an endpoint to the server first**, reading markdown; never store data in the app.

## 4. Rules

- The app holds **no knowledge** (P01): no local database, no app-only fields. If you need a new field, it goes into the notes' frontmatter.
- **Writes go only into markdown,** through the server, and each kind of write is explicit and small (like ticking a task).
- Keep it **thin**: if a feature needs a lot of code, ask whether it belongs in a script or in an external tool instead (P08).
- Listen on localhost only.

## 5. Production build (optional)

`npm run build` produces static files in `dist/`. Serve them from the minimal server, so one process serves both: `node server.mjs <vault> --public <path-to>/paros-view/dist`.

## 6. When to go back

If updates break the build, or the app is not used for weeks, return to the minimal view. Nothing is lost.
