// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report Dashboard', {
	// refresh: function(frm) {
	// 	frm.disable_save()
	// },
	download: function (frm) {
		if (frm.doc.report == 'Form-26') {
			var path = "boss.boss.doctype.report_dashboard.form_26.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&company=%(company)s&client=%(client)s'
		}
		if (frm.doc.report == 'Common Register') {
			var path = "boss.boss.doctype.report_dashboard.common_register.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&company=%(company)s&client=%(client)s'
		}
		
		if (frm.doc.report == 'DSV Register') {
			var path = "boss.boss.doctype.report_dashboard.dsv_register.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&company=%(company)s'
		}
		if (frm.doc.site == 'DSV - Ford HK') {
			var path = "boss.boss.doctype.report_dashboard.ford_hk.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&site=%(site)s'
		}
		if (frm.doc.site == 'DSV - FORD') {
			var path = "boss.boss.doctype.report_dashboard.ford.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&site=%(site)s'
		}
		if (frm.doc.site == 'DSV - ORAGADAM - RE') {
			var path = "boss.boss.doctype.report_dashboard.oragadam_re.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&site=%(site)s'
		}
		if (frm.doc.site == 'DSV - ORAGADAM - WAREHOUSE') {
			var path = "boss.boss.doctype.report_dashboard.oragadam_warehouse.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&site=%(site)s'
		}
		
		if (frm.doc.site == 'DSV - MM Nagar') {
			var path = "boss.boss.doctype.report_dashboard.mm_nagar.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&site=%(site)s'
		}
		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				// date: frm.doc.date,
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
				company : frm.doc.company || "",
				client : frm.doc.client,
				site : frm.doc.site
				// employment_type:frm.doc.employment_type,
				// plant:frm.doc.plant,
				// shift : frm.doc.shift
			});
		}
	},
});
