// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ticket", {
	refresh(frm) {
        // On draft and not yet auto assigned, show Auto Assignment button
        if (frm.doc.docstatus == 0 && !frm.doc.auto_assign) {
            frm.add_custom_button(__("Auto Assignment"), () => {
				frm.set_value("auto_assign", 1);
                frm.save();
			});
        }
        // On resolved and not yet used, show Create Ticket Summary button
        if (frm.doc.status == 'Resolved' && frm.doc.customer && !frm.doc.ref_ticket_summary) {
            frm.add_custom_button(__("Create Ticket Summary"), () => {
                frappe.new_doc("Ticket Summary", { customer: frm.doc.customer })
            });
        }
	},
});
