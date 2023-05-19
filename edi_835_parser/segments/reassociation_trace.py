from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.reference_qualifier import ReferenceQualifier
from edi_835_parser.segments.utilities import split_segment, get_element


#
# TRN01 'Trace Type Code'
# TRN02 'Check or EFT Trace Number'
# TRN03 'Payer Identifier'
# TRN04 'Originating Company Co Supplemental Code'

class ReassociationTrace:
  identification = 'TRN'

  identifier = Identifier()

  def __init__(self, segment: str):
    self.segment = segment
    segment = split_segment(segment)

    self.identifier = segment[0]
    self.trace_type_code = get_element(segment, 1)
    self.check_or_eft_trace_number = get_element(segment, 2)
    self.payer_identifier = get_element(segment, 3)
    self.originating_company_co_supplemental_code = get_element(segment, 4)

  def __repr__(self) -> str:
    return '\n'.join(str(item) for item in self.__dict__.items())

  def __str__(self) -> str:
    return f'{self.qualifier}: {self.value}'


if __name__ == '__main__':
  pass
