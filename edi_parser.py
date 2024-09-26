from edi_835_parser import parse
from edi_835_parser import find_edi_835_files
from edi_835_parser.log_conf import Logger


input_dir = 'input'
output_dir = 'output/remits_poc'


files = find_edi_835_files(input_dir)

for file in files:
	file_path = f'{input_dir}/{file}'
	transaction_set = parse(file_path)

	remits_df = transaction_set.build_remits()
	remits_df.insert(1, 'file_name', file, False)
	Logger.logr.info(f'Writing remits DataFrame for {file} to CSV')
	remits_df.to_csv(f'{output_dir}/remits/{file}', sep='|', index=False)

	remit_payers_df = transaction_set.build_remit_payers()
	remit_payers_df.insert(1, 'file_name', file, False)
	Logger.logr.info('Writing remit_payers DataFrame to CSV')
	remit_payers_df.to_csv(f'{output_dir}/remit_payers/{file}', sep='|', index=False)

	remit_fin_info_df = transaction_set.build_payment_fin_info()
	remit_fin_info_df.insert(0, 'file_name', file, False)
	Logger.logr.info('Writing remit_fin_info DataFrame to CSV')
	remit_fin_info_df.to_csv(f'{output_dir}/payment_financial_info/{file}', sep='|', index=False)

	remit_service_lines_df = transaction_set.build_remit_service_lines()
	remit_service_lines_df.insert(2, 'file_name', file, False)
	Logger.logr.info('Writing remit_service_lines DataFrame to CSV')
	remit_service_lines_df.to_csv(f'{output_dir}/remit_service_lines/{file}', sep='|', index=False)

	remit_adjustments_df = transaction_set.build_remit_adjustments()
	remit_adjustments_df.insert(0, 'file_name', file, False)
	Logger.logr.info('Writing remit_adjustments DataFrame to CSV')
	remit_adjustments_df.to_csv(f'{output_dir}/remit_adjustments/{file}', sep='|', index=False)

	remit_remarks_adjudications_df = transaction_set.build_remit_remarks_adjudications()
	remit_remarks_adjudications_df.insert(1, 'file_name', file, False)
	Logger.logr.info('Writing remit_remarks_adjudications_df to CSV')
	remit_remarks_adjudications_df.to_csv(
		f'{output_dir}/remit_remarks_adjudications/{file}', sep='|', index=False
	)

	provider_adjustments_df = transaction_set.build_provider_adjustments()
	provider_adjustments_df.insert(0, 'file_name', file, False)
	Logger.logr.info('Writing provider_adjustments_df to CSV')
	provider_adjustments_df.to_csv(
		f'{output_dir}/provider_adjustments/{file}', sep='|', index=False
	)

	service_line_adjustment_df = transaction_set.build_service_line_adjustments()
	service_line_adjustment_df.insert(0, 'file_name', file, False)
	Logger.logr.info('Writing service_line_adjustment_df to CSV')
	service_line_adjustment_df.to_csv(
		f'{output_dir}/service_line_adjustments/{file}', sep='|', index=False
	)

	service_line_remarks_df = transaction_set.build_service_line_remarks()
	if len(service_line_remarks_df) > 0 and service_line_remarks_df.isnull().values.any():
		service_line_remarks_df.insert(0, 'file_name', file, False)
	else:
		service_line_remarks_df['file_name'] = ''
	Logger.logr.info('Writing service_line_remarks_df to CSV')
	service_line_remarks_df.to_csv(
		f'{output_dir}/service_line_remarks/{file}', sep='|', index=False
	)
	#
	service_line_rendering_providers_df = transaction_set.build_service_line_rendering_providers()
	if (
		len(service_line_rendering_providers_df) > 0
		and service_line_rendering_providers_df.isnull().values.any()
	):
		service_line_rendering_providers_df.insert(0, 'file_name', file, False)
	else:
		service_line_rendering_providers_df['file_name'] = ''
	Logger.logr.info('Writing service_line_rendering_providers_df to CSV')
	service_line_rendering_providers_df.to_csv(
		f'{output_dir}/service_line_rendering_providers/{file}', sep='|', index=False
	)
