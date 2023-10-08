# Copyright (c) 2023, Ahmed Emam and contributors
# For license information, please see license.txt
import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate, cint



def execute(filters=None):
	columns, data = [], []
	
	data = get_data(filters)
	columns = get_columns(filters)

	if filters.get("group_customer"):
		return columns, data

	customer_totals = {}
	index_dict = {}

	# Iterate through the list of dictionaries
	for index, entry in enumerate(data):
		customer = entry['customer_code']
		outstanding_amount = entry['outstanding_amount']
		# Check if the customer is already in the dictionary, if not, initialize it to 0
		if customer not in customer_totals:
			customer_totals[customer] = 0
		
		# Add the total to the customer's running total
		customer_totals[customer] += outstanding_amount
	
	for index, entry in enumerate(data):
		customer = entry['customer_code']

		# Check if the customer is already in the index_dict
		if customer not in index_dict:
			index_dict[customer] = index
		else:
			# If the customer is already in the index_dict, update the end index
			index_dict[customer] = index

	
	ind = 1
	for key, value in customer_totals.items():
		append_dict = {}
		indx = index_dict.get(key)+ind # last 0
		print(key, index_dict.get(key), value, indx)
		
		append_dict['outstanding_amount'] = value
		data.insert(indx, append_dict)
		ind += 1

	return columns, data

def get_data(filters):

	bound_val = ""

	if filters.get("from_value") and filters.get("to_value"):
		bound_val += "outstanding_amount not between %(from_value)s and %(to_value)s and outstanding_amount != 0"
	else:
		bound_val += "outstanding_amount not between -1 and 1"

	if filters.get("group_customer"):
		invoices = frappe.db.sql(
			"""SELECT
				customer,customer_code,
				currency,
				outstanding_amount
			FROM `tabSales Invoice` inv
			WHERE
				{bound_val}
				AND docstatus = 1
				AND posting_date <= %(posting_date)s
				AND company = %(company)s group by customer,customer_code, currency
				order by customer_code""".format(bound_val=bound_val),
			{
				'company': filters.get("company"),
				'posting_date': filters.get("till_date"),
				'from_value': filters.get("from_value"),
				'to_value': filters.get("to_value"),
			},
			as_dict=1
		)

		return invoices

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
			{bound_val}
			AND docstatus = 1
			AND posting_date <= %(posting_date)s
			AND company = %(company)s order by customer_code""".format(bound_val=bound_val),
		{
			'company': filters.get("company"),
			'posting_date': filters.get("till_date"),
			'from_value': filters.get("from_value"),
			'to_value': filters.get("to_value"),
		},
		as_dict=1
	)

	return invoices

def get_columns(filters):

	if filters.get("group_customer"):
		return [
		{
			"label": _("Client"),
			"fieldname": "customer_code",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("Currency"),
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency",
			"width": 100,
		},
		{
			"label": _("Current Balance"),
			"fieldname": "outstanding_amount",
			"fieldtype": "Currency",
			"width": 140,
		},
	]

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