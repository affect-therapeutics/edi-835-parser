from edi_835_parser.elements import Element

codes = {
	'01': 'ABA Transit Routing Number Including Check Digits (9 digits)',
	'02': 'Swift Identification (8 or 11 characters)',
	'03': 'CHIPS (3 or 4 digits)',
	'04': 'Canadian Bank Branch and Institution Number',
	'ZZ': 'Mutually Defined',
}


class DfiIdNumberQualifier(Element):
	def parser(self, value: str) -> str:
		value = value.strip()
		return codes.get(value, value)
