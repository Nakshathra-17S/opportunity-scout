# Opportunity Scout

An open innovation tool that collects outside opportunities
(hackathons, internships) from the web into one dashboard,
using the TinyFish Web Agent API.

## Open innovation link
The app brings external opportunities and ideas to the user
(inbound open innovation) instead of searching each site by hand.

## Pipeline (FEKS)
- Find: list of source websites
- Extract: TinyFish Agent API reads each site and returns JSON
- Keep: SQLite database (opps.db) with duplicate removal
- Show: Streamlit dashboard with search, category filter, deadline sort

## Files
- fetch_one.py: runs the TinyFish agent on one site
- collect.py: scans all sources and saves to the database
- app.py: Streamlit dashboard
- opps.db: sample collected data

## How to run
    pip install -r requirements.txt
    set TINYFISH_API_KEY=your_key
    python collect.py
    python -m streamlit run app.py

Get a free key at agent.tinyfish.ai.

## Limitations
- Agent runs take 25 to 130 seconds per site, so results are cached.
- Some sites (for example Unstop) block automated agents.