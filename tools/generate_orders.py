"""Génère la journée de commandes des hawker centres de Singapour (graine 1515)."""
import csv, random, datetime as dt
from pathlib import Path
random.seed(1515)
CENTRES = {"Maxwell": 1.15, "Lau Pa Sat": 1.0, "Old Airport Road": 0.9, "Tiong Bahru": 0.75, "Chomp Chomp": 0.7}
DISHES = {"Chicken rice": 5.0, "Laksa": 6.5, "Char kway teow": 6.0, "Satay": 1.2, "Hokkien mee": 6.0,
          "Nasi lemak": 4.5, "Bak kut teh": 8.5, "Kaya toast": 3.2}
WEIGHT = {"Chicken rice": 1.6, "Laksa": 1.1, "Char kway teow": 1.0, "Satay": 0.9, "Hokkien mee": 0.9,
          "Nasi lemak": 1.2, "Bak kut teh": 0.7, "Kaya toast": 1.0}
rows, oid = [], 15000
day = dt.datetime(2026, 11, 9, 7, 0)
cs, cw = list(CENTRES), list(CENTRES.values())
ds, dw = list(DISHES), list(WEIGHT.values())
for i in range(640):
    oid += 1
    c = random.choices(cs, cw)[0]; d = random.choices(ds, dw)[0]
    q = random.choice([10, 20, 30]) if d == "Satay" else random.choices([1, 2, 3, 4], [5, 3, 1.5, .5])[0]
    p = f"{DISHES[d]:.2f}"
    t = day + dt.timedelta(minutes=random.randint(0, 15 * 60))
    rows.append([oid, c, d, q, p, t.strftime("%Y-%m-%d %H:%M:%S")])
bad = random.sample(range(len(rows)), 27)
for k, j in enumerate(bad):
    if k % 3 == 0: rows[j][3] = 0          # assiette annulée
    elif k % 3 == 1: rows[j][3] = -rows[j][3]  # remboursement
    else: rows[j][4] = ""                 # prix manquant
rows.sort(key=lambda r: r[5])
with open(Path(__file__).resolve().parent.parent / "data" / "orders" / "orders_2026-11-09.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["order_id", "centre", "dish", "qty", "unit_price_sgd", "ordered_at"]); w.writerows(rows)
