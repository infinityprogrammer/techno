# Copyright (c) 2023, Ahmed Emam and contributors
# For license information, please see license.txt
import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate, cint



def execute(filters=None):
	columns, data = [], []
	
	data = get_data(filters)
	columns = get_columns(filters)

	return columns, data

def get_data(filters):
	invoices = frappe.db.sql(
		"""SELECT
			name,
			customer,customer_code,
			posting_date,
			currency,
			grand_total,
			due_date,
			DATEDIFF(curdate(), due_date) AS due_days,
			outstanding_amount,remarks,
			(SELECT group_concat(description) FROM `tabSales Invoice Item` it where it.parent = inv.name)description
		FROM `tabSales Invoice` inv
		WHERE
			outstanding_amount not between -1 and 1
			AND docstatus = 1
			AND company = %(company)s order by customer_code""",
		{
			'company': filters.get("company"),
		},
		as_dict=1
	)

	return invoices

def get_columns(filters):
	return [
		{
			"label": _("Client"),
			"fieldname": "customer_code",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("Invoice No"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 170,
		},
		{
			"label": _("Invoice Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 130,
		},
		{
			"label": _("Deadline for Payment"),
			"fieldname": "due_date",
			"fieldtype": "Date",
			"width": 160,
		},
		{
			"label": _("Currency"),
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency",
			"width": 100,
		},
		{
			"label": _("Invoice Sum"),
			"fieldname": "grand_total",
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"label": _("Invoice Content"),
			"fieldname": "description",
			"fieldtype": "Data",
			"width": 280,
		},
		{
			"label": _("Current Balance"),
			"fieldname": "outstanding_amount",
			"fieldtype": "Currency",
			"width": 140,
		},
	]