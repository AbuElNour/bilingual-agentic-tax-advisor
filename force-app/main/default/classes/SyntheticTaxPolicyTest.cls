@IsTest
private class SyntheticTaxPolicyTest {
    @IsTest
    static void confirmationIsAlwaysRequired() {
        List<SyntheticTaxPolicy.Decision> decisions =
            SyntheticTaxPolicy.evaluate(new List<Decimal>{ 100, -1 });
        System.assertEquals(true, decisions[0].confirmationRequired);
        System.assertEquals(true, decisions[1].confirmationRequired);
        System.assert(decisions[1].reason.contains('positive'));
    }
}

