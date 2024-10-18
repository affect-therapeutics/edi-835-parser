from edi_835_parser.elements.contact_communication_number_qualifier import (
	ContactCommunicationNumberQualifier,
)
from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.contact_function_code import ContactFunctionCode
from edi_835_parser.segments.utilities import split_segment, get_element


class PayerContact:
	identification = 'PER'

	identifier = Identifier()
	code = ContactFunctionCode()
	communication_no_or_url_qualifier = ContactCommunicationNumberQualifier()
	communication_no_or_url_qualifier_2 = ContactCommunicationNumberQualifier()
	communication_no_or_url_qualifier_3 = ContactCommunicationNumberQualifier()

	def __init__(self, segment: str):
		self.index = segment.split(':', 1)[0]
		segment = segment.split(':', 1)[1]

		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.code = segment[1]
		self.name = get_element(segment, 2)

		self.communication_no_or_url_qualifier = get_element(segment, 3)
		self.communication_no_or_url = get_element(segment, 4)
		self.communication_no_or_url_qualifier_2 = get_element(segment, 5)
		self.communication_no_or_url_2 = get_element(segment, 6)
		self.communication_no_or_url_qualifier_3 = get_element(segment, 7)
		self.communication_no_or_url_3 = get_element(segment, 8)

		self._comm_groups = [
			(self.communication_no_or_url_qualifier, self.communication_no_or_url),
			(self.communication_no_or_url_qualifier_2, self.communication_no_or_url_2),
			(self.communication_no_or_url_qualifier_3, self.communication_no_or_url_3),
		]

	@property
	def phone_number(self):
		num = ''
		ext = ''
		for i, (qualifier, number) in enumerate(self._comm_groups):
			if qualifier == 'phone':
				num = number
				if i + 1 < len(self._comm_groups) and self._comm_groups[i + 1][0] == 'ext':
					ext = self._comm_groups[i + 1][1]
					break

		if ext:
			return f'{num}x{ext}'
		return num

	@property
	def fax_number(self):
		qualifier = 'fax'
		num = ''
		ext = ''
		for i, (q, number) in enumerate(self._comm_groups):
			if q == qualifier:
				num = number
				# Check if the next qualifer is 'ext'
				if i + 1 < len(self._comm_groups) and self._comm_groups[i + 1][0] == 'ext':
					ext = self._comm_groups[i + 1][1]
					break

		if ext:
			return f'{num}x{ext}'
		return num

	@property
	def email(self):
		for qualifier, email in self._comm_groups:
			if qualifier == 'email':
				return email

	@property
	def url(self):
		for qualifier, url in self._comm_groups:
			if qualifier == 'url':
				return url

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
