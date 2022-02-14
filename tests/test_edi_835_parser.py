from tests.conftest import current_path


def test_claim_count(
		blue_cross_nc_sample,
		emedny_sample,
		sample_835,
		sample2_835,
		sample3_835
):
	assert blue_cross_nc_sample.count_claims() == 1
	assert emedny_sample.count_claims() == 3
	assert sample_835.count_claims() == 6
	assert sample2_835.count_claims() == 50
	assert sample3_835.count_claims() == 115


def test_transaction_count(
		blue_cross_nc_sample,
		emedny_sample,
		sample_835,
		sample2_835,
		sample3_835
):
	assert blue_cross_nc_sample.count_transactions() == 1
	assert emedny_sample.count_transactions() == 1
	assert sample_835.count_transactions() == 2
	assert sample2_835.count_transactions() == 1
	assert sample3_835.count_transactions() == 3


def test_service_count(
		blue_cross_nc_sample,
		emedny_sample,
		sample_835,
		sample2_835,
		sample3_835
):
	assert blue_cross_nc_sample.count_services() == 3
	assert emedny_sample.count_services() == 10
	assert sample_835.count_services() == 12
	assert sample2_835.count_services() == 282
	assert sample3_835.count_services() == 223


# test no. of rows for claim level DataFrame
def test_build_remits(
		blue_cross_nc_sample,
		emedny_sample,
		sample_835,
		sample2_835,
		sample3_835
):
	assert blue_cross_nc_sample.build_remits().shape[0] == 1
	assert emedny_sample.build_remits().shape[0] == 3
	assert sample_835.build_remits().shape[0] == 6
	assert sample2_835.build_remits().shape[0] == 50
	assert sample3_835.build_remits().shape[0] == 115


# test no. of rows for transaction level DataFrame
def test_build_payment_fin_info(
		blue_cross_nc_sample,
		emedny_sample,
		sample_835,
		sample2_835,
		sample3_835
):
	assert blue_cross_nc_sample.build_payment_fin_info().shape[0] == 1
	assert emedny_sample.build_payment_fin_info().shape[0] == 1
	assert sample_835.build_payment_fin_info().shape[0] == 2
	assert sample2_835.build_payment_fin_info().shape[0] == 1
	assert sample3_835.build_payment_fin_info().shape[0] == 3


# test no. of rows for service level DataFrame
def test_build_remit_service_lines(
		blue_cross_nc_sample,
		emedny_sample,
		sample_835,
		sample2_835,
		sample3_835
):
	assert blue_cross_nc_sample.build_remit_service_lines().shape[0] == 3
	assert emedny_sample.build_remit_service_lines().shape[0] == 10
	assert sample_835.build_remit_service_lines().shape[0] == 12
	assert sample2_835.build_remit_service_lines().shape[0] == 282
	assert sample3_835.build_remit_service_lines().shape[0] == 223

