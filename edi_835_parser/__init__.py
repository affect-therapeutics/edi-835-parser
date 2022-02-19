import os
from typing import List

from edi_835_parser.transaction_set.transaction_set import TransactionSet

from log_conf import Logger


def parse(path: str, debug: bool=False) -> TransactionSet:
	if path[0] == '~':
		path = os.path.expanduser(path)

	if os.path.isdir(path):
		transaction_set = None
		files = find_edi_835_files(path)
		for file in files:
			file_path = f'{path}/{file}'
			if debug:
				transaction_set = TransactionSet.build(file_path)
			else:
				try:
					transaction_set = TransactionSet.build(file_path)
				except:
					Logger.logr.error(f'Failed to build a transaction set from {file_path}')
	else:
		transaction_set = TransactionSet.build(path)

	return transaction_set


def find_edi_835_files(path: str) -> List[str]:
	files = []
	for file in os.listdir(path):
		files.append(file)

	return files


if __name__ == '__main__':
	pass