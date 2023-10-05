# Copyright (c) 2023, Ahmed Emam and contributors
# For license information, please see license.txt

import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate


def execute(filters=None):
	columns, data = [], []
	if not filters.get("company"):
		return

	data = get_data(filters)
	columns = get_columns(filters)

	return columns, data

def get_all_customer(company):

	customers = frappe.db.sql(
        """SELECT distinct customer FROM `tabSales Invoice` 
		where outstanding_amount != 0 and docstatus = 1 and company = '{0}'""".format(company),
        as_dict=1,
    )

	return customers

def get_data(filters):
	data_inv = []
	customer_list = get_all_customer(filters.get("company"))

	for customer in customer_list:

		invoices = frappe.db.sql(
			"""SELECT name, customer,posting_date, currency, grand_total,
				due_date,DATEDIFF(curdate(), due_date)due_days, outstanding_amount, 
				(DATEDIFF(curdate(), due_date) * outstanding_amount)val_out
				FROM `tabSales Invoice` where outstanding_amount != 0 and docstatus = 1
				and customer = '{0}' and company = '{1}'""".format(customer.customer, filters.get("company")),
			as_dict=1,
		)
		due_days_sum = 0
		outstanding_sum = 0
		last_customer = None
		value_outstanding_sum = 0

		for inv in invoices:
			context = {}
			context['invoice_no'] = inv.name
			context['customer_code'] = inv.customer
			context['customer_name'] = inv.customer
			context['posting_date'] = inv.posting_date
			context['grand_total'] = inv.grand_total
			context['currency'] = inv.currency
			context['due_date'] = inv.due_date
			context['due_days'] = inv.due_days
			context['customer_balance'] = inv.outstanding_amount
			context['total_balance'] = inv.outstanding_amount
			context['value_outstanding'] = inv.due_days * inv.outstanding_amount

			due_days_sum += inv.due_days
			outstanding_sum += inv.outstanding_amount
			value_outstanding_sum += inv.due_days * inv.outstanding_amount
			last_customer = inv.customer

			data_inv.append(context)
		
		cons_context = {}
		cons_context['customer_code'] = f"<b>{last_customer}</b>"
		cons_context['customer_name'] = last_customer
		cons_context['due_days'] = due_days_sum
		cons_context['customer_balance'] = outstanding_sum
		cons_context['value_outstanding'] = value_outstanding_sum
		cons_context['avg_value_outstanding'] = value_outstanding_sum / due_days_sum
		
		data_inv.append(cons_context)

	return data_inv


def get_columns(filters):
	return [
		{
			"label": _("Invoice No"),
			"fieldname": "invoice_no",
			"fieldtype": "Data",
			"width": 170,
		},
		{
			"label": _("Customer Code"),
			"fieldname": "customer_code",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Customer Name"),
			"fieldname": "customer_name",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150,
		},
		{
			"label": _("Invoice Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 130,
		},
		{
			"label": _("Grand Total"),
			"fieldname": "grand_total",
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"label": _("Currency"),
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency",
			"width": 100,
		},
		{
			"label": _("Due Date"),
			"fieldname": "due_date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"label": _("Due Days"),
			"fieldname": "due_days",
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"label": _("Customer Balance"),
			"fieldname": "customer_balance",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Total Balance"),
			"fieldname": "total_balance",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Value Outstanding"),
			"fieldname": "value_outstanding",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Average Value Outstanding"),
			"fieldname": "avg_value_outstanding",
			"fieldtype": "Currency",
			"width": 200,
		}
	]