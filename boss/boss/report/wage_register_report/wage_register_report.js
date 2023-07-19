// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Wage Register Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From"),
			"fieldtype": "Date",
			"default": [frappe.datetime.add_months(frappe.datetime.get_today(),-1)],
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To"),
			"fieldtype": "Date",
			"default": [frappe.datetime.add_months(frappe.datetime.get_today())],
			"reqd": 1
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname": "docstatus",
			"label": __("Document Status"),
			"fieldtype": "Select",
			"options": ["Draft", "Submitted", "Cancelled"],
			"default": "Draft"
		},
		{
			"fieldname": "client",
			"label": __("Client"),
			"fieldtype": "Link",
			"options": "Client"

		},
		{
			"fieldname": "site",
			"label": __("Site"),
			"fieldtype": "Link",
			"options": "Site",
		}
	]
};
