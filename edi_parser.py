from edi_835_parser import parse
path = 'input/sample_835.txt'

transaction_set = parse(path)

remits_df = transaction_set.build_remits()
remits_df.to_csv("output/sample_remits_835.txt", sep='|', index=False)

remit_payers_df = transaction_set.build_remit_payers()

remit_payers_df.to_csv("output/sample_payers_835.txt", sep='|', index=False)

remit_fin_info = transaction_set.build_payment_fin_info()
remit_fin_info.to_csv("output/sample_fin_info.txt", sep='|', index=False)

remit_service_lines_df = transaction_set.build_remit_service_lines()

remit_service_lines_df.to_csv("output/sample_remit_service_lines.txt", sep='|', index=False)
