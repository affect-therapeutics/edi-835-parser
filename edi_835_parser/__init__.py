import os
from typing import List
from warnings import warn

from edi_835_parser.transaction_set.transaction_set import TransactionSet


def parse(path: str, debug: bool=False) -> TransactionSet:
	if path[0] == '~':
		path = os.path.expanduser(path)

	if os.path.isdir(path):
		transaction_set = None
		files = _find_edi_835_files(path)
		for file in files:
			file_path = f'{path}/{file}'
			if debug:
				transaction_set = TransactionSet.build(file_path)
			else:
				try:
					transaction_set = TransactionSet.build(file_path)
				except:
					warn(f'Failed to build a transaction set from {file_path}')
	else:
		transaction_set = TransactionSet.build(path)

	return transaction_set


def _find_edi_835_files(path: str) -> List[str]:
	files = []
	for file in os.listdir(path):
		if file.endswith('.txt'):
			files.append(file)

	return files


def sum_payments(self) -> float:
	amount = 0
	for transaction_set in self:
		amount += transaction_set.financial_information.amount_paid

	return amount


def count_claims(self) -> int:
	count = 0
	for transaction_set in self:
		count += len(transaction_set.claims)

	return count


def count_patients(self) -> int:
	patients = []
	for transaction_set in self:
		for claim in transaction_set.claims:
			patient = claim.patient
			patients.append(patient.identification_code)

	patients = set(patients)
	return len(patients)


def count_transactions(self) -> int:
	count = 0
	for transaction_set in self:
		count += len(transaction_set.transactions)

	return count


if __name__ == '__main__':
	pass