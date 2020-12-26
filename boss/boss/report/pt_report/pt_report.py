# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt


def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()

    data = []
    row = []
    conditions, filters = get_conditions(filters)
    total = 0
    salary_slips = get_salary_slips(conditions, filters)

    for ss in salary_slips:
        # employee = frappe.db.get_value(
        #     "Employee", {'employee': ss.employee}, ['esi_number'])
        # if esino:
        #     row = [esino]
        # else:
        #     row = [0]

        if ss.employee:
            row += [ss.employee]
        else:
            row += [0]

        if ss.employee_name:
            row += [ss.employee_name]
        else:
            row += [0]

        if ss.md:
            row += [ss.md]
        else:
            row += [0]

        if ss.gp:
            row += [ss.gp]
        else:
            row += [0]
        pt = frappe.db.get_value(
            "Salary Detail", {'abbr': 'PT', 'parent': ss.name}, ['amount'])
        if pt:
            row += [pt]
        else:
            row += [""]

        if row[4]:
            data.append(row)

    return columns, data


def get_columns():
    columns = [
        _("Employee") + ":Data:50",
        _("Employee Name") + ":Data:90",
        _("Payment Days") + ":Int:50",
        _("Gross Pay") + ":Currency:100",
        _("PT") + ":Currency:100"

    ]
    return columns


def get_salary_slips(conditions, filters):
    salary_slips = frappe.db.sql("""select ss.employee as employee,ss.employee_name as employee_name,ss.name as name,ss.payment_days as md,ss.gross_pay as gp from `tabSalary Slip` ss 
    where %s order by employee""" % conditions, filters, as_dict=1)
    return salary_slips


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += "start_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and end_date >= %(to_date)s"

    return conditions, filters
