// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ticket Summary", {

	setup: function (frm) {
        // Cancel this doc without cancel Ticket that link here
		frm.ignore_doctypes_on_cancel_all = [
			"Ticket",
		];
	},

	refresh(frm) {
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(__("Create Sales Invoice"), () => {
                frappe.new_doc("Sales Invoice", {
                    customer: frm.doc.customer,
                    custom_ref_ticket_summary: frm.doc.name
                }).then( async () => {
                    // Get setting data
                    var item = await frappe.db.get_single_value("Ticket Settings", "ticket_item")
                    var rate = await frappe.db.get_single_value("Ticket Settings", "hours_rate")
                    // Get item detail
                    var item_detail = await frappe.call({
                        method: "erpnext.stock.doctype.item.item.get_item_details",
                        args: {
                            item_code: item,
                            company: cur_frm.doc.company,
                        }
                    })
                    // Set value
                    cur_frm.set_value("items", [{
                        item_code: item_detail.message.item_code,
                        item_name: item_detail.message.item_name,
                        income_account: item_detail.message.income_account,
                        uom: item_detail.message.stock_uom,
                        qty: frm.doc.total_hours,
                        rate: rate
                    }]);
                });
			});
        }
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
