from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.entity_code import EntityCode
from edi_835_parser.elements.entity_type import EntityType
from edi_835_parser.segments.utilities import split_segment, get_element


class Entity:
	identification = 'NM1'

	identifier = Identifier()
	entity = EntityCode()
	type = EntityType()

	def __init__(self, segment: str):
		self.index = segment.split(':', 1)[0]
		segment = segment.split(':', 1)[1]

		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.entity = segment[1]
		self.entity_code = segment[1]
		self.type = segment[2]
		self.type_code = segment[2]
		self.last_name = get_element(segment, 3)
		self.first_name = get_element(segment, 4)
		self.middle_name = get_element(segment, 5)
		self.name_suffix = get_element(segment, 7)
		self.name_prefix = get_element(segment, 6)
		self.identification_code_qualifier = get_element(segment, 8)
		self.identification_code = get_element(segment, 9)
		self.patient_relationship = get_element(segment, 10)

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())

	@property
	def name(self) -> str:
		return f'{self.first_name} {self.last_name}'.strip().upper()


if __name__ == '__main__':
	pass
