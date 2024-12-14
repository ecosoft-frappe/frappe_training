// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", {

	refresh: function (frm) {
        frm.add_custom_button(__("Create Ticket Summary"), () => {
            frappe.route_options = {
                "customer": frm.doc.name
            };
            frappe.set_route("Form", "Ticket Summary", "new");
        }, "Actions");
	},

});
