# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TicketSummary(Document):


	def on_submit(self):
		for t in self.tickets:
			if frappe.db.get_value("Ticket", t.ticket, "ref_ticket_summary"):
				frappe.throw("Ticket {0} already linked to another Ticket Summary".format(t.ticket))
			frappe.db.set_value("Ticket", t.ticket, "ref_ticket_summary", self.name)


	def before_cancel(self):
		self.flags.ignore_links = True
		for t in self.tickets:
			frappe.db.set_value("Ticket", t.ticket, "ref_ticket_summary", "")


	@frappe.whitelist()
	def get_resolved_tickets(self):
		tickets = frappe.get_list(
			"Ticket",
			filters={
				"status": "Resolved",
				"docstatus": 1,
				"hours": [">", 0],
				"customer": self.customer,
				"ref_ticket_summary": "",
			},
			fields=["name", "hours"]
		)
		return (tickets, sum([t.hours for t in tickets]))
	
