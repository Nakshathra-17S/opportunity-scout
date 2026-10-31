import json, ast, sqlite3, subprocess, sys, time

db = sqlite3.connect("opps.db")
db.execute("""CREATE TABLE IF NOT EXISTS opps
              (title TEXT, deadline TEXT, reward TEXT,
               link TEXT UNIQUE, category TEXT)""")

SOURCES = [
    ("https://devpost.com/hackathons", "Hackathon"),
    ("https://internshala.com/internships", "Internship"),
]
TIMEOUT = 180

def find_items(x):
    if isinstance(x, str):
        try:
            x = json.loads(x)
        except Exception:
            try:
                x = ast.literal_eval(x)
            except Exception:
                return []
    if isinstance(x, list):
        if x and all(isinstance(i, dict) for i in x):
            return x
        for i in x:
            r = find_items(i)
            if r:
                return r
    if isinstance(x, dict):
        for v in x.values():
            r = find_items(v)
            if r:
                return r
    return []

def pick(o, *names):
    for n in names:
        if o.get(n):
            return o[n]
    return "N/A"

for url, cat in SOURCES:
    start = time.time()
    print("Scanning:", url, flush=True)
    try:
        p = subprocess.run([sys.executable, "fetch_one.py", url],
                           capture_output=True, text=True, timeout=TIMEOUT)
        line = [l for l in p.stdout.splitlines() if l.startswith("RESULT_JSON:")]
        if not line:
            print("  Skipped: no result", p.stderr[-200:], flush=True)
            continue
        data = find_items(json.loads(line[0][len("RESULT_JSON:"):]))
        for o in data:
            db.execute("INSERT OR IGNORE INTO opps VALUES (?,?,?,?,?)",
                       (pick(o, "name", "title"), pick(o, "deadline"),
                        pick(o, "prize", "reward", "stipend"),
                        pick(o, "link", "url"), cat))
        db.commit()
        print(f"  done in {int(time.time()-start)}s, got {len(data)} items", flush=True)
    except subprocess.TimeoutExpired:
        print(f"  Skipped: took more than {TIMEOUT}s", flush=True)
    except Exception as e:
        print("  Skipped (error):", e, flush=True)

print("Saved. Total rows:", db.execute("SELECT COUNT(*) FROM opps").fetchone()[0])