# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt
import json
import frappe
from frappe.model.document import Document


class Ticket(Document):
	

	def before_validate(self):
		self.hours = 0.0
		for t in self.tasks:
			self.hours = t.hours + self.hours


	def before_save(self):
		if self.status == "Resolved" and self.hours == 0:
			frappe.msgprint("Please fill in hours")

	
	def before_submit(self):
		if not self.status:
			frappe.throw("Please choose status as Resolved/Rejected before submit")


@frappe.whitelist()
def validate_ticket_summary_creation(names):
	names = json.loads(names)
	tickets = frappe.db.get_all("Ticket", filters={"name": ["in", names]}, fields=["name", "customer", "status", "hours", "ref_ticket_summary"])
	# Test that all names must be in the same customer, resolved and not linked to any Ticket Summary
	customer = list(set(t["customer"] for t in tickets))
	status = list(set(t["status"] for t in tickets))
	ref_ticket_summary = list(set(t["ref_ticket_summary"] for t in tickets))
	if len(customer) != 1 and not customer[0]:
		frappe.throw("All tickets must be of the same customer")
	if status != ["Resolved"]:
		frappe.throw("All tickets must be Resolved")
	if ref_ticket_summary != [None]:
		frappe.throw("All tickets must not linked to any Ticket Summary")
	# Return Customer and Tickets, i..e, 
	# {
	# 	"customer": "Cust1",
	# 	"tickets": [
	# 		{'ticket': 'FT-00002', 'hours': 1},
	# 	]
	# }
	return {
		"customer": customer[0],
		"tickets": list([{"ticket": t.name, "hours": t.hours} for t in tickets])
	}
