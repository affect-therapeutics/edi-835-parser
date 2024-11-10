import datetime
from edi_835_parser.segments.address import Address
from edi_835_parser.segments.location import Location


def test_transaction_properties(sample_835):
	transaction = sample_835.transactions[0]
	assert transaction.transaction.transaction_set_identifier_code == '835'
	assert transaction.transaction.transaction_set_control_no == '1002'


def test_transaction_address(sample_835):
	transaction = sample_835.transactions[0]
	assert isinstance(transaction.payer_address, Address)
	assert transaction.payer_address.address_line1 == '400 BROADWAY'
	assert isinstance(transaction.payer_location, Location)


def test_transaction_production_date(sample_835):
	transaction = sample_835.transactions[0]
	assert transaction.production_date == datetime.datetime(2022, 1, 5, 0, 0)


def test_transaction_reference_identification_number(sample_835):
	transaction = sample_835.transactions[0]
	assert transaction.reference_identification_number.value == 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


def test_transaction_header_number(sample_835):
	transaction = sample_835.transactions[0]
	assert transaction.header_number.number == 1


def test_payee_identification(sample_835):
	transaction = sample_835.transactions[0]

	assert transaction.payee_identification.value == '204881619'
	assert transaction.payee_identification.qualifier_code == 'TJ'


def test_payee_indentification_with_tax_id_on_n1(sample_835_with_func):
	def modify(content):
		return content.replace(
			'N1*PE*UNIVERSITY HOSPITALS MEDICAL GROUP INC*XX*1669499414~',
			'N1*PE*UNIVERSITY HOSPITALS MEDICAL GROUP INC*FI*130871925~',
		)

	sample_835 = sample_835_with_func(modify)
	transaction = sample_835.transactions[0]

	assert transaction.payee_identification.value == '130871925'
	assert transaction.payee_identification.qualifier_code == 'TJ'
	assert transaction.payee_identification.qualifier == 'federal taxpayer identification number'
