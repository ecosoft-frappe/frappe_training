// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ticket", {
	refresh(frm) {
        if (frm.doc.docstatus == 0 && !frm.doc.auto_assign) {
            frm.add_custom_button(__("Auto Assignment"), () => {
				frm.set_value("auto_assign", 1);
                frm.save();
			});
        }
	},
});
