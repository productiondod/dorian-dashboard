import os, json, requests
from datetime import datetime, timezone

TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

DB_PROJETS       = "59513012-9016-821f-b528-87b6d58739b5"
DB_TRANSACTIONS  = "75413012-9016-8374-b6df-87d8f54573ed"
DB_OPPORTUNITES  = "5fe13012-9016-8218-84d2-07ad14db2bcd"


def query_db(db_id, payload=None):
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    results, cursor = [], None
    while True:
        body = payload.copy() if payload else {}
        if cursor:
            body["start_cursor"] = cursor
        r = requests.post(url, headers=HEADERS, json=body)
        r.raise_for_status()
        data = r.json()
        results.extend(data["results"])
        if not data.get("has_more"):
            break
        cursor = data["next_cursor"]
    return results


def title(p, key="Nom"):
    t = p["properties"].get(key, {}).get("title", [])
    return t[0]["plain_text"] if t else ""

def status(p, key):
    s = p["properties"].get(key, {}).get("status")
    return s["name"] if s else None

def number(p, key):
    return p["properties"].get(key, {}).get("number")

def formula_number(p, key):
    f = p["properties"].get(key, {}).get("formula", {})
    return f.get("number")

def formula_string(p, key):
    f = p["properties"].get(key, {}).get("formula", {})
    return f.get("string") or ""

def select_val(p, key):
    s = p["properties"].get(key, {}).get("select")
    return s["name"] if s else None

def date_val(p, key):
    d = p["properties"].get(key, {}).get("date")
    return d["start"] if d else None


# ── Projets actifs ────────────────────────────────────────
projets_raw = query_db(DB_PROJETS, {
    "filter": {
        "property": "Avancement",
        "status": {"does_not_equal": "Terminé"}
    }
})
projets = []
for p in projets_raw:
    nom = title(p)
    if not nom:
        continue
    projets.append({
        "nom": nom,
        "montant": number(p, "Montant"),
        "avancement": status(p, "Avancement"),
        "deadline": date_val(p, "Deadline"),
        "reste": formula_number(p, "Reste à payer"),
    })

# ── Transactions du mois courant ──────────────────────────
now = datetime.now(timezone.utc)
mois_debut = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d")

transactions_raw = query_db(DB_TRANSACTIONS, {
    "filter": {
        "property": "Date",
        "date": {"on_or_after": mois_debut}
    }
})

ca_mois = 0.0
depenses_mois = 0.0
for p in transactions_raw:
    montant = number(p, "Montant TTC") or 0
    t = select_val(p, "Type transaction")
    if t == "Entrée":
        ca_mois += montant
    elif t == "Sortie":
        depenses_mois += montant

# À encaisser = somme des "Reste à payer" non nuls
a_encaisser = sum(p["reste"] for p in projets if p["reste"])

# ── Opportunités actives ──────────────────────────────────
opps_raw = query_db(DB_OPPORTUNITES, {
    "filter": {
        "property": "Statut",
        "status": {"does_not_equal": "Perdu"}
    }
})
opportunites = []
for p in opps_raw:
    nom = title(p)
    if not nom or nom == "Opportunité":
        continue
    opportunites.append({
        "nom": nom,
        "statut": status(p, "Statut"),
        "montant": number(p, "Montant"),
        "relance": formula_string(p, "Relance"),
    })

# ── Export ────────────────────────────────────────────────
data = {
    "updated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "projets": projets,
    "financier": {
        "ca_mois": round(ca_mois, 2),
        "depenses_mois": round(depenses_mois, 2),
        "a_encaisser": round(a_encaisser, 2),
    },
    "opportunites": opportunites,
}

with open("notion-data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✓ {len(projets)} projets · CA {ca_mois}€ · {len(opportunites)} opportunités")
