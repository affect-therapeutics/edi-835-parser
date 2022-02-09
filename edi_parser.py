from edi_835_parser import parse
from edi_835_parser import find_edi_835_files
import os
import logging.config

logging.config.fileConfig(fname='edi_835_parser/logging.conf')
logger = logging.getLogger()


input_dir = 'input'
output_dir = 'output'

files = find_edi_835_files(input_dir)

for file in files:
	file_name = os.path.basename(file).split(".")[0]
	file_extension = os.path.basename(file).split(".")[1]
	file_path = f'{input_dir}/{file}'
	transaction_set = parse(file_path)

	remits_df = transaction_set.build_remits()
	logger.info("Writing remits DataFrame to CSV")
	remits_df.to_csv(f'{output_dir}/{file_name}_remits.{file_extension}', sep='|', index=False)

	remit_payers_df = transaction_set.build_remit_payers()
	logger.info("Writing remit_payers DataFrame to CSV")
	remit_payers_df.to_csv(f'{output_dir}/{file_name}_remit_payers.{file_extension}', sep='|', index=False)

	remit_fin_info = transaction_set.build_payment_fin_info()
	logger.info("Writing remit_fin_info DataFrame to CSV")
	remit_fin_info.to_csv(f'{output_dir}/{file_name}_fin_info.{file_extension}', sep='|', index=False)

	remit_service_lines_df = transaction_set.build_remit_service_lines()
	logger.info("Writing remit_service_lines DataFrame to CSV")
	remit_service_lines_df.to_csv(f'{output_dir}/{file_name}_remit_service_lines.{file_extension}', sep='|', index=False)

	remit_adjustments_df = transaction_set.build_remit_adjustments()
	logger.info("Writing remit_adjustments DataFrame to CSV")
	remit_adjustments_df.to_csv(f'{output_dir}/{file_name}_remit_adjustments.{file_extension}', sep='|', index=False)

	remit_remarks_adjudications_df = transaction_set.build_remit_remarks_adjudications()
	logger.info("Writing remit_remarks_adjudications_df to CSV")
	remit_remarks_adjudications_df.to_csv(f'{output_dir}/{file_name}_remit_remarks_adjudications.{file_extension}',
											sep='|', index=False)

	provider_adjustments_df = transaction_set.build_provider_adjustments()
	logger.info("Writing provider_adjustments_df to CSV")
	provider_adjustments_df.to_csv(f'{output_dir}/{file_name}_provider_adjustments.{file_extension}',
											sep='|', index=False)




