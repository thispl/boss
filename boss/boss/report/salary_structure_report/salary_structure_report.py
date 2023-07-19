# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from six.moves import range
from six import string_types
import frappe
import json
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
from datetime import date

def execute(filters=None):
    if not filters:
        filters = {}
    columns = get_columns()
    data = []
    row = []
    conditions, filters = get_conditions(filters)
    Salary_structure = get_salary_structure(conditions,filters)
    for ss in Salary_structure:
        data.append(ss)
    return columns, data

def get_columns():
    columns = [
        _("ID") + ":Data:200",
        _("Employee") + ":Data:120",
        _("Employee Name") + ":Data:120",
        _("Department") + ":Data:120",
        _("Salary Structure") + ":Data:120",
        _("Basic") + ":Data:50",
        _("HRA") + ":Data:50",
        _("LWW") + ":Data:50",
        _("Statutory Bonus") + ":Data:50",
        _("Other Allownance") + ":Data:50"
    ]
    return columns


def get_salary_structure(conditions,filters):
    employee = frappe.db.sql("""Select name, employee_name, department, site,date_of_joining,designation 
    From `tabEmployee` Where status = "Active" and %s """% conditions,filters, as_dict=1)
    row = []
    now_date = frappe.utils.datetime.datetime.now().date()
    start_date = date(now_date.year, now_date.month, 1)
    end_date = date(now_date.year, now_date.month, 31)
    total_working_days = date_diff(end_date, start_date) + 1
    frappe.errprint(total_working_days)
    payment_days = total_working_days
    for emp in employee:
        frappe.errprint(emp)
        st_name = frappe.db.sql("""
            select sa.salary_structure, sa.base
            from `tabSalary Structure Assignment` sa join `tabSalary Structure` ss
            where sa.salary_structure=ss.name
                and sa.docstatus = 1 and ss.docstatus = 1 and ss.is_active ='Yes' and sa.employee = %s
            order by sa.from_date desc
            limit 1
        """,emp.name,as_dict=1)
        if st_name:
            ss = st_name[0]
            # precision = 0
            frappe.errprint(ss)
            salary_component = frappe.db.sql("""select salary_component,abbr,amount,amount_based_on_formula,formula from 
            `tabSalary Detail` where parent = %s """,ss.salary_structure,as_dict=1)
            if salary_component:
                # ss_component = salary_component[0]
                sc = salary_component[0]
                # for sc in ss_component:
                frappe.errprint(salary_component)
                amount = sc.amount
                if sc.amount_based_on_formula:
                    data = frappe._dict()
                    salary_components = frappe.get_all("Salary Component", fields=["salary_component_abbr"])
                    for sca in salary_components:
                        data.setdefault(sca.salary_component_abbr, 0)
                        # data.setdefault(sc.abbr, 0)
                    # for key in data:
                    #     frappe.errprint(key)
                    #     for d in data.get(key):
                    #         frappe.errprint(d)
                    #         data[d.abbr] = d.amount
                    whitelisted_globals = {
                        "int": int,
                        "float": float,
                        "long": int,
                        "round": round,
                        "date": datetime.date,
                        "getdate": getdate,
                        "total_working_days": total_working_days,
                        "payment_days": payment_days
                    }
                    if sc.abbr == "B":
                        formula = sc.formula.strip().replace("\n", " ") if sc.formula else None
                        if formula:
                            frappe.errprint(formula)
                            frappe.errprint(whitelisted_globals)
                            frappe.errprint(data)
                            amount_1 = sc.abbr("amount")
                            frappe.errprint(amount_1)
                            amount = flt(frappe.safe_eval(formula, whitelisted_globals, data), sc.abbr("amount"))
                            frappe.errprint(amount)
                if amount:
                    data[sc.abbr] = amount
                    frappe.errprint(data)


    return row

def get_conditions(filters):
    conditions = ""
    if filters.get("company"): conditions += " company = %(company)s"
    if filters.get("employee"): conditions += " and employee = %(employee)s"
    if filters.get("department"): conditions += " and department = %(department)s"

    return conditions, filters