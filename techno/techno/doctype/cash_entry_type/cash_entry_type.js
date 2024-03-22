// Copyright (c) 2023, Ahmed Emam and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Entry Type', {
	// refresh: function(frm) {

	// }
});
cur_frm.cscript.onload_post_render = function() {
    // set the filter for the child table
    cur_frm.fields_dict['accounts'].grid.get_field('default_account').get_query = function(doc, cdt, cdn) {
        var child = locals[cdt][cdn];
        var company = child.company;
        return {
            filters: [
				["Account", "company", "=", company],
				["Account","is_group", "=", 0]
            ]
        };
	};
	cur_frm.fields_dict['accounts'].grid.get_field('cost_center').get_query = function(doc, cdt, cdn) {
        var child = locals[cdt][cdn];
        var company = child.company;
        return {
            filters: [
				["Cost Center", "company", "=", company],
				["Cost Center","is_group", "=", 0]
            ]
        };
    };
};

// cur_frm.cscript.onload_post_render = function() {
//     // set the filter for the child table
//     cur_frm.fields_dict['accounts'].grid.get_field('cost_center').get_query = function(doc, cdt, cdn) {
//         var child = locals[cdt][cdn];
//         var company = child.company;
//         return {
//             filters: [
// 				["Cost Center", "company", "=", company],
// 				["Cost Center","is_group", "=", 0]
//             ]
//         };
//     };
// };

