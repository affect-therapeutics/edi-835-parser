import datetime
from edi_835_parser.segments.address import Address
from edi_835_parser.segments.location import Location


def test_transaction_other_payer_identification(sample_835):
	transaction = sample_835.transactions[0]
	assert transaction.other_payer_identification.identification == 'REF'
	assert transaction.other_payer_identification.value == '31048'


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
