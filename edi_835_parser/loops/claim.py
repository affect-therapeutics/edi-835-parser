from typing import Iterator, Tuple, Optional, List

from edi_835_parser.segments.claim import Claim as ClaimSegment
from edi_835_parser.segments.entity import Entity as EntitySegment
from edi_835_parser.segments.reference import Reference as ReferenceSegment
from edi_835_parser.segments.date import Date as DateSegment
from edi_835_parser.segments.amount import Amount as AmountSegment
from edi_835_parser.segments.utilities import find_identifier
from edi_835_parser.segments.inpatient_adjudication import InpatientAdjudication as InpatientAdjudicationSegment
from edi_835_parser.segments.outpatient_adjudication import OutpatientAdjudication as OutpatientAdjudicationSegment
from edi_835_parser.segments.provider_adjustment import ProviderAdjustment as ProviderAdjustmentSegment
from edi_835_parser.loops.service import Service as ServiceLoop
from edi_835_parser.segments.adjustment import Adjustment as ClaimAdjustmentSegment


from log_conf import Logger


class Claim:
	initiating_identifier = ClaimSegment.identification
	terminating_identifiers = [
		ClaimSegment.identification, ProviderAdjustmentSegment.identification,
		'SE'
	]

	def __init__(
			self,
			claim: ClaimSegment = None,
			entities: List[EntitySegment] = None,
			services: List[ServiceLoop] = None,
			references: List[ReferenceSegment] = None,
			dates: List[DateSegment] = None,
			amount: AmountSegment = None,
			inpatient: InpatientAdjudicationSegment = None,
			outpatient: OutpatientAdjudicationSegment = None,
			adjustment: ClaimAdjustmentSegment = None
	):
		self.claim = claim
		self.entities = entities if entities else []
		self.services = services if services else []
		self.references = references if references else []
		self.dates = dates if dates else []
		self.amount = amount
		self.inpatient = inpatient
		self.outpatient = outpatient
		self.adjustment = adjustment

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())

	@property
	def rendering_provider(self) -> Optional[EntitySegment]:
		rendering_provider = [e for e in self.entities if e.entity == 'rendering provider']
		assert len(rendering_provider) <= 1

		if len(rendering_provider) == 1:
			return rendering_provider[0]

	@property
	def insured(self) -> Optional[EntitySegment]:
		insured = [e for e in self.entities if e.entity == 'insured']
		assert len(insured) <= 1

		if len(insured) == 1:
			return insured[0]

	@property
	def subscriber(self) -> Optional[EntitySegment]:
		subscriber = [e for e in self.entities if e.entity == 'subscriber']
		assert len(subscriber) <= 1

		if len(subscriber) == 1:
			return subscriber[0]



	@property
	def claim_statement_period_start(self) -> Optional[DateSegment]:
		statement_period_start = [d for d in self.dates if d.qualifier == 'claim statement period start']
		assert len(statement_period_start) <= 1

		if len(statement_period_start) == 1:
			return statement_period_start[0]

	@property
	def claim_statement_period_end(self) -> Optional[DateSegment]:
		statement_period_end = [d for d in self.dates if d.qualifier == 'claim statement period end']
		assert len(statement_period_end) <= 1

		if len(statement_period_end) == 1:
			return statement_period_end[0]

	@property
	def claim_received_date(self) -> Optional[DateSegment]:
		claim_received = [d for d in self.dates if d.qualifier == 'received']
		assert len(claim_received) <= 1

		if len(claim_received) == 1:
			return claim_received[0]


	@property
	def claim_coverage_expiration(self) -> Optional[DateSegment]:
		coverage_expiration = [d for d in self.dates if d.qualifier == 'expiration']
		assert len(coverage_expiration) <= 1

		if len(coverage_expiration) == 1:
			return coverage_expiration[0]

	@property
	def claim_contract_code(self) -> Optional[ReferenceSegment]:
		contract_code = [r for r in self.references if r.qualifier == 'contract code']
		if len(contract_code) >= 1:
			return contract_code[0]

	@property
	def patient(self) -> EntitySegment:
		patient = [e for e in self.entities if e.entity == 'patient']
		assert len(patient) == 1

		return patient[0]

	@classmethod
	def build(cls, segment: str, segments: Iterator[str]) -> Tuple['Claim', Optional[Iterator[str]], Optional[str]]:
		claim = Claim()
		claim.claim = ClaimSegment(segment)

		segment = segments.__next__()
		while True:
			try:
				if segment is None:
					segment = segments.__next__()

				identifier = find_identifier(segment)

				if identifier == ServiceLoop.initiating_identifier:
					service, segment, segments = ServiceLoop.build(segment, segments)
					claim.services.append(service)

				elif identifier == EntitySegment.identification:
					entity = EntitySegment(segment)
					claim.entities.append(entity)
					segment = None

				elif identifier == ReferenceSegment.identification:
					reference = ReferenceSegment(segment)
					claim.references.append(reference)
					segment = None

				elif identifier == DateSegment.identification:
					date = DateSegment(segment)
					claim.dates.append(date)
					segment = None

				elif identifier == AmountSegment.identification:
					amount = AmountSegment(segment)
					claim.amount = amount
					segment = None

				elif identifier == InpatientAdjudicationSegment.identification:
					inpatient = InpatientAdjudicationSegment(segment)
					claim.inpatient = inpatient
					segment = None

				elif identifier == OutpatientAdjudicationSegment.identification:
					outpatient = OutpatientAdjudicationSegment(segment)
					claim.outpatient = outpatient
					segment = None

				elif identifier == ClaimAdjustmentSegment.identification:
					adjustment = ClaimAdjustmentSegment(segment)
					claim.adjustment = adjustment
					segment = None

				elif identifier in cls.terminating_identifiers:
					return claim, segments, segment

				else:
					segment = None
					message = f'Identifier: {identifier} not handled in claim loop.'
					Logger.logr.warning(message)

			except StopIteration:
				return claim, None, None
