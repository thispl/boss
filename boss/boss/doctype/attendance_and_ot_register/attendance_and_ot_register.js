// Copyright (c) 2020, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance and OT Register', {
	// refresh: function(frm) {

	// }
	start_date: function (frm) {
		frappe.call({
			method: 'boss.boss.doctype.attendance_and_ot_register.attendance_and_ot_register.get_end_date',
			args: {
				frequency: "monthly",
				start_date: frm.doc.start_date
			},
			callback: function (r) {
				if (r.message) {
					frm.set_value('end_date', r.message.end_date);
				}
			}
		});
	},
});
