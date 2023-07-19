from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta
from frappe.utils import cint, flt, nowdate, add_days, getdate, fmt_money, add_to_date, DATE_FORMAT, date_diff, money_in_words
from frappe import _
import functools
from datetime import datetime, timedelta

@frappe.whitelist()
def bank_remittance(salary_slip_id):
    bank_remittance = frappe.db.get_value("Bank Remittance",{"salary_slip":salary_slip_id},["name"])
    # print(bank_remittance)
    if not bank_remittance:
        salary_detail = frappe.get_all('Salary Detail',{'parent':salary_slip_id},['*'])
        print(salary_detail)     
        ctc_amount = 0
        for sd in salary_detail:
            if sd.salary_component == "Cost to Company":
                ctc_amount += sd.amount
        salary_slip = frappe.new_doc('Bank Remittance')
        salary_slip.update({
            "salary_slip": salary_slip_id,
            "cost_to_company": ctc_amount
        })
        salary_slip.save(ignore_permissions=True)
        salary_slip.submit()
        frappe.db.commit()

