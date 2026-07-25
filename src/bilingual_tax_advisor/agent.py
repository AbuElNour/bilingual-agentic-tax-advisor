from __future__ import annotations

import re
from dataclasses import dataclass


ARABIC = re.compile(r"[\u0600-\u06ff]")
SENSITIVE_ID = re.compile(r"\b\d{9,16}\b")


@dataclass(frozen=True)
class Guidance:
    source_id: str
    terms_en: frozenset[str]
    terms_ar: frozenset[str]
    text_en: str
    text_ar: str


GUIDANCE = (
    Guidance(
        source_id="SYNTH-GUIDE-01",
        terms_en=frozenset({"invoice", "invoices", "receipt"}),
        terms_ar=frozenset({"فاتورة", "فواتير", "إيصال"}),
        text_en="A fictional invoice needs a date, amount, and synthetic supplier alias.",
        text_ar="تتطلب الفاتورة التجريبية تاريخًا ومبلغًا واسمًا مستعارًا للمورد.",
    ),
    Guidance(
        source_id="SYNTH-GUIDE-02",
        terms_en=frozenset({"filing", "deadline", "submit"}),
        terms_ar=frozenset({"إقرار", "موعد", "تقديم"}),
        text_en="The illustrative filing deadline is 30 June 2027.",
        text_ar="الموعد التجريبي لتقديم الإقرار هو 30 يونيو 2027.",
    ),
    Guidance(
        source_id="SYNTH-GUIDE-03",
        terms_en=frozenset({"rate", "small", "business"}),
        terms_ar=frozenset({"نسبة", "ضريبة", "مشروع"}),
        text_en="The fictional small-business rate is 10 percent.",
        text_ar="النسبة التجريبية للمشروعات الصغيرة هي 10 بالمائة.",
    ),
)


class BilingualTaxAdvisor:
    def answer(self, question: str) -> dict:
        language = "ar" if ARABIC.search(question) else "en"
        trace = [{"step": "language.detected", "language": language}]
        if SENSITIVE_ID.search(question):
            trace.append({"step": "privacy.blocked", "reason": "possible sensitive identifier"})
            return self._result(
                language,
                "blocked",
                "Remove personal or financial identifiers before continuing.",
                "احذف أي أرقام شخصية أو مالية قبل المتابعة.",
                [],
                trace,
            )

        normalized = question.lower()
        matches = [
            item
            for item in GUIDANCE
            if any(term in normalized for term in (item.terms_ar if language == "ar" else item.terms_en))
        ]
        trace.append({"step": "retrieval.completed", "sources": [item.source_id for item in matches]})
        if not matches:
            trace.append({"step": "handoff.created", "reason": "unsupported request"})
            return self._result(
                language,
                "human_handoff",
                "The synthetic knowledge base does not support this request. A qualified human should review it.",
                "لا تدعم قاعدة المعرفة التجريبية هذا الطلب. يجب أن يراجعه مختص مؤهل.",
                [],
                trace,
            )

        answer = " ".join(
            f"{item.text_ar if language == 'ar' else item.text_en} [{item.source_id}]" for item in matches
        )
        trace.append({"step": "answer.completed", "grounded": True})
        return {
            "language": language,
            "status": "completed",
            "answer": answer,
            "citations": [item.source_id for item in matches],
            "trace": trace,
            "disclaimer": self._disclaimer(language),
        }

    def prepare_invoice(self, payload: dict, confirmed: bool = False) -> dict:
        safe_payload = {key: payload.get(key) for key in ("date", "amount_xcu", "supplier_alias")}
        missing = [key for key, value in safe_payload.items() if value in (None, "")]
        trace = [{"step": "tool.requested", "tool": "mock_invoice.create"}]
        if missing:
            trace.append({"step": "tool.rejected", "reason": "missing fields"})
            return {"status": "invalid", "missing": missing, "trace": trace}
        if not isinstance(safe_payload["amount_xcu"], (int, float)) or safe_payload["amount_xcu"] <= 0:
            trace.append({"step": "tool.rejected", "reason": "invalid amount"})
            return {"status": "invalid", "reason": "amount_xcu must be positive", "trace": trace}
        if not confirmed:
            trace.append({"step": "approval.required"})
            return {"status": "approval_required", "preview": safe_payload, "trace": trace}
        trace.extend(({"step": "approval.recorded"}, {"step": "tool.completed", "mode": "mock"}))
        return {
            "status": "completed",
            "invoice_id": "SYNTH-INVOICE-DEMO",
            "payload": safe_payload,
            "trace": trace,
        }

    @staticmethod
    def _result(language: str, status: str, en: str, ar: str, citations: list[str], trace: list[dict]) -> dict:
        return {
            "language": language,
            "status": status,
            "answer": ar if language == "ar" else en,
            "citations": citations,
            "trace": trace,
            "disclaimer": BilingualTaxAdvisor._disclaimer(language),
        }

    @staticmethod
    def _disclaimer(language: str) -> str:
        return "مثال خيالي وليس استشارة ضريبية." if language == "ar" else "Fictional example; not tax advice."

