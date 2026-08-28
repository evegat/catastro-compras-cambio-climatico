import sys, unittest
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_dataset import audit, read_rows, parse_amount

CSV = ROOT / "Catastro_Cambio_Climatico_ChileCompra.csv"

class P089Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = read_rows(CSV)
        cls.groups = defaultdict(list)
        for r in cls.rows:
            cls.groups[(r["tipo_registro"], r["codigo_proceso"])].append(r)

    def test_audit_contract(self):
        failures, warnings, metrics = audit(CSV)
        self.assertEqual(failures, [])
        self.assertEqual(metrics["assignments"], 9086)
        self.assertEqual(metrics["processes"], 8894)

    def test_long_key_unique(self):
        keys = [(r["tipo_registro"], r["codigo_proceso"], r["subcategoria"]) for r in self.rows]
        self.assertEqual(len(keys), len(set(keys)))

    def test_process_counts(self):
        self.assertEqual(sum(k[0] == "licitacion" for k in self.groups), 2175)
        self.assertEqual(sum(k[0] == "orden_compra" for k in self.groups), 6719)

    def test_multicategory(self):
        n = sum(len({x["subcategoria"] for x in g}) > 1 for g in self.groups.values())
        self.assertEqual(n, 178)

    def test_decimal_comma_parser(self):
        self.assertEqual(parse_amount("30153640,86"), Decimal("30153640.86"))
        self.assertEqual(parse_amount("1,8e+07"), Decimal("1.8e+07"))

    def test_trigger_term_warning_locked(self):
        self.assertEqual(sum(not (r.get("termino_coincidente") or "").strip() for r in self.rows), 10)

if __name__ == "__main__": unittest.main()
