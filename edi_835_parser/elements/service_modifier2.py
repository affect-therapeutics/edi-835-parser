from typing import Optional

from edi_835_parser.elements import Element
from edi_835_parser.elements.utilities import split_element


class ServiceModifier2(Element):

	def parser(self, value: str) -> Optional[str]:
		if value is not None:
			value = split_element(value)
			if len(value) > 3:
				return value[3]
