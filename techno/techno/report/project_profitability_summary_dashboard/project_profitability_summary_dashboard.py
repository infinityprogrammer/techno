# ... (your imports and license information)

import frappe
from frappe import _
from datetime import datetime, timedelta

def execute(filters=None):
    columns = [
        {"label": _("Project"), "fieldname": "project", "fieldtype": "Data", "width": 160},
        {"label": _(f"Total Income"), "fieldname": f"total_income", "fieldtype": "Float", "width": 200},
        {"label": _(f"Total Expenses"), "fieldname": f"total_expenses", "fieldtype": "Float", "width": 200},
        {"label": _(f"Profit "), "fieldname": f"profit", "fieldtype": "Float", "width": 200},
    ]

    fiscal_year = get_fiscal_year(filters)
    start_date, end_date = get_fiscal_year_dates(fiscal_year)

    month_name = filters.get("month_name")
    month_number = get_month_number(month_name)

    data = []

    project_filter = filters.get("project", None)
    projects = frappe.get_all("Project", filters={"status": "Open", "name": project_filter} if project_filter else {"status": "Open"})

    for project in projects:
        project_doc = frappe.get_doc("Project", project.name)

        start_date, end_date = get_start_and_end_date(fiscal_year, month_number)
        total_income, total_expenses = get_project_financials(project_doc.name, start_date, end_date)

        profit = total_income - total_expenses

        project_row = {
            "project": project_doc.name,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "profit": profit,
        }

        data.append(project_row)

    # Sort data by profit
    data_sorted_by_profit = sorted(data, key=lambda x: x.get('profit', 0), reverse=True)

    return columns, data_sorted_by_profit


def get_project_financials(project, start_date, end_date):
    # Fetch total credit and total expenses from GL entries for the project within the specified date range
    result = frappe.db.sql("""
        SELECT 
            SUM(credit_in_account_currency) AS total_credit,
            SUM(debit_in_account_currency) AS total_expenses
        FROM `tabGL Entry`
        WHERE project = %s
          AND posting_date <= %s
          AND is_cancelled = 0
    """, (project, end_date), as_dict=True)[0]

    return result['total_credit'] or 0, result['total_expenses'] or 0

# (Remaining functions remain unchanged)
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
    try:
        # Try parsing the month name with year
        date_object = datetime.strptime(month_name, "%B %Y")
    except ValueError:
        try:
            # Try parsing the month name without year
            date_object = datetime.strptime(month_name, "%B")
        except ValueError:
            # Handle the case when parsing fails
            raise ValueError(f"Invalid month name: {month_name}")

    # Extract the month number from the datetime object
    month_number = date_object.month

    return month_number



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
