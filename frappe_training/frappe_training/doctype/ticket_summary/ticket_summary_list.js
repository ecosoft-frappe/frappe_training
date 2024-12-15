// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.listview_settings["Ticket Summary"] = {
	onload: function (listview) {
		listview.page.add_action_item(__("Sales Invoice"), () => {
			erpnext.bulk_transaction_processing.create(listview, "Ticket Summary", "Sales Invoice");
		});
    }
}