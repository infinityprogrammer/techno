// Copyright (c) 2023, Ahmed Emam and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cashflow Simple"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		// {
		// 	"fieldname":"bank_account",
		// 	"label": __("Bank Account"),
		// 	"fieldtype": "Link",
		// 	"options": "Account",
		// 	"reqd": 1,
		// 	"get_query": function() {
        //         return {
        //             "filters": [
        //                 ["Account", "account_type", "=", "Bank"],
        //                 ["Account", "company", "=", frappe.query_report.get_filter_value("company")],
        //             ]
        //         };
        //     }
		// },
		{
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
			"options": "Fiscal Year",
			"reqd": 1,
			"width": "60px"
		},
	]
};
