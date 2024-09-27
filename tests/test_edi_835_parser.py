from decimal import Decimal

from utils import count_claims, count_transactions, count_services, sum_interests


def test_claim_count(blue_cross_nc_sample, emedny_sample, sample_835):
	assert count_claims(blue_cross_nc_sample) == 1
	assert count_claims(emedny_sample) == 3
	assert count_claims(sample_835) == 6


def test_transaction_count(blue_cross_nc_sample, emedny_sample, sample_835):
	assert count_transactions(blue_cross_nc_sample) == 1
	assert count_transactions(emedny_sample) == 1
	assert count_transactions(sample_835) == 2


def test_service_count(blue_cross_nc_sample, emedny_sample, sample_835):
	assert count_services(blue_cross_nc_sample) == 3
	assert count_services(emedny_sample) == 10
	assert count_services(sample_835) == 12


# test no. of rows for claim level DataFrame
def test_build_remits(blue_cross_nc_sample, emedny_sample, sample_835):
	assert blue_cross_nc_sample.build_remits().shape[0] == 1
	assert emedny_sample.build_remits().shape[0] == 3
	assert sample_835.build_remits().shape[0] == 6


# test no. of rows for transaction level DataFrame
def test_build_payment_fin_info(blue_cross_nc_sample, emedny_sample, sample_835):
	assert blue_cross_nc_sample.build_payment_fin_info().shape[0] == 1
	assert emedny_sample.build_payment_fin_info().shape[0] == 1
	assert sample_835.build_payment_fin_info().shape[0] == 2


# test no. of rows for service level DataFrame
def test_build_remit_service_lines(blue_cross_nc_sample, emedny_sample, sample_835):
	assert blue_cross_nc_sample.build_remit_service_lines().shape[0] == 3
	assert emedny_sample.build_remit_service_lines().shape[0] == 10
	assert sample_835.build_remit_service_lines().shape[0] == 12


def test_total_interests(sample_935_with_interests):
	assert sum_interests(sample_935_with_interests) == round(Decimal(10.3), 2)
