#!/usr/bin/env python3
"""gapi.py: one Google Workspace CLI for every agent (PAROS kit: google-workspace).

One OAuth token per account, one command surface for Sheets, Forms, Drive and
Calendar. Agents call it through Bash, so access lives in the token, not in the
agent's tool list. Every write is a DRY RUN unless --apply is given.

Credentials (never inside the vault, never printed):

    $GAPI_HOME                      overrides everything: one folder holding
                                    client_secret.json and token.json
    $PAROS_SECRETS_DIR/google/      default root (PAROS_SECRETS_DIR defaults to
                                    ~/.paros/secrets)
        client_secret.json          the desktop OAuth client, shared by all accounts
        accounts.json               optional: account names and expected emails
        <account>/token.json        one token per account, created by `auth`

Account selection: --account NAME anywhere on the command line, else
$GAPI_ACCOUNT, else "default" in accounts.json, else the name "default".

Scopes: the full set below unless $GAPI_SCOPES narrows it (comma separated
short names: sheets, forms, forms-responses, drive, drive-readonly, calendar,
calendar-readonly). A token keeps the scopes it was granted; a command that
needs a missing scope tells you to run `auth` again.

Run `python gapi.py --help` or `python gapi.py <group> --help` for commands.
Requirements: pip install google-api-python-client google-auth-oauthlib
(python-docx only for `drive export` of .docx files).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, time, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

# --- configuration ------------------------------------------------------------

SCOPE_MAP = {
    "sheets": "https://www.googleapis.com/auth/spreadsheets",
    "forms": "https://www.googleapis.com/auth/forms.body",
    "forms-responses": "https://www.googleapis.com/auth/forms.responses.readonly",
    "drive": "https://www.googleapis.com/auth/drive",
    "drive-readonly": "https://www.googleapis.com/auth/drive.readonly",
    "calendar": "https://www.googleapis.com/auth/calendar",
    "calendar-readonly": "https://www.googleapis.com/auth/calendar.readonly",
}
DEFAULT_SCOPES = ["sheets", "forms", "forms-responses", "drive", "calendar"]

MIME_SHEET = "application/vnd.google-apps.spreadsheet"
MIME_FORM = "application/vnd.google-apps.form"
MIME_GDOC = "application/vnd.google-apps.document"
MIME_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _scopes() -> list[str]:
    names = [s.strip() for s in os.environ.get("GAPI_SCOPES", "").split(",") if s.strip()]
    names = names or DEFAULT_SCOPES
    unknown = [n for n in names if n not in SCOPE_MAP]
    if unknown:
        sys.exit(f"ERROR: unknown scope name(s) in GAPI_SCOPES: {', '.join(unknown)}. "
                 f"Known: {', '.join(SCOPE_MAP)}")
    return [SCOPE_MAP[n] for n in names]


def _google_root() -> Path:
    base = os.environ.get("PAROS_SECRETS_DIR") or str(Path.home() / ".paros" / "secrets")
    return Path(base).expanduser() / "google"


def _accounts_file() -> dict:
    p = _google_root() / "accounts.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        sys.exit(f"ERROR: {p} is not valid JSON: {e}")


class Ctx:
    """Where the current account's files live."""

    def __init__(self, account: str | None):
        cfg = _accounts_file()
        self.override = bool(os.environ.get("GAPI_HOME"))
        if self.override:
            self.account = "(GAPI_HOME)"
            self.home = Path(os.environ["GAPI_HOME"]).expanduser()
            self.email = None
            self.client_candidates = [self.home / "client_secret.json"]
        else:
            name = account or os.environ.get("GAPI_ACCOUNT") or cfg.get("default") or "default"
            known = cfg.get("accounts", {})
            if known and name not in known:
                sys.exit(f"ERROR: unknown account '{name}'. Known: {', '.join(known)} "
                         f"(edit {_google_root() / 'accounts.json'})")
            self.account = name
            self.home = _google_root() / name
            self.email = (known.get(name) or {}).get("email")
            self.client_candidates = [self.home / "client_secret.json",
                                      _google_root() / "client_secret.json"]
        self.token = self.home / "token.json"


CTX: Ctx | None = None


# --- auth ---------------------------------------------------------------------

def _need_libs():
    try:
        from google.auth.transport.requests import Request  # noqa: F401
        from google.oauth2.credentials import Credentials  # noqa: F401
        from google_auth_oauthlib.flow import InstalledAppFlow  # noqa: F401
        from googleapiclient.discovery import build  # noqa: F401
    except ImportError:
        sys.exit("ERROR: missing libraries. Install once: "
                 "pip install google-api-python-client google-auth-oauthlib")


def _client_secret() -> Path:
    for p in CTX.client_candidates:
        if p.exists():
            return p
    sys.exit(f"ERROR: no OAuth client found. Put the desktop client JSON at "
             f"{CTX.client_candidates[-1]} and run: gapi.py auth")


def _check_account(creds):
    """After a fresh consent: refuse to save a token for the wrong Google account.
    Browsers offer the last used account, so this mistake is easy to make."""
    if not CTX.email:
        return
    from googleapiclient.discovery import build
    about = build("drive", "v3", credentials=creds, cache_discovery=False).about().get(
        fields="user(emailAddress)").execute()
    got = about.get("user", {}).get("emailAddress", "")
    if got.lower() != CTX.email.lower():
        sys.exit(f"ERROR: you signed in as a different account than '{CTX.account}' expects. "
                 "The token was NOT saved. Run auth again and pick the right account.")


def _creds(require: str | None = None, force: bool = False):
    """Load the token with the scopes it was granted. A command that needs a
    scope the token lacks fails with a clear message instead of a 403."""
    _need_libs()
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if CTX.token.exists() and not force:
        creds = Credentials.from_authorized_user_file(str(CTX.token))
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not force and not sys.stdin.isatty():
                sys.exit(f"ERROR: no valid token for account '{CTX.account}'. "
                         "The owner runs `gapi.py auth` once in a terminal.")
            flow = InstalledAppFlow.from_client_secrets_file(str(_client_secret()), _scopes())
            kw = {"prompt": "consent select_account"}
            if CTX.email:
                kw["login_hint"] = CTX.email
            creds = flow.run_local_server(port=0, **kw)
            _check_account(creds)
        CTX.home.mkdir(parents=True, exist_ok=True)
        CTX.token.write_text(creds.to_json(), encoding="utf-8")
        try:
            os.chmod(CTX.token, 0o600)
        except OSError:
            pass
    if require and require not in (creds.scopes or []):
        sys.exit(f"ERROR: the token for '{CTX.account}' lacks the scope {require}. "
                 "Run once: gapi.py [--account NAME] auth")
    return creds


def _svc(name: str, version: str, require: str | None = None):
    creds = _creds(require=require)
    from googleapiclient.discovery import build
    return build(name, version, credentials=creds, cache_discovery=False)


def _sheets():
    return _svc("sheets", "v4")


def _forms():
    return _svc("forms", "v1")


def _drive():
    return _svc("drive", "v3")


def _calendar(write: bool = False):
    if write:
        return _svc("calendar", "v3", require=SCOPE_MAP["calendar"])
    return _svc("calendar", "v3")


def _dry(what: str, payload=None):
    print(f"DRY RUN: {what}")
    if payload is not None:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("\nNothing was written. Add --apply to do it.")


# --- auth / whoami / accounts ---------------------------------------------------

def cmd_auth(a):
    _creds(force=True)
    print(f"OK: token saved for account '{CTX.account}' at {CTX.token}")
    cmd_whoami(a)


def cmd_whoami(a):
    try:
        about = _drive().about().get(fields="user(emailAddress,displayName)").execute()
        u = about.get("user", {})
        print(f"account: {CTX.account}  signed in as: {u.get('displayName')} <{u.get('emailAddress')}>")
    except Exception as e:  # noqa: BLE001
        print(f"account: {CTX.account}  (lookup failed: {type(e).__name__})")
    if CTX.token.exists():
        d = json.loads(CTX.token.read_text(encoding="utf-8"))
        print("scopes:", ", ".join(d.get("scopes") or []))


def cmd_accounts(a):
    """List configured accounts and whether each has a token. Never prints a value."""
    cfg = _accounts_file()
    root = _google_root()
    print(f"root: {root}")
    print(f"shared client: {'present' if (root / 'client_secret.json').exists() else 'missing'}")
    names = list(cfg.get("accounts", {})) or sorted(
        p.name for p in root.iterdir() if p.is_dir()) if root.exists() else []
    if not names:
        print("(no accounts yet: run `gapi.py --account <name> auth`)")
    for n in names:
        tok = (root / n / "token.json").exists()
        mark = " (default)" if n == (cfg.get("default") or "default") else ""
        print(f"  {n}{mark}: token {'present' if tok else 'missing'}")


# --- sheet --------------------------------------------------------------------

def _values(raw: str):
    src = Path(raw)
    text = src.read_text(encoding="utf-8") if src.suffix == ".json" and src.exists() else raw
    try:
        vals = json.loads(text)
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: <json> is not valid JSON: {e}")
    if not isinstance(vals, list) or not all(isinstance(r, list) for r in vals):
        sys.exit("ERROR: <json> must be a 2D list, for example '[[\"Name\",12],[\"Milk\",6]]'")
    return vals


def _tabs(sheet_id: str) -> dict:
    meta = _sheets().spreadsheets().get(
        spreadsheetId=sheet_id, fields="sheets(properties(title,sheetId))").execute()
    return {s["properties"]["title"]: s["properties"]["sheetId"] for s in meta["sheets"]}


def _col(col: str) -> int:
    idx = 0
    for ch in col.upper():
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def _grid(a1: str, title_to_id: dict) -> dict:
    if "!" not in a1:
        sys.exit("ERROR: include the tab, for example 'Sheet1!B2:B8'")
    tab, rng = a1.rsplit("!", 1)
    tab = tab.strip("'")
    if tab not in title_to_id:
        sys.exit(f"ERROR: no tab named {tab!r}")
    m = re.match(r"^([A-Za-z]+)(\d+)(?::([A-Za-z]+)(\d+))?$", rng)
    if not m:
        sys.exit(f"ERROR: cannot parse range {rng!r} (use 'B2:B8' or 'B2')")
    c1, r1, c2, r2 = m.groups()
    return {"sheetId": title_to_id[tab],
            "startRowIndex": int(r1) - 1, "endRowIndex": int(r2) if r2 else int(r1),
            "startColumnIndex": _col(c1), "endColumnIndex": _col(c2) + 1 if c2 else _col(c1) + 1}


def cmd_sheet_tabs(a):
    meta = _sheets().spreadsheets().get(
        spreadsheetId=a.id,
        fields="properties(title,locale),sheets(properties(title,sheetId,gridProperties))").execute()
    print(f"# {meta['properties']['title']}  (locale {meta['properties'].get('locale', '?')})")
    for s in meta.get("sheets", []):
        p = s["properties"]
        g = p.get("gridProperties", {})
        print(f"  - {p['title']}  (gid={p['sheetId']}, {g.get('rowCount', '?')}x{g.get('columnCount', '?')})")


def cmd_sheet_read(a):
    kw = {}
    if a.formulas:
        kw["valueRenderOption"] = "FORMULA"
    elif a.raw:
        kw["valueRenderOption"] = "UNFORMATTED_VALUE"
    res = _sheets().spreadsheets().values().get(spreadsheetId=a.id, range=a.range, **kw).execute()
    rows = res.get("values", [])
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"\n({len(rows)} rows, range {res.get('range')}, "
          f"render {kw.get('valueRenderOption', 'FORMATTED_VALUE')})", file=sys.stderr)


def cmd_sheet_write(a):
    vals = _values(a.json)
    if not a.apply:
        return _dry(f"write to {a.id} / {a.range}", vals)
    res = _sheets().spreadsheets().values().update(
        spreadsheetId=a.id, range=a.range, valueInputOption="USER_ENTERED",
        body={"values": vals}).execute()
    print(f"OK: {res.get('updatedCells')} cells updated ({res.get('updatedRange')}).")


def cmd_sheet_append(a):
    vals = _values(a.json)
    if not a.apply:
        return _dry(f"append to the bottom of tab {a.tab!r} in {a.id}", vals)
    res = _sheets().spreadsheets().values().append(
        spreadsheetId=a.id, range=f"{a.tab}!A1", valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS", body={"values": vals}).execute()
    up = res.get("updates", {})
    print(f"OK: {up.get('updatedRows')} rows appended ({up.get('updatedRange')}).")


def cmd_sheet_create(a):
    if not a.apply:
        return _dry(f"create a new empty spreadsheet titled {a.title!r}")
    res = _sheets().spreadsheets().create(
        body={"properties": {"title": a.title}}, fields="spreadsheetId,spreadsheetUrl").execute()
    print(f"OK: spreadsheet created.\n  id:  {res['spreadsheetId']}\n  url: {res['spreadsheetUrl']}")


def cmd_sheet_addtab(a):
    body = {"requests": [{"addSheet": {"properties": {"title": a.title}}}]}
    if not a.apply:
        return _dry(f"add tab {a.title!r} to {a.id}")
    res = _sheets().spreadsheets().batchUpdate(spreadsheetId=a.id, body=body).execute()
    p = res["replies"][0]["addSheet"]["properties"]
    print(f"OK: tab created: {p['title']} (gid={p['sheetId']}).")


def cmd_sheet_insertrows(a):
    t2i = _tabs(a.id)
    if a.tab not in t2i:
        sys.exit(f"ERROR: no tab named {a.tab!r}")
    body = {"requests": [{"insertDimension": {
        "range": {"sheetId": t2i[a.tab], "dimension": "ROWS",
                  "startIndex": a.before - 1, "endIndex": a.before - 1 + a.count},
        "inheritFromBefore": False}}]}
    if not a.apply:
        return _dry(f"insert {a.count} row(s) in tab {a.tab!r} before row {a.before} "
                    "(rows below move down; formulas pointing at them follow)", body)
    _sheets().spreadsheets().batchUpdate(spreadsheetId=a.id, body=body).execute()
    print(f"OK: {a.count} row(s) inserted before row {a.before} in {a.tab}.")


def cmd_sheet_format(a):
    grid = _grid(a.range, _tabs(a.id))
    body = {"requests": [{"repeatCell": {
        "range": grid,
        "cell": {"userEnteredFormat": {"numberFormat": {"type": a.type, "pattern": a.pattern}}},
        "fields": "userEnteredFormat.numberFormat"}}]}
    if not a.apply:
        return _dry(f"set number format {a.type} {a.pattern!r} on {a.range}", grid)
    _sheets().spreadsheets().batchUpdate(spreadsheetId=a.id, body=body).execute()
    print(f"OK: format applied to {a.range}.")


def cmd_sheet_style(a):
    grid = _grid(a.range, _tabs(a.id))
    tf = {}
    if a.bold:
        tf["bold"] = True
    if a.font_size:
        tf["fontSize"] = a.font_size
    if a.font_family:
        tf["fontFamily"] = a.font_family
    reqs = []
    if tf:
        reqs.append({"repeatCell": {"range": grid, "cell": {"userEnteredFormat": {"textFormat": tf}},
                                    "fields": "userEnteredFormat.textFormat"}})
    if a.border_top:
        reqs.append({"updateBorders": {"range": grid, "top": {
            "style": "SOLID_MEDIUM", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}}}})
    if not reqs:
        sys.exit("ERROR: give at least one of --bold, --font-size, --font-family, --border-top")
    body = {"requests": reqs}
    if not a.apply:
        return _dry(f"style {a.range}", body)
    _sheets().spreadsheets().batchUpdate(spreadsheetId=a.id, body=body).execute()
    print(f"OK: style applied to {a.range}.")


# --- form ---------------------------------------------------------------------

def cmd_form_get(a):
    f = _forms().forms().get(formId=a.id).execute()
    info = f.get("info", {})
    print(f"# {info.get('title', '(untitled)')}")
    if info.get("description"):
        print(info["description"])
    items = f.get("items", [])
    print(f"\n{len(items)} items:")
    for i, it in enumerate(items):
        q = it.get("questionItem", {}).get("question", {})
        kind = "question" if q else ("section" if "pageBreakItem" in it else "other")
        print(f"  {i}. [{kind}] {it.get('title', '(untitled)')}")


def cmd_form_dump(a):
    out = json.dumps(_forms().forms().get(formId=a.id).execute(), ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")
        print(f"OK: written to {a.out}")
    else:
        print(out)


def cmd_form_responses(a):
    res = _forms().forms().responses().list(formId=a.id).execute()
    rs = res.get("responses", [])
    print(json.dumps(rs, ensure_ascii=False, indent=1) if a.json else f"{len(rs)} responses")


def cmd_form_create(a):
    if not a.apply:
        return _dry(f"create a new empty form titled {a.title!r}")
    res = _forms().forms().create(body={"info": {"title": a.title}}).execute()
    print(f"OK: form created.\n  id:     {res['formId']}\n  answer: {res.get('responderUri', '')}\n"
          f"  edit:   https://docs.google.com/forms/d/{res['formId']}/edit")


def cmd_form_update(a):
    body = json.loads(Path(a.requests).read_text(encoding="utf-8"))
    if "requests" not in body:
        sys.exit('ERROR: requests.json must be an object {"requests": [...]}')
    if not a.apply:
        return _dry(f"run {len(body['requests'])} batchUpdate request(s) on form {a.id}", body)
    _forms().forms().batchUpdate(formId=a.id, body=body).execute()
    print(f"OK: {len(body['requests'])} request(s) applied to form {a.id}.")


# --- drive --------------------------------------------------------------------

def _q_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def _type_filter(t: str) -> list[str]:
    return {"sheet": [f"mimeType='{MIME_SHEET}'"], "form": [f"mimeType='{MIME_FORM}'"],
            "doc": [f"(mimeType='{MIME_GDOC}' or mimeType='{MIME_DOCX}')"]}.get(t, [])


def cmd_drive_find(a):
    q = [f"name contains '{_q_escape(a.query)}'", "trashed=false", *_type_filter(a.type)]
    res = _drive().files().list(
        q=" and ".join(q), pageSize=50, orderBy="modifiedTime desc",
        fields="files(id,name,mimeType,owners(emailAddress),modifiedTime)",
        supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
    files = res.get("files", [])
    if not files:
        print("(no match)")
    for f in files:
        owner = (f.get("owners") or [{}])[0].get("emailAddress", "?")
        print(f"  {f['name']}\n     id={f['id']}  type={f['mimeType'].rsplit('.', 1)[-1]}  "
              f"owner={owner}  modified={f.get('modifiedTime', '')[:10]}")


def cmd_drive_list(a):
    q = ["trashed=false", *_type_filter(a.type)]
    files, token = [], None
    while True:
        res = _drive().files().list(
            q=" and ".join(q), pageSize=1000, pageToken=token, orderBy="modifiedTime desc",
            fields="nextPageToken,files(id,name,mimeType,owners(emailAddress),modifiedTime)",
            supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        files.extend(res.get("files", []))
        token = res.get("nextPageToken")
        if not token or len(files) >= a.max:
            break
    for f in files[: a.max]:
        owner = (f.get("owners") or [{}])[0].get("emailAddress", "?")
        print(f"{f.get('modifiedTime', '')[:10]}\t{f['id']}\t{owner}\t{f['name']}")
    print(f"\n({min(len(files), a.max)} files)", file=sys.stderr)


def cmd_drive_export(a):
    meta = _drive().files().get(fileId=a.id, supportsAllDrives=True, fields="name,mimeType").execute()
    mime = meta.get("mimeType", "")
    if mime == MIME_GDOC:
        data = _drive().files().export(fileId=a.id, mimeType="text/plain").execute()
        text = data.decode("utf-8", errors="replace") if isinstance(data, bytes) else str(data)
    elif mime == MIME_DOCX:
        try:
            import io
            import docx
        except ImportError:
            sys.exit("ERROR: exporting .docx needs python-docx (pip install python-docx).")
        data = _drive().files().get_media(fileId=a.id, supportsAllDrives=True).execute()
        d = docx.Document(io.BytesIO(data))
        parts = [p.text for p in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                parts.append("\t".join(c.text for c in row.cells))
        text = "\n".join(parts)
    else:
        sys.exit(f"ERROR: cannot export {mime} (a native Google Doc or a .docx is needed).")
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"OK: {meta.get('name')} -> {a.out} ({len(text)} characters)")
    else:
        print(text)


def cmd_drive_info(a):
    f = _drive().files().get(
        fileId=a.id, supportsAllDrives=True,
        fields="name,mimeType,owners(displayName,emailAddress),capabilities(canEdit),"
               "permissions(emailAddress,role),modifiedTime").execute()
    print(f"name: {f.get('name')}\ntype: {f.get('mimeType')}\nmodified: {f.get('modifiedTime', '')[:10]}")
    for o in f.get("owners", []):
        print(f"owner: {o.get('displayName')} <{o.get('emailAddress')}>")
    print(f"can edit: {'yes' if f.get('capabilities', {}).get('canEdit') else 'no'}")
    for p in f.get("permissions", []):
        print(f"  shared with: {p.get('emailAddress', '(link or anyone)')}: {p.get('role')}")


# --- cal ----------------------------------------------------------------------

def _default_tz() -> str | None:
    return os.environ.get("GAPI_TZ") or None


def _rfc3339(s: str | None, end_of_day: bool = False) -> str | None:
    if not s:
        return None
    if len(s) == 10:
        dt = datetime.combine(datetime.fromisoformat(s).date(),
                              time(23, 59, 59) if end_of_day else time(0, 0))
    else:
        dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.astimezone()
    return dt.isoformat()


def _when(s: str, tz: str | None) -> dict:
    """Date only means all day; date and time means a timed event. Without a
    named zone the machine's current offset is written into the timestamp."""
    if len(s) == 10:
        return {"date": s}
    if tz:
        return {"dateTime": s if len(s) > 16 else s + ":00", "timeZone": tz}
    return {"dateTime": _rfc3339(s)}


def _fmt_when(w: dict) -> str:
    if "dateTime" in w:
        return datetime.fromisoformat(w["dateTime"]).astimezone().strftime("%Y-%m-%d %H:%M")
    return w.get("date", "?")


def cmd_cal_list(a):
    items = _calendar().calendarList().list(showHidden=True).execute().get("items", [])
    if a.json:
        print(json.dumps(items, ensure_ascii=False, indent=1))
        return
    for c in items:
        flags = ("P" if c.get("primary") else "-") + ("H" if c.get("hidden") else "-")
        print(f"{flags} {c.get('accessRole', ''):<14} {c.get('summary')}\n      id: {c['id']}")


def cmd_cal_events(a):
    svc = _calendar()
    t_min = _rfc3339(a.frm) or datetime.now().astimezone().replace(
        hour=0, minute=0, second=0, microsecond=0).isoformat()
    t_max = _rfc3339(a.to, end_of_day=True) or (
        datetime.fromisoformat(t_min) + timedelta(days=a.days)).isoformat()
    cals = svc.calendarList().list(showHidden=True).execute().get("items", [])
    names = {c["id"]: c.get("summary") for c in cals}
    ids = [c["id"] for c in cals if not c.get("hidden")] if a.cal == "all" else [a.cal]
    out = []
    for cid in ids:
        token = None
        while True:
            res = svc.events().list(calendarId=cid, timeMin=t_min, timeMax=t_max, singleEvents=True,
                                    orderBy="startTime", q=a.q, maxResults=250,
                                    pageToken=token).execute()
            for e in res.get("items", []):
                e["_calendar"] = names.get(cid, cid)
                out.append(e)
            token = res.get("nextPageToken")
            if not token:
                break
    out.sort(key=lambda e: _fmt_when(e.get("start", {})))
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    for e in out:
        loc = f"  @ {e['location']}" if e.get("location") else ""
        print(f"{_fmt_when(e.get('start', {}))}  [{e['_calendar']}]  {e.get('summary', '(no title)')}{loc}")
        print(f"      id: {e['id']}")
    print(f"-- {len(out)} events, {t_min[:10]} .. {t_max[:10]}")


def cmd_cal_create(a):
    body = {"summary": a.title, "start": _when(a.start, a.tz), "end": _when(a.end, a.tz)}
    if a.desc:
        body["description"] = a.desc
    if a.location:
        body["location"] = a.location
    if a.attendees:
        body["attendees"] = [{"email": x.strip()} for x in a.attendees.split(",") if x.strip()]
    send = "all" if a.notify else "none"
    if not a.apply:
        return _dry(f"create event in calendar {a.cal} (notifications: {send})", body)
    e = _calendar(write=True).events().insert(calendarId=a.cal, body=body, sendUpdates=send).execute()
    print(f"OK: {e['id']}  {e.get('htmlLink')}")


def cmd_cal_update(a):
    p = Path(a.patch)
    patch = json.loads(p.read_text(encoding="utf-8") if p.exists() else a.patch)
    send = "all" if a.notify else "none"
    svc = _calendar(write=a.apply)
    if not a.apply:
        cur = svc.events().get(calendarId=a.cal, eventId=a.event_id).execute()
        return _dry(f"patch '{cur.get('summary')}' ({_fmt_when(cur.get('start', {}))}), "
                    f"notifications: {send}", patch)
    e = svc.events().patch(calendarId=a.cal, eventId=a.event_id, body=patch, sendUpdates=send).execute()
    print(f"OK: {e['id']}  {e.get('htmlLink')}")


def cmd_cal_delete(a):
    svc = _calendar(write=a.apply)
    cur = svc.events().get(calendarId=a.cal, eventId=a.event_id).execute()
    send = "all" if a.notify else "none"
    if not a.apply:
        return _dry(f"delete '{cur.get('summary')}' ({_fmt_when(cur.get('start', {}))}), "
                    f"notifications: {send}")
    svc.events().delete(calendarId=a.cal, eventId=a.event_id, sendUpdates=send).execute()
    print(f"OK: deleted (in the calendar's trash, restorable for 30 days): {cur.get('summary')}")


def cmd_cal_acl(a):
    for r in _calendar().acl().list(calendarId=a.cal).execute().get("items", []):
        sc = r.get("scope", {})
        print(f"{r.get('role'):<16} {sc.get('type')}: {sc.get('value', '')}")


def cmd_cal_new(a):
    tz = a.tz or _default_tz()
    if not tz:
        sys.exit("ERROR: a new calendar needs a named time zone: --tz Area/City or GAPI_TZ")
    body = {"summary": a.name, "timeZone": tz}
    if a.desc:
        body["description"] = a.desc
    if not a.apply:
        return _dry("create calendar", body)
    c = _calendar(write=True).calendars().insert(body=body).execute()
    print(f"OK: {c['id']}")


def cmd_cal_share(a):
    body = {"role": a.role, "scope": {"type": "user", "value": a.email}}
    if not a.apply:
        return _dry(f"share calendar {a.cal} with {a.email} as {a.role}")
    _calendar(write=True).acl().insert(calendarId=a.cal, body=body,
                                       sendNotifications=a.notify).execute()
    print(f"OK: {a.email} -> {a.role}")


# --- parser -------------------------------------------------------------------

def _apply(x):
    x.add_argument("--apply", action="store_true", help="really write (default: dry run)")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gapi", description="One Google Workspace CLI: Sheets, Forms, Drive, Calendar. "
        "Writes are dry runs unless --apply. --account NAME may appear anywhere.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("auth", help="one-time browser consent, saves the token").set_defaults(fn=cmd_auth)
    sub.add_parser("whoami", help="which account, which scopes").set_defaults(fn=cmd_whoami)
    sub.add_parser("accounts", help="configured accounts and token presence").set_defaults(fn=cmd_accounts)

    sh = sub.add_parser("sheet", help="Google Sheets").add_subparsers(dest="sub", required=True)
    x = sh.add_parser("tabs", help="tabs with gid, size, and the file's locale")
    x.add_argument("id"); x.set_defaults(fn=cmd_sheet_tabs)
    x = sh.add_parser("read", help="read a range")
    x.add_argument("id"); x.add_argument("range", help="for example 'Sheet1!A1:E10'")
    x.add_argument("--formulas", action="store_true", help="formulas instead of computed values")
    x.add_argument("--raw", action="store_true", help="unformatted raw values")
    x.set_defaults(fn=cmd_sheet_read)
    x = sh.add_parser("write", help="write cells (2D JSON list or a .json file)")
    x.add_argument("id"); x.add_argument("range"); x.add_argument("json"); _apply(x)
    x.set_defaults(fn=cmd_sheet_write)
    x = sh.add_parser("append", help="append rows to the bottom of a tab")
    x.add_argument("id"); x.add_argument("tab"); x.add_argument("json"); _apply(x)
    x.set_defaults(fn=cmd_sheet_append)
    x = sh.add_parser("create", help="new empty spreadsheet")
    x.add_argument("title"); _apply(x); x.set_defaults(fn=cmd_sheet_create)
    x = sh.add_parser("add-tab", help="new tab in an existing spreadsheet")
    x.add_argument("id"); x.add_argument("title"); _apply(x); x.set_defaults(fn=cmd_sheet_addtab)
    x = sh.add_parser("insert-rows", help="insert empty rows before a 1-based row number")
    x.add_argument("id"); x.add_argument("tab"); x.add_argument("before", type=int)
    x.add_argument("count", type=int, nargs="?", default=1); _apply(x)
    x.set_defaults(fn=cmd_sheet_insertrows)
    x = sh.add_parser("format", help="number format on a range (display only)")
    x.add_argument("id"); x.add_argument("range"); x.add_argument("pattern")
    x.add_argument("--type", default="NUMBER", choices=["NUMBER", "CURRENCY", "TEXT"]); _apply(x)
    x.set_defaults(fn=cmd_sheet_format)
    x = sh.add_parser("style", help="bold, font, top border on a range")
    x.add_argument("id"); x.add_argument("range"); x.add_argument("--bold", action="store_true")
    x.add_argument("--font-size", type=int); x.add_argument("--font-family")
    x.add_argument("--border-top", action="store_true"); _apply(x)
    x.set_defaults(fn=cmd_sheet_style)

    fm = sub.add_parser("form", help="Google Forms").add_subparsers(dest="sub", required=True)
    x = fm.add_parser("get", help="title and item list"); x.add_argument("id"); x.set_defaults(fn=cmd_form_get)
    x = fm.add_parser("dump", help="full forms.get JSON")
    x.add_argument("id"); x.add_argument("out", nargs="?"); x.set_defaults(fn=cmd_form_dump)
    x = fm.add_parser("responses", help="responses (count, or --json)")
    x.add_argument("id"); x.add_argument("--json", action="store_true"); x.set_defaults(fn=cmd_form_responses)
    x = fm.add_parser("create", help="new empty form")
    x.add_argument("title"); _apply(x); x.set_defaults(fn=cmd_form_create)
    x = fm.add_parser("update", help='batchUpdate from a {"requests": [...]} file')
    x.add_argument("id"); x.add_argument("requests"); _apply(x); x.set_defaults(fn=cmd_form_update)

    dr = sub.add_parser("drive", help="Google Drive").add_subparsers(dest="sub", required=True)
    x = dr.add_parser("find", help="search by name")
    x.add_argument("query"); x.add_argument("--type", choices=["sheet", "form", "doc", "any"], default="any")
    x.set_defaults(fn=cmd_drive_find)
    x = dr.add_parser("list", help="full inventory as TSV")
    x.add_argument("--type", choices=["sheet", "form", "doc", "any"], default="sheet")
    x.add_argument("--max", type=int, default=2000); x.set_defaults(fn=cmd_drive_list)
    x = dr.add_parser("export", help="plain text of a Google Doc or .docx")
    x.add_argument("id"); x.add_argument("--out"); x.set_defaults(fn=cmd_drive_export)
    x = dr.add_parser("info", help="owner, edit right, sharing")
    x.add_argument("id"); x.set_defaults(fn=cmd_drive_info)

    ca = sub.add_parser("cal", help="Google Calendar").add_subparsers(dest="sub", required=True)
    x = ca.add_parser("list", help="calendars: P primary, H hidden, access, id")
    x.add_argument("--json", action="store_true"); x.set_defaults(fn=cmd_cal_list)
    x = ca.add_parser("events", help="events in local time, across visible calendars")
    x.add_argument("--cal", default="all", help="calendar id, 'primary' or 'all' (default)")
    x.add_argument("--from", dest="frm"); x.add_argument("--to")
    x.add_argument("--days", type=int, default=14); x.add_argument("--q")
    x.add_argument("--json", action="store_true"); x.set_defaults(fn=cmd_cal_events)
    x = ca.add_parser("create", help="new event")
    x.add_argument("cal"); x.add_argument("--title", required=True)
    x.add_argument("--start", required=True, help="2030-05-01T09:00, or 2030-05-01 for all day")
    x.add_argument("--end", required=True, help="for all-day events the end date is exclusive")
    x.add_argument("--tz", default=_default_tz(), help="named zone, for example Europe/Lisbon")
    x.add_argument("--desc"); x.add_argument("--location")
    x.add_argument("--attendees", help="comma separated emails")
    x.add_argument("--notify", action="store_true", help="send invitation emails (default: none)")
    _apply(x); x.set_defaults(fn=cmd_cal_create)
    x = ca.add_parser("update", help="events.patch with JSON or a JSON file")
    x.add_argument("cal"); x.add_argument("event_id"); x.add_argument("patch")
    x.add_argument("--notify", action="store_true"); _apply(x); x.set_defaults(fn=cmd_cal_update)
    x = ca.add_parser("delete", help="delete an event (restorable for 30 days)")
    x.add_argument("cal"); x.add_argument("event_id")
    x.add_argument("--notify", action="store_true"); _apply(x); x.set_defaults(fn=cmd_cal_delete)
    x = ca.add_parser("acl", help="who the calendar is shared with")
    x.add_argument("cal"); x.set_defaults(fn=cmd_cal_acl)
    x = ca.add_parser("new", help="new calendar")
    x.add_argument("name"); x.add_argument("--desc"); x.add_argument("--tz")
    _apply(x); x.set_defaults(fn=cmd_cal_new)
    x = ca.add_parser("share", help="share a calendar with a person")
    x.add_argument("cal"); x.add_argument("email")
    x.add_argument("--role", default="reader", choices=["freeBusyReader", "reader", "writer", "owner"])
    x.add_argument("--notify", action="store_true"); _apply(x); x.set_defaults(fn=cmd_cal_share)
    return p


def _pop_account(argv: list[str]) -> tuple[str | None, list[str]]:
    out, account, i = [], None, 0
    while i < len(argv):
        a = argv[i]
        if a == "--account":
            account = argv[i + 1] if i + 1 < len(argv) else None
            i += 2
            continue
        if a.startswith("--account="):
            account = a.split("=", 1)[1]
        else:
            out.append(a)
        i += 1
    return account, out


def main(argv: list[str] | None = None) -> None:
    global CTX
    account, argv = _pop_account(list(sys.argv[1:] if argv is None else argv))
    args = build_parser().parse_args(argv)
    _scopes()  # fail early on a mistyped GAPI_SCOPES
    CTX = Ctx(account)
    args.fn(args)


if __name__ == "__main__":
    main()
