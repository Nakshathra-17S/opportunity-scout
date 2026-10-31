import sqlite3, subprocess, sys
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Opportunity Scout")
st.title("Opportunity Scout")
st.caption("Open innovation: outside opportunities, collected by TinyFish")

if st.button("Refresh data"):
    with st.spinner("TinyFish is scanning the web... a few minutes"):
        subprocess.run([sys.executable, "collect.py"])
    st.rerun()

db = sqlite3.connect("opps.db")
rows = db.execute(
    "SELECT title, deadline, reward, link, category FROM opps").fetchall()

def parse(d):
    try:
        end = d.split(" - ")[-1].strip()
        return datetime.strptime(end, "%b %d, %Y")
    except Exception:
        return datetime.max

cats = ["All"] + sorted({r[4] for r in rows if r[4]})
c1, c2 = st.columns(2)
cat = c1.selectbox("Category", cats)
hide_old = c2.checkbox("Hide expired", value=True)
q = st.text_input("Search")

rows.sort(key=lambda r: parse(r[1]))
shown = []
for r in rows:
    if q.lower() not in (r[0] or "").lower():
        continue
    if cat != "All" and r[4] != cat:
        continue
    if hide_old and parse(r[1]) < datetime.now():
        continue
    shown.append(r)

st.write(f"Showing {len(shown)} of {len(rows)} opportunities")
for t, d, rw, l, c in shown:
    with st.container(border=True):
        st.caption(c)
        st.subheader(t)
        st.write(f"Deadline: {d}  |  Reward: {rw}")
        st.link_button("Open", l)