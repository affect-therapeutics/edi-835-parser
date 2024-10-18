from edi_835_parser.elements import Element

contact_communication_number_qualifer = {
	'FX': 'fax',
	'TE': 'phone',
	'EM': 'email',
	'UR': 'url',
	'EX': 'ext',
}


class ContactCommunicationNumberQualifier(Element):
	def parser(self, value: str) -> str:
		return contact_communication_number_qualifer.get(value, value)
