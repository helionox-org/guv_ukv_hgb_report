import frappe
frappe.flags.in_test = True
frappe.in_test = True

from guv_ukv_hgb_report.ukv_reporting.report.guv_ukv_hgb_275.tests import test_guv_ukv_hgb_275_data as test_data

def resolve_account_by_number(account_str, company):
	parts = account_str.split(" - ", 1)
	if parts and parts[0].isdigit():
		number = parts[0]
		real_name = frappe.db.get_value("Account", {"account_number": number, "company": company}, "name")
		if real_name:
			return real_name
	return account_str

def replace_abbr_recursive(data, old_abbr, new_abbr, old_company, new_company):
	if isinstance(data, dict):
		if "account" in data and isinstance(data["account"], str):
			data["account"] = resolve_account_by_number(data["account"], new_company)
		for k, v in data.items():
			data[k] = replace_abbr_recursive(v, old_abbr, new_abbr, old_company, new_company)
	elif isinstance(data, list):
		for i, v in enumerate(data):
			data[i] = replace_abbr_recursive(v, old_abbr, new_abbr, old_company, new_company)
	elif isinstance(data, str):
		val = data.replace(f" - {old_abbr}", f" - {new_abbr}")
		if val == old_company:
			return new_company
		return val
	return data

def ensure_parties_exist(company):
	if not frappe.db.exists("Customer", "Grant Plastics Ltd."):
		doc = frappe.get_doc({
			"doctype": "Customer",
			"customer_name": "Grant Plastics Ltd.",
			"type": "Individual"
		})
		doc.flags.ignore_permissions = True
		doc.insert()
		print("Created Customer: Grant Plastics Ltd.")

	if not frappe.db.exists("Supplier", "MA Inc."):
		doc = frappe.get_doc({
			"doctype": "Supplier",
			"supplier_name": "MA Inc.",
			"supplier_type": "Individual",
			"supplier_group": "Local"
		})
		doc.flags.ignore_permissions = True
		doc.insert()
		print("Created Supplier: MA Inc.")

def populate():
	# Enable test flag to bypass password strength checks and validations during bootstrap
	frappe.flags.in_test = True

	# 0. Clean up / ensure clean state for Test GmbH (Demo)
	company_name = "Test GmbH (Demo)"
	abbr = "TGD"
	
	print("Cleaning up existing 'Test GmbH (Demo)' data...")
	# Clean up database records for this company to guarantee scratch setup
	frappe.db.sql("DELETE FROM `tabGL Entry` WHERE company = %s", company_name)
	frappe.db.sql("DELETE FROM `tabJournal Entry Account` WHERE parent IN (SELECT name FROM `tabJournal Entry` WHERE company = %s)", company_name)
	frappe.db.sql("DELETE FROM `tabJournal Entry` WHERE company = %s", company_name)
	frappe.db.sql("DELETE FROM `tabCost Center` WHERE company = %s", company_name)
	frappe.db.sql("DELETE FROM `tabAccount` WHERE company = %s", company_name)
	frappe.db.sql("DELETE FROM `tabCompany` WHERE name = %s", company_name)
	frappe.db.commit()

	# 1. Bootstrap default test data / settings if not already done
	if not frappe.db.exists("Price List", "Standard Buying"):
		print("Bootstrapping standard ERPNext test presets...")
		# Clean up any Standard Buying/Selling that might cause duplicate entry error
		try:
			frappe.db.sql("DELETE FROM `tabPrice List` WHERE name IN ('Standard Buying', 'Standard Selling')")
			frappe.db.commit()
		except Exception:
			pass
		from erpnext.tests.utils import BootStrapTestData
		BootStrapTestData()

	# 2. Create the company 'Test GmbH (Demo)'
	print(f"Creating Company: {company_name}")
	company_doc = frappe.get_doc({
		"doctype": "Company",
		"company_name": company_name,
		"abbr": "TGD",
		"country": "Germany",
		"default_currency": "EUR",
		"create_chart_of_accounts_based_on": "Standard Template",
	})
	company_doc.flags.ignore_permissions = True
	company_doc.insert()

	# 3. Import SKR04 Blueprint Chart of Accounts
	print("Importing SKR04 Chart of Accounts...")
	csv_path = "/workspace/guv_ukv_hgb_report/SKR04_Blueprint_chart_of_accounts.csv"
	file_name = "/private/files/SKR04_Blueprint_chart_of_accounts.csv"
	file_url = file_name
	if not frappe.db.exists("File", {"file_url": file_name}):
		with open(csv_path, "rb") as f:
			file_doc = frappe.get_doc({
				"doctype": "File",
				"file_name": "SKR04_Blueprint_chart_of_accounts.csv",
				"file_url": file_name,
				"content": f.read(),
				"is_private": 1
			})
			file_doc.insert()
			file_url = file_doc.file_url
	
	from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import import_coa
	import_coa(file_url, company_name)

	# Get root Cost Center
	root_cc = frappe.db.get_value("Cost Center", {"company": company_name, "is_group": 1, "parent_cost_center": ""}, "name")
	if not root_cc:
		root_cc = frappe.db.get_value("Cost Center", {"company": company_name, "is_group": 1}, "name")
		
	# 4. Create cost centers
	ccs = [
		{"name": f"Main - {abbr}", "cost_center_name": "Main", "is_group": 0, "parent": root_cc, "umsatzkostenverfahren_type": ""},
		{"name": f"P1 - Golden Mango - {abbr}", "cost_center_name": "P1 - Golden Mango", "is_group": 1, "parent": root_cc, "umsatzkostenverfahren_type": ""},
		{"name": f"P2 - Green Apple - {abbr}", "cost_center_name": "P2 - Green Apple", "is_group": 1, "parent": root_cc, "umsatzkostenverfahren_type": ""},
		{"name": f"P1-2 - Herstellungskosten - {abbr}", "cost_center_name": "P1-2 - Herstellungskosten", "is_group": 0, "parent": f"P1 - Golden Mango - {abbr}", "umsatzkostenverfahren_type": "Herstellungskosten"},
		{"name": f"P2-3 - Herstellungskosten - {abbr}", "cost_center_name": "P2-3 - Herstellungskosten", "is_group": 0, "parent": f"P2 - Green Apple - {abbr}", "umsatzkostenverfahren_type": "Herstellungskosten"},
		{"name": f"P1-5 - Verwaltungskosten - {abbr}", "cost_center_name": "P1-5 - Verwaltungskosten", "is_group": 0, "parent": f"P1 - Golden Mango - {abbr}", "umsatzkostenverfahren_type": "Verwaltungskosten"},
		{"name": f"P2-5 - Verwaltungskosten - {abbr}", "cost_center_name": "P2-5 - Verwaltungskosten", "is_group": 0, "parent": f"P2 - Green Apple - {abbr}", "umsatzkostenverfahren_type": "Verwaltungskosten"},
		{"name": f"P1-4 - Vertriebskosten - {abbr}", "cost_center_name": "P1-4 - Vertriebskosten", "is_group": 0, "parent": f"P1 - Golden Mango - {abbr}", "umsatzkostenverfahren_type": "Vertriebskosten"},
		{"name": f"P2-4 - Vertriebskosten - {abbr}", "cost_center_name": "P2-4 - Vertriebskosten", "is_group": 0, "parent": f"P2 - Green Apple - {abbr}", "umsatzkostenverfahren_type": "Vertriebskosten"},
		{"name": f"P1-6 - Sonstige betriebliche Aufwendungen - {abbr}", "cost_center_name": "P1-6 - Sonstige betriebliche Aufwendungen", "is_group": 0, "parent": f"P1 - Golden Mango - {abbr}", "umsatzkostenverfahren_type": "Sonstige betriebliche Aufwendungen"},
		{"name": f"P2-6 - Sonstige betriebliche Aufwendungen - {abbr}", "cost_center_name": "P2-6 - Sonstige betriebliche Aufwendungen", "is_group": 0, "parent": f"P2 - Green Apple - {abbr}", "umsatzkostenverfahren_type": "Sonstige betriebliche Aufwendungen"},
	]
	
	for cc_data in ccs:
		if not frappe.db.exists("Cost Center", cc_data["name"]):
			doc = frappe.get_doc({
				"doctype": "Cost Center",
				"cost_center_name": cc_data["cost_center_name"],
				"company": company_name,
				"is_group": cc_data["is_group"],
				"parent_cost_center": cc_data["parent"],
				"umsatzkostenverfahren_type": cc_data["umsatzkostenverfahren_type"]
			})
			doc.flags.ignore_permissions = True
			doc.name = cc_data["name"]
			doc.insert()
			print(f"Created Cost Center: {cc_data['name']}")

	# Ensure parties exist
	ensure_parties_exist(company_name)

	# 5. Insert all Journal Entries
	original_get_doc = frappe.get_doc
	
	def custom_get_doc(*args, **kwargs):
		if args and isinstance(args[0], dict):
			replace_abbr_recursive(args[0], "TGD", abbr, "Test GmbH (Demo)", company_name)
		return original_get_doc(*args, **kwargs)
		
	frappe.get_doc = custom_get_doc
	try:
		for name in sorted(dir(test_data)):
			if name.startswith("create_acc_jv_"):
				func = getattr(test_data, name)
				print(f"Running {name}...")
				try:
					func(None)
				except Exception as e:
					print(f"Failed to run {name}: {e}")
	finally:
		frappe.get_doc = original_get_doc
	
	frappe.db.commit()
	print("Successfully populated all data and committed to database.")
