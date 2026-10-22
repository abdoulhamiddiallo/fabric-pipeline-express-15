"""Recalcule ce que doivent contenir les vues argent et or, à partir du CSV brut."""
import csv
from collections import defaultdict
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "data" / "orders" / "orders_2026-11-09.csv"
rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
ok = [r for r in rows if int(r["qty"]) > 0 and r["unit_price_sgd"] != ""]
print(f"bronze.orders        {len(rows)} lignes")
print(f"silver.orders_clean  {len(ok)} lignes ({len(rows) - len(ok)} écartées)")
print(f"  qty_ok   écarte {sum(int(r['qty']) <= 0 for r in rows)} lignes (annulations et remboursements)")
print(f"  price_ok écarte {sum(r['unit_price_sgd'] == '' for r in rows)} lignes (prix vide)")
centre, dish = defaultdict(lambda: [0, 0, 0.0]), defaultdict(lambda: [0, 0.0])
for r in ok:
    q, a = int(r["qty"]), int(r["qty"]) * float(r["unit_price_sgd"])
    c = centre[r["centre"]]; c[0] += 1; c[1] += q; c[2] += a
    d = dish[r["dish"]]; d[0] += q; d[1] += a
print("\ngold.centre_board")
for k, (n, q, a) in sorted(centre.items(), key=lambda kv: -kv[1][2]):
    print(f"  {k:<18} {n:>4} commandes {q:>5} portions {a:>9.2f} SGD")
print("\ngold.dish_board")
for k, (q, a) in sorted(dish.items(), key=lambda kv: -kv[1][1]):
    print(f"  {k:<16} {q:>5} portions {a:>9.2f} SGD")
print(f"\nTotal valide {sum(v[2] for v in centre.values()):.2f} SGD")
