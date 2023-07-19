// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report Register Dashboard', {
	// refresh: function(frm) {

	// }
	download: function (frm) {
		if (frm.doc.sites == 'FORD - HK') {
			var path = "boss.boss.doctype.report_register_dashboard.ford_hk.download"
			var args = 'payroll_date=%(payroll_date)s'
		}
		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				date: frm.doc.Pay,
			});
		}
	}
});
