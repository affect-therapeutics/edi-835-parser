from edi_835_parser.elements import Element
from edi_835_parser.elements.utilities import split_element


class ProviderAdjustmentID(Element):

	def parser(self, value: str) -> str:
		if value is not None:
			value = split_element(value)
			if len(value) > 1:
				return value[1]
