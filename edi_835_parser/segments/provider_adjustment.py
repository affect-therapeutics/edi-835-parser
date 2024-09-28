from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.date import Date
from edi_835_parser.segments.utilities import split_segment, get_element
from edi_835_parser.elements.provider_adjustment_id import ProviderAdjustmentID
from edi_835_parser.elements.provider_adjustment_reason_code import ProviderAdjustmentReasonCode


class ProviderAdjustment:
	identification = 'PLB'

	identifier = Identifier()
	fiscal_period_date = Date()
	reason_code1 = ProviderAdjustmentReasonCode()
	reason_code2 = ProviderAdjustmentReasonCode()
	reason_code3 = ProviderAdjustmentReasonCode()
	reason_code4 = ProviderAdjustmentReasonCode()
	reason_code5 = ProviderAdjustmentReasonCode()
	reason_code6 = ProviderAdjustmentReasonCode()
	id1 = ProviderAdjustmentID()
	id2 = ProviderAdjustmentID()
	id3 = ProviderAdjustmentID()
	id4 = ProviderAdjustmentID()
	id5 = ProviderAdjustmentID()
	id6 = ProviderAdjustmentID()

	def __init__(self, segment: str):
		self.index = segment.split(':', 1)[0]
		segment = segment.split(':', 1)[1]

		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.provider_id = segment[1]
		self.fiscal_period_date = segment[2]
		self.reason_code1 = get_element(segment, 3)
		self.id1 = get_element(segment, 3)
		self.amount1 = get_element(segment, 4)
		self.reason_code2 = get_element(segment, 5)
		self.id2 = get_element(segment, 5)
		self.amount2 = get_element(segment, 6)
		self.reason_code3 = get_element(segment, 7)
		self.id3 = get_element(segment, 7)
		self.amount3 = get_element(segment, 8)
		self.reason_code4 = get_element(segment, 9)
		self.id4 = get_element(segment, 9)
		self.amount4 = get_element(segment, 10)
		self.reason_code5 = get_element(segment, 11)
		self.id5 = get_element(segment, 11)
		self.amount5 = get_element(segment, 12)
		self.reason_code6 = get_element(segment, 13)
		self.id6 = get_element(segment, 13)
		self.amount6 = get_element(segment, 14)

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
