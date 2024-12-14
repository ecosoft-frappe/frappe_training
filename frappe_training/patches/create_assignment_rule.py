import frappe
from frappe.model.naming import append_number_if_name_exists

def execute():
    rule_doc = frappe.new_doc("Assignment Rule")
    rule_doc.name = append_number_if_name_exists(
        "Assignment Rule", "Auto Assign Ticket"
    )
    rule_doc.document_type = "Ticket"
    rule_doc.assign_condition = "auto_assign==1"
    rule_doc.priority = 0
    rule_doc.disabled = False
    for day in [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]:
        day_doc = frappe.get_doc({"doctype": "Assignment Rule Day", "day": day})
        rule_doc.append("assignment_days", day_doc)
    rule_doc.append("users", {"user": "Administrator"})
    rule_doc.save(ignore_permissions=True)
    return
