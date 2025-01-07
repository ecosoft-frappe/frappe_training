// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.listview_settings["Ticket"] = {
	hide_name_column: false,
    // Add fields to list view that was not already in the DocType's list view
	add_fields: ["ref_ticket_summary"],
    // This is when document has field Status
    // Active only when DocType's Document States (colors) is not set
    // And when docstatus = 1, else docstatus = 0 is Draft and 2 is Cancelled 
	get_indicator: function (doc) {
        if (doc.status == "Resolved" && !doc.ref_ticket_summary) {
			return [__("Resolved"), "green", "status,=,Resolved|ref_ticket_summary,is,not set"];
		} else if (doc.status == "Resolved" && doc.ref_ticket_summary) {
			return [__("Ticket Summary"), "green", "status,=,Resolved|ref_ticket_summary,is,set"];
        } else if (doc.status == "Rejected") {
			return [__("Rejected"), "red", "status,=,Rejected"];
		}
	},
	onload: function (listview) {
        var method = "frappe_training.frappe_training.doctype.ticket.ticket.create_ticket_summary";
		listview.page.add_action_item(__("Create Ticket Summary"), function () {
            frappe.call({
                method: method,
                args: { names: listview.get_checked_items(true) },
                freeze: true,
                callback: (r) => {  // Create New Document
                    console.log(r.message)
                    frappe.new_doc("Ticket Summary", {
                        customer: r.message.customer
                    }).then(() => {
                        cur_frm.set_value("tickets", r.message.tickets);
                    });
                },
            });
		});
    }
}