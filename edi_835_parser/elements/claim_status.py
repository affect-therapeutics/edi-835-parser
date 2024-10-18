from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from warnings import warn


from edi_835_parser.elements import Element


class PayerClassification(Enum):
	PRIMARY = auto()
	SECONDARY = auto()
	TERTIARY = auto()
	UNSPECIFIED = auto()
	UNKNOWN = auto()

	def __str__(self) -> str:
		return str(self.name).lower()


@dataclass
class Status:
	"""
	Attributes:

	- code (:class:`str`): The code provided in the EDI 835 file.
	- description (:class:`str`): The description of the code per `stedi <https://www.stedi.com/edi/x12/segment/CLP>`_.
	- payer_classification (:class:`PayerClassification`)
	- was_forwarded (:class:`bool`): True if the claim was forwarded to an additional payer
	"""

	code: str
	description: str
	payer_classification: PayerClassification
	was_forwarded: bool


_REGISTRY = [
	Status('1', 'processed as primary', PayerClassification.PRIMARY, False),
	Status('2', 'processed as secondary', PayerClassification.SECONDARY, False),
	Status('3', 'processed as tertiary', PayerClassification.TERTIARY, False),
	Status('4', 'denial', PayerClassification.UNSPECIFIED, False),
	Status(
		'19', 'processed as primary, forwarded to additional payer(s)', PayerClassification.PRIMARY, True
	),
	Status(
		'20',
		'processed as secondary, forwarded to additional payer(s)',
		PayerClassification.SECONDARY,
    True,
	),
	Status(
		'21',
		'processed as tertiary, forwarded to additional payer(s)',
		PayerClassification.TERTIARY,
    True,
	),
	Status('22', 'reversal of previous payment', PayerClassification.UNSPECIFIED, False),
]


def _lookup_status(code: str) -> Status:
	status = [s for s in _REGISTRY if s.code == code]
	if len(status) == 0:
		warn(
			f'ClaimStatus: Code {code} does not match a status in the edi-835-parser claim status registry.'
		)
		return Status(
			code=code,
			description='uncategorized',
			payer_classification=PayerClassification.UNKNOWN,
		)

	return status[0]


class ClaimStatus(Element):
	def parser(self, value: str) -> Status:
		return _lookup_status(value)
