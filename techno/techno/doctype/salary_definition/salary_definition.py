# Copyright (c) 2023, Ahmed Emam and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalaryDefinition(Document):
	def on_submit(self):
		basic = frappe.db.get_single_value("Salary Definition Setting", "basic")
		insurance = frappe.db.get_single_value("Salary Definition Setting", "insurance")
		commission = frappe.db.get_single_value("Salary Definition Setting", "commission")
		over_time = frappe.db.get_single_value("Salary Definition Setting", "over_time")
		expenses = frappe.db.get_single_value("Salary Definition Setting", "expenses")
		for x in self.salary_definition_employee:
			if x.basic > 0 :
				new_doc = frappe.get_doc(dict(
							doctype='Additional Salary',
							employee=x.employee,
							company=self.company,
							salary_component=basic,
							currency=x.salary_currency,
							amount=x.basic,
							payroll_date=self.payroll_date,
							overwrite_salary_structure_amount=1,
							ref_doctype="Salary Definition",
							ref_docname=self.name
						))
				new_doc.insert()
				new_doc.submit()
			if x.insurance > 0 :
				new_doc = frappe.get_doc(dict(
							doctype='Additional Salary',
							employee=x.employee,
							company=self.company,
							salary_component=insurance,
							currency=x.salary_currency,
							amount=x.insurance,
							payroll_date=self.payroll_date,
							overwrite_salary_structure_amount=1,
							ref_doctype="Salary Definition",
							ref_docname=self.name
						))
				new_doc.insert()
				new_doc.submit()
			if x.commission > 0 :
				new_doc = frappe.get_doc(dict(
							doctype='Additional Salary',
							employee=x.employee,
							company=self.company,
							salary_component=commission,
							currency=x.salary_currency,
							amount=x.commission,
							payroll_date=self.payroll_date,
							overwrite_salary_structure_amount=1,
							ref_doctype="Salary Definition",
							ref_docname=self.name
						))
				new_doc.insert()
				new_doc.submit()
			if x.over_time > 0 :
				new_doc = frappe.get_doc(dict(
							doctype='Additional Salary',
							employee=x.employee,
							company=self.company,
							salary_component=over_time,
							currency=x.salary_currency,
							amount=x.over_time,
							payroll_date=self.payroll_date,
							overwrite_salary_structure_amount=1,
							ref_doctype="Salary Definition",
							ref_docname=self.name
						))
				new_doc.insert()
				new_doc.submit()
			if x.expenses > 0 :
				new_doc = frappe.get_doc(dict(
							doctype='Additional Salary',
							employee=x.employee,
							company=self.company,
							salary_component=expenses,
							currency=x.salary_currency,
							amount=x.expenses,
							payroll_date=self.payroll_date,
							overwrite_salary_structure_amount=1,
							ref_doctype="Salary Definition",
							ref_docname=self.name
						))
				new_doc.insert()
				new_doc.submit()
