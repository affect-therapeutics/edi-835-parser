from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.integer import Integer
from edi_835_parser.elements.claim_status import ClaimStatus
from edi_835_parser.segments.utilities import split_segment, get_element


class Claim:
	identification = 'CLP'

	identifier = Identifier()
	index = Integer()
	status = ClaimStatus()

	def __init__(self, segment: str):
		self.index = segment.split(':', 1)[0]
		self.key = str(self.index + 1)
		segment = segment.split(':', 1)[1]

		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.patient_control_number = segment[1]
		self.status = segment[2]
		self.charge_amount = segment[3]
		self.paid_amount = segment[4]
		self.patient_responsibility_amount = get_element(segment, 5)
		self.claim_filing_indicator_code = get_element(segment, 6)
		self.payer_claim_control_number = get_element(segment, 7)
		self.facility_type_code = get_element(segment, 8)
		self.claim_frequency_code = get_element(segment, 9)
		self.drg_code = get_element(segment, 11)


	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
