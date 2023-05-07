// Copyright (c) 2023, Ahmed Emam and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Profit and Loss"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_start_date"),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_end_date"),
			"reqd": 1
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options" : "Company",
			"reqd": 0
		},

		{
			"fieldname":"cluster",
			"label": __("Cluster"),
			"fieldtype": "Link",
            "options" : "cluster",
			"reqd": 0
		}
	]
}
