public with sharing class SyntheticTaxPolicy {
    public class Decision {
        @AuraEnabled public Boolean confirmationRequired;
        @AuraEnabled public String reason;
    }

    @InvocableMethod(label='Evaluate Synthetic Invoice Policy')
    public static List<Decision> evaluate(List<Decimal> amounts) {
        List<Decision> decisions = new List<Decision>();
        for (Decimal amount : amounts) {
            Decision decision = new Decision();
            decision.confirmationRequired = true;
            decision.reason = amount != null && amount > 0
                ? 'Explicit confirmation is required'
                : 'A positive synthetic amount is required';
            decisions.add(decision);
        }
        return decisions;
    }
}

