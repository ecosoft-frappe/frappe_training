# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

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