import functools, itertools
from locale import currency

import frappe
from frappe import _
from frappe.query_builder import functions as fn
from frappe.utils import flt, getdate
from pypika import Case
from pypika.terms import Bracket, ExistsCriterion, LiteralValue


from frappe import _
from frappe.utils import flt, getdate

from erpnext.accounts.doctype.financial_report_template.financial_report_engine import (
    FinancialReportEngine,
    get_xlsx_styles,  #! DO NOT REMOVE - hook for styling
)

import erpnext.accounts.report.financial_statements as fs
import erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement as pnl

# Import the execute function from the standard P&L report
from erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement import (
    execute as standard_pnl_execute,
)
from .constants import (
    GUV_POSITIONS,
    HERSTELLUNGSKOSTEN,
    VERTRIEBSKOSTEN,
    VERTRIEBSKOSTEN_PREFIX,
    VERWALTUNGSKOSTEN,
    VERWALTUNGSKOSTEN_PREFIX,
    SONSTIGE_AUFWENDUNGEN,
    SONSTIGE_AUFWENDUNGEN_PREFIX,
    CC_HERSTELLUNG,
    CC_VERTRIEB,
    CC_VERWALTUNG,
    CC_SONSTIGE,
)

import copy


#! overwrite function from financial_statement.py
def get_data(
    company,
    root_type,
    balance_must_be,
    period_list,
    filters=None,
    accumulated_values=1,
    only_current_fiscal_year=True,
    ignore_closing_entries=False,
    ignore_accumulated_values_for_fy=False,
    total=True,
):
    accounts = fs.get_accounts(company, root_type)
    if not accounts:
        return None

    # ! --- code for UKV ---
    if root_type == "Expense":
        accounts = copy_account_hierarchy(
            accounts, HERSTELLUNGSKOSTEN, VERTRIEBSKOSTEN, VERTRIEBSKOSTEN_PREFIX
        )
        accounts = copy_account_hierarchy(
            accounts, HERSTELLUNGSKOSTEN, VERWALTUNGSKOSTEN, VERWALTUNGSKOSTEN_PREFIX
        )
        accounts = copy_account_hierarchy(
            accounts,
            HERSTELLUNGSKOSTEN,
            SONSTIGE_AUFWENDUNGEN,
            SONSTIGE_AUFWENDUNGEN_PREFIX,
        )

    accounts, accounts_by_name, parent_children_map = fs.filter_accounts(accounts)

    company_currency = fs.get_appropriate_currency(company, filters)

    gl_entries_by_account = {}
    for root in frappe.db.sql(
        """select lft, rgt from tabAccount
			where root_type=%s and ifnull(parent_account, '') = ''""",
        root_type,
        as_dict=1,
    ):
        fs.set_gl_entries_by_account(
            company,
            period_list[0]["year_start_date"] if only_current_fiscal_year else None,
            period_list[-1]["to_date"],
            filters,
            gl_entries_by_account,
            root.lft,
            root.rgt,
            root_type=root_type,
            ignore_closing_entries=ignore_closing_entries,
        )

    calculate_values(
        accounts_by_name,
        gl_entries_by_account,
        period_list,
        accumulated_values,
        ignore_accumulated_values_for_fy,
    )
    fs.accumulate_values_into_parents(accounts, accounts_by_name, period_list)
    out = fs.prepare_data(
        accounts,
        balance_must_be,
        period_list,
        company_currency,
        accumulated_values=filters.accumulated_values,
    )
    out = fs.filter_out_zero_value_rows(
        out, parent_children_map, filters.show_zero_values
    )

    # if out and total:
    #     fs.add_total_row(out, root_type, balance_must_be, period_list, company_currency)

    return out


def copy_account_hierarchy(
    accounts_list: list[dict],
    source_root_account: str,
    target_root_account: str,
    prefix: str,
    max_iterations: int = 50_000,
):
    """
    Copies the hierarchy (all descendants) of a source root account into a target root account.

    Args:
        accounts_list (list of dict): The list containing all account dictionaries.
        source_root_account (str): The 'name' of the source root account to copy from.
        target_root_account (str): The 'name' of the target root account to attach to.
        prefix (str): The string to prepend to the 'name' of copied accounts.

    Returns:
        list of dict: The updated accounts list with the appended entries.
    """

    # Step 1: Discover all descendants of the source_root_account
    descendant_names = set()

    # We use a while loop to ensure we catch all levels of depth,
    # even if the list is completely unordered.
    i = 0
    while True and i < max_iterations:
        added = False
        for acc in accounts_list:
            # weird issue with frappes get() where parent_account
            # does not get assigned an empty string value if it is
            # None. in this case we skip the rest
            if acc.get("parent_account") is None:
                continue

            if acc["name"] not in descendant_names:
                # An account is a descendant if its parent is the root OR a known descendant
                if (
                    acc.get("parent_account").rsplit(" - ", 1)[0] == source_root_account
                    or acc.get("parent_account") in descendant_names
                ):
                    descendant_names.add(acc["name"])
                    added = True

        # If no new descendants were found in this pass, our set is complete
        if not added:
            break

    # Step 2: Create the modified copies while maintaining original order
    new_entries = []

    for acc in accounts_list:

        if acc["name"] in descendant_names:

            # Deep copy to ensure we don't accidentally mutate the original dictionaries
            new_acc = copy.deepcopy(acc)

            # 1. Prepend the prefix to the unique name identifier
            new_acc["name"] = f"{prefix}{new_acc['name']}"

            # 2. Re-map the parent_account relationship
            if acc.get("parent_account").rsplit(" - ", 1)[0] == source_root_account:
                suffix = acc.get("parent_account").rsplit(" - ", 1)[1]
                # Immediate children of the source attach directly to the target root
                new_acc["parent_account"] = f"{target_root_account} - {suffix}"
            else:
                # Deeper nodes attach to their new, prefixed parent nodes
                new_acc["parent_account"] = f"{prefix}{acc['parent_account']}"

            # 3. Reset the Nested Set structural bounds (Note: Using 'rgt' to match your schema keys)
            new_acc["lft"] = None
            new_acc["rgt"] = None

            new_entries.append(new_acc)

    # Step 3: Append all new entries to the end of the original list
    accounts_list.extend(new_entries)

    return accounts_list


#! overwrite function from financial_statement.py
def calculate_values(
    accounts_by_name,
    gl_entries_by_account,
    period_list,
    accumulated_values,
    ignore_accumulated_values_for_fy,
):
    warnings = []
    for entries in gl_entries_by_account.values():
        for entry in entries:
            # 1. Check the original root account to see if we need to
            # reroute the entry declare root account for the leaf and
            # remove the shortened company suffix
            root = root_account(accounts_by_name[entry.account], accounts_by_name)
            root_account_name = root["name"].rsplit(" - ", 1)[0]

            # 2. Update the entry.account string to point to the newly copied accounts
            if root_account_name == HERSTELLUNGSKOSTEN:
                if entry.umsatzkostenverfahren_type == CC_HERSTELLUNG:
                    # Stays in the original Herstellungskosten account
                    pass
                elif entry.umsatzkostenverfahren_type == CC_VERTRIEB:
                    entry.account = VERTRIEBSKOSTEN_PREFIX + entry.account
                elif entry.umsatzkostenverfahren_type == CC_VERWALTUNG:
                    entry.account = VERWALTUNGSKOSTEN_PREFIX + entry.account
                elif entry.umsatzkostenverfahren_type == CC_SONSTIGE:
                    entry.account = SONSTIGE_AUFWENDUNGEN_PREFIX + entry.account
                else:
                    warnings.append({
                        'account': entry.account,
                        'debit': flt(entry.debit),
                        'credit': flt(entry.credit),
                        'debit_in_account_currency': flt(entry.debit_in_account_currency),
                        'credit_in_account_currency': flt(entry.credit_in_account_currency),
                        'account_currency': entry.account_currency,
                        'umsatzkostenverfahren_type': entry.umsatzkostenverfahren_type or '',
                        'posting_date': entry.posting_date,
                        'is_opening': entry.is_opening or 'No',
                        'fiscal_year': entry.fiscal_year,
                    })

            # 3. NOW fetch the account dictionary (d) using the
            #    potentially updated entry.account
            d = accounts_by_name.get(entry.account)

            if not d:
                frappe.msgprint(
                    _("Could not retrieve information for {0}.").format(entry.account),
                    title="Error",
                    raise_exception=1,
                )

            # 4. Accumulate values into the correct 'd'
            for period in period_list:
                # check if posting date is within the period
                if entry.posting_date <= period.to_date:
                    if (
                        accumulated_values or entry.posting_date >= period.from_date
                    ) and (
                        not ignore_accumulated_values_for_fy
                        or entry.fiscal_year == period.to_date_fiscal_year
                    ):
                        d[period.key] = (
                            d.get(period.key, 0.0)
                            + flt(entry.debit)
                            - flt(entry.credit)
                        )

            if entry.posting_date < period_list[0].year_start_date:
                d["opening_balance"] = (
                    d.get("opening_balance", 0.0) + flt(entry.debit) - flt(entry.credit)
                )

    if warnings:
        frappe.msgprint(
            _(
                "Found general ledger entries that should have a cost center type assigned but do not."
                "These are now assumed to be CC_HERSTELLUNG."
                f"Following entries have this issue: {warnings}"
            ),
            title="Warning journal entries without cost center assignment",
            raise_exception=0,
        )


def root_account(account: frappe.dict, accounts_by_name: dict, max_depth=20) -> dict:
    i = 0
    root = account
    while root.parent_account is not None:
        if i == max_depth:
            frappe.throw(
                msg=_(
                    f"Maximum recursion depth of {max_depth} exceeded while searching for the root"
                    f"account of <b>{account.name}</b>. Please check your Chart of Accounts for circular"
                    f"references or excessively nested structures."
                ),
                title=_("Recursion Limit Exceeded"),
                exc=frappe.ValidationError,
            )

        i += 1
        root = accounts_by_name[root.parent_account]

    return root


#! overwrite function from financial_statement.py
def get_accounting_entries(
    doctype,
    from_date,
    to_date,
    filters,
    root_lft=None,
    root_rgt=None,
    root_type=None,
    ignore_closing_entries=None,
    period_closing_voucher=None,
    ignore_opening_entries=False,
    group_by_account=False,
    ignore_reporting_currency=True,
):
    gl_entry = frappe.qb.DocType(doctype)
    # ! --- UKV code ---
    cc = frappe.qb.DocType("Cost Center")
    query = (
        frappe.qb.from_(gl_entry)
        .left_join(cc)
        .on(gl_entry.cost_center == cc.name)
        .select(
            gl_entry.account,
            (
                gl_entry.debit
                if not group_by_account
                else Sum(gl_entry.debit).as_("debit")
            ),
            (
                gl_entry.credit
                if not group_by_account
                else Sum(gl_entry.credit).as_("credit")
            ),
            (
                gl_entry.debit_in_account_currency
                if not group_by_account
                else Sum(gl_entry.debit_in_account_currency).as_(
                    "debit_in_account_currency"
                )
            ),
            (
                gl_entry.credit_in_account_currency
                if not group_by_account
                else Sum(gl_entry.credit_in_account_currency).as_(
                    "credit_in_account_currency"
                )
            ),
            # when grouping by account the non-aggregated columns must be aggregated for postgres;
            # account_currency is constant per account so Max() returns the same value.
            (
                gl_entry.account_currency
                if not group_by_account
                else Max(gl_entry.account_currency).as_("account_currency")
            ),
            # ! --- UKV code ---
            # this is used to map the correct cost type for the UKV
            # profit and loss per HGB. Vertriebs- and Verwaltungskosten
            # have to be moved out of the Herstellungskosten account
            cc.umsatzkostenverfahren_type,
        )
        .where(gl_entry.company == filters.company)
    )

    if not ignore_reporting_currency:
        query = query.select(
            (
                gl_entry.debit_in_reporting_currency
                if not group_by_account
                else Sum(gl_entry.debit_in_reporting_currency).as_(
                    "debit_in_reporting_currency"
                )
            ),
            (
                gl_entry.credit_in_reporting_currency
                if not group_by_account
                else Sum(gl_entry.credit_in_reporting_currency).as_(
                    "credit_in_reporting_currency"
                )
            ),
        )

    ignore_is_opening = frappe.get_single_value(
        "Accounts Settings", "ignore_is_opening_check_for_reporting"
    )

    if doctype == "GL Entry":
        # aggregate the non-grouped columns when grouping by account (postgres requirement)
        if group_by_account:
            query = query.select(
                Max(gl_entry.posting_date).as_("posting_date"),
                Max(gl_entry.is_opening).as_("is_opening"),
                Max(gl_entry.fiscal_year).as_("fiscal_year"),
            )
        else:
            query = query.select(
                gl_entry.posting_date, gl_entry.is_opening, gl_entry.fiscal_year
            )
        query = query.where(gl_entry.is_cancelled == 0)
        query = query.where(gl_entry.posting_date <= to_date)
        # FORCE INDEX is MySQL-only; postgres has no index hints (its planner uses the index anyway)
        if frappe.db.db_type != "postgres":
            query = query.force_index("posting_date_company_index")

        if ignore_opening_entries and not ignore_is_opening:
            query = query.where(gl_entry.is_opening == "No")
    else:
        query = query.select(
            Max(gl_entry.closing_date).as_("posting_date")
            if group_by_account
            else gl_entry.closing_date.as_("posting_date")
        )
        query = query.where(gl_entry.period_closing_voucher == period_closing_voucher)

    query = fs.apply_additional_conditions(
        doctype, query, from_date, ignore_closing_entries, filters
    )

    if (root_lft and root_rgt) or root_type:
        account_filter_query = fs.get_account_filter_query(
            root_lft, root_rgt, root_type, gl_entry
        )
        query = query.where(ExistsCriterion(account_filter_query))

    if group_by_account:
        query = query.groupby("account")

    from frappe.desk.reportview import build_match_conditions

    if match_conditions := build_match_conditions(doctype):
        query = query.where(Bracket(LiteralValue(match_conditions)))

    return query.run(as_dict=True)


def organize_into_guv_hgb_structure(
    data: list[dict], period_list, company=None
) -> list[dict]:
    def get_substructure(root: str) -> list:
        # Case if there are no accounts under root
        # I.e. if filter was set on cost center
        # for which account group has no journal entries
        if root not in accounts_by_name:
            return [generate_line_item(root)]

        structure = [accounts_by_name[root]]

        def recurse(parent):
            for child in parent_children_map[parent]:
                structure.append(child)
                if child.is_group:
                    recurse(child.account)

        recurse(root)
        return structure

    def compute_sub_total(line_item: dict, add: list, subtract: list):
        # "Inspiration" for this function was taken from `accumulate_values_into_parents`
        # from `financial_statements.py`. For total i checked `prepare_data`.

        # Check if all required guv line items exists in accounts by name.
        # This might not be the case if a cost center or project filter was
        # selected for which the line item had no journal entries.
        # The code is now setup to assume they are 0 if they don't exist.
        missing = [
            item
            for item in itertools.chain(add, subtract)
            if item not in accounts_by_name
        ]
        if missing:
            frappe.msgprint(
                _(
                    "A cost center or project filter was selected for which the following top "
                    "level GuV line items had no journal entries. They will be assumed to be 0. "
                    f"This might be incorrect! Missing GuV line items: {missing}"
                ),
                title="Warning: Missing GuV Items",
                raise_exception=0,
            )

        # ~~~ Periods
        for period in period_list:
            line_item[period.key] = 0.0

            for item in add:
                if item in accounts_by_name:
                    line_item[period.key] += accounts_by_name[item][period.key]
            for item in subtract:
                if item in accounts_by_name:
                    line_item[period.key] -= accounts_by_name[item][period.key]

        # ~~~ Opening balance & Total
        # Note on total
        # In the `financial_statements.py` the logic depends on `accumulated_values`
        # If true, this just grabs the latest period
        # If false, all periods are agggregated.
        # Trick: just aggegrate the totals, then we don't need to pull the `accumulated_values`
        for item in add:
            if item in accounts_by_name:
                line_item["opening_balance"] += accounts_by_name[item].get(
                    "opening_balance", 0.0
                )
                line_item["total"] += accounts_by_name[item].get("total", 0.0)
        for item in subtract:
            if item in accounts_by_name:
                line_item["opening_balance"] -= accounts_by_name[item].get(
                    "opening_balance", 0.0
                )
                line_item["total"] -= accounts_by_name[item].get("total", 0.0)

    def generate_line_item(name: str) -> dict:
        company_currency = (
            frappe.get_cached_value("Company", company, "default_currency")
            if company
            else ""
        )
        return {
            "account": name,
            "parent_account": "",
            "indent": 0.0,
            "year_start_date": period_list[0]["year_start_date"],
            "year_end_date": period_list[0]["year_end_date"],
            "currency": company_currency,
            "include_in_gross": 0,
            "account_type": "",
            "is_group": 0,
            "opening_balance": 0.0,
            "account_name": name.rsplit("-", 1)[0].strip(),
            "acc_name": name.rsplit("-", 1)[0].strip(),
            "has_value": True,
            "total": 0.0,
        }

    def prepare() -> tuple[dict, dict, list]:
        parent_children_map = frappe._dict()
        accounts_by_name = frappe._dict()
        for d in data:
            # Ensure that all groups have entries (even if they are empty)
            # in the parent_children_map
            if d.is_group:
                parent_children_map[d.account] = []
            parent_children_map.setdefault(d.parent_account or None, []).append(d)
            accounts_by_name[d.account] = d

        # Fetch company suffix to append to all line items
        company_suffix = frappe.get_cached_value("Company", company, "abbr")

        guv_positions = [f"{pos} - {company_suffix}" for pos in GUV_POSITIONS]

        return accounts_by_name, parent_children_map, guv_positions

    accounts_by_name, parent_children_map, guv_positions = prepare()

    guv = []

    # ! We need to bring the out data into the correct order and add
    # ! some important rows
    #   "1 - Umsatzerloese"
    # - "2 - Herstellungskosten der zur Erzielung der Umsatzerloese erbrachten Leistungen"
    # = "3 - Bruttoergebnis vom Umsatz"
    # - "4 - Vertriebskosten"
    # - "5 - allgemeine Verwaltungskosten"
    # + "6 - sonstige betriebliche Ertraege"
    # - "7 - sonstige betriebliche Aufwendungen"
    # + "8 - Ertraege aus Beteiligungen"
    # + "9 - Erträge aus anderen Wertpapieren und Ausleihungen des Finanzanlagevermögens"
    # + "10 - sonstige Zinsen und ähnliche Erträge"
    # - "11 - Abschreibungen auf Finanzanlagen and auf Wertpapiere des Umlaufvermögens"
    # - "12 - Zinsen und ähnliche Aufwendungen"
    # - "13 - Steuern vom Einkommen und vom Ertrag"
    # = "14 - Ergebnis nach Steuern"
    # + 15 - sonstige Steuern
    # = 16 - Jahresüberschuss/Jahresfehlbetrag
    add = []
    subtract = []
    # Note: I chose to do +1/-1 for better human matching of the index to the line item
    for i, line_item in enumerate(guv_positions):
        # --- Bruttoergebnis vom Umsatz
        if i + 1 == 3:
            brutto_vom_umsatz = generate_line_item(line_item)
            add.append(guv_positions[0])  # 1 - Umsatzerloese
            subtract.append(guv_positions[1])  # 2 - Herstellungskosten
            compute_sub_total(brutto_vom_umsatz, add, subtract)
            guv.append(brutto_vom_umsatz)
        # --- Ergebnis nach Steuern
        elif i + 1 == 14:
            ergebnis_nach_steuern = generate_line_item(line_item)
            add.extend(
                [guv_positions[j - 1] for j in [6, 8, 9, 10]]
            )  # 1 - Umsatzerloese 6 - sonstige betriebliche Ertraege 8 - Ertraege aus Beteiligungen 9 - Erträge aus anderen Wertpapieren 10 - sonstige Zinsen und ähnliche Erträge
            subtract.extend(
                [guv_positions[j - 1] for j in [4, 5, 7, 11, 12, 13]]
            )  # 2 - Herstellungskosten 4 - Vertriebskosten 5 - allgemeine Verwaltungskosten 7 - sonstige betriebliche Aufwendungen 11 - Abschreibungen auf Finanzanlagen 12 - Zinsen und ähnliche Aufwendungen 13 - Steuern vom Einkommen und vom Ertrag
            compute_sub_total(ergebnis_nach_steuern, add, subtract)
            guv.append(ergebnis_nach_steuern)
        # --- Jahresueberschuss
        elif i + 1 == 16:
            jahresueberschuss = generate_line_item(line_item)
            subtract.append(guv_positions[15 - 1])  # 15 - sonstige Steuern
            compute_sub_total(jahresueberschuss, add, subtract)
            guv.append(jahresueberschuss)
        # --- All other lines do not need to be computed, but their child structure
        else:
            guv.extend(get_substructure(guv_positions[i]))

    # compute total income and cost for chart
    total_income = generate_line_item(_("Total Income"))
    compute_sub_total(total_income, add, [])

    total_cost = generate_line_item(_("Total Cost"))
    compute_sub_total(total_cost, subtract, [])

    return guv, total_income, total_cost


def patch_functions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Backup original functions
        original_get_accounting_entries = fs.get_accounting_entries

        try:
            # 2. Monkey-patch the functions in the module
            fs.get_accounting_entries = get_accounting_entries
            # 3. Call the intended function
            return func(*args, **kwargs)

        finally:
            # 4. Undo monkey patch
            fs.get_accounting_entries = original_get_accounting_entries

    return wrapper


@patch_functions
def execute(filters=None):
    filters = frappe._dict(filters)
    if filters and filters.report_template:
        return FinancialReportEngine().execute(filters)

    period_list = fs.get_period_list(
        filters.from_fiscal_year,
        filters.to_fiscal_year,
        filters.period_start_date,
        filters.period_end_date,
        filters.filter_based_on,
        filters.periodicity,
        company=filters.company,
    )

    income = get_data(
        filters.company,
        "Income",
        "Credit",
        period_list,
        filters=filters,
        accumulated_values=filters.accumulated_values,
        ignore_closing_entries=True,
    )

    expense = get_data(
        filters.company,
        "Expense",
        "Debit",
        period_list,
        filters=filters,
        accumulated_values=filters.accumulated_values,
        ignore_closing_entries=True,
    )

    data = []
    data.extend(income or [])
    data.extend(expense or [])

    data, total_income, total_cost = organize_into_guv_hgb_structure(
        data, period_list, filters.company
    )

    # By convention of the `organize_into_guv_hgb_structure` the last value
    # of the list is the "Jahresueberschuss", which matches the net_profit_loss
    net_profit_loss = data[-1]

    columns = fs.get_columns(
        filters.periodicity, period_list, filters.accumulated_values, filters.company
    )

    currency = filters.presentation_currency or frappe.get_cached_value(
        "Company", filters.company, "default_currency"
    )
    total_income = [total_income, []]
    total_cost = [total_cost, []]
    chart = pnl.get_chart_data(
        filters, period_list, total_income, total_cost, net_profit_loss, currency
    )

    report_summary, primitive_summary = pnl.get_report_summary(
        period_list,
        filters.periodicity,
        total_income,
        total_cost,
        net_profit_loss,
        currency,
        filters,
    )

    if filters.get("selected_view") == "Growth":
        fs.compute_growth_view_data(data, period_list)

    if filters.get("selected_view") == "Margin":
        fs.compute_margin_view_data(data, period_list, filters.accumulated_values)

    return columns, data, None, chart, report_summary, primitive_summary
