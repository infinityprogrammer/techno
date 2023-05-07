from frappe import _

def execute(filters=None):
    columns = [
        _("Account") + ":Link/Account:200",
        _("Total Debit") + ":Currency:120",
        _("Total Credit") + ":Currency:120"
    ]
    data = []

    # Filter for GL Entries
    gl_filters = {
        "doctype": "GL Entry",
        "posting_date": ["between", [filters.get("from_date"), filters.get("to_date")]],
        "account_type": ["in", ["Income", "Expense"]]
    }

    # Filter for Income Accounts
    income_account_filters = {
        "account_type": "Income"
    }

    # Filter for Expense Accounts
    expense_account_filters = {
        "account_type": "Expense"
    }

    # Get Income Accounts
    income_accounts = frappe.get_all("Account",
        filters=income_account_filters,
        pluck="name"
    )
    for account in income_accounts:
        account_data = frappe.db.sql("""
            SELECT SUM(debit) AS debit, SUM(credit) AS credit
            FROM `tabGL Entry`
            WHERE account=%s AND {conditions}
        """.format(conditions=frappe.db.build_conditions(gl_filters)),
            (account,)
        )[0]
        if account_data.debit or account_data.credit:
            data.append([account, account_data.debit, account_data.credit])

    # Get Total Income
    total_income = {
        "Account": _("Total Income"),
        "Total Debit": sum(row[1] for row in data),
        "Total Credit": sum(row[2] for row in data)
    }
    if total_income["Total Debit"] or total_income["Total Credit"]:
        data.append([
            total_income["Account"], total_income["Total Debit"], total_income["Total Credit"]
        ])

    # Get Expense Accounts
    expense_accounts = frappe.get_all("Account",
        filters=expense_account_filters,
        pluck="name"
    )
    for account in expense_accounts:
        account_data = frappe.db.sql("""
            SELECT SUM(debit) AS debit, SUM(credit) AS credit
            FROM `tabGL Entry`
            WHERE account=%s AND {conditions}
        """.format(conditions=frappe.db.build_conditions(gl_filters)),
            (account,)
        )[0]
        if account_data.debit or account_data.credit:
            data.append([account, account_data.debit, account_data.credit])

    # Get Total Expenses
    total_expenses = {
        "Account": _("Total Expenses"),
        "Total Debit": sum(row[1] for row in data) - total_income["Total Debit"],
        "Total Credit": sum(row[2] for row in data) - total_income["Total Credit"]
    }
    if total_expenses["Total Debit"] or total_expenses["Total Credit"]:
        data.append([
            total_expenses["Account"], total_expenses["Total Debit"], total_expenses["Total Credit"]
        ])

    # Calculate Net Income/Loss
    net_income_loss = {
        "Account": _("Net Income/Loss"),
        "Total Debit": total_income["Total Debit"] - total_expenses["Total Debit"],
        "Total Credit": total_income["Total Credit"] - total_expenses["Total Credit"]
    }
    if net_income_loss["Total Debit"] or net_income_loss["Total Credit"]:
        data.append([
            net_income_loss["Account"], net_income_loss["Total Debit"], net_income_loss["Total Credit"]
        ])

    return