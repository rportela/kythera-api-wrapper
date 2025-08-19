=== Summary of Changes ===

=== Paths ===
New paths:
  + /v1/indexes/values
  + /v1/risk-factors/parameters

=== Components ===
New schemas:
  + IndexValueDto
  + RiskFactorParameterDto
Modified schema FundNavDto:
    * schema FundNavDto. property added: sourceId
    * schema FundNavDto. property added: sourceName
    * schema FundNavDto. property added: statusId
    * schema FundNavDto. property added: statusName
Modified schema InstrumentDto:
    * schema InstrumentDto. property added: enabled
Modified schema InstrumentGroupDto:
    * schema InstrumentGroupDto. property added: nomenclatures
Modified schema IntradayPnlEntryDto:
    * schema IntradayPnlEntryDto. property added: riskFactorCashMain
    * schema IntradayPnlEntryDto. property added: riskFactorCashSecondary
    * schema IntradayPnlEntryDto. property added: riskFactorFixing
    * schema IntradayPnlEntryDto. property added: riskFactorMain
    * schema IntradayPnlEntryDto. property added: riskFactorSecondary
    * schema IntradayPnlEntryDto. required added: riskFactorCashMain
    * schema IntradayPnlEntryDto. required added: riskFactorCashSecondary
    * schema IntradayPnlEntryDto. required added: riskFactorFixing
    * schema IntradayPnlEntryDto. required added: riskFactorMain
    * schema IntradayPnlEntryDto. required added: riskFactorSecondary
Modified schema SubclassNavDto:
    * schema SubclassNavDto. property added: sourceId
    * schema SubclassNavDto. property added: sourceName
    * schema SubclassNavDto. property added: statusId
    * schema SubclassNavDto. property added: statusName

=== End ===