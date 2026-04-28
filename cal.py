#!/usr/bin/env python3
"""
cal.py — Gestion du calendrier Apple via ligne de commande
Usage :
  python3 cal.py add  --title "Gym" --date "2026-05-05" --start "08:00" --end "09:00" --cal "DodProduction"
  python3 cal.py add  --title "EVJF" --date "2026-05-08" --allday --cal "Nine & Dod ❤️"
  python3 cal.py del  --title "Gym" --date "2026-05-05"
  python3 cal.py list --days 7
"""
import argparse, subprocess, sys
from datetime import datetime, timedelta

CALENDARS = {
    "pro":     "DodProduction",
    "perso":   "Nine & Dod ❤️",
    "default": "DodProduction",
}

MONTHS_FR = {
    1:"janvier",2:"février",3:"mars",4:"avril",5:"mai",6:"juin",
    7:"juillet",8:"août",9:"septembre",10:"octobre",11:"novembre",12:"décembre"
}
WEEKDAYS_FR = {0:"lundi",1:"mardi",2:"mercredi",3:"jeudi",4:"vendredi",5:"samedi",6:"dimanche"}

def iso_to_applescript(date_str, time_str="00:00"):
    """'2026-05-05', '08:00' → 'lundi 5 mai 2026 à 08:00:00'"""
    d = datetime.strptime(date_str, "%Y-%m-%d")
    h, m = map(int, time_str.split(":"))
    d = d.replace(hour=h, minute=m)
    wd = WEEKDAYS_FR[d.weekday()]
    mo = MONTHS_FR[d.month]
    return f"{wd} {d.day} {mo} {d.year} à {d.strftime('%H:%M:%S')}"

def run_apple(script):
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Erreur AppleScript : {r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return r.stdout.strip()

def resolve_cal(name):
    return CALENDARS.get(name.lower(), name)

# ── ADD ───────────────────────────────────────────────────────────────────────
def cmd_add(args):
    cal  = resolve_cal(args.cal)
    date = args.date

    if args.allday:
        start_as = iso_to_applescript(date, "00:00")
        end_as   = iso_to_applescript(date, "23:59")
        script = f'''
tell application "Calendar"
    tell calendar "{cal}"
        set startD to date "{start_as}"
        set endD   to date "{end_as}"
        set newEvent to make new event at end with properties {{summary:"{args.title}", start date:startD, end date:endD, allday event:true}}
    end tell
    reload calendars
end tell'''
    else:
        start_as = iso_to_applescript(date, args.start or "09:00")
        end_as   = iso_to_applescript(date, args.end   or "10:00")
        notes_prop = f', description:"{args.notes}"' if args.notes else ''
        script = f'''
tell application "Calendar"
    tell calendar "{cal}"
        set startD to date "{start_as}"
        set endD   to date "{end_as}"
        set newEvent to make new event at end with properties {{summary:"{args.title}", start date:startD, end date:endD{notes_prop}}}
    end tell
    reload calendars
end tell'''

    run_apple(script)
    day_label = "Toute la journée" if args.allday else f"{args.start or '09:00'} → {args.end or '10:00'}"
    print(f"✓ Ajouté : «{args.title}» le {date} ({day_label}) dans {cal}")

# ── DELETE ────────────────────────────────────────────────────────────────────
def cmd_del(args):
    cal_filter = f'and calendar is calendar "{resolve_cal(args.cal)}"' if args.cal else ''
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
        start_as = iso_to_applescript(args.date, "00:00")
        end_as   = iso_to_applescript(args.date, "23:59")
        filter_clause = f'whose summary is "{args.title}" and start date >= date "{start_as}" and start date <= date "{end_as}"'
    else:
        filter_clause = f'whose summary is "{args.title}"'

    script = f'''
tell application "Calendar"
    set deleted to 0
    repeat with c in calendars
        set toDelete to (every event of c {filter_clause})
        repeat with e in toDelete
            delete e
            set deleted to deleted + 1
        end repeat
    end repeat
    reload calendars
    return deleted
end tell'''
    count = run_apple(script)
    print(f"✓ Supprimé {count} événement(s) : «{args.title}»")

# ── LIST ──────────────────────────────────────────────────────────────────────
def cmd_list(args):
    days = args.days or 7
    script = f'''
tell application "Calendar"
    set output to ""
    set startDate to current date
    set endDate to startDate + ({days} * days)
    repeat with c in calendars
        set cName to name of c
        if cName is "DodProduction" or cName is "Nine & Dod ❤️" then
            set evts to (every event of c whose start date >= startDate and start date <= endDate)
            repeat with e in evts
                set output to output & cName & "||" & summary of e & "||" & (start date of e as string) & "\\n"
            end repeat
        end if
    end repeat
    return output
end tell'''
    out = run_apple(script)
    if not out.strip():
        print("Aucun événement dans les prochains jours.")
        return
    print(f"\nProchains {days} jours :\n")
    for line in sorted(out.strip().splitlines()):
        parts = line.split("||")
        if len(parts) >= 3:
            cal, title, date = parts[0], parts[1], parts[2]
            print(f"  {date[:30]:32} {title:35} [{cal}]")

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Gestion calendrier Apple")
    sub = p.add_subparsers(dest="cmd")

    a = sub.add_parser("add")
    a.add_argument("--title", required=True)
    a.add_argument("--date",  required=True, help="YYYY-MM-DD")
    a.add_argument("--start", help="HH:MM")
    a.add_argument("--end",   help="HH:MM")
    a.add_argument("--cal",   default="pro", help="pro | perso | nom exact")
    a.add_argument("--allday", action="store_true")
    a.add_argument("--notes")

    d = sub.add_parser("del")
    d.add_argument("--title", required=True)
    d.add_argument("--date",  help="YYYY-MM-DD")
    d.add_argument("--cal")

    l = sub.add_parser("list")
    l.add_argument("--days", type=int, default=7)

    args = p.parse_args()
    if   args.cmd == "add":  cmd_add(args)
    elif args.cmd == "del":  cmd_del(args)
    elif args.cmd == "list": cmd_list(args)
    else: p.print_help()

if __name__ == "__main__":
    main()
