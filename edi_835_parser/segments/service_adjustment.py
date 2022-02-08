from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.dollars import Dollars
# from edi_835_parser.elements.adjustment_group_code import AdjustmentGroupCode
# from edi_835_parser.elements.adjustment_reason_code import AdjustmentReasonCode
from edi_835_parser.segments.utilities import split_segment, get_element


class ServiceAdjustment:
	identification = 'CAS'

	identifier = Identifier()
	# group_code = AdjustmentGroupCode()
	# reason_code = AdjustmentReasonCode()
	amount = Dollars()

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.group_code = segment[1]
		self.reason_code = segment[2]
		self.amount = segment[3]
		self.quantity = get_element(segment, 4)

		if len(self.segment) > 5:
			self.reason_code2 = get_element(segment, 5)
			self.amount2 = get_element(segment, 6)
			self.quantity2 = get_element(segment, 7)
			self.reason_code3 = get_element(segment, 8)
			self.amount3 = get_element(segment, 9)
			self.quantity3 = get_element(segment, 10)
			self.reason_code4 = get_element(segment, 11)
			self.amount4 = get_element(segment, 12)
			self.quantity4 = get_element(segment, 13)
			self.reason_code5 = get_element(segment, 14)
			self.amount5 = get_element(segment, 15)
			self.quantity5 = get_element(segment, 16)
			self.reason_code6 = get_element(segment, 17)
			self.amount6 = get_element(segment, 18)
			self.quantity6 = get_element(segment, 19)

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
