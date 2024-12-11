from edi_835_parser.elements.service_code import ServiceCode


class ServiceCodeMock:
	code = ServiceCode()

	def __init__(self, value):
		self.code = value


def test_ignores_sub_elements():
	mock = ServiceCodeMock('HC:99213:GT')
	assert mock.code == '99213'


def test_handles_none():
	mock = ServiceCodeMock(None)
	assert mock.code is None
