from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.segments.utilities import split_segment, get_element


class InpatientAdjudication:
	identification = 'MIA'

	identifier = Identifier()

	def __init__(self, segment: str):
		self.index = segment.split(':', 1)[0]
		segment = segment.split(':', 1)[1]

		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.covered_days_visits_count = segment[1]
		self.pps_operating_outlier_amount = get_element(segment, 2)
		self.lifetime_psychiatric_days_count = get_element(segment, 3)
		self.claim_drg_amount = get_element(segment, 4)
		self.claim_payment_remark_code = get_element(segment, 5)
		self.claim_disproportionate_share_amount = get_element(segment, 6)
		self.claim_msp_pass_though_amount = get_element(segment, 7)
		self.claim_pps_capital_amount = get_element(segment, 8)
		self.pps_capital_fsp_drg_amount = get_element(segment, 9)
		self.pps_capital_hsp_drg_amount = get_element(segment, 10)
		self.pps_capital_dsh_drg_amount = get_element(segment, 11)
		self.old_capital_amount = get_element(segment, 12)
		self.pps_capital_ime_amount = get_element(segment, 13)
		self.pps_operating_hospital_specific_drg_amount = get_element(segment, 14)
		self.cost_report_day_count = get_element(segment, 15)
		self.pps_operating_federal_specific_drg_amount = get_element(segment, 16)
		self.claim_pps_capital_outlier_amount = get_element(segment, 17)
		self.claim_indirect_teaching_amount = get_element(segment, 18)
		self.non_payable_professional_component_amount = get_element(segment, 19)
		self.remark_code1 = get_element(segment, 20)
		self.remark_code2 = get_element(segment, 21)
		self.remark_code3 = get_element(segment, 22)
		self.remark_code4 = get_element(segment, 23)
		self.pps_capital_exception_amount = get_element(segment, 24)

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
