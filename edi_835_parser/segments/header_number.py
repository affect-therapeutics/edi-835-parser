from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.integer import Integer
from edi_835_parser.segments.utilities import split_segment


class HeaderNumber:
	identification = 'LX'

	identifier = Identifier()
	number = Integer()

	def __init__(self, segment: str):
		self.index = segment.split(':', 1)[0]
		segment = segment.split(':', 1)[1]

		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.number = segment[1]

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
