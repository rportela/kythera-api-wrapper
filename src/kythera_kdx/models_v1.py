from datetime import date as DateType, time as TimeType
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class FundAdministratorDto(BaseModel):
    id: Optional[int] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)


class FundDto(BaseModel):
    id: Optional[int] = Field(None)
    shortName: Optional[str] = Field(None)
    fullName: Optional[str] = Field(None)
    cotaAbertura: Optional[bool] = Field(None)
    isEnabled: Optional[bool] = Field(None)
    characteristics: Optional[Dict[str, str]] = Field(None)
    administrator: Optional[FundAdministratorDto] = Field(None)


class FundNavDto(BaseModel):
    id: Optional[int] = Field(None)
    navTypeId: Optional[int] = Field(None)
    navType: Optional[str] = Field(None)
    fundId: Optional[int] = Field(None)
    fundName: Optional[str] = Field(None)
    date: Optional[DateType] = Field(None)
    value: Optional[float] = Field(None)


class CalendarDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    description: str
    holidays: List[DateType]


class CountryDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    twoLetterCode: str
    threeLetterCode: str
    code: Optional[int] = Field(None)


class CurrencyDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    threeLetterCode: str
    code: Optional[int] = Field(None)
    priority: Optional[int] = Field(None)


class InstitutionDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    fullName: str
    typeId: Optional[int] = Field(None)
    typeName: str
    characteristics: Optional[Dict[str, str]] = Field(None)


class InstitutionTypeDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    description: str


class IssuerDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    description: str
    tinNumber: str
    countryId: Optional[int] = Field(None)
    issuerCountryId: Optional[int] = Field(None)
    countryName: Optional[str] = Field(None)
    issuerCountryName: str
    parentIssuerId: Optional[int] = Field(None)
    parentIssuerName: str
    characteristics: Optional[Dict[str, str]] = Field(None)


class InstrumentGroupDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    description: str
    characteristics: Optional[Dict[str, str]] = Field(None)


# New nested DTOs for Instrument details per spec
class InstrumentIssuerDto(BaseModel):
    issuerId: Optional[int] = Field(None)
    name: str
    description: str
    tinNumber: str
    countryId: Optional[int] = Field(None)
    country: str
    characteristics: Optional[Dict[str, str]] = Field(None)


class InstrumentBasketUnderlyingDto(BaseModel):
    id: Optional[int] = Field(None)
    underlyingId: Optional[int] = Field(None)
    underlyingInstrumentGroup: str
    underlyingInstrument: str
    entryDate: Optional[DateType] = Field(None)
    settlementDate: Optional[DateType] = Field(None)
    quantity: Optional[float] = Field(None)
    price: Optional[float] = Field(None)
    tradeFee: Optional[float] = Field(None)
    fundingSpread: Optional[float] = Field(None)
    observation: str


class InstrumentCashFlowDto(BaseModel):
    id: Optional[int] = Field(None)
    cashFlowTypeId: Optional[int] = Field(None)
    cashFlowType: str
    fixingDate: Optional[DateType] = Field(None)
    endAccrualDate: Optional[DateType] = Field(None)
    settleDate: Optional[DateType] = Field(None)
    fixingPmtFactor: Optional[float] = Field(None)


class InstrumentNomenclatureDto(BaseModel):
    id: Optional[int] = Field(None)
    counterparty: str
    application: str
    namingParameter: str
    definition: str


class InstrumentDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    groupId: Optional[int] = Field(None)
    groupName: str
    group: Optional['InstrumentGroupDto'] = Field(None)
    characteristics: Optional[Dict[str, str]] = Field(None)
    issuers: Optional[List[InstrumentIssuerDto]] = Field(None)
    baskets: Optional[List[InstrumentBasketUnderlyingDto]] = Field(None)
    cashFlows: Optional[List[InstrumentCashFlowDto]] = Field(None)
    nomenclatures: Optional[List[InstrumentNomenclatureDto]] = Field(None)


class InstrumentParameterDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    description: str


class IntradayPriceDto(BaseModel):
    """Placeholder model for intraday prices - fields not defined in OpenAPI spec"""
    pass


class IntradayRiskFactorValueDto(BaseModel):
    """Placeholder model for intraday risk factor values - fields not defined in OpenAPI spec"""
    pass


class IntradayPnlEntryDto(BaseModel):
    pnl: Optional[float] = Field(None)
    pnlTrade: Optional[float] = Field(None)
    pnlPosition: Optional[float] = Field(None)
    pnlInstrumentCurrency: Optional[float] = Field(None)
    pnlFx: Optional[float] = Field(None)
    pnlCarryCalc: Optional[float] = Field(None)
    pnlCarryEffect: Optional[float] = Field(None)
    pnlMainRiskFactor: Optional[float] = Field(None)
    openPrice: Optional[float] = Field(None)
    lastPrice: Optional[float] = Field(None)
    openPriceMainRiskFactor: Optional[float] = Field(None)
    lastPriceMainRiskFactor: Optional[float] = Field(None)
    openNotional: Optional[float] = Field(None)
    closeNotional: Optional[float] = Field(None)
    closeNotionalPosition: Optional[float] = Field(None)
    closeNotionalTrade: Optional[float] = Field(None)
    closeNotionalBaseCurrency: Optional[float] = Field(None)
    closeNotionalMainRiskFactor: Optional[float] = Field(None)
    closeNotionalFundCurrency: Optional[float] = Field(None)
    tradeLongQuantity: Optional[float] = Field(None)
    tradeShortQuantity: Optional[float] = Field(None)
    openQuantity: Optional[float] = Field(None)
    closeQuantity: Optional[float] = Field(None)
    tradeLongNotional: Optional[float] = Field(None)
    tradeShortNotional: Optional[float] = Field(None)
    deltaBs: Optional[float] = Field(None)
    gammaBs: Optional[float] = Field(None)
    deltaSmile: Optional[float] = Field(None)
    gammaSmile: Optional[float] = Field(None)
    deltaCashMain: Optional[float] = Field(None)
    deltaCashSecondary: Optional[float] = Field(None)
    deltaSecBs: Optional[float] = Field(None)
    gammaSecBs: Optional[float] = Field(None)
    deltaSecSmile: Optional[float] = Field(None)
    gammaSecSmile: Optional[float] = Field(None)
    theta: Optional[float] = Field(None)
    vega: Optional[float] = Field(None)
    fixingDelta: Optional[float] = Field(None)
    riskFactorMain: Optional[str] = Field(None)
    riskFactorMainType: Optional[str] = Field(None)
    riskFactorSecondary: Optional[str] = Field(None)
    riskFactorSecondaryType: Optional[str] = Field(None)
    riskFactorFixing: Optional[str] = Field(None)
    riskFactorFixingType: Optional[str] = Field(None)
    riskFactorCashMain: Optional[str] = Field(None)
    riskFactorCashMainType: Optional[str] = Field(None)
    riskFactorCashSecondary: Optional[str] = Field(None)
    riskFactorCashSecondaryType: Optional[str] = Field(None)
    settleDate: Optional[DateType] = Field(None)
    cashSettleDate: Optional[DateType] = Field(None)
    portfolioName: Optional[str] = Field(None)
    fundName: Optional[str] = Field(None)
    baseFundName: Optional[str] = Field(None)
    tagName: Optional[str] = Field(None)
    instrumentGroupName: Optional[str] = Field(None)
    instrumentName: Optional[str] = Field(None)
    custodianName: Optional[str] = Field(None)
    mesaName: Optional[str] = Field(None)
    hasPnlProblem: Optional[bool] = Field(None)
    hasRiskProblem: Optional[bool] = Field(None)
    hasAnyProblem: Optional[bool] = Field(None)
    problemMessage: Optional[str] = Field(None)
    fxClose: Optional[float] = Field(None)
    baseCurrency: Optional[str] = Field(None)
    fxConsolidatedInstrument: Optional[str] = Field(None)


class PositionDto(BaseModel):
    id: Optional[int] = Field(None)
    isOpen: Optional[bool] = Field(None)
    positionDate: Optional[DateType] = Field(None)
    settleDate: Optional[DateType] = Field(None)
    fundId: Optional[int] = Field(None)
    fundName: Optional[str] = Field(None)
    portfolioId: Optional[int] = Field(None)
    portfolioName: Optional[str] = Field(None)
    instrumentGroupId: Optional[int] = Field(None)
    instrumentGroupName: Optional[str] = Field(None)
    instrumentId: Optional[int] = Field(None)
    instrumentName: Optional[str] = Field(None)
    quantity: Optional[float] = Field(None)
    custodianId: Optional[int] = Field(None)
    custodianName: Optional[str] = Field(None)
    tagId: Optional[int] = Field(None)
    tagName: Optional[str] = Field(None)


class PriceDto(BaseModel):
    date: Optional[DateType] = Field(None)
    typeId: Optional[int] = Field(None)
    typeName: Optional[str] = Field(None)
    sourceId: Optional[int] = Field(None)
    sourceName: Optional[str] = Field(None)
    instrumentGroupId: Optional[int] = Field(None)
    instrumentGroupName: Optional[str] = Field(None)
    instrumentId: Optional[int] = Field(None)
    instrumentName: Optional[str] = Field(None)
    price: Optional[float] = Field(None)


class PriceTypeDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    description: str
    priceOwner: str


class RiskFactorDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    description: str
    riskFactorTypeId: Optional[int] = Field(None)
    riskFactorTypeName: str
    numberOfDimensions: Optional[float] = Field(None)
    characteristics: Optional[Dict[str, str]] = Field(None)


class RiskFactorValueDto(BaseModel):
    id: Optional[int] = Field(None)
    valuationDate: Optional[DateType] = Field(None)
    riskFactorId: Optional[int] = Field(None)
    riskFactorName: str
    riskValueTypeId: Optional[int] = Field(None)
    riskValueTypeName: str
    dimensionOneValue: Optional[float] = Field(None)
    dimensionTwoValue: Optional[float] = Field(None)
    dimensionThreeValue: Optional[float] = Field(None)
    dimensionFourValue: Optional[float] = Field(None)
    dimensionFiveValue: Optional[float] = Field(None)
    value: Optional[float] = Field(None)


class RiskValueTypeDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str


class TradeDto(BaseModel):
    id: Optional[int] = Field(None)
    tradeRawId: Optional[int] = Field(None)
    tradeDate: Optional[DateType] = Field(None)
    tradeTime: Optional[TimeType] = Field(None)
    effectiveDate: Optional[DateType] = Field(None)
    settlementDate: Optional[DateType] = Field(None)
    fundId: Optional[int] = Field(None)
    fundName: Optional[str] = Field(None)
    accountId: Optional[int] = Field(None)
    accountName: Optional[str] = Field(None)
    portfolioId: Optional[int] = Field(None)
    portfolioName: Optional[str] = Field(None)
    instrumentGroupId: Optional[int] = Field(None)
    instrumentGroupName: Optional[str] = Field(None)
    instrumentId: Optional[int] = Field(None)
    instrumentName: Optional[str] = Field(None)
    quantity: Optional[float] = Field(None)
    price: Optional[float] = Field(None)
    traderId: Optional[int] = Field(None)
    traderName: Optional[str] = Field(None)
    dealerId: Optional[int] = Field(None)
    dealerName: Optional[str] = Field(None)
    settleDealerId: Optional[int] = Field(None)
    settleDealerName: Optional[str] = Field(None)
    tagId: Optional[int] = Field(None)
    tagName: Optional[str] = Field(None)
    tradeStateId: Optional[int] = Field(None)
    tradeStateName: Optional[str] = Field(None)
    tradeSourceId: Optional[int] = Field(None)
    tradeSourceName: Optional[str] = Field(None)
    observation: Optional[str] = Field(None)


class OverrideInstrumentPriceRequest(BaseModel):
    instrumentId: int = Field(..., description="The instrument ID to override the price for.")
    price: float = Field(..., description="The new price.")
    rate: float = Field(..., description="The new rate.")


class RiskFactorPoint(BaseModel):
    """The points to override with."""
    riskFactorValue: Optional[float] = Field(None)
    dimensionOne: Optional[float] = Field(None)
    dimensionTwo: Optional[float] = Field(None)
    dimensionThree: Optional[float] = Field(None)
    dimensionFour: Optional[float] = Field(None)
    dimensionFive: Optional[float] = Field(None)


class OverrideRiskFactorValueRequest(BaseModel):
    riskFactorId: Optional[int] = Field(None, description="The ID of the risk factor to be overridden. Use this or the risk factor name.")
    riskFactor: Optional[str] = Field(None, description="The name of the risk factor to be overridden. Use this or the risk factor ID.")
    riskFactorType: str = Field(..., description="The risk factor type name.")
    riskFactorPoint: RiskFactorPoint = Field(..., description="The points to override with.")


class FundCounterpartyMarginDto(BaseModel):
    id: Optional[int] = Field(None)
    sessionDate: str
    notificationDate: str
    coveringDate: str
    fundId: Optional[int] = Field(None)
    fundName: str
    counterpartyId: Optional[int] = Field(None)
    counterpartyName: str
    marginTypeId: Optional[int] = Field(None)
    marginTypeName: str
    currencyId: Optional[int] = Field(None)
    currencyCode: str


class FundRiskMeasureDto(BaseModel):
    id: Optional[int] = Field(None)
    effectiveDate: Optional[str] = Field(None)
    fundId: Optional[int] = Field(None)
    fundName: str
    portfolioId: Optional[int] = Field(None)
    portfolioName: str
    riskMetricId: Optional[int] = Field(None)
    riskMetricName: str
    measureValue: Optional[float] = Field(None)


class FundFamilyDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    description: str
    baseCurrencyId: Optional[int] = Field(None)
    baseCurrencyCode: str
    riskViewCurrencyId: Optional[int] = Field(None)
    riskViewCurrencyCode: str


class FundFamilyRelationDto(BaseModel):
    id: Optional[int] = Field(None)
    fundFamilyId: Optional[int] = Field(None)
    fundFamilyName: str
    fundId: Optional[int] = Field(None)
    fundName: str
    navMultiplier: Optional[float] = Field(None)
    riskMultiplier: Optional[float] = Field(None)


class PortfolioDto(BaseModel):
    id: Optional[int] = Field(None)
    parentPortfolioId: Optional[int] = Field(None)
    name: str
    description: str
    characteristics: Optional[Dict[str, str]] = Field(None)


class SubclassNavDto(BaseModel):
    id: Optional[int] = Field(None)
    date: Optional[DateType] = Field(None)
    subclassNavTypeId: Optional[int] = Field(None)
    subclassNavTypeName: str
    subclassId: Optional[int] = Field(None)
    subclassName: str
    value: Optional[float] = Field(None)


class InstrumentEventDto(BaseModel):
    id: Optional[int] = Field(None)
    instrumentId: Optional[int] = Field(None)
    eventType: Optional[str] = Field(None)
    eventDate: Optional[DateType] = Field(None)
    description: Optional[str] = Field(None)


class PnlExplainDto(BaseModel):
    id: Optional[int] = Field(None)
    portfolioId: Optional[int] = Field(None)
    instrumentId: Optional[int] = Field(None)
    pnl: Optional[float] = Field(None)
    explainDetails: Optional[Dict[str, Any]] = Field(None)


class SubclassDto(BaseModel):
    id: Optional[int] = Field(None)
    name: Optional[str] = Field(None)
    fullName: Optional[str] = Field(None)
    fundClassId: Optional[int] = Field(None)
    fundClassName: str
    transferAgentId: Optional[int] = Field(None)
    transferAgentName: str
    isEnabled: Optional[bool] = Field(None)
    characteristics: Optional[Dict[str, str]] = Field(None)


class TradeFeeDto(BaseModel):
    id: Optional[int] = Field(None)
    effectiveDate: Optional[DateType] = Field(None)
    tradeId: Optional[int] = Field(None)
    executionFee: Optional[float] = Field(None)
    clearingFee: Optional[float] = Field(None)
    exchangeFee: Optional[float] = Field(None)
    registerFee: Optional[float] = Field(None)
    nonPnlFee: Optional[float] = Field(None)
    observation: Optional[str] = Field(None)


class TradeInternalDto(BaseModel):
    id: Optional[int] = Field(None)
    tradeId: Optional[int] = Field(None)
    internalType: Optional[str] = Field(None)
    value: Optional[float] = Field(None)


class IndexDto(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    description: str
    type: str
    currencyId: Optional[int] = Field(None)
    currency: str
    characteristics: Optional[Dict[str, str]] = Field(None)


class PriceModelDto(BaseModel):
    id: Optional[int] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    riskFactorsCount: Optional[int] = Field(None)


class InstrumentPriceModelDto(BaseModel):
    instrumentId: Optional[int] = Field(None)
    instrumentName: str
    id: Optional[int] = Field(None)
    instrumentGroupId: Optional[int] = Field(None)
    instrumentGroupName: str
    priceModelId: Optional[int] = Field(None)
    priceModelName: str
    groupingId: Optional[int] = Field(None)
    groupingName: str
    actionRiskFactors: Optional[Dict[str, str]] = Field(None)


class InstrumentGroupPriceModelDto(BaseModel):
    id: Optional[int] = Field(None)
    instrumentGroupId: Optional[int] = Field(None)
    instrumentGroupName: str
    priceModelId: Optional[int] = Field(None)
    priceModelName: str
    groupingId: Optional[int] = Field(None)
    groupingName: str
    actionRiskFactors: Optional[Dict[str, str]] = Field(None)


class PriceModelInstrumentDto(BaseModel):
    id: Optional[int] = Field(None)
    priceModelId: Optional[int] = Field(None)
    instrumentId: Optional[int] = Field(None)
    details: Optional[Dict[str, Any]] = Field(None)


class PriceModelInstrumentGroupDto(BaseModel):
    id: Optional[int] = Field(None)
    priceModelId: Optional[int] = Field(None)
    instrumentGroupId: Optional[int] = Field(None)
    details: Optional[Dict[str, Any]] = Field(None)


# Update model references for forward references
InstrumentDto.model_rebuild()

