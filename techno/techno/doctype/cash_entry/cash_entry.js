// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt


frappe.ui.form.on('Cash Entry', 'mode_of_payment',  function(frm) {
   if(cur_frm.doc.payment_type == "Receive"){
       frappe.call({ method: "frappe.client.get_value",
args: { doctype: "Mode of Payment Account",
fieldname: "default_account",
parent: "Mode of Payment",
filters:  { 'parent': cur_frm.doc.mode_of_payment,'company':cur_frm.doc.company},
}, callback: function(r)
{cur_frm.set_value("account_paid_to", r.message.default_account);
  } });
   }
if(cur_frm.doc.payment_type == "Pay"){
       frappe.call({ method: "frappe.client.get_value",
args: { doctype: "Mode of Payment Account",
fieldname: "default_account",
parent: "Mode of Payment",
filters: { 'parent': cur_frm.doc.mode_of_payment,'company':cur_frm.doc.company},
}, callback: function(r)
{cur_frm.set_value("account_paid_from", r.message.default_account);
  } });
   }
});

frappe.ui.form.on('Cash Entry',{

    setup: function(frm) {
  cur_frm.fields_dict['expense_entry_account'].grid.get_field("party_type").get_query = function(doc, cdt, cdn)
  {
  	return {
    filters:  [
    	["DocType","name", "in", ["Employee"]]
    ]
    	};
  };
	}
});
frappe.ui.form.on('Cash Entry',{
    setup: function(frm) {
  cur_frm.fields_dict['expense_entry_account'].grid.get_field("account").get_query = function(doc, cdt, cdn)
  {
  	return {
    filters:  [
    	["Account","is_group", "=", 0]
    ]
    	};
  };
	}
});


frappe.ui.form.on('Cash Entry Account', {
    status: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        if (child.employee == 0) {
            frm.set_df_property('Cash Entry Account', 'party', 'read_only', 1);
        } else {
            frm.set_df_property('Cash Entry Account', 'party', 'read_only', 0);
        }
    }
});

frappe.ui.form.on('Cash Entry',{
    setup: function(frm) {
  cur_frm.fields_dict['expense_entry_account'].grid.get_field("cost_center").get_query = function(doc, cdt, cdn) 
  {
  	return {
    filters:  [
        ["Cost Center", "company", "=", cur_frm.doc.company],
        ["Cost Center","is_group", "=", 0]
    ]
    	};
  };
	}
});

frappe.ui.form.on("Cash Entry", "company", function(frm){
    cur_frm.set_value("mode_of_payment","");
    cur_frm.set_value("account_paid_to","");
    cur_frm.set_value("account_paid_from","");
});