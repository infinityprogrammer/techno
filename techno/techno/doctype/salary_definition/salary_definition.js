// Copyright (c) 2023, Ahmed Emam and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Definition', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Salary Definition',{
    setup: function(frm) {
  cur_frm.fields_dict['salary_definition_employee'].grid.get_field("employee").get_query = function(doc, cdt, cdn) 
  {
  	return {
    filters:  [
        ["Employee", "company", "=", cur_frm.doc.company],
        ["Employee","status", "=", "Active"]
    ]
    	};
  };
	}
});
