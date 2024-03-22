frappe.query_reports["Project Profitability Summary Dashboard"] = {
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
        {
			"fieldname": "month_name",
			"label": __("Month Name"),
			"fieldtype": "Select",
			"options": "January\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
			"default": "January"  // Set the default to January
		},
    ],
    "onload": function (report) {
        // Add any additional customization or logic when the report loads
    },
};
