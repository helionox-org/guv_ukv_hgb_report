import frappe

def create_acc_jv_2026_00025(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "4860 - Grundst\u00fccksertr\u00e4ge - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 20000.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 20000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00024_1(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2025-06-18",
            "accounts": [
                {
                    "account": "7642 - Gewerbesteuererstattungen Vorjahre - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 56789.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 56789.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00024(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "7642 - Gewerbesteuererstattungen Vorjahre - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 56789.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 56789.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00023(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2025-06-18",
            "accounts": [
                {
                    "account": "6000 - L\u00f6hne und Geh\u00e4lter - TGD",
                    "debit_in_account_currency": 123456.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P1-2 - Herstellungskosten - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 123456.0,
                    "cost_center": "P1-2 - Herstellungskosten - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00022_1(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "7309 - Zinsen und \u00e4hnliche Aufwendungen an verb. Unternehmen - TGD",
                    "debit_in_account_currency": 1500.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 1500.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00022(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "7305 - Zinsaufwendungen \u00a7 233a AO betriebliche Steuern - TGD",
                    "debit_in_account_currency": 1500.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 1500.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00021(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 500.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "7105 - Zinsertr\u00e4ge \u00a7 233a AO steuerpflichtig - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 500.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00020(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 2000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "7014 - Ertr\u00e4ge aus Anteilen an Kap.Ges. (Finanzanlageverm\u00f6gen, inl\u00e4ndische Kap.Ges.) - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 2000.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00019(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 10000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "7004 - Ertr\u00e4ge aus Beteiligungen an Personengesellschaften (verb. Unternehmen), \u00a7 9 GewStG - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 10000.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00018(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "7685 - Kfz-Steuer - TGD",
                    "debit_in_account_currency": 350.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P2-3 - Herstellungskosten - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 350.0,
                    "cost_center": "P2-3 - Herstellungskosten - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00017(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "7610 - Gewerbesteuer - TGD",
                    "debit_in_account_currency": 3000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 3000.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00016(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "7300 - Zinsen und \u00e4hnliche Aufwendungen - TGD",
                    "debit_in_account_currency": 1200.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 1200.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00015(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Depreciation Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "7200 - Abschreibungen auf Finanzanlagen (dauerhaft) - TGD",
                    "debit_in_account_currency": 2500.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "0900 - Wertpapiere des Anlageverm\u00f6gens - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 2500.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00014(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 50.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "7100 - Sonstige Zinsen und \u00e4hnliche Ertr\u00e4ge - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 50.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00013(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 1500.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "7010 - Ertr\u00e4ge aus anderen Wertpapieren und Ausleihungen des Finanzanlageverm\u00f6gens - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 1500.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00012(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 5000.0,
                    "credit_in_account_currency": 0.0,
                },
                {
                    "account": "7000 - Ertr\u00e4ge aus Beteiligungen - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 5000.0,
                    "cost_center": "Main - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00011(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "6520 - Kfz-Versicherungen - TGD",
                    "debit_in_account_currency": 800.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P1-5 - Verwaltungskosten - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 800.0,
                    "cost_center": "P1-5 - Verwaltungskosten - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00010(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "3000 - R\u00fcckstellungen f. Pensionen und \u00e4hnliche Verplicht. - TGD",
                    "debit_in_account_currency": 2000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P2-5 - Verwaltungskosten - TGD",
                },
                {
                    "account": "4930 - Ertr\u00e4ge aus der Aufl\u00f6sung von R\u00fcckstellungen - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 2000.0,
                    "cost_center": "P2-5 - Verwaltungskosten - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00009(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "6815 - B\u00fcrobedarf - TGD",
                    "debit_in_account_currency": 100.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P1-5 - Verwaltungskosten - TGD",
                },
                {
                    "account": "1406 - Abziehbare Vorsteuer 19 % - TGD",
                    "debit_in_account_currency": 19.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P1-5 - Verwaltungskosten - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 119.0,
                    "cost_center": "P1-5 - Verwaltungskosten - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00008(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "6600 - Werbekosten - TGD",
                    "debit_in_account_currency": 500.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P2-4 - Vertriebskosten - TGD",
                },
                {
                    "account": "1406 - Abziehbare Vorsteuer 19 % - TGD",
                    "debit_in_account_currency": 95.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P2-4 - Vertriebskosten - TGD",
                },
                {
                    "account": "3300 - Verb. aus Lieferungen und Leistungen - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 595.0,
                    "cost_center": "P2-4 - Vertriebskosten - TGD",
                    "party_type": "Supplier",
                    "party": "MA Inc.",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00007(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "5000 - Aufwendungen f. Roh-, Hilfs- und Betriebsstoffe und f. bezogene Waren - TGD",
                    "debit_in_account_currency": 5000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P2-3 - Herstellungskosten - TGD",
                },
                {
                    "account": "1000 - Roh-, Hilfs- und Betriebsstoffe (Bestand) - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 5000.0,
                    "cost_center": "P2-3 - Herstellungskosten - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00006_2(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "1200 - Forderungen aus Lieferungen und Leistungen - TGD",
                    "debit_in_account_currency": 1190.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P2-3 - Herstellungskosten - TGD",
                    "party_type": "Customer",
                    "party": "Grant Plastics Ltd.",
                },
                {
                    "account": "4400 - Erl\u00f6se 19 % USt - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 1000.0,
                    "cost_center": "P2-3 - Herstellungskosten - TGD",
                },
                {
                    "account": "3806 - Umsatzsteuer 19 % - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 190.0,
                    "cost_center": "P2-3 - Herstellungskosten - TGD",
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00006_1(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "1200 - Forderungen aus Lieferungen und Leistungen - TGD",
                    "debit_in_account_currency": 1190.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P2-3 - Herstellungskosten - TGD",
                    "party_type": "Customer",
                    "party": "Grant Plastics Ltd.",
                },
                {
                    "account": "4400 - Erl\u00f6se 19 % USt - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 1000.0,
                    "cost_center": "P2-3 - Herstellungskosten - TGD",
                },
                {
                    "account": "3806 - Umsatzsteuer 19 % - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 190.0,
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00006(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-18",
            "accounts": [
                {
                    "account": "1200 - Forderungen aus Lieferungen und Leistungen - TGD",
                    "debit_in_account_currency": 1190.0,
                    "credit_in_account_currency": 0.0,
                    "party_type": "Customer",
                    "party": "Grant Plastics Ltd.",
                },
                {
                    "account": "4400 - Erl\u00f6se 19 % USt - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 1000.0,
                    "cost_center": "P2-3 - Herstellungskosten - TGD",
                },
                {
                    "account": "3806 - Umsatzsteuer 19 % - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 190.0,
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00005(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-17",
            "accounts": [
                {
                    "account": "6000 - L\u00f6hne und Geh\u00e4lter - TGD",
                    "debit_in_account_currency": 10000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P1-5 - Verwaltungskosten - TGD",
                },
                {
                    "account": "1810 - Bank 1 - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 10000.0,
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00004(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-17",
            "accounts": [
                {
                    "account": "6000 - L\u00f6hne und Geh\u00e4lter - TGD",
                    "debit_in_account_currency": 88000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P1-4 - Vertriebskosten - TGD",
                },
                {
                    "account": "1820 - Bank 2 - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 88000.0,
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00003(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-17",
            "accounts": [
                {
                    "account": "6000 - L\u00f6hne und Geh\u00e4lter - TGD",
                    "debit_in_account_currency": 25000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P1-5 - Verwaltungskosten - TGD",
                },
                {
                    "account": "1810 - Bank 1 - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 25000.0,
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00002(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-17",
            "accounts": [
                {
                    "account": "6000 - L\u00f6hne und Geh\u00e4lter - TGD",
                    "debit_in_account_currency": 7000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P1-5 - Verwaltungskosten - TGD",
                },
                {
                    "account": "1820 - Bank 2 - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 7000.0,
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00001(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-17",
            "accounts": [
                {
                    "account": "6000 - L\u00f6hne und Geh\u00e4lter - TGD",
                    "debit_in_account_currency": 10000.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P1-2 - Herstellungskosten - TGD",
                },
                {
                    "account": "1810 - Bank 1 - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 10000.0,
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00059(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-25",
            "accounts": [
                {
                    "account": "6392 - Zuwendungen, Spenden f\u00fcr mildt\u00e4tige Zwecke - TGD",
                    "debit_in_account_currency": 99999.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "P2-6 - Sonstige betriebliche Aufwendungen - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 99999.0,
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv


def create_acc_jv_2026_00060(self, do_not_submit=False):
    frappe.set_user("Administrator")
    jv = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "company": "Test GmbH (Demo)",
            "voucher_type": "Journal Entry",
            "posting_date": "2026-06-25",
            "accounts": [
                {
                    "account": "6392 - Zuwendungen, Spenden f\u00fcr mildt\u00e4tige Zwecke - TGD",
                    "debit_in_account_currency": 11111.0,
                    "credit_in_account_currency": 0.0,
                    "cost_center": "Main - TGD",
                },
                {
                    "account": "1800 - Bank - TGD",
                    "debit_in_account_currency": 0.0,
                    "credit_in_account_currency": 11111.0,
                },
            ],
        }
    )
    jv = jv.insert()
    if not do_not_submit:
        jv = jv.submit()
    return jv
