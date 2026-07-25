import unittest

from bilingual_tax_advisor import BilingualTaxAdvisor


class BilingualTaxAdvisorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.advisor = BilingualTaxAdvisor()

    def test_english_answer_is_cited(self) -> None:
        result = self.advisor.answer("What is the filing deadline?")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["citations"], ["SYNTH-GUIDE-02"])

    def test_arabic_answer_is_cited(self) -> None:
        result = self.advisor.answer("ما هي نسبة الضريبة للمشروع؟")
        self.assertEqual(result["language"], "ar")
        self.assertEqual(result["citations"], ["SYNTH-GUIDE-03"])

    def test_unknown_question_hands_off(self) -> None:
        result = self.advisor.answer("Can I deduct a real overseas transaction?")
        self.assertEqual(result["status"], "human_handoff")

    def test_sensitive_number_is_blocked(self) -> None:
        result = self.advisor.answer("Look up account 123456789012")
        self.assertEqual(result["status"], "blocked")

    def test_invoice_requires_confirmation(self) -> None:
        result = self.advisor.prepare_invoice(
            {"date": "2026-07-25", "amount_xcu": 100, "supplier_alias": "Supplier-A"}
        )
        self.assertEqual(result["status"], "approval_required")

    def test_invoice_tool_ignores_extra_fields(self) -> None:
        result = self.advisor.prepare_invoice(
            {
                "date": "2026-07-25",
                "amount_xcu": 100,
                "supplier_alias": "Supplier-A",
                "access_token": "must-not-propagate",
            },
            confirmed=True,
        )
        self.assertEqual(result["status"], "completed")
        self.assertNotIn("access_token", result["payload"])


if __name__ == "__main__":
    unittest.main()

