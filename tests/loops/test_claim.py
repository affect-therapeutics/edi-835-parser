from utils import count_claims, count_transactions, count_services, get_claim_by_control_number


def test_medicaid_sample(nevada_medicaid_sample):
	assert count_claims(nevada_medicaid_sample) == 3
	assert count_transactions(nevada_medicaid_sample) == 3
	assert count_services(nevada_medicaid_sample) == 0

	claim_loop = get_claim_by_control_number(nevada_medicaid_sample, '77777777')
	assert claim_loop.claim.charge_amount == '72232'
