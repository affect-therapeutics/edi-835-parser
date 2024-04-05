from edi_835_parser.elements import Element
from edi_835_parser.elements.utilities import split_element


class ProviderAdjustmentReasonCode(Element):

	def parser(self, value: str) -> str:
		if value is not None:
			value = split_element(value)
			reason_code, *_ = value
			return reason_code
