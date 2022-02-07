from typing import Optional

from edi_835_parser.elements import Element
from edi_835_parser.elements.utilities import split_element


class ServiceModifier4(Element):

	def parser(self, value: str) -> Optional[str]:
		if value is not None:
			value = split_element(value)
			if len(value) > 5:
				return value[5]
