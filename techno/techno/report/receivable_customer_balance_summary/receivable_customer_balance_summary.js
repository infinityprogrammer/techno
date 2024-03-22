// Copyright (c) 2023, Ahmed Emam and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Receivable Customer Balance Summary"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"till_date",
			"label": __("Till Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"from_value",
			"label": __("From Value"),
			"fieldtype": "Int",
		},
		{
			"fieldname":"to_value",
			"label": __("To Value"),
			"fieldtype": "Int",
		},
		{
			"fieldname":"group_customer",
			"label": __("Group By Customer"),
			"fieldtype": "Check",
		},
	]
};
