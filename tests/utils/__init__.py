from decimal import Decimal


def count_claims(transaction_set) -> int:
	count = 0
	for transaction in transaction_set.transactions:
		count += len(transaction.claims)
	return count


def count_transactions(transaction_set) -> int:
	count = 0
	count += len(transaction_set.transactions)

	return count


def count_services(transaction_set) -> int:
	count = 0
	for transaction in transaction_set.transactions:
		for claim in transaction.claims:
			count += len(claim.services)

	return count


def sum_interests(transaction_set):
	total_interest = 0
	for transaction in transaction_set.transactions:
		for claim in transaction.claims:
			for amount in claim.amounts:
				if amount.qualifier == 'I':
					total_interest += Decimal(amount.amount)

	return total_interest


def get_claim_by_control_number(transaction_set, claim_id):
	for transaction in transaction_set.transactions:
		for claim in transaction.claims:
			if claim.claim.patient_control_number == claim_id:
				return claim

	assert False, f'Claim with ID {claim_id} not found'
