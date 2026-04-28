#!/usr/bin/env python3
"""
sync_calendar.py
Lit les événements iCal via AppleScript, génère events.json,
puis pousse automatiquement sur GitHub Pages.
"""
import subprocess, json, os, sys
from datetime import datetime

CALENDARS  = ["Nine & Dod ❤️", "DodProduction"]
DAYS_AHEAD = 14
OUT_FILE   = os.path.join(os.path.dirname(__file__), "events.json")
REPO_DIR   = os.path.dirname(__file__)

CAL_COLORS = {
    "Nine & Dod ❤️":  "#47c4ff",
    "DodProduction":  "#e8ff47",
}

SCRIPT = f"""
tell application "Calendar"
    set output to ""
    set startDate to current date
    set endDate to startDate + ({DAYS_AHEAD} * days)
    repeat with calName in {{{', '.join(f'"{c}"' for c in CALENDARS)}}}
        try
            set c to calendar calName
            set evts to (every event of c whose start date >= startDate and start date <= endDate)
            repeat with e in evts
                set eTitle to summary of e
                set eStart to start date of e
                set allDay to allday event of e
                try
                    set eEnd to end date of e
                on error
                    set eEnd to eStart
                end try
                set output to output & calName & "||" & eTitle & "||" & (eStart as string) & "||" & (eEnd as string) & "||" & (allDay as string) & "\\n"
            end repeat
        end try
    end repeat
    return output
end tell
"""

DAYS_FR = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
MONTHS_FR = ["","janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]

def parse_applescript_date(s):
    """Parse 'vendredi 8 mai 2026 à 00:00:00' → datetime"""
    s = s.strip()
    try:
        # Format: "jour_semaine jour mois année à hh:mm:ss"
        parts = s.replace(" à ", " ").split()
        # parts: [weekday, day, month, year, time]
        day_num = int(parts[1])
        month_num = MONTHS_FR.index(parts[2].lower())
        year_num  = int(parts[3])
        time_parts = parts[4].split(":")
        h, m, sec = int(time_parts[0]), int(time_parts[1]), int(time_parts[2])
        return datetime(year_num, month_num, day_num, h, m, sec)
    except Exception as e:
        return None

def run():
    result = subprocess.run(["osascript", "-e", SCRIPT],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print("AppleScript error:", result.stderr)
        sys.exit(1)

    raw = result.stdout.strip()
    events = []
    for line in raw.splitlines():
        line = line.strip()
        if not line: continue
        parts = line.split("||")
        if len(parts) < 4: continue
        cal, title, start_s, end_s = parts[0], parts[1], parts[2], parts[3]
        all_day = parts[4].strip().lower() == "true" if len(parts) > 4 else False

        start_dt = parse_applescript_date(start_s)
        end_dt   = parse_applescript_date(end_s)
        if not start_dt: continue

        events.append({
            "cal":     cal,
            "color":   CAL_COLORS.get(cal, "#888"),
            "title":   title,
            "start":   start_dt.isoformat(),
            "end":     end_dt.isoformat() if end_dt else start_dt.isoformat(),
            "allDay":  all_day,
            "startTs": int(start_dt.timestamp()),
        })

    events.sort(key=lambda e: e["startTs"])

    payload = {
        "synced": datetime.now().isoformat(),
        "events": events
    }

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"✓ {len(events)} événements exportés → events.json")

    # Push to GitHub
    cmds = [
        ["git", "-C", REPO_DIR, "add", "events.json"],
        ["git", "-C", REPO_DIR, "commit", "-m", f"sync: calendar {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
        ["git", "-C", REPO_DIR, "push"],
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 and "nothing to commit" not in r.stdout + r.stderr:
            print(f"Git warning: {r.stderr.strip()}")

    print("✓ Publié sur GitHub Pages")

if __name__ == "__main__":
    run()
