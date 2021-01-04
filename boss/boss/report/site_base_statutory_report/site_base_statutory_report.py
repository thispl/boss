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
        row = []

        if ss.client:
            row = [ss.client]
        else:
            row = [""]

        if ss.site:
            row += [ss.site]
        else:
            row = [""]

        basic = frappe.db.get_value("Salary Detail", {'abbr': 'B', 'parent': ss.name}, ['amount'])
        if basic:
            row += [basic]
        else:
            row += [0]
        
        pf = frappe.db.get_value("Salary Detail", {'abbr': 'PF', 'parent': ss.name}, ['amount'])
        if basic:
            row += [pf]
        else:
            row += [0]

        esi = frappe.db.get_value("Salary Detail", {'abbr': 'ESI', 'parent': ss.name}, ['amount'])
        if esi:
            row += [esi]
        else:
            row += [0]

        pt = frappe.db.get_value("Salary Detail", {'abbr': 'PT', 'parent': ss.name}, ['amount'])
        if pt:
            row += [pt]
        else:
            row += [0]

        ctc = frappe.db.get_value("Salary Detail", {'abbr': 'CTC', 'parent': ss.name}, ['amount'])
        if ctc:
            row += [ctc]
        else:
            row += [0]
        data.append(row)
    return columns, data


def get_columns():
    columns = [
        _("Client") + ":Data:300",
        _("Site") + ":Data:150",
        _("Basic") + ":Currency:120",
        _("PF") + ":Currency:120",
        _("ESI") + ":Currency:120",
        _("PT") + ":Currency:120",
        _("CTC") + ":Currency:120"
    ]
    return columns


def get_salary_slips(conditions, filters):
    # salary_slips = frappe.db.sql("""select sum(`tabSalary Detail`.amount), ss.client_name as client,ss.site as site,ss.name as name from `tabSalary Slip` ss 
    # left join `tabSalary Detail` on ss.name = `tabSalary Detail`.parent
    # where `tabSalary Detail`.salary %s order by site""" % conditions, filters, as_dict=1)
    salary_slips = frappe.db.sql("""select ss.client_name as client,ss.site as site,ss.name as name from `tabSalary Slip` ss
    where %s order by site""" % conditions, filters, as_dict=1)
    return salary_slips


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += "start_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and end_date >= %(to_date)s"
    if filters.get("client"): conditions += " and client_name = %(client)s"
    if filters.get("site"): conditions += " and site = %(site)s"

    return conditions, filters