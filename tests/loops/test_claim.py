from utils import count_claims, count_transactions, count_services, get_claim_by_control_number


def test_medicaid_sample(nevada_medicaid_sample):
	assert count_claims(nevada_medicaid_sample) == 3
	assert count_transactions(nevada_medicaid_sample) == 3
	assert count_services(nevada_medicaid_sample) == 0

	claim_loop = get_claim_by_control_number(nevada_medicaid_sample, '77777777')
	assert claim_loop.claim.charge_amount == '72232'


def test_can_parse_a_claim_contact(exhaustive_sample):
	claim_loop = get_claim_by_control_number(exhaustive_sample, 'X')
	assert claim_loop.contacts[0].name == 'XXXXX'
	assert claim_loop.contacts[0].communication_no_or_url_qualifier == 'TE'
	assert claim_loop.contacts[0].communication_no_or_url == 'XXXX'


def test_reader_for_claim_payer_contacts(exhaustive_sample):
	claim_loop = get_claim_by_control_number(exhaustive_sample, 'X')

	assert claim_loop.claim_payer_contact.name == 'XXXXX'
	assert claim_loop.claim_payer_contact.communication_no_or_url_qualifier == 'TE'
	assert claim_loop.claim_payer_contact.communication_no_or_url == 'XXXX'
