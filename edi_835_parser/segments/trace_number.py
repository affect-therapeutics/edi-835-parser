from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.segments.utilities import split_segment, get_element


class TraceNumber:
    identification = 'TRN'

    identifier = Identifier()

    def __init__(self, segment: str):
        self.index = segment.split(':', 1)[0]
        segment = segment.split(':', 1)[1]

        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.type_code = segment[1]
        self.ref_identification = segment[2]
        self.origin_company_identifier = segment[3]
        self.origin_company_supplemental_code = get_element(segment, 4)
