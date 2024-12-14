// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ticket Summary", {

	setup: function (frm) {
        // Cancel this doc without cancel Ticket that link here
		frm.ignore_doctypes_on_cancel_all = [
			"Ticket",
		];
	},

	customer(frm) {
        frappe.call({
            method: "get_resolved_tickets",
            doc: frm.doc,
            callback: function (r) {
                cur_frm.clear_table("tickets");
                r.message[0].forEach(function (element) {
                    var c = frm.add_child("tickets");
                    c.ticket = element.name;
                    c.hours = element.hours;
                });
                frm.doc.total_hours = r.message[1];
                frm.refresh_fields()
            },
        });
	},
});
