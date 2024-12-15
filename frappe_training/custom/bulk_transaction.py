def get_task_mapper():
	from frappe_training.frappe_training.doctype.ticket_summary import ticket_summary
	mapper = {
		"Ticket Summary": {
			"Sales Invoice": ticket_summary.make_sales_invoice,
		},
	}
	return mapper