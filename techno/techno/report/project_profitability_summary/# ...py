# ... (your imports and license information)

import calendar
import frappe
from frappe import _
from datetime import datetime, timedelta


def execute(filters=None):
	columns = [
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Data", "width": 160},
	]

	fiscal_year = get_fiscal_year(filters)
	start_date, end_date = get_fiscal_year_dates(fiscal_year)

	month_name = filters.get("month_name")

	columns.extend([
		{"label": _(f"Total Income {month_name}"), "fieldname": f"total_income_{month_name}", "fieldtype": "Currency", "width": 200},
		{"label": _(f"Total Expenses {month_name}"), "fieldname": f"total_expenses_{month_name}", "fieldtype": "Currency", "width": 200},
		{"label": _(f"Profit {month_name}"), "fieldname": f"profit_{month_name}", "fieldtype": "Currency", "width": 200},
	])

	data = []  # Initialize data as an empty list

	project_filter = filters.get("project", None)

	for project in frappe.get_all("Project", filters={"status": "Open", "name": project_filter} if project_filter else {"status": "Open"}):
		project_doc = frappe.get_doc("Project", project.name)

		project_row = {
			"project": project_doc.name,
			"project_name": project_doc.get("project_name") or project.name,
		}

		month_name = filters.get("month_name")
		month_number = get_month_number(month_name)

		start_date1, end_date1 = get_start_and_end_date(fiscal_year, month_number)
		total_income = get_total_income(project_doc.name, start_date1, end_date1)
		total_expenses = get_total_expenses(project_doc.name, start_date1, end_date1)
		profit = total_income - total_expenses

		project_row[f"total_income_{month_name}"] = total_income
		project_row[f"total_expenses_{month_name}"] = total_expenses
		project_row[f"profit_{month_name}"] = profit

	data.append(project_row)  # Append project_row to the data list

	return columns, data


def get_fiscal_year(filters):
	"""Return fiscal year based on filters"""
	
	fiscal_year = filters.get("fiscal_year")
	
	if not fiscal_year:
		"""If fiscal year not in filters, get default fiscal year"""
		
		fiscal_year = frappe.get_value("Fiscal Year", {"company": filters.get("company"), "is_default": 1}, "name")
	
	return fiscal_year

def get_fiscal_year_dates(fiscal_year):
	fiscal_year_data = frappe.get_doc("Fiscal Year", fiscal_year)
	start_date = fiscal_year_data.year_start_date
	end_date = fiscal_year_data.year_end_date
	return start_date, end_date

def get_total_income(project, start_date, end_date):
	# Fetch total credit from GL entries for the project within the specified date range
	total_credit = frappe.db.sql("""
		SELECT SUM(credit_in_account_currency) AS total_credit
		FROM `tabGL Entry`
		WHERE project = %s
		  AND posting_date BETWEEN %s AND %s
		  AND is_cancelled = 0
	""", (project, start_date, end_date), as_dict=True)[0]['total_credit']

	return total_credit or 0

def get_total_expenses(project, start_date, end_date):
	# Fetch total expenses for the project within the specified date range
	total_expenses = frappe.db.sql("""
		SELECT SUM(debit_in_account_currency) AS total_expenses
		FROM `tabGL Entry`
		WHERE project = %s
		  AND posting_date BETWEEN %s AND %s
		  AND is_cancelled = 0
	""", (project, start_date, end_date), as_dict=True)[0]['total_expenses']

	return total_expenses or 0

def get_months_in_range(start_date, end_date):
	current_date = start_date
	while current_date <= end_date:
		yield current_date.month
		current_date = frappe.utils.add_months(current_date, 1)



def get_start_and_end_date(year, month_number):
	# Convert year and month_number to integers
	year = int(year)
	month_number = int(month_number)

	# Ensure month_number is in the valid range 1 to 12
	month_number = (month_number - 1) % 12 + 1

	# Calculate the first day of the month
	start_date = datetime(year, month_number, 1).date()

	# Calculate the last day of the month
	if month_number == 12:
		end_date = (datetime(year + 1, 1, 1) - timedelta(days=1)).date()
	else:
		end_date = (datetime(year, month_number + 1, 1) - timedelta(days=1)).date()

	return start_date, end_date


def get_month_number(month_name):
	# Convert the month name to a datetime object with a specific day (e.g., 1st day of the month)
	date_object = datetime.strptime(month_name, "%B %Y")  # Assuming the month_name is in the format "Month Year"
	
	# Extract the month number from the datetime object
	month_number = date_object.month
	
	return month_number