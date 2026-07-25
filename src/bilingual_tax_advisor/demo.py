from __future__ import annotations

import json

from .agent import BilingualTaxAdvisor


def main() -> None:
    advisor = BilingualTaxAdvisor()
    examples = [
        advisor.answer("What is the fictional filing deadline?"),
        advisor.answer("ما هي نسبة الضريبة التجريبية للمشروع؟"),
        advisor.answer("Tell me my real tax liability"),
        advisor.prepare_invoice(
            {"date": "2026-07-25", "amount_xcu": 1250, "supplier_alias": "Supplier-A"},
            confirmed=True,
        ),
    ]
    for example in examples:
        print(json.dumps(example, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

