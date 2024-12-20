from typing import Optional

from edi_835_parser.elements import Element


class Dollars(Element):
	def parser(self, value: str) -> Optional[float]:
		if value != '' and value is not None:
			return float(value)
