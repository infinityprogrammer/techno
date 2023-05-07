# Copyright (c) 2013, erpcloud.systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("Company"),
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 200
        },

        {
            "label": _("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Cluster"),
            "fieldname": "cost_center",
            "fieldtype": "Link",
            "options": "Cost Center",
            "width": 200
        },
        {
            "label": _("Total Income"),
            "fieldname": "income",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Total Expense"),
            "fieldname": "expence",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Profit"),
            "fieldname": "profit",
            "fieldtype": "Float",
            "width": 150
        }

    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and `tabGL Entry`.posting_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabGL Entry`.posting_date<=%(to_date)s"
    if filters.get("company"):
        conditions += " and `tabGL Entry`.company =%(company)s"
    if filters.get("cost_center"):
        conditions += " and `tabGL Entry`.cluster = %(cluster)s"
    item_results = frappe.db.sql("""
				select
						`tabGL Entry`.company as company,
						`tabGL Entry`.posting_date as posting_date,
						`tabGL Entry`.cluster as cluster,
						`tabGL Entry`.debit as debit,
						`tabGL Entry`.credit as credit

				from
				`tabGL Entry`

				where
				`tabGL Entry`.docstatus = 1
				and `tabGL Entry`.is_cancelled = 0
				{conditions}
				
				order by
				`tabGL Entry`.posting_date asc
                group by `tabGL Entry`.cluster



				""".format(conditions=conditions), filters, as_dict=1)

    # price_list_names = list(set([item.price_list_name for item in item_results]))

    # buying_price_map = get_price_map(price_list_names, buying=1)
    # selling_price_map = get_price_map(price_list_names, selling=1)

    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'company': item_dict.company,
                'posting_date': _(item_dict.posting_date),
                'cluster': _(item_dict.cluster),
                'debit': item_dict.debit,
                'credit': item_dict.credit,
                'balance': item_dict.debit - item_dict.credit,

            }
            result.append(data)

    return result
