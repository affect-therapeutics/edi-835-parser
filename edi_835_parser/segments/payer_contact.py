from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.contact_function_code import ContactFunctionCode
from edi_835_parser.segments.utilities import split_segment, get_element


class PayerContact:
    identification = 'PER'

    identifier = Identifier()
    code = ContactFunctionCode()

    def __init__(self, segment: str):
        self.index = segment.split(':')[0]
        segment = segment.split(':')[1]

        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.code = segment[1]
        self.name = get_element(segment, 2)
        self.communication_no_or_url_qualifier = get_element(segment, 3)
        self.communication_no_or_url = get_element(segment, 4)

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
    pass
