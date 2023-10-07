// Copyright (c) 2023, Ahmed Emam and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Outstanding Invoices and Average Value"] = {
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
			"reqd": 1,
			"width": "60px"
		},
		// {
		// 	"fieldname":"outstanding_bound",
		// 	"label": __("Outstanding Bound"),
		// 	"fieldtype": "Currency",
		// 	"default": 0,
		// 	"width": "60px"
		// },
	]
};
