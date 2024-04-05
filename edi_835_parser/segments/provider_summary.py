from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.segments.utilities import split_segment, get_element


class ProviderSummary:
	identification = 'TS3'

	identifier = Identifier()

	def __init__(self, segment: str):
		self.index = segment.split(':', 1)[0]
		segment = segment.split(':', 1)[1]
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.facility_type_code = get_element(segment, 2)

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass