from edi_835_parser.segments.payer_contact import PayerContact


def test_payer_contact_initialization():
	segment = '0:PER*CX*XX*FX*XXXXX*FX*XXXXXX*EX*XXX'
	payer_contact = PayerContact(segment)

	assert payer_contact.index == '0'
	assert payer_contact.identifier == 'PER'
	assert payer_contact.code == 'payers_claim_office'
	assert payer_contact.name == 'XX'

	assert payer_contact.communication_no_or_url_qualifier == 'fax'
	assert payer_contact.communication_no_or_url == 'XXXXX'

	assert payer_contact.communication_no_or_url_qualifier_2 == 'fax'
	assert payer_contact.communication_no_or_url_2 == 'XXXXXX'

	assert payer_contact.communication_no_or_url_qualifier_3 == 'EX'
	assert payer_contact.communication_no_ext == 'XXX'


def test_payer_contact_phone_number():
	segment = '0:PER*CX*WESTERN SOUTHERN BENEFITS*TE*5136291100'
	payer_contact = PayerContact(segment)

	assert payer_contact.phone_number == '5136291100'


def test_payer_contact_phone_number_with_ext():
	segment = '0:PER*CX*WESTERN SOUTHERN BENEFITS*TE*5136291100*EX*123*FX*5136291109'
	payer_contact = PayerContact(segment)

	assert payer_contact.phone_number == '5136291100x123'


def test_payer_contact_fax():
	segment = '0:PER*CX*WESTERN SOUTHERN BENEFITS*TE*5136291100*FX*5136291109*EX*123'
	payer_contact = PayerContact(segment)

	assert payer_contact.fax_number == '5136291109x123'


def test_payer_contact_email():
	segment = '0:PER*BL*Nevada Medicaid*TE*8776383472*EM*nvmmis.edisupport@dxc.com'
	payer_contact = PayerContact(segment)

	assert payer_contact.phone_number == '8776383472'
	assert payer_contact.email == 'nvmmis.edisupport@dxc.com'


def test_payer_contact_url():
	segment = '0:PER*BL*PROVIDER SERVICES*TE*8003439000*UR*www.emedny.org'
	payer_contact = PayerContact(segment)

	assert payer_contact.url == 'www.emedny.org'
