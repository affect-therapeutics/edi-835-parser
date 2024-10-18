from edi_835_parser.elements.claim_status import ClaimStatus, PayerClassification


class ClaimMock:
	claim_status = ClaimStatus()

	def __init__(self, value):
		self.claim_status = value


def test_claim_status_element():
	mock = ClaimMock('1')
	assert mock.claim_status.description == 'processed as primary'
	assert mock.claim_status.payer_classification == PayerClassification.PRIMARY
	assert mock.claim_status.code == '1'


def test_if_status_not_found():
	mock = ClaimMock('999')
	assert mock.claim_status.description == 'uncategorized'
	assert mock.claim_status.payer_classification == PayerClassification.UNKNOWN
	assert mock.claim_status.code == '999'
