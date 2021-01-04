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

        if ss.np:
            row += [ss.np]
        else:
            row += [0]

        if not ss.ifsc:
            ss.ifsc = frappe.db.get_value("Employee", {'employee': ss.employee}, ['ifsc_no'])
        if ss.ifsc:
            row += ["0300102000016056",ss.ifsc]
        else:
            row += ["0300102000016056",""]

        if ss.acc_no:
            row += [ss.acc_no,"SB A/C"]
        else:
            row += ["","SB A/C"]
        
        if ss.employee_name:
            row += [ss.employee_name,"CHENNAI","RTGS","BOSS"]
        else:
            row += ["","CHENNAI","RTGS","BOSS"]

        data.append(row)
    return columns, data

    # for ss in salary_slips:
    #     row = []

    #     if ss.name:
    #         row = [ss.name]
    #     else:
    #         row = [""]

    #     if ss.employee:
    #         row += [ss.employee]
    #     else:
    #         row += [""]

    #     if ss.employee_name:
    #         row += [ss.employee_name]
    #     else:
    #         row += [""]

    #     client = frappe.db.get_value("Employee", {'employee': ss.employee}, ['client'])
    #     if client:
    #         row += [client]
    #     else:
    #         row += [""]

    #     site = frappe.db.get_value("Employee", {'employee': ss.employee}, ['site'])
    #     if site:
    #         row += [site]
    #     else:
    #         row += [""]

    #     if ss.pd:
    #         row += [ss.pd]
    #     else:
    #         row += [0]

    #     if ss.np:
    #         row += [ss.np]
    #     else:
    #         row += [0]
        
    #     if ss.bank_name:
    #         row += [ss.bank_name]
    #     else:
    #         row += [""]

    #     if ss.acc_no:
    #         row += [ss.acc_no]
    #     else:
    #         row += [""]

    #     if ss.ifsc:
    #         row += [ss.ifsc]
    #     else:
    #         row += [""]

    #     data.append(row)

    # return columns, data


def get_columns():
    # columns = [
    #     _("Salary Slip ID") + ":Data:120",
    #     _("Employee") + ":Data:120",
    #     _("Employee Name") + ":Data:120",
    #     _("Client") + ":Data:100",
    #     _("Site") + ":Data:100",
    #     _("Payment Days") + ":Int:50",
    #     _("Net Pay") + ":Currency:100",
    #     _("Bank Name") + ":Data:120",
    #     _("Account No") + ":Data:120",
    #     _("IFSC No") + ":Data:120"
    # ]
    columns = [
        _("AMT") + ":Data:120",
        _("SENDER A/C") + ":Data:120",
        _("IFSC") + ":Data:120",
        _("RECEIVER A/C") + ":Data:120",
        _("A/C TYPE") + ":Data:120",
        _("BENE NAME") + ":Data:120",
        _("BENE-ADDRESS") + ":Data:120",
        _("PARTICULARS") + ":Data:120",
        _("SENDER NAME") + ":Data:120"
    ]
    return columns


def get_salary_slips(conditions, filters):
    salary_slips = frappe.db.sql("""select ss.name as name,ss.employee as employee,ss.employee_name as employee_name,
    ss.payment_days as pd,ss.net_pay as np,ss.bank_name as bank_name,ss.bank_account_no as acc_no
    ,ss.ifsc_no as ifsc from `tabSalary Slip` ss 
    where %s order by employee""" % conditions, filters, as_dict=1)
    return salary_slips


def get_conditions(filters):
    conditions = ""
    doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

    if filters.get("docstatus"):
        conditions += "docstatus = {0}".format(doc_status[filters.get("docstatus")])

    if filters.get("from_date"): conditions += " and start_date >= %(from_date)s"
    if filters.get("to_date"): conditions += " and end_date <= %(to_date)s"
    if filters.get("client"): conditions += " and client_name = %(client)s"
    if filters.get("site"): conditions += " and site = %(site)s"

    return conditions, filters