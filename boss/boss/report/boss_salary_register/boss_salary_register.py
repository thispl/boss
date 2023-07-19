# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from logging import basicConfig
import frappe
from datetime import date, timedelta
from frappe import get_request_header, msgprint, _
from frappe.utils import cstr, cint, getdate
from frappe.utils import cstr, add_days, date_diff, getdate, get_last_day,get_first_day
from datetime import date, timedelta, datetime

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	columns = [
		_("Salary Slip ID") + ":Link/Salary Slip:100", _("Employee") + ":Link/Employee:100",_('Employee Name') +':Data:100',_('Date of Joining') +':Data:100',

		_('Client Name') +':Data:100',_('Site') +':Data:100',_('Designation')+':Data:100',_('Company') +':Data:100',_('Start Date') +':Data:100',

		_('End Date')+':Data:100',_('Cal Days') +':Data:100',_('Absent Days') +':Data:100',_('Payment Days') +':Data:100',

		_(' Fixed Basic') +':Data:100',_('Fixed Dearness Allowance') +':Data:100',_('Fixed HRA') +':Data:100',_('Fixed Other Allowance') +':Data:100',
		
		_('Fixed LWW') +':Data:100',_('Fixed Special Allowance') +':Data:100',('Fixed Service Charge') +':Data:100',_('Fixed Advance Bonus') +':Data',

		_('Attendance Bonus') +':Data:100',_('Fixed OT Rate') +':Data:100',_('Fixed Conveyance') +':Data:100',_('Fixed Statutory Bonus') +':Data:100',	

		_('Fixed Canteen Allowance') +':Data:100',_('Fixed Transportation Allowance') +':Data:100',_('Fixed Uniform Allowance') +':Data:100',

		_('Basic') +':Data:100',_('HRA') +':Datta:100',_('DA') +':Data:100',_('OA') +':Data:100',_('Special Allowance') +':Data:100',
		
		_('Service Charge') +':Data:100',_('Cantenn Allowace') +':Data:100',

		_('LWW') +':Data:100',_('Employer ESIC') +':Data:100',_('Employer PF') +':Data:100',_('Uniform Allowance') +':Data:100',

		_('Statutory Bonus') +':Data:100',_('Night Shift Allownace') +':Data:100',_('Over Time') +':Data:100',_('Week Off') +':Data:100',_('Gross Pay') +':Data:100',

		_('ESI') +':Data:100',_('Professional Tax') +':Data:100',_('Employee PF') +':Data:100',_('Total Deduction') +':Data:100',_('Net Pay') +':Data:100',

		_('Account No') +':Data:100',_('IFSC NO') +':Data:100',_('PF NO') +':Data:100',_('ESI NO') +':Data:100'
	]
	return columns

def get_data(filters):
	data = []
	if filters.employee:
		salary_slip = frappe.db.get_all('Salary Slip',{'employee':filters.employee,'start_date':filters.from_date},['*'])
	elif filters.client_name:
		salary_slip = frappe.db.get_all('Salary Slip',{'client_name':filters.client_name,'start_date':filters.from_date},['*'])
	elif filters.site:
		salary_slip = frappe.db.get_all('Salary Slip',{'site':filters.site,'start_date':filters.from_date},['*'])
	elif filters.company:
		salary_slip = frappe.db.get_all('Salary Slip',{'company':filters.company,'start_date':filters.from_date},['*'])	
	else:
		salary_slip = frappe.db.get_all('Salary Slip',{'start_date':filters.from_date},['*'])
	
	for ss in salary_slip:
		emp = frappe.get_doc('Employee',ss.employee,['*'])
		
		basic = frappe.db.get_value('Salary Detail',{'abbr':'B','parent':ss.name},'amount')
		hra = frappe.db.get_value('Salary Detail',{'abbr':'HRA','parent':ss.name},'amount')
		da = frappe.db.get_value('Salary Detail',{'abbr':'DA','parent':ss.name},'amount')
		oa = frappe.db.get_value('Salary Detail',{'abbr':'OA','parent':ss.name},'amount')
		sa = frappe.db.get_value('Salary Detail',{'abbr':'SA','parent':ss.name},'amount')
		sc = frappe.db.get_value('Salary Detail',{'abbr':'SC','parent':ss.name},'amount')
		ca = frappe.db.get_value('Salary Detail',{'abbr':'CA','parent':ss.name},'amount')
		lww = frappe.db.get_value('Salary Detail',{'abbr':'LWW','parent':ss.name},'amount')
		essic = frappe.db.get_value('Salary Detail',{'abbr':'EESIC','parent':ss.name},'amount')
		epf = frappe.db.get_value('Salary Detail',{'abbr':'EPF','parent':ss.name},'amount')
		ua = frappe.db.get_value('Salary Detail',{'abbr':'UA','parent':ss.name},'amount')
		sb = frappe.db.get_value('Salary Detail',{'abbr':'SB','parent':ss.name},'amount')
		nsa = frappe.db.get_value('Salary Detail',{'abbr':'NSA','parent':ss.name},'amount')
		ot = frappe.db.get_value('Salary Detail',{'abbr':'OT','parent':ss.name},'amount')
		wo = frappe.db.get_value('Salary Detail',{'abbr':'WO','parent':ss.name},'amount')
		esi = frappe.db.get_value('Salary Detail',{'abbr':'ESIC','parent':ss.name},'amount')
		pt = frappe.db.get_value('Salary Detail',{'abbr':'PT','parent':ss.name},'amount')
		pf = frappe.db.get_value('Salary Detail',{'abbr':'PF','parent':ss.name},'amount')
		
		row = [
			ss.name,ss.employee,ss.employee_name,ss.date_of_joning,ss.client_name,ss.site,emp.designation,ss.company,ss.start_date,ss.end_date,
			ss.total_working_days,ss.absent_days,ss.payment_days,emp.basic,emp.dearness_allowance,emp.house_rent_allowance,emp.other_allowance,
			emp.lww,emp.special_allowance,emp.service_charge,emp.advance_bonus,emp.attendance_bonus,emp.ot_rate,emp.conveyance,emp.statutory_bonus,
			emp.canteen_allowance,emp.transportation_allowance,emp.uniform_allowance,basic,hra,oa,da,sa,sc,ca,lww,essic,epf,ua,sb,nsa,ot,wo,
			ss.gross,esi,pt,pf,ss.total_deduction,ss.net_pay,ss.bank_account_no,ss.ifsc_no,ss.pf_number,ss.esi_no
		]	
		data.append(row)
	return data

# def get_conditions(filters):
#     conditions = ""
#     doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

#     if filters.get("docstatus"):
#         conditions += "docstatus = {0}".format(doc_status[filters.get("docstatus")])

#     if filters.get("from_date"): conditions += " and start_date >= %(from_date)s"
#     if filters.get("to_date"): conditions += " and end_date <= %(to_date)s"
#     if filters.get("company"): conditions += " and company = %(company)s"
#     if filters.get("employee"): conditions += " and employee = %(employee)s"
#     if filters.get("client_name"): conditions += " and client_name = %(client_name)s"
#     if filters.get("site"): conditions += " and site = %(site)s"

	