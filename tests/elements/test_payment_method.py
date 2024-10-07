from edi_835_parser.elements.payment_method import PaymentMethod


class PaymentMethodMock:
	payment_method = PaymentMethod()

	def __init__(self, value):
		self.payment_method = value


def test_payment_method_element():
	mock = PaymentMethodMock('ACH')
	assert mock.payment_method.description == 'Automated Clearing House (ACH)'

	mock = PaymentMethodMock('CHK')
	assert mock.payment_method.description == 'Check'

	mock = PaymentMethodMock('NON')
	assert mock.payment_method.description == 'Non-Payment Data'

	mock = PaymentMethodMock('BOP')
	assert mock.payment_method.description == 'Financial Institution Option'
