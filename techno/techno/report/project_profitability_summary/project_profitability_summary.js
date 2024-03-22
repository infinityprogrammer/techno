// Copyright (c) 2023, techno and contributors
// For license information, please see license.txt

frappe.query_reports["Project Profitability Summary"] = {
	"filters": [
		{
			"fieldname": "fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"reqd": 1,
			"default": frappe.datetime.get_today().split("-")[0]  // Set the default to the current fiscal year
		
		},
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
	],
	"onload": function (report) {
		// Add any additional customization or logic when the report loads
	},
};