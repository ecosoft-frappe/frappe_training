# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document


class TicketSummary(Document):


	def on_submit(self):
		for t in self.tickets:
			if frappe.db.get_value("Ticket", t.ticket, "ref_ticket_summary"):
				frappe.throw("Ticket {0} already linked to another Ticket Summary".format(t.ticket))
			frappe.db.set_value("Ticket", t.ticket, "ref_ticket_summary", self.name)


	def before_cancel(self):
		# self.flags.ignore_links = True
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
	

@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	from frappe.model.mapper import get_mapped_doc
	from erpnext.stock.doctype.item.item import get_item_details

	def set_missing_values(source, target):
		target.run_method("set_missing_values")
		item = frappe.db.get_single_value("Ticket Settings", "ticket_item")
		rate = frappe.db.get_single_value("Ticket Settings", "hours_rate")
		item_detail = get_item_details(item, target.company)
		target.append(
			"items",
			dict(
				item_code=item_detail.item_code,
				item_name=item_detail.item_name,
				income_account=item_detail.income_account,
				uom=item_detail.stock_uom,
				qty=source.total_hours,
				rate=rate,
				amount=flt(source.total_hours) * flt(rate),
				base_rate=rate,
				base_amount=flt(source.total_hours) * flt(rate)
			),
		)

	doclist = get_mapped_doc(
		"Ticket Summary",
		source_name,
		{
			"Ticket Summary": {
				"doctype": "Sales Invoice",
				"field_map": {
					"customer": "customer",
				},
				"validation": {"docstatus": ["=", 1]},
			},
		},
		target_doc,
		set_missing_values,
	)

	return doclist
