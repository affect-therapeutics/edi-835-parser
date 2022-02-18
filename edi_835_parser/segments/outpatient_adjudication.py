from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.segments.utilities import split_segment, get_element


class OutpatientAdjudication:
	identification = 'MOA'

	identifier = Identifier()

	def __init__(self, segment: str):
		self.index = segment.split(':', 1)[0]
		segment = segment.split(':', 1)[1]

		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.reimbursement_rate = segment[1],
		self.claim_hcpcs_payment_amount = segment[2]
		self.remark_code1 = get_element(segment, 3)
		self.remark_code2 = get_element(segment, 4)
		self.remark_code3 = get_element(segment, 5)
		self.remark_code4 = get_element(segment, 6)
		self.remark_code5 = get_element(segment, 7)
		self.claim_esrd_payment_amount = get_element(segment, 8)
		self.non_payable_professional_component_amount = get_element(segment, 9)

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
