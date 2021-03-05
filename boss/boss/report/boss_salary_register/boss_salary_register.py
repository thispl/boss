# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, erpnext
from frappe.utils import flt
from frappe import _

def execute(filters=None):
    if not filters: filters = {}
    currency = None
    
    if filters.get('currency'):
        currency = filters.get('currency')
    company_currency = erpnext.get_company_currency(filters.get("company"))
    salary_slips = get_salary_slips(filters, company_currency)
    if not salary_slips: return [], []

    columns, earning_types, ded_types = get_columns(salary_slips)
    ss_earning_map = get_ss_earning_map(salary_slips, currency, company_currency)
    ss_ded_map = get_ss_ded_map(salary_slips,currency, company_currency)
    doj_map = get_employee_doj_map()

    data = []
    for ss in salary_slips:
        basic_da = 0
        house_rent_allowance = 0
        leave_with_wages = 0
        statutory_bonus = 0
        row = [ss.name, ss.employee, ss.employee_name, doj_map.get(ss.employee), ss.client_name, ss.site, ss.designation,
            ss.company, ss.start_date, ss.end_date, ss.total_working_days, ss.absent_days, ss.payment_days]

        if ss.client_name is not None: columns[3] = columns[3].replace('-1','120')
        if ss.site is not None: columns[4] = columns[4].replace('-1','120')
        if ss.designation is not None: columns[5] = columns[5].replace('-1','120')
        # if ss.working_days is not None: columns[9] = columns[9].replace('-1','130')

        fixed_basic_da = 0
        fixed_basic_da = frappe.db.get_value("Employee", {'employee': ss.employee}, ['basic_and_da'])
        frappe.errprint(fixed_basic_da)
        if fixed_basic_da:
            row += [fixed_basic_da]
        else:
            row += [0]

        house_rent_allowance = frappe.db.get_value("Employee", {'employee': ss.employee}, ['house_rent_allowance'])
        frappe.errprint(house_rent_allowance)
        if house_rent_allowance:
            row += [house_rent_allowance]
        else:
            row += [0]
        
        leave_with_wages = frappe.db.get_value("Employee", {'employee': ss.employee}, ['leave_with_wages'])
        frappe.errprint(leave_with_wages)
        if leave_with_wages:
            row += [leave_with_wages]
        else:
            row += [0]

        statutory_bonus = frappe.db.get_value("Employee", {'employee': ss.employee}, ['statutory_bonus'])
        frappe.errprint(statutory_bonus)
        if statutory_bonus:
            row += [statutory_bonus]
        else:
            row += [0]

        # total = 0
        # total = basic_da + house_rent_allowance + leave_with_wages + statutory_bonus
        # if total:
        #     row += [total]
        # else:
        #     row += [0]

        for e in earning_types:
            row.append(ss_earning_map.get(ss.name, {}).get(e))

        if currency == company_currency:
            row += [flt(ss.gross_pay) * flt(ss.exchange_rate)]
        else:
            row += [ss.gross_pay]

        for d in ded_types:
            row.append(ss_ded_map.get(ss.name, {}).get(d))

        # row.append(ss.total_loan_repayment)

        if currency == company_currency:
            row += [flt(ss.total_deduction) * flt(ss.exchange_rate), flt(ss.net_pay) * flt(ss.exchange_rate),ss.bank_account_no,ss.ifsc_no,ss.pf_number,ss.esi_number]
        else:
            row += [ss.total_deduction, ss.net_pay,ss.bank_account_no,ss.ifsc_no,ss.pf_number,ss.esi_number]
        row.append(currency or company_currency)
        data.append(row)

    return columns, data

def get_columns(salary_slips):
    """
    columns = [
        _("Salary Slip ID") + ":Link/Salary Slip:150",
        _("Employee") + ":Link/Employee:120",
        _("Employee Name") + "::140",
        _("Date of Joining") + "::80",
        _("Client Name") + ":Link/Client:120",
        _("Site") + ":Link/Site:120",
        _("Designation") + ":Link/Designation:120",
        _("Company") + ":Link/Company:120",
        _("Start Date") + "::80",
        _("End Date") + "::80",
        _("Cal Days") + ":Float:130",
        _("Absent Days") + ":Float:130",
        _("Payment Days") + ":Float:120",
        _("Currency") + ":Link/Currency:80"
    ]
    """
    columns = [
        _("Salary Slip ID") + ":Link/Salary Slip:150",
        _("Employee") + ":Link/Employee:120",
        _("Employee Name") + "::140",
        _("Date of Joining") + "::80",
        _("Client Name") + ":Link/Client::80",
        _("Site") + ":Link/Site::80",
        _("Designation") + ":Link/Designation:120",
        _("Company") + ":Link/Company:120",
        _("Start Date") + "::80",
        _("End Date") + "::80",
        _("Cal Days") + ":Float:120",
        _("Absent Days") + ":Float:120",
        _("Payment Days") + ":Float:120",
        _("Fixed Basic") + "::80",
        _("Fixed HRA") + "::80",
        _("Fixed LWW") + "::80",
        _("Fixed Statutory Bonus") + "::80",
        # _("Total") + "::80"
    ]

    salary_components = {_("Earning"): [], _("Deduction"): []}

    for component in frappe.db.sql("""select distinct sd.salary_component, sc.type
        from `tabSalary Detail` sd, `tabSalary Component` sc
        where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s)""" %
        (', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1):
        salary_components[_(component.type)].append(component.salary_component)

    columns = columns + [(e + ":Currency:120") for e in salary_components[_("Earning")]] + \
        [_("Gross Pay") + ":Currency:120"] + [(d + ":Currency:120") for d in salary_components[_("Deduction")]] + \
        [_("Total Deduction") + ":Currency:120", _("Net Pay") + ":Currency:120",_("Account No") + ":Data:120",_("IFSC No") + ":Data:120"
        ,_("PF No") + ":Data:120",_("ESI No") + ":Data:120"]

    return columns, salary_components[_("Earning")], salary_components[_("Deduction")]

def get_salary_slips(filters, company_currency):
    filters.update({"from_date": filters.get("from_date"), "to_date":filters.get("to_date")})
    conditions, filters = get_conditions(filters, company_currency)
    salary_slips = frappe.db.sql("""select * from `tabSalary Slip` where %s
        order by employee""" % conditions, filters, as_dict=1)

    return salary_slips or []

def get_conditions(filters, company_currency):
    conditions = ""
    doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

    if filters.get("docstatus"):
        conditions += "docstatus = {0}".format(doc_status[filters.get("docstatus")])

    if filters.get("from_date"): conditions += " and start_date >= %(from_date)s"
    if filters.get("to_date"): conditions += " and end_date <= %(to_date)s"
    if filters.get("company"): conditions += " and company = %(company)s"
    if filters.get("employee"): conditions += " and employee = %(employee)s"
    if filters.get("client_name"): conditions += " and client_name = %(client_name)s"
    if filters.get("site"): conditions += " and site = %(site)s"
    # if filters.get("currency") and filters.get("currency") != company_currency:
    # 	conditions += " and currency = %(currency)s"

    return conditions, filters

def get_employee_doj_map():
    return	frappe._dict(frappe.db.sql("""
                SELECT
                    employee,
                    date_of_joining
                FROM `tabEmployee`
                """))

def get_ss_earning_map(salary_slips, currency, company_currency):
    ss_earnings = frappe.db.sql("""select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
        from `tabSalary Detail` sd, `tabSalary Slip` ss where sd.parent=ss.name and sd.parent in (%s)""" %
        (', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

    ss_earning_map = {}
    for d in ss_earnings:
        ss_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
        if currency == company_currency:
            ss_earning_map[d.parent][d.salary_component] = flt(d.amount) * flt(d.exchange_rate if d.exchange_rate else 1)
        else:
            ss_earning_map[d.parent][d.salary_component] = flt(d.amount)

    return ss_earning_map

def get_ss_ded_map(salary_slips, currency, company_currency):
    ss_deductions = frappe.db.sql("""select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
        from `tabSalary Detail` sd, `tabSalary Slip` ss where sd.parent=ss.name and sd.parent in (%s)""" %
        (', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

    ss_ded_map = {}
    for d in ss_deductions:
        ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
        if currency == company_currency:
            ss_ded_map[d.parent][d.salary_component] = flt(d.amount) * flt(d.exchange_rate if d.exchange_rate else 1)
        else:
            ss_ded_map[d.parent][d.salary_component] = flt(d.amount)

    return ss_ded_map