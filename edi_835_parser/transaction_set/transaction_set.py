from typing import List, Iterator, Optional
from collections import namedtuple

import pandas as pd

from edi_835_parser.loops.claim import Claim as ClaimLoop
from edi_835_parser.loops.transaction import Transaction as TransactionLoop
from edi_835_parser.loops.service import Service as ServiceLoop
from edi_835_parser.loops.organization import Organization as OrganizationLoop
from edi_835_parser.segments.utilities import find_identifier
from edi_835_parser.segments.interchange import Interchange as InterchangeSegment
from edi_835_parser.segments.adjustment import Adjustment as ServiceAdjustmentSegment

from log_conf import Logger

BuildAttributeResponse = namedtuple('BuildAttributeResponse', 'key value segment segments')


class TransactionSet:

	def __init__(
			self,
			interchange: InterchangeSegment,
			transactions: List[TransactionLoop]
	):
		self.interchange = interchange
		self.transactions = transactions

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())

	def build_remits(self) -> pd.DataFrame:
		"""flatten the remittance advice by claim to a pandas DataFrame"""

		Logger.logr.info("Building remits DataFrame")

		remits_data = []

		for transaction in self.transactions:
			for claim in transaction.claims:

				remits_dict = TransactionSet.serialize_claim(claim, transaction)['remits_dict']

				remits_data.append(remits_dict)

		remits_data = pd.DataFrame(remits_data, columns=remits_data[0].keys())

		return remits_data

	def build_remit_payers(self) -> pd.DataFrame:
		"""flatten the remittance advice payers by claim to a pandas DataFrame"""

		Logger.logr.info("Building remits_payers DataFrame")

		remit_payers_data = []

		for transaction in self.transactions:
			for claim in transaction.claims:

				remit_payers_dict = TransactionSet.serialize_claim(claim, transaction)['remit_payers_dict']

				remit_payers_data.append(remit_payers_dict)

		remit_payers_data = pd.DataFrame(remit_payers_data, columns=remit_payers_data[0].keys())

		return remit_payers_data

	def build_payment_fin_info(self) -> pd.DataFrame:
		"""flatten the remittance payment financial info by transaction to a pandas DataFrame"""

		Logger.logr.info("Building payment_fin_info DataFrame")

		remit_financial_info_df = []

		for transaction in self.transactions:

			remit_financial_info_dict = TransactionSet.serialize_transaction(transaction)['remit_financial_info_dict']

			remit_financial_info_df.append(remit_financial_info_dict)

		remit_financial_info_df = pd.DataFrame(remit_financial_info_df, columns=remit_financial_info_df[0].keys())

		return remit_financial_info_df

	def build_remit_service_lines(self) -> pd.DataFrame:
		"""flatten the remittance advice by service lines to a pandas DataFrame"""

		Logger.logr.info("Building remit_service_lines DataFrame")
		remit_service_lines_df = []

		for transaction in self.transactions:
			for claim in transaction.claims:
				for service in claim.services:

					remit_service_lines_dict = TransactionSet.serialize_service(
						transaction, claim, service)['remit_service_lines_dict']

					remit_service_lines_df.append(remit_service_lines_dict)

		remit_service_lines_df = pd.DataFrame(remit_service_lines_df, columns=remit_service_lines_df[0].keys())

		return remit_service_lines_df

	def build_remit_adjustments(self) -> pd.DataFrame:
		"""flatten the remittance advice by service lines to a pandas DataFrame"""

		Logger.logr.info("Building remit_adjustments DataFrame")
		remit_adjustments_data = []

		for transaction in self.transactions:
			for claim in transaction.claims:
				remit_adjustments_dict = TransactionSet.serialize_claim(claim, transaction)['remit_adjustments_dict']
				remit_adjustments_data.append(remit_adjustments_dict)

		remit_adjustments_data = pd.DataFrame(remit_adjustments_data)

		return remit_adjustments_data

	def build_service_line_adjustments(self) -> pd.DataFrame:
		"""flatten the remittance advice by service lines adjustments to a pandas DataFrame"""

		Logger.logr.info("Building remit_adjustments DataFrame")
		service_line_adjustments_data = []

		for transaction in self.transactions:
			for claim in transaction.claims:
				for service in claim.services:
					for adjustment in service.adjustments:
						service_line_adjustments_dict = TransactionSet.serialize_adjustment(
							transaction, claim, service, adjustment)['service_line_adjustments_dict']

						service_line_adjustments_data.append(service_line_adjustments_dict)
		if len(service_line_adjustments_data) < 1:
			service_line_adjustments_data.append({
				'remit_key': None,
				'edi_transaction_id_st02': None,
				'claim_service_line_id': None,
				'remit_service_line_key': None,
				'adjustment_group_code': None,
				'adjustment_reason_code': None,
				'adjustment_amount': None,
				'adjustment_quantity': None,
				'adjustment_reason_code2': None,
				'adjustment_amount2': None,
				'adjustment_quantity2': None,
				'adjustment_reason_code3': None,
				'adjustment_amount3': None,
				'adjustment_quantity3': None,
				'adjustment_reason_code4': None,
				'adjustment_amount4': None,
				'adjustment_quantity4': None,
				'adjustment_reason_code5': None,
				'adjustment_amount5': None,
				'adjustment_quantity5': None,
				'adjustment_reason_code6': None,
				'adjustment_amount6': None,
				'adjustment_quantity6': None,
				'created_at': None
									})

		service_line_adjustments_data = pd.DataFrame(service_line_adjustments_data)

		return service_line_adjustments_data

	def build_service_line_remarks(self) -> pd.DataFrame:
		"""flatten the remittance remarks by service line to a pandas DataFrame"""

		Logger.logr.info("Building service_line_remarks DataFrame")
		service_line_remarks_data = []

		for transaction in self.transactions:
			for claim in transaction.claims:
				for service in claim.services:
					for remark in service.remarks:
						remit_service_lines_remarks_dict = TransactionSet.serialize_service(transaction, claim, service)['remit_service_lines_remarks_dict']

						remit_service_lines_remarks_dict.update({'remark_code_list_qualifier': remark.qualifier,
																					'remark_code': remark.code})
						service_line_remarks_data.append(remit_service_lines_remarks_dict)

		if len(service_line_remarks_data) < 1:

			service_line_remarks_data.append({
				'remit_key': None,
				'edi_transaction_id_st02': None,
				'claim_service_line_id': None,
				'remit_service_line_key': None,
				'remark_code_list_qualifier': None,
				'remark_code': None,
				'created_at': None
			})

		service_line_remarks_data = pd.DataFrame(service_line_remarks_data)

		return pd.DataFrame(service_line_remarks_data)

	def build_service_line_rendering_providers(self) -> pd.DataFrame:
		"""flatten the remittance rendering_providers by service line to a pandas DataFrame"""

		Logger.logr.info("Building service_line_remarks DataFrame")
		rendering_providers_data = []

		for transaction in self.transactions:
			for claim in transaction.claims:
				for service in claim.services:
					if service.rendering_provider:
						service_line_rendering_providers_dict = TransactionSet.serialize_service(
							transaction, claim, service)['service_line_rendering_providers_dict']
						rendering_providers_data.append(service_line_rendering_providers_dict)

		if len(rendering_providers_data) < 1:
			rendering_providers_data.append({
				'remit_key': None,
				'edi_transaction_id_st02': None,
				'remit_service_line_key': None,
				'claim_service_line_id': None,
				'rendering_provider_qualifier': None,
				'rendering_provider_id': None,
				'created_at': None
					})
		rendering_providers_data = pd.DataFrame(rendering_providers_data)

		return pd.DataFrame(rendering_providers_data)

	def build_remit_remarks_adjudications(self) -> pd.DataFrame:
		"""flatten the remittance advice by inpatient/outpatient adjudication info to a pandas DataFrame"""

		Logger.logr.info("Building remit_remarks_adjudications DataFrame")
		remit_remarks_adjudications_data = []

		for transaction in self.transactions:
			for claim in transaction.claims:
				remit_remarks_adjudications_dict = TransactionSet.serialize_claim(claim, transaction)['remit_remarks_adjudications_dict']
				remit_remarks_adjudications_data.append(remit_remarks_adjudications_dict)
		remit_remarks_adjudications_data = pd.DataFrame(remit_remarks_adjudications_data,
														columns=remit_remarks_adjudications_data[0].keys())
		return remit_remarks_adjudications_data

	def build_provider_adjustments(self) -> pd.DataFrame:
		"""flatten the remittance advice by provider adjustment info to a pandas DataFrame"""

		Logger.logr.info("Building provider_adjustments DataFrame")
		provider_adjustments_data = []

		for transaction in self.transactions:
			provider_adjustment_dict = TransactionSet.serialize_transaction(transaction)['provider_adjustment_dict']
			provider_adjustments_data.append(provider_adjustment_dict)

		provider_adjustments_data = pd.DataFrame(provider_adjustments_data, columns=provider_adjustments_data[0].keys())

		return provider_adjustments_data


	@staticmethod
	def serialize_claim(
			claim: ClaimLoop,
			transaction: TransactionLoop
	) -> dict[str, dict]:

		remits_dict = {
			'remit_key': claim.claim.key,
			'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
			'client_id': None,  # populated after transformation
			'patient_control_id': claim.claim.patient_control_number,
			'patient_id_qualifier': claim.patient.identification_code_qualifier,
			'patient_id': claim.patient.identification_code,
			'patient_last_name': claim.patient.last_name,
			'patient_first_name': claim.patient.first_name,
			'patient_middle_name': claim.patient.middle_name,
			'patient_name_suffix': claim.patient.name_suffix,
			'patient_name_prefix': claim.patient.name_prefix,
			'subscriber_id_qualifier': None,
			'subscriber_id': None,
			'subscriber_last_name': None,
			'subscriber_first_name': None,
			'subscriber_middle_name': None,
			'subscriber_suffix': None,
			'subscriber_prefix': None,
			'subscriber_patient_relationship': None,
			'payer_id': transaction.payer.identification_code,
			'payer_name': transaction.payer.name,
			'bt_facility_type_code_CLP08': claim.claim.facility_type_code,
			'bt_facility_type_code_CLP09': claim.claim.claim_frequency_code,
			'bt_facility_type_code_TS302': transaction.provider_summary.facility_type_code
			if transaction.provider_summary else None,
			'payee_id_qualifier': transaction.payee.identification_code_qualifier,
			'payee_id': transaction.payee.identification_code,
			'payee_name': transaction.payee.name,
			'provider_entity_type_qualifier': None,
			'provider_id_qualifier': None,
			'provider_id': None,
			'provider_name': None,
			'provider_first_name': None,
			'provider_middle_name': None,
			'provider_suffix': None,
			'provider_prefix': None,
			'claim_received_date': claim.claim_received_date.date if claim.claim_received_date else None,
			'claim_paid_date': transaction.financial_information.transaction_date,
			'claim_status': claim.claim.status,
			'claim_total_charge_amount': claim.claim.charge_amount,
			'claim_payment_amount': claim.claim.paid_amount,
			'claim_patient_responsibility': claim.claim.patient_responsibility_amount,
			'claim_filing_indicator': claim.claim.claim_filing_indicator_code,
			'payer_claim_control_number': claim.claim.payer_claim_control_number,
			'drg_code': claim.claim.drg_code,
			'corrected_insured_last_name': None,
			'corrected_insured_first_name': None,
			'corrected_insured_middle_name': None,
			'corrected_insured_prefix': None,
			'corrected_insured_suffix': None,
			'corrected_insured_id_qualifier': None,
			'corrected_insured_id': None,
			'claim_statement_period_start': claim.claim_statement_period_start.date
			if claim.claim_statement_period_start else None,
			'claim_statement_period_end': claim.claim_statement_period_end.date
			if claim.claim_statement_period_end else None,
			'claim_coverage_expiration': claim.claim_coverage_expiration.date
			if claim.claim_coverage_expiration else None,
			'claim_coverage_amount': claim.amount.amount if claim.amount else None,
			'claim_contract_code': claim.claim_contract_code.value if claim.claim_contract_code else None,
			'created_at': None,
			'case_number': None  # populated after transformation

		}

		if claim.subscriber:
			remits_dict.update({
				'subscriber_id_qualifier': claim.subscriber.identification_code_qualifier,
				'subscriber_id': claim.subscriber.identification_code,
				'subscriber_last_name': claim.subscriber.last_name,
				'subscriber_first_name': claim.subscriber.first_name,
				'subscriber_middle_name': claim.subscriber.middle_name,
				'subscriber_suffix': claim.subscriber.name_suffix,
				'subscriber_prefix': claim.subscriber.name_prefix,
				'subscriber_patient_relationship': claim.subscriber.patient_relationship,

			})

		if claim.rendering_provider:
			remits_dict.update({
				'provider_entity_type_qualifier': claim.rendering_provider.type_code,
				'provider_id_qualifier': claim.rendering_provider.identification_code_qualifier,
				'provider_id': claim.rendering_provider.identification_code,
				'provider_name': claim.rendering_provider.name,
				'provider_first_name': claim.rendering_provider.first_name,
				'provider_middle_name': claim.rendering_provider.middle_name,
				'provider_suffix': claim.rendering_provider.name_suffix,
				'provider_prefix': claim.rendering_provider.name_prefix

			})

		if claim.insured:
			remits_dict.update({
				'corrected_insured_last_name': claim.insured.last_name,
				'corrected_insured_first_name': claim.insured.first_name,
				'corrected_insured_middle_name': claim.insured.middle_name,
				'corrected_insured_prefix': claim.insured.name_prefix,
				'corrected_insured_suffix': claim.insured.name_suffix,
				'corrected_insured_id_qualifier': claim.insured.identification_code_qualifier,
				'corrected_insured_id': claim.insured.identification_code
				}
			)

		remit_payers_dict = {
			'remit_key': claim.claim.key,
			'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
			'payer_id': transaction.payer.identification_code,
			'payer_name': transaction.payer.name,
			'payer_address_line1': transaction.payer_address.address_line1,
			'payer_address_line2': transaction.payer_address.address_line2,
			'payer_city': transaction.payer_location.city,
			'payer_state': transaction.payer_location.state,
			'payer_zip': transaction.payer_location.zip_code,
			'payer_country': transaction.payer_location.country,
			'payer_contact_business': None,
			'payer_contact_business_qualifier': None,
			'payer_contact_business_name': None,
			'payer_contact_technical': None,
			'payer_contact_technical_qualifier': None,
			'payer_contact_technical_name': None,
			'payer_contact_web': None,
			'payer_contact_web_qualifier': None,
			'payer_contact_web_name': None,
			'payer_id_add': transaction.payer_identification.value if transaction.payer_identification else None,
			'created_at': None

		}

		if transaction.payer_contact_business:
			remit_payers_dict.update({
				'payer_contact_business': transaction.payer_contact_business.communication_no_or_url,
				'payer_contact_business_qualifier': transaction.payer_contact_business.communication_no_or_url_qualifier,
				'payer_contact_business_name': transaction.payer_contact_business.name,
			})

		if transaction.payer_contact_technical:
			remit_payers_dict.update({
				'payer_contact_technical': transaction.payer_contact_technical.communication_no_or_url,
				'payer_contact_technical_qualifier': transaction.payer_contact_technical.communication_no_or_url_qualifier,
				'payer_contact_technical_name': transaction.payer_contact_technical.name,
			})

		if transaction.payer_contact_web:
			remit_payers_dict.update({
				'payer_contact_web': transaction.payer_contact_web.communication_no_or_url,
				'payer_contact_web_qualifier': transaction.payer_contact_web.communication_no_or_url_qualifier,
				'payer_contact_web_name': transaction.payer_contact_web.name,
			})

		remit_remarks_adjudications_dict = {
			'remit_key': claim.claim.key,
			'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
			'MIA_covered_days_visits_count': None,
			'MIA_pps_operating_outlier_amount': None,
			'MIA_lifetime_psychiatric_days_count': None,
			'MIA_claim_drg_amount': None,
			'MIA_claim_payment_remark_code': None,
			'MIA_claim_disproportionate_share_amount': None,
			'MIA_claim_msp_pass_though_amount': None,
			'MIA_claim_pps_capital_amount': None,
			'MIA_pps_capital_fsp_drg_amount': None,
			'MIA_pps_capital_hsp_drg_amount': None,
			'MIA_pps_capital_dsh_drg_amount': None,
			'MIA_old_capital_amount': None,
			'MIA_pps_capital_ime_amount': None,
			'MIA_pps_operating_hospital_specific_drg_amount': None,
			'MIA_cost_report_day_count': None,
			'MIA_pps_operating_federal_specific_drg_amount': None,
			'MIA_claim_pps_capital_outlier_amount': None,
			'MIA_claim_indirect_teaching_amount': None,
			'MIA_non_payable_professional_component_amount': None,
			'MIA_claim_remark_code1': None,
			'MIA_claim_remark_code2': None,
			'MIA_claim_remark_code3': None,
			'MIA_claim_remark_code4': None,
			'MIA_pps_capital_exception_amount': None,
			'MOA_reimbursement_rate': None,
			'MOA_claim_hcpcs_payment_amount': None,
			'MOA_claim_remark_code1': None,
			'MOA_claim_remark_code2': None,
			'MOA_claim_remark_code3': None,
			'MOA_claim_remark_code4': None,
			'MOA_claim_remark_code5': None,
			'MOA_claim_esrd_payment_amount': None,
			'MOA_non_payable_professional_component_amount': None,
			'created_at': None

		}

		if claim.inpatient:
			remit_remarks_adjudications_dict.update({
				'remit_key': claim.claim.key,
				'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
				'MIA_covered_days_visits_count': claim.inpatient.covered_days_visits_count,
				'MIA_pps_operating_outlier_amount': claim.inpatient.pps_operating_outlier_amount,
				'MIA_lifetime_psychiatric_days_count': claim.inpatient.lifetime_psychiatric_days_count,
				'MIA_claim_drg_amount': claim.inpatient.claim_drg_amount,
				'MIA_claim_payment_remark_code': claim.inpatient.claim_payment_remark_code,
				'MIA_claim_disproportionate_share_amount': claim.inpatient.claim_disproportionate_share_amount,
				'MIA_claim_msp_pass_though_amount': claim.inpatient.claim_msp_pass_though_amount,
				'MIA_claim_pps_capital_amount': claim.inpatient.claim_pps_capital_amount,
				'MIA_pps_capital_fsp_drg_amount': claim.inpatient.pps_capital_fsp_drg_amount,
				'MIA_pps_capital_hsp_drg_amount': claim.inpatient.pps_capital_hsp_drg_amount,
				'MIA_pps_capital_dsh_drg_amount': claim.inpatient.pps_capital_dsh_drg_amount,
				'MIA_old_capital_amount': claim.inpatient.old_capital_amount,
				'MIA_pps_capital_ime_amount': claim.inpatient.pps_capital_ime_amount,
				'MIA_pps_operating_hospital_specific_drg_amount': claim.inpatient.pps_operating_hospital_specific_drg_amount,
				'MIA_cost_report_day_count': claim.inpatient.cost_report_day_count,
				'MIA_pps_operating_federal_specific_drg_amount': claim.inpatient.pps_operating_federal_specific_drg_amount,
				'MIA_claim_pps_capital_outlier_amount': claim.inpatient.claim_pps_capital_outlier_amount,
				'MIA_claim_indirect_teaching_amount': claim.inpatient.claim_indirect_teaching_amount,
				'MIA_nonpayable_professional_component_amount': claim.inpatient.non_payable_professional_component_amount,
				'MIA_claim_remark_code1': claim.inpatient.remark_code1,
				'MIA_claim_remark_code2': claim.inpatient.remark_code2,
				'MIA_claim_remark_code3': claim.inpatient.remark_code3,
				'MIA_claim_remark_code4': claim.inpatient.remark_code4,
				'MIA_pps_capital_exception_amount': claim.inpatient.pps_capital_exception_amount

			})

		if claim.outpatient:
			remit_remarks_adjudications_dict.update({
				'remit_key': claim.claim.key,
				'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
				'MOA_reimbursement_rate': claim.outpatient.reimbursement_rate,
				'MOA_claim_hcpcs_payment_amount': claim.outpatient.claim_hcpcs_payment_amount,
				'MOA_claim_remark_code1': claim.outpatient.remark_code1,
				'MOA_claim_remark_code2': claim.outpatient.remark_code2,
				'MOA_claim_remark_code3': claim.outpatient.remark_code3,
				'MOA_claim_remark_code4': claim.outpatient.remark_code4,
				'MOA_claim_remark_code5': claim.outpatient.remark_code5,
				'MOA_claim_esrd_payment_amount': claim.outpatient.claim_esrd_payment_amount,
				'MOA_nonpayable_professional_component_amount': claim.outpatient.
				non_payable_professional_component_amount


			})

		remit_adjustments_dict = {
			'remit_key': None,
			'edi_transaction_id_st02': None,
			'adjustment_group_code': None,
			'adjustment_reason_code': None,
			'adjustment_amount': None,
			'adjustment_quantity': None,
			'adjustment_reason_code2': None,
			'adjustment_amount2': None,
			'adjustment_quantity2': None,
			'adjustment_reason_code3': None,
			'adjustment_amount3': None,
			'adjustment_quantity3': None,
			'adjustment_reason_code4': None,
			'adjustment_amount4': None,
			'adjustment_quantity4': None,
			'adjustment_reason_code5': None,
			'adjustment_amount5': None,
			'adjustment_quantity5': None,
			'adjustment_reason_code6': None,
			'adjustment_amount6': None,
			'adjustment_quantity6': None,
			'created_at': None
		}

		if claim.adjustment:

			remit_adjustments_dict.update({
					'remit_key': claim.claim.key,
					'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
					'adjustment_group_code': claim.adjustment.group_code,
					'adjustment_reason_code': claim.adjustment.reason_code,
					'adjustment_amount': claim.adjustment.amount,
					'adjustment_quantity': claim.adjustment.quantity,
					'adjustment_reason_code2': claim.adjustment.reason_code2,
					'adjustment_amount2': claim.adjustment.amount2,
					'adjustment_quantity2': claim.adjustment.quantity2,
					'adjustment_reason_code3': claim.adjustment.reason_code3,
					'adjustment_amount3': claim.adjustment.amount3,
					'adjustment_quantity3': claim.adjustment.quantity3,
					'adjustment_reason_code4': claim.adjustment.reason_code4,
					'adjustment_amount4': claim.adjustment.amount4,
					'adjustment_quantity4': claim.adjustment.quantity4,
					'adjustment_reason_code5': claim.adjustment.reason_code5,
					'adjustment_amount5': claim.adjustment.amount5,
					'adjustment_quantity5': claim.adjustment.quantity5,
					'adjustment_reason_code6': claim.adjustment.reason_code6,
					'adjustment_amount6': claim.adjustment.amount6,
					'adjustment_quantity6': claim.adjustment.quantity6,
					'created_at': None
				})

		return {'remits_dict': remits_dict, 'remit_payers_dict': remit_payers_dict,
										'remit_remarks_adjudications_dict': remit_remarks_adjudications_dict,
										'remit_adjustments_dict': remit_adjustments_dict}

	@staticmethod
	def serialize_transaction(
			transaction: TransactionLoop
	) -> dict[str, dict]:

		remit_financial_info_dict = {
			'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
			'alt_id': None,  # this col gets populated during transformation
			'fin_info_payer_id': transaction.financial_information.payer_id,
			'fin_info_receiver_account_number_qualifier': transaction.financial_information.account_no_qualifier,
			'fin_info_receiver_account_number': transaction.financial_information.receiver_or_provider_acc_no,
			'fin_info_originating_company_identifier': transaction.financial_information.origin_company_code,
			'fin_info_transaction_handling_code': transaction.financial_information.transaction_handling_code,
			'fin_info_total_check_amount': transaction.financial_information.amount_paid,
			'fin_info_credit_debit_flag': transaction.financial_information.credit_debit_flag,
			'fin_info_payment_method_code': transaction.financial_information.payment_method,
			'fin_info_payment_format_code': transaction.financial_information.payment_format,
			'fin_info_sender_dfi_id_number_qualifier': transaction.financial_information.id_qualifier,
			'fin_info_sender_dfi_identification_number': transaction.financial_information.id,
			'fin_info_sender_account_number_qualifier': transaction.financial_information.acc_qualifier,
			'fin_info_sender_account_number': transaction.financial_information.sender_acc_no,
			'trace_originating_company_supplemental_code': transaction.trace_number.origin_company_supplemental_code,
			'fin_info_check_date': transaction.financial_information.transaction_date,
			'trace_type_code': transaction.trace_number.type_code,
			'trace_ein_tin': transaction.trace_number.origin_company_identifier,
			'trace_reference_identification_check_num': transaction.trace_number.ref_identification,
			'payer_name': transaction.payer.name,
			'payee_name': transaction.payee.name,
			'created_at': None,
			'tax_payee_id_qualifier': transaction.payee_identification.qualifier_code if transaction.payee_identification else None,
			'tax_payee_id': transaction.payee_identification.value if transaction.payee_identification else None,
			'payee_id_qualifier': transaction.payee.identification_code_qualifier,
			'payee_id': transaction.payee.identification_code,
			'other_payee_id_qualifier' : transaction.other_payee_identification.qualifier_code
			if transaction.other_payee_identification else None,
			'other_payee_id': transaction.other_payee_identification.value
			if transaction.other_payee_identification else None


		}

		provider_adjustment_dict = {
			'provider_id': None,
			'edi_transaction_id_st02': None,
			'fiscal_period_date': None,
			'provider_adjustment_reason_code1': None,
			'provider_adjustment_id1': None,
			'provider_adjustment_amount1': None,
			'provider_adjustment_reason_code2': None,
			'provider_adjustment_id2': None,
			'provider_adjustment_amount2': None,
			'provider_adjustment_reason_code3': None,
			'provider_adjustment_id3': None,
			'provider_adjustment_amount3': None,
			'provider_adjustment_reason_code4': None,
			'provider_adjustment_id4': None,
			'provider_adjustment_amount4': None,
			'provider_adjustment_reason_code5': None,
			'provider_adjustment_id5': None,
			'provider_adjustment_amount5': None,
			'provider_adjustment_reason_code6': None,
			'provider_adjustment_id6': None,
			'provider_adjustment_amount6': None,
			'created_at': None

		}

		if transaction.provider_adjustment:
			provider_adjustment_dict.update({
				'provider_id': transaction.provider_adjustment.provider_id,
				'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
				'fiscal_period_date': transaction.provider_adjustment.fiscal_period_date,
				'provider_adjustment_reason_code1': transaction.provider_adjustment.reason_code1,
				'provider_adjustment_id1': transaction.provider_adjustment.id1,
				'provider_adjustment_amount1': transaction.provider_adjustment.amount1,
				'provider_adjustment_reason_code2': transaction.provider_adjustment.reason_code2,
				'provider_adjustment_id2': transaction.provider_adjustment.id2,
				'provider_adjustment_amount2': transaction.provider_adjustment.amount2,
				'provider_adjustment_reason_code3': transaction.provider_adjustment.reason_code3,
				'provider_adjustment_id3': transaction.provider_adjustment.id3,
				'provider_adjustment_amount3': transaction.provider_adjustment.amount3,
				'provider_adjustment_reason_code4': transaction.provider_adjustment.reason_code4,
				'provider_adjustment_id4': transaction.provider_adjustment.id4,
				'provider_adjustment_amount4': transaction.provider_adjustment.amount4,
				'provider_adjustment_reason_code5': transaction.provider_adjustment.reason_code5,
				'provider_adjustment_id5': transaction.provider_adjustment.id5,
				'provider_adjustment_amount5': transaction.provider_adjustment.amount5,
				'provider_adjustment_reason_code6': transaction.provider_adjustment.reason_code6,
				'provider_adjustment_id6': transaction.provider_adjustment.id6,
				'provider_adjustment_amount6': transaction.provider_adjustment.amount6


			})

		return {'remit_financial_info_dict': remit_financial_info_dict,
										'provider_adjustment_dict': provider_adjustment_dict}



	@staticmethod
	def serialize_service(
			transaction: TransactionLoop,
			claim: ClaimLoop,
			service: ServiceLoop
	) -> dict[str, dict]:

		# if the service doesn't have a start date assume the service and claim dates match
		start_date = None
		if service.service_period_start:
			start_date = service.service_period_start.date
		elif claim.claim_statement_period_start:
			start_date = claim.claim_statement_period_start.date

		# if the service doesn't have an end date assume the service and claim dates match
		end_date = None
		if service.service_period_end:
			end_date = service.service_period_end.date
		elif claim.claim_statement_period_end:
			end_date = claim.claim_statement_period_end.date

		remit_service_lines_dict = {
			'remit_key': claim.claim.key,
			'remit_service_line_key': claim.claim.key + '_' + service.service.key,
			'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
			'claim_service_line_id': service.service_identification.value
			if service.service_identification else None,
			'adjudicated_product_service_id': service.service.code,
			'adjudicated_modifier1': service.service.modifier1,
			'adjudicated_modifier2': service.service.modifier2,
			'adjudicated_modifier3': service.service.modifier3,
			'adjudicated_modifier4': service.service.modifier4,
			'adjudicated_line_item_amount_charged': service.service.charge_amount,
			'adjudicated_line_item_amount_paid': service.service.paid_amount,
			'adjudicated_revenue_code': service.service.NUBC_revenue_code,
			'adjudicated_product_service_id_qualifer': service.service.qualifier,
			'adjudicated_line_item_quantity': service.service.adjudicated_line_item_quantity,
			'submitted_product_service_id_qualifer': service.service.product_qualifier,
			'submitted_product_service_id':service.service.procedure_code,
			'submitted_adjudicated_modifier1': service.service.procedure_modifier1,
			'submitted_adjudicated_modifier2': service.service.procedure_modifier2,
			'submitted_adjudicated_modifier3': service.service.procedure_modifier3,
			'submitted_adjudicated_modifier4': service.service.procedure_modifier4,
			'submitted_description': service.service.code_description,
			'submitted_line_item_quantity': service.service.submitted_line_item_quantity,
			'line_allowed_amount': service.allowed_amount,
			'service_date_qualifier': service.service_date.qualifier_code if service.service_date else None,
			'service_line_start_date': start_date,
			'service_line_end_date': end_date,
			'created_at': None

		}

		remit_service_lines_remarks_dict = {
			'remit_key': claim.claim.key,
			'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
			'claim_service_line_id': service.service_identification.value
			if service.service_identification else None,
			'remit_service_line_key': claim.claim.key + '_' + service.service.key,
			'remark_code_list_qualifier': None,
			'remark_code': None,
			'created_at': None
		}

		service_line_rendering_providers_dict = {
			'remit_key': claim.claim.key,
			'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
			'remit_service_line_key': claim.claim.key + '_' + service.service.key,
			'claim_service_line_id': service.service_identification.value
			if service.service_identification else None,
			'rendering_provider_qualifier': service.rendering_provider.qualifier_code
			if service.rendering_provider else None,
			'rendering_provider_id': service.rendering_provider.identification if service.rendering_provider else None,
			'created_at': None

		}

		return {'remit_service_lines_dict': remit_service_lines_dict, 'remit_service_lines_remarks_dict':
				remit_service_lines_remarks_dict, 'service_line_rendering_providers_dict':
													service_line_rendering_providers_dict }

	@staticmethod
	def serialize_adjustment(
			transaction: TransactionLoop,
			claim: ClaimLoop,
			service: ServiceLoop,
			adjustment: ServiceAdjustmentSegment
	) -> dict[str, dict]:

		service_line_adjustments_dict = {
			'remit_key': None,
			'edi_transaction_id_st02': None,
			'claim_service_line_id': None,
			'remit_service_line_key': None,
			'adjustment_group_code': None,
			'adjustment_reason_code': None,
			'adjustment_amount': None,
			'adjustment_quantity': None,
			'adjustment_reason_code2': None,
			'adjustment_amount2': None,
			'adjustment_quantity2': None,
			'adjustment_reason_code3': None,
			'adjustment_amount3': None,
			'adjustment_quantity3': None,
			'adjustment_reason_code4': None,
			'adjustment_amount4': None,
			'adjustment_quantity4': None,
			'adjustment_reason_code5': None,
			'adjustment_amount5': None,
			'adjustment_quantity5': None,
			'adjustment_reason_code6': None,
			'adjustment_amount6': None,
			'adjustment_quantity6': None,
			'created_at': None
								}

		if adjustment:

			service_line_adjustments_dict.update({
				'remit_key': claim.claim.key,
				'edi_transaction_id_st02': transaction.transaction.transaction_set_control_no,
				'claim_service_line_id': service.service_identification.value
				if service.service_identification else None,
				'remit_service_line_key': claim.claim.key + '_' + service.service.key,
				'adjustment_group_code': adjustment.group_code,
				'adjustment_reason_code': adjustment.reason_code,
				'adjustment_amount': adjustment.amount,
				'adjustment_quantity': adjustment.quantity,
				'adjustment_reason_code2': adjustment.reason_code2,
				'adjustment_amount2': adjustment.amount2,
				'adjustment_quantity2': adjustment.quantity2,
				'adjustment_reason_code3': adjustment.reason_code3,
				'adjustment_amount3': adjustment.amount3,
				'adjustment_quantity3': adjustment.quantity3,
				'adjustment_reason_code4': adjustment.reason_code4,
				'adjustment_amount4': adjustment.amount4,
				'adjustment_quantity4': adjustment.quantity4,
				'adjustment_reason_code5': adjustment.reason_code5,
				'adjustment_amount5': adjustment.amount5,
				'adjustment_quantity5': adjustment.quantity5,
				'adjustment_reason_code6': adjustment.reason_code6,
				'adjustment_amount6': adjustment.amount6,
				'adjustment_quantity6': adjustment.quantity6,
				'created_at': None

			})
		return {'service_line_adjustments_dict': service_line_adjustments_dict}

	@classmethod
	def build(cls, file_path: str) -> 'TransactionSet':
		interchange = None
		transactions = []

		with open(file_path) as f:
			file = f.read()

		segments = file.split('~')
		segments = [segment.strip() for segment in segments]
		segments = [f'{index}:{segment}' for index, segment in enumerate(segments)]
		segments = iter(segments)
		segment = None

		while True:
			response = cls.build_attribute(segment, segments)
			segment = response.segment
			segments = response.segments

			# no more segments to parse
			if response.segments is None:
				break

			if response.key == 'interchange':
				interchange = response.value

			if response.key == 'transaction':
				transactions.append(response.value)

			# if response.key in cls.terminating_identifiers:

		return TransactionSet(interchange, transactions)

	@classmethod
	def build_attribute(cls, segment: Optional[str], segments: Iterator[str]) -> BuildAttributeResponse:
		if segment is None:
			try:
				segment = segments.__next__()
			except StopIteration:
				return BuildAttributeResponse(None, None, None, None)

		identifier = find_identifier(segment)

		if identifier == InterchangeSegment.identification:
			interchange = InterchangeSegment(segment)
			return BuildAttributeResponse('interchange', interchange, None, segments)

		if identifier == OrganizationLoop.initiating_identifier:
			organization, segments, segment = OrganizationLoop.build(segment, segments)
			return BuildAttributeResponse('organization', organization, segment, segments)

		elif identifier == ClaimLoop.initiating_identifier:
			claim, segments, segment = ClaimLoop.build(segment, segments)
			return BuildAttributeResponse('claim', claim, segment, segments)

		elif identifier == TransactionLoop.initiating_identifier:
			transaction, segments, segment = TransactionLoop.build(segment, segments)
			return BuildAttributeResponse('transaction', transaction, segment, segments)

		else:
			return BuildAttributeResponse(None, None, None, segments)

	def count_claims(self) -> int:
		count = 0
		for transaction in self.transactions:
			count += len(transaction.claims)

		return count

	def count_transactions(self) -> int:
		count = 0
		count += len(self.transactions)

		return count

	def count_services(self) -> int:
		count = 0
		for transaction in self.transactions:
			for claim in transaction.claims:
				count += len(claim.services)

		return count


if __name__ == '__main__':
	pass