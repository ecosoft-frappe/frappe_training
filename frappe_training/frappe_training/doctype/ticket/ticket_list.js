// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.listview_settings["Ticket"] = {
	hide_name_column: true,
    // Add fields to list view that was not already in the DocType's list view
	add_fields: ["ref_ticket_summary"],
    // From kittiu's observatoin
    // This is when document has field Status
    // Active only when DocType's Document States (colors) is not set
    // And when docstatus = 1, else docstatus = 0 is Draft and 2 is Cancelled 
	get_indicator: function (doc) {
        console.log(doc.docstatus);
        if (doc.status == "Resolved" && !doc.ref_ticket_summary) {
			return [__("Resolved"), "green", "status,=,Resolved|ref_ticket_summary,is,not set"];
		} else if (doc.status == "Resolved" && doc.ref_ticket_summary) {
			return [__("Ticket Summary"), "green", "status,=,Resolved|ref_ticket_summary,is,set"];
        } else if (doc.status == "Rejected") {
			return [__("Rejected"), "red", "status,=,Rejected"];
		}
	}
}