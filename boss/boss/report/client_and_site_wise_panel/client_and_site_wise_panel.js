// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Client and Site Wise Panel"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"hidden": 0,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"hidden": 0,
			"default": frappe.datetime.get_today()
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
