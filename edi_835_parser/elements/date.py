from typing import Union
from datetime import datetime
import logging.config
from edi_835_parser.elements import Element

from log_conf import Logger

class Date(Element):

	def parser(self, value: str) -> Union[datetime, str]:
		if len(value) == 10:
			year, month, day, minute, second = [int(value[i:i + 2]) for i in range(0, len(value), 2)]
			return datetime(2000 + year, month, day, minute, second)

		elif len(value) == 8:
			year, month, day = int(value[:4]), int(value[4:6]), int(value[6:])
			return datetime(year, month, day)

		else:
			Logger.logr.warning(f'Unable to parse {value} into a datetime')
			return value
