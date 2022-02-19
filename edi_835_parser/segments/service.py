from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.service_code import ServiceCode
from edi_835_parser.elements.service_qualifier import ServiceQualifier
from edi_835_parser.elements.service_modifier1 import ServiceModifier1
from edi_835_parser.elements.service_modifier2 import ServiceModifier2
from edi_835_parser.elements.service_modifier3 import ServiceModifier3
from edi_835_parser.elements.service_modifier4 import ServiceModifier4
from edi_835_parser.elements.procedure_code_description import ProcedureCodeDescription
from edi_835_parser.elements.integer import Integer
from edi_835_parser.segments.utilities import split_segment, get_element


class Service:
	identification = 'SVC'

	identifier = Identifier()
	code = ServiceCode()
	index = Integer()
	procedure_code = ServiceCode()
	qualifier = ServiceQualifier()
	product_qualifier = ServiceQualifier()
	modifier1 = ServiceModifier1()
	modifier2 = ServiceModifier2()
	modifier3 = ServiceModifier3()
	modifier4 = ServiceModifier4()
	procedure_modifier1 = ServiceModifier1()
	procedure_modifier2 = ServiceModifier2()
	procedure_modifier3 = ServiceModifier3()
	procedure_modifier4 = ServiceModifier4()
	code_description = ProcedureCodeDescription()
	allowed_units = Integer()
	billed_units = Integer()

	def __init__(self, segment: str):
		self.index = segment.split(':', 1)[0]
		self.key = str(self.index+1)
		segment = segment.split(':', 1)[1]

		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.code = segment[1]
		self.qualifier = segment[1]
		self.modifier1 = segment[1]
		self.modifier2 = segment[1]
		self.modifier3 = segment[1]
		self.modifier4 = segment[1]
		self.charge_amount = get_element(segment, 2)
		self.paid_amount = get_element(segment, 3)
		self.NUBC_revenue_code = get_element(segment, 4)
		self.adjudicated_line_item_quantity = get_element(segment, 5)
		self.submitted_line_item_quantity = get_element(segment, 7)
		self.product_qualifier = get_element(segment, 6)
		self.procedure_code = get_element(segment, 6)
		self.procedure_modifier1 = get_element(segment, 6)
		self.procedure_modifier2 = get_element(segment, 6)
		self.procedure_modifier3 = get_element(segment, 6)
		self.procedure_modifier4 = get_element(segment, 6)
		self.code_description = get_element(segment, 6)

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
