import frappe
from frappe.utils import get_link_to_form


def check_duplicated_ticket_summary(doc, method):
    # Make sure that ticket summary is not linked twice in Sales Invoice
    existing_ts = frappe.get_all(
        "Sales Invoice",    
        filters={
            "custom_ref_ticket_summary": doc.custom_ref_ticket_summary,
            "docstatus": ["!=", 2],
            "name": ["!=", doc.name]
        },
        pluck="name"
    )
    if existing_ts:
        frappe.throw(
            "Ticket Summary {0} already linked to another Sales Invoice {1}".format(
                get_link_to_form("Ticket Summary", doc.custom_ref_ticket_summary),
                get_link_to_form("Sales Invoice", existing_ts[0])
            )
        )
