// Copyright (c) 2023, Ahmed Emam and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cash flow Exchange Rate"] = {
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
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"exchange_rate",
			"label": __("Exchange Rate"),
			"fieldtype": "Float",
			"default": 1,
			"width": "60px"
		},
	]
};
