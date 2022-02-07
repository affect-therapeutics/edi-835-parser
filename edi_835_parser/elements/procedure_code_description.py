from typing import Optional

from edi_835_parser.elements import Element
from edi_835_parser.elements.utilities import split_element


class ProcedureCodeDescription(Element):

	def parser(self, value: str) -> Optional[str]:
		if value is not None:
			value = split_element(value)
			if len(value) > 6:
				return value[6]
