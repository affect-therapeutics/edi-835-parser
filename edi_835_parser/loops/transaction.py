from typing import Iterator, Tuple, Optional, List

from edi_835_parser.loops.claim import Claim as ClaimLoop
from edi_835_parser.loops.organization import Organization as OrganizationLoop
from edi_835_parser.segments.utilities import find_identifier
from edi_835_parser.segments.transaction import Transaction as TransactionSegment
from edi_835_parser.segments.organization import Organization as OrganizationSegment
from edi_835_parser.segments.location import Location as LocationSegment
from edi_835_parser.segments.address import Address as AddressSegment
from edi_835_parser.segments.payer_contact import PayerContact as PayerContactSegment
from edi_835_parser.segments.financial_information import FinancialInformation as FinancialInformationSegment
from edi_835_parser.segments.trace_number import TraceNumber as TraceNumberSegment
from edi_835_parser.segments.reference import Reference as ReferenceSegment
from edi_835_parser.segments.provider_adjustment import ProviderAdjustment as ProviderAdjustmentSegment
from edi_835_parser.segments.provider_summary import ProviderSummary as ProviderSummarySegment

from log_conf import Logger


class Transaction:
    initiating_identifier = TransactionSegment.identification
    terminating_identifiers = [
        TransactionSegment.identification,  # Transaction segment (ST) has to end with an 'SE' segment
        'SE'
    ]

    def __init__(
            self,
            transaction: TransactionSegment = None,
            financial_information: FinancialInformationSegment = None,
            trace_number: TraceNumberSegment = None,
            provider_adjustment: ProviderAdjustmentSegment = None,
            provider_summary: ProviderSummarySegment = None,
            claims: List[ClaimLoop] = None,
            organizations: List[OrganizationLoop] = None
    ):
        self.transaction = transaction
        self.financial_information = financial_information
        self.trace_number = trace_number
        self.provider_adjustment = provider_adjustment
        self.provider_summary = provider_summary
        self.claims = claims if claims else []
        self.organizations = organizations if organizations else []

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    @property
    def payer(self) -> OrganizationSegment:
            payer = [c for c in self.organizations if c.organization.type == 'payer']
            assert len(payer) == 1
            return payer[0].organization

    @property
    def payer_address(self) -> AddressSegment:
            payer = [c for c in self.organizations if c.organization.type == 'payer']
            assert len(payer) == 1
            return payer[0].address

    @property
    def payer_location(self) -> LocationSegment:
            payer = [c for c in self.organizations if c.organization.type == 'payer']
            assert len(payer) == 1
            return payer[0].location

    @property
    def payer_contact_business(self) -> Optional[PayerContactSegment]:
        payer = [c for c in self.organizations if c.organization.type == 'payer']
        assert len(payer) == 1
        contact_business = [a for a in payer[0].contacts if a.code == 'payers_claim_office']
        assert len(contact_business) <= 1
        if len(contact_business) == 1:
            return contact_business[0]

    @property
    def payer_contact_web(self) -> Optional[PayerContactSegment]:
        payer = [c for c in self.organizations if c.organization.type == 'payer']
        assert len(payer) == 1
        contact_web = [a for a in payer[0].contacts if a.code == 'information_contact']
        assert len(contact_web) <= 1
        if len(contact_web) == 1:
            return contact_web[0]

    @property
    def payer_contact_technical(self) -> Optional[PayerContactSegment]:
        payer = [c for c in self.organizations if c.organization.type == 'payer']
        assert len(payer) == 1
        contact_technical = [a for a in payer[0].contacts if a.code == 'technical_contact']
        assert len(contact_technical) <= 1
        if len(contact_technical) == 1:
            return contact_technical[0]


    @property
    def payee(self) -> OrganizationSegment:
            payee = [c for c in self.organizations if c.organization.type == 'payee']
            assert len(payee) == 1
            return payee[0].organization

    @property
    def payee_identification(self) -> Optional[ReferenceSegment]:
        payee_id = [c for c in self.organizations if c.organization.type == 'payee']
        for a in payee_id:
            for ref in a.references:
                if ref.qualifier == 'federal taxpayer identification number':
                    return ref

    @property
    def other_payee_identification(self) -> Optional[ReferenceSegment]:
        payee_id = [c for c in self.organizations if c.organization.type == 'payee' and c.references != []]
        assert len(payee_id) <= 1
        if len(payee_id) == 1:
            for a in payee_id:
                for ref in a.references:
                    if ref.qualifier == 'payee identification':
                        return ref

    @property
    def payer_identification(self) -> Optional[ReferenceSegment]:
        payer_id = [c for c in self.organizations if c.organization.type == 'payer' and c.references != []]
        assert len(payer_id) <= 1
        if len(payer_id) == 1:
            for a in payer_id:
                for ref in a.references:
                    return ref

    @classmethod
    def build(cls, segment: str, segments: Iterator[str]) -> Tuple['Transaction', Optional[Iterator[str]], Optional[str]]:
        transaction = Transaction()
        transaction.transaction = TransactionSegment(segment)

        segment = segments.__next__()
        while True:
            try:
                if segment is None:
                    segment = segments.__next__()

                identifier = find_identifier(segment)

                if identifier == ClaimLoop.initiating_identifier:
                    claim, segments, segment = ClaimLoop.build(segment, segments)
                    transaction.claims.append(claim)

                elif identifier == OrganizationLoop.initiating_identifier:
                    organization, segments, segment = OrganizationLoop.build(segment, segments)
                    transaction.organizations.append(organization)

                elif identifier == FinancialInformationSegment.identification:
                    financial_information = FinancialInformationSegment(segment)
                    transaction.financial_information = financial_information
                    segment = None

                elif identifier == TraceNumberSegment.identification:
                    trace_number = TraceNumberSegment(segment)
                    transaction.trace_number = trace_number
                    segment = None

                elif identifier == ProviderAdjustmentSegment.identification:
                    provider_adjustment = ProviderAdjustmentSegment(segment)
                    transaction.provider_adjustment = provider_adjustment
                    segment = None

                elif identifier == ProviderSummarySegment.identification:
                    provider_summary = ProviderSummarySegment(segment)
                    transaction.provider_summary = provider_summary
                    segment = None

                elif identifier in cls.terminating_identifiers:
                    return transaction, segments, segment

                else:
                    segment = None
                    message = f'Identifier: {identifier} not handled in transaction loop.'
                    Logger.logr.warning(message)

            except StopIteration:
                return transaction, None, None



