from typing import Iterator, Tuple, Optional, List
from warnings import warn


from edi_835_parser.segments.organization import Organization as OrganizationSegment
from edi_835_parser.segments.claim import Claim as ClaimSegment
from edi_835_parser.segments.address import Address as AddressSegment
from edi_835_parser.segments.location import Location as LocationSegment
from edi_835_parser.segments.payer_contact import PayerContact as PayerContactSegment
from edi_835_parser.segments.utilities import find_identifier


class Organization:
	initiating_identifier = OrganizationSegment.identification
	terminating_identifiers = [
		ClaimSegment.identification,
		OrganizationSegment.identification,
		'SE'
	]

	def __init__(self, organization: OrganizationSegment = None, location: LocationSegment = None,
						address: AddressSegment = None, contacts: List[PayerContactSegment] = None):
		self.organization = organization
		self.location = location
		self.address = address
		self.contacts = contacts if contacts else []

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


	@classmethod
	def build(cls, current_segment: str, segments: Iterator[str]) -> Tuple[
		'OrganizationSegment', Optional[Iterator[str]], Optional[str]]:

		organization = Organization()
		organization.organization = OrganizationSegment(current_segment)

		segment = segments.__next__()
		while True:
			try:
				if segment is None:
					segment = segments.__next__()

				identifier = find_identifier(segment)

				if identifier == AddressSegment.identification:
					organization.address = AddressSegment(segment)
					segment = None

				elif identifier == LocationSegment.identification:
					organization.location = LocationSegment(segment)
					segment = None

				elif identifier == PayerContactSegment.identification:
					contact = PayerContactSegment(segment)
					organization.contacts.append(contact)
					segment = None

				elif identifier in cls.terminating_identifiers:
					return organization, segments, segment

				else:
					segment = None
					message = f'Identifier: {identifier} not handled in organization loop.'
					warn(message)

			except StopIteration:
				return organization, None, None


if __name__ == '__main__':
	pass