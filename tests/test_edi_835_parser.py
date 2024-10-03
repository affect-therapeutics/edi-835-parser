from decimal import Decimal
import os
import subprocess

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


def test_cli_output_snapshot():
	OUTPUT_DIR = 'output/remits_poc'
	# List all the files in the output directory recursively
	output_files = [
		f'{OUTPUT_DIR}/{dir}/{file}'
		for dir in os.listdir(OUTPUT_DIR)
		for file in os.listdir(f'{OUTPUT_DIR}/{dir}')
	]
	# Load the contents of each file
	output_file_contents = {file: open(file, 'r').read() for file in output_files}

	# run edi_parser.py
	subprocess.run(['python', 'edi_parser.py'], stdout=subprocess.PIPE).stdout.decode()
	#

	current_output = [
		f'{OUTPUT_DIR}/{dir}/{file}'
		for dir in os.listdir(OUTPUT_DIR)
		for file in os.listdir(f'{OUTPUT_DIR}/{dir}')
	]
	# Load the contents of each file
	current_output_files = {file: open(file, 'r').read() for file in current_output}

	# compare the output
	assert (
		output_file_contents == current_output_files
	), 'Output files have changed run check git for differences'
