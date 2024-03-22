# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from json import loads
from typing import TYPE_CHECKING, List, Optional, Tuple

import frappe
import frappe.defaults
from frappe import _, throw
from frappe.model.meta import get_field_precision
from frappe.utils import (
	cint,
	create_batch,
	cstr,
	flt,
	formatdate,
	get_number_format_info,
	getdate,
	now,
	nowdate,
)
from six import string_types
import erpnext
# imported to enable erpnext.accounts.utils.get_account_currency
from erpnext.accounts.doctype.account.account import get_account_currency  # noqa
from erpnext.stock import get_warehouse_account_map
from erpnext.stock.utils import get_stock_value_on

if TYPE_CHECKING:
	from erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import RepostItemValuation


class FiscalYearError(frappe.ValidationError):
	pass


class PaymentEntryUnlinkError(frappe.ValidationError):
	pass


GL_REPOSTING_CHUNK = 100
import frappe
from frappe import _

# from erpnext.accounts.utils import get_balance_on


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	columns = [
		{
			"label": _("Account"),
			"fieldtype": "Link",
			"fieldname": "account",
			"options": "Account",
			"width": 100,
		},
		{
			"label": _("Currency"),
			"fieldtype": "Link",
			"fieldname": "currency",
			"options": "Currency",
			"hidden": 1,
			"width": 50,
		},
		{
			"label": _("Balance"),
			"fieldtype": "Currency",
			"fieldname": "balance",
			"options": "currency",
			"width": 100,
		},
	]

	return columns


@frappe.whitelist()
def get_fiscal_year(
	date=None, fiscal_year=None, label="Date", verbose=1, company=None, as_dict=False
):
	return get_fiscal_years(date, fiscal_year, label, verbose, company, as_dict=as_dict)[0]

def get_fiscal_years(
	transaction_date=None, fiscal_year=None, label="Date", verbose=1, company=None, as_dict=False
):
	fiscal_years = frappe.cache().hget("fiscal_years", company) or []

	if not fiscal_years:
		# if year start date is 2012-04-01, year end date should be 2013-03-31 (hence subdate)
		cond = ""
		if fiscal_year:
			cond += " and fy.name = {0}".format(frappe.db.escape(fiscal_year))
		if company:
			cond += """
				and (not exists (select name
					from `tabFiscal Year Company` fyc
					where fyc.parent = fy.name)
				or exists(select company
					from `tabFiscal Year Company` fyc
					where fyc.parent = fy.name
					and fyc.company=%(company)s)
				)
			"""

		fiscal_years = frappe.db.sql(
			"""
			select
				fy.name, fy.year_start_date, fy.year_end_date
			from
				`tabFiscal Year` fy
			where
				disabled = 0 {0}
			order by
				fy.year_start_date desc""".format(
				cond
			),
			{"company": company},
			as_dict=True,
		)

		frappe.cache().hset("fiscal_years", company, fiscal_years)

	if not transaction_date and not fiscal_year:
		return fiscal_years

	if transaction_date:
		transaction_date = getdate(transaction_date)

	for fy in fiscal_years:
		matched = False
		if fiscal_year and fy.name == fiscal_year:
			matched = True

		if (
			transaction_date
			and getdate(fy.year_start_date) <= transaction_date
			and getdate(fy.year_end_date) >= transaction_date
		):
			matched = True

		if matched:
			if as_dict:
				return (fy,)
			else:
				return ((fy.name, fy.year_start_date, fy.year_end_date),)

	error_msg = _("""{0} {1} is not in any active Fiscal Year""").format(
		label, formatdate(transaction_date)
	)
	if company:
		error_msg = _("""{0} for {1}""").format(error_msg, frappe.bold(company))

	if verbose == 1:
		frappe.msgprint(error_msg)
	raise FiscalYearError(error_msg)


def get_conditions(filters):
    conditions = {}

    if filters.account:
        conditions["account"] = filters.account

    if filters.account_type:
        conditions["account_type"] = filters.account_type

    if filters.company:
        conditions["company"] = filters.company

    if filters.root_type:
        conditions["root_type"] = filters.root_type

    return conditions



def get_data(filters):
    data = []
    conditions = get_conditions(filters)

    if filters.account:
        # If an account is specified, get data for that specific account
        account = frappe.get_doc("Account", filters.account)
        balance = get_balance_on(account=account.name, date=filters.report_date)
        row = {"account": account.name, "balance": balance, "currency": account.account_currency}
        data.append(row)
    else:
        # If no specific account is specified, fetch data for all accounts based on the filters
        accounts = frappe.db.get_all(
            "Account", fields=["name", "account_currency"], filters=conditions, order_by="name"
        )

        for account in accounts:
            balance = get_balance_on(account=account.name, date=filters.report_date)
            row = {"account": account.name, "balance": balance, "currency": account.account_currency}
            data.append(row)

    return data

@frappe.whitelist()
def get_balance_on(
	account=None,
	date=None,
	party_type=None,
	party=None,
	company=None,
	in_account_currency=True,
	cost_center=None,
	ignore_account_permission=False,
):
	if not account and frappe.form_dict.get("account"):
		account = frappe.form_dict.get("account")
	if not date and frappe.form_dict.get("date"):
		date = frappe.form_dict.get("date")
	if not party_type and frappe.form_dict.get("party_type"):
		party_type = frappe.form_dict.get("party_type")
	if not party and frappe.form_dict.get("party"):
		party = frappe.form_dict.get("party")
	if not cost_center and frappe.form_dict.get("cost_center"):
		cost_center = frappe.form_dict.get("cost_center")

	cond = ["is_cancelled=0"]
	if date:
		cond.append("posting_date <= %s" % frappe.db.escape(cstr(date)))
	else:
		# get balance of all entries that exist
		date = nowdate()

	if account:
		acc = frappe.get_doc("Account", account)

	try:
		year_start_date = get_fiscal_year(date, company=company, verbose=0)[1]
	except FiscalYearError:
		if getdate(date) > getdate(nowdate()):
			# if fiscal year not found and the date is greater than today
			# get fiscal year for today's date and its corresponding year start date
			year_start_date = get_fiscal_year(nowdate(), verbose=1)[1]
		else:
			# this indicates that it is a date older than any existing fiscal year.
			# hence, assuming balance as 0.0
			return 0.0

	if account:
		report_type = acc.report_type
	else:
		report_type = ""

	if cost_center and report_type == "Profit and Loss":
		cc = frappe.get_doc("Cost Center", cost_center)
		if cc.is_group:
			cond.append(
				""" exists (
				select 1 from `tabCost Center` cc where cc.name = gle.cost_center
				and cc.lft >= %s and cc.rgt <= %s
			)"""
				% (cc.lft, cc.rgt)
			)

		else:
			cond.append("""gle.cost_center = %s """ % (frappe.db.escape(cost_center, percent=False),))

	if account:

		if not (frappe.flags.ignore_account_permission or ignore_account_permission):
			acc.check_permission("read")

		if report_type == "Profit and Loss":
			# for pl accounts, get balance within a fiscal year
			cond.append(
				"posting_date >= '%s' and voucher_type != 'Period Closing Voucher'" % year_start_date
			)
		# different filter for group and ledger - improved performance
		if acc.is_group:
			cond.append(
				"""exists (
				select name from `tabAccount` ac where ac.name = gle.account
				and ac.lft >= %s and ac.rgt <= %s
			)"""
				% (acc.lft, acc.rgt)
			)

			# If group and currency same as company,
			# always return balance based on debit and credit in company currency
			if acc.account_currency == frappe.get_cached_value("Company", acc.company, "default_currency"):
				in_account_currency = False
		else:
			cond.append("""gle.account = %s """ % (frappe.db.escape(account, percent=False),))

	if party_type and party:
		cond.append(
			"""gle.party_type = %s and gle.party = %s """
			% (frappe.db.escape(party_type), frappe.db.escape(party, percent=False))
		)

	if company:
		cond.append("""gle.company = %s """ % (frappe.db.escape(company, percent=False)))

	if account or (party_type and party):
		if in_account_currency:
			select_field = "sum(debit_in_account_currency) - sum(credit_in_account_currency)"
		else:
			select_field = "sum(debit) - sum(credit)"
		bal = frappe.db.sql(
			"""
			SELECT {0}
			FROM `tabGL Entry` gle
			WHERE {1}""".format(
				select_field, " and ".join(cond)
			)
		)[0][0]

		# if bal is None, return 0
		return flt(bal)

