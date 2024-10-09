from edi_835_parser.elements import Element

# https://www.stedi.com/edi/x12/element/1032
claim_types = {
}


class ClaimType(Element):

    def parser(self, value: str) -> str:
        return claim_types.get(value, value)
