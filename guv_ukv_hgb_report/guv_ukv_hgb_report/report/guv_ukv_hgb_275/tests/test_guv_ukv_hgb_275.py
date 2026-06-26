import json
import os
import frappe

# Clean up Price Lists to prevent BootStrapTestData DuplicateEntryError on currency mismatch
try:
	frappe.db.sql("DELETE FROM `tabPrice List` WHERE name IN ('Standard Buying', 'Standard Selling')")
	frappe.db.commit()
except Exception:
	pass

from frappe.utils import today
from erpnext.accounts.test.accounts_mixin import AccountsTestMixin
from erpnext.tests.utils import ERPNextTestSuite
from guv_ukv_hgb_report.guv_ukv_hgb_report.report.guv_ukv_hgb_275.guv_ukv_hgb_275 import execute
from . import test_guv_ukv_hgb_275_data as test_data

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

	if not frappe.db.exists("Supplier", "MA Inc."):
		doc = frappe.get_doc({
			"doctype": "Supplier",
			"supplier_name": "MA Inc.",
			"supplier_type": "Individual",
			"supplier_group": "Local"
		})
		doc.flags.ignore_permissions = True
		doc.insert()

class TestGuVUKVHGB275(ERPNextTestSuite, AccountsTestMixin):
	def create_company(self, company_name="Test GmbH (Demo)", abbr="TGD"):
		self.company = company_name
		self.company_abbr = abbr
		
		if not frappe.db.exists("Company", company_name):
			company = frappe.get_doc(
				{
					"doctype": "Company",
					"company_name": company_name,
					"abbr": abbr,
					"country": "Germany",
					"default_currency": "EUR",
					"create_chart_of_accounts_based_on": "Standard Template",
				}
			)
			company.flags.ignore_permissions = True
			company.insert()
			
			# Import Chart of Accounts from CSV
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

		company_doc = frappe.get_doc("Company", company_name)
		self.company_abbr = company_doc.abbr
		self.cost_center = company_doc.cost_center
		self.warehouse = "Stores - " + self.company_abbr
		self.finished_warehouse = "Finished Goods - " + self.company_abbr
		self.income_account = "Sales - " + self.company_abbr
		self.expense_account = "Cost of Goods Sold - " + self.company_abbr
		self.debit_to = "Debtors - " + self.company_abbr
		self.cash = "Cash - " + self.company_abbr
		self.creditors = "Creditors - " + self.company_abbr
		self.retained_earnings = "Retained Earnings - " + self.company_abbr

	def setUp(self):
		self.create_company()
		self.create_customer()
		self.create_item()

	def get_fiscal_year(self):
		active_fy = frappe.db.get_all(
			"Fiscal Year",
			filters={"disabled": 0, "year_start_date": ("<=", today()), "year_end_date": (">=", today())},
		)[0]
		return frappe.get_doc("Fiscal Year", active_fy.name)

	def get_report_filters(self):
		from_fy = frappe.db.get_value("Fiscal Year", {"year_start_date": "2025-01-01"}, "name")
		to_fy = frappe.db.get_value("Fiscal Year", {"year_end_date": "2026-12-31"}, "name")
		return frappe._dict(
			company=self.company,
			from_fiscal_year=from_fy or "_Test Fiscal Year 2025",
			to_fiscal_year=to_fy or "_Test Fiscal Year 2026",
			period_start_date="2025-01-01",
			period_end_date="2026-12-31",
			filter_based_on="Fiscal Year",
			periodicity="Yearly",
			accumulated_values=True,
			show_zero_values=1,
		)

	def test_report_execution(self):
		filters = self.get_report_filters()
		try:
			columns, data, message, chart, report_summary, primitive_summary = execute(filters)
			# Basic checks to ensure execution succeeded and returned structured data
			self.assertTrue(isinstance(columns, list))
			self.assertTrue(isinstance(data, list))
		except Exception as e:
			self.fail(f"Report execution failed: {e}")

	def create_cost_centers_if_missing(self):
		company = self.company
		root_cc = frappe.db.get_value("Cost Center", {"company": company, "is_group": 1, "parent_cost_center": ""}, "name")
		if not root_cc:
			root_cc = frappe.db.get_value("Cost Center", {"company": company, "is_group": 1}, "name")
			
		ccs = [
			{"name": f"Main - {self.company_abbr}", "cost_center_name": "Main", "is_group": 0, "parent": root_cc, "umsatzkostenverfahren_type": ""},
			{"name": f"P1 - Golden Mango - {self.company_abbr}", "cost_center_name": "P1 - Golden Mango", "is_group": 1, "parent": root_cc, "umsatzkostenverfahren_type": ""},
			{"name": f"P2 - Green Apple - {self.company_abbr}", "cost_center_name": "P2 - Green Apple", "is_group": 1, "parent": root_cc, "umsatzkostenverfahren_type": ""},
			{"name": f"P1-2 - Herstellungskosten - {self.company_abbr}", "cost_center_name": "P1-2 - Herstellungskosten", "is_group": 0, "parent": f"P1 - Golden Mango - {self.company_abbr}", "umsatzkostenverfahren_type": "Herstellungskosten"},
			{"name": f"P2-3 - Herstellungskosten - {self.company_abbr}", "cost_center_name": "P2-3 - Herstellungskosten", "is_group": 0, "parent": f"P2 - Green Apple - {self.company_abbr}", "umsatzkostenverfahren_type": "Herstellungskosten"},
			{"name": f"P1-5 - Verwaltungskosten - {self.company_abbr}", "cost_center_name": "P1-5 - Verwaltungskosten", "is_group": 0, "parent": f"P1 - Golden Mango - {self.company_abbr}", "umsatzkostenverfahren_type": "Verwaltungskosten"},
			{"name": f"P2-5 - Verwaltungskosten - {self.company_abbr}", "cost_center_name": "P2-5 - Verwaltungskosten", "is_group": 0, "parent": f"P2 - Green Apple - {self.company_abbr}", "umsatzkostenverfahren_type": "Verwaltungskosten"},
			{"name": f"P1-4 - Vertriebskosten - {self.company_abbr}", "cost_center_name": "P1-4 - Vertriebskosten", "is_group": 0, "parent": f"P1 - Golden Mango - {self.company_abbr}", "umsatzkostenverfahren_type": "Vertriebskosten"},
			{"name": f"P2-4 - Vertriebskosten - {self.company_abbr}", "cost_center_name": "P2-4 - Vertriebskosten", "is_group": 0, "parent": f"P2 - Green Apple - {self.company_abbr}", "umsatzkostenverfahren_type": "Vertriebskosten"},
			{"name": f"P1-6 - Sonstige betriebliche Aufwendungen - {self.company_abbr}", "cost_center_name": "P1-6 - Sonstige betriebliche Aufwendungen", "is_group": 0, "parent": f"P1 - Golden Mango - {self.company_abbr}", "umsatzkostenverfahren_type": "Sonstige betriebliche Aufwendungen"},
			{"name": f"P2-6 - Sonstige betriebliche Aufwendungen - {self.company_abbr}", "cost_center_name": "P2-6 - Sonstige betriebliche Aufwendungen", "is_group": 0, "parent": f"P2 - Green Apple - {self.company_abbr}", "umsatzkostenverfahren_type": "Sonstige betriebliche Aufwendungen"},
		]
		
		for cc_data in ccs:
			if not frappe.db.exists("Cost Center", cc_data["name"]):
				doc = frappe.get_doc({
					"doctype": "Cost Center",
					"cost_center_name": cc_data["cost_center_name"],
					"company": company,
					"is_group": cc_data["is_group"],
					"parent_cost_center": cc_data["parent"],
					"umsatzkostenverfahren_type": cc_data["umsatzkostenverfahren_type"]
				})
				doc.flags.ignore_permissions = True
				doc.name = cc_data["name"]
				doc.insert()

	def test_integration_compare_expected(self):
		company = self.company
		# 0. Clean database to ensure reproducible state
		frappe.db.sql("DELETE FROM `tabGL Entry` WHERE company = %s", company)
		frappe.db.sql("DELETE FROM `tabJournal Entry Account` WHERE parent IN (SELECT name FROM `tabJournal Entry` WHERE company = %s)", company)
		frappe.db.sql("DELETE FROM `tabJournal Entry` WHERE company = %s", company)

		# 0.5 Ensure cost centers and parties exist
		self.create_cost_centers_if_missing()
		ensure_parties_exist(company)

		# 1. Create all test data from test_data helper methods
		original_get_doc = frappe.get_doc
		
		def custom_get_doc(*args, **kwargs):
			if args and isinstance(args[0], dict):
				replace_abbr_recursive(args[0], "TGD", self.company_abbr, "Test GmbH (Demo)", company)
			return original_get_doc(*args, **kwargs)
			
		frappe.get_doc = custom_get_doc
		try:
			for name in sorted(dir(self)):
				if name.startswith("create_acc_jv_") and name != "create_acc_jv_2026_00060":
					getattr(self, name)()
		finally:
			frappe.get_doc = original_get_doc

		# 2. Execute report
		filters = self.get_report_filters()
		columns, data, message, chart, report_summary, primitive_summary = execute(filters)

		actual_output = {
			"columns": columns,
			"data": data,
			"chart": chart,
			"report_summary": report_summary,
			"primitive_summary": primitive_summary
		}

		expected_path = os.path.join(os.path.dirname(__file__), "expected_output.json")

		# 3. Generate expected file if it does not exist
		if not os.path.exists(expected_path):
			with open(expected_path, "w") as f:
				json.dump(actual_output, f, indent=2, default=str)

		# 4. Read expected output
		with open(expected_path, "r") as f:
			expected_output = json.load(f)

		# Replace default TGD abbreviation and company name in expected output with active ones dynamically
		expected_output = replace_abbr_recursive(expected_output, "TGD", self.company_abbr, "Test GmbH (Demo)", self.company)

		# 5. Compare actual vs expected
		actual_serialized = json.loads(json.dumps(actual_output, default=str))
		self.assertEqual(actual_serialized, expected_output)

	def test_warning_message_for_missing_cost_center_type(self):
		company = self.company
		# 0. Clean database
		frappe.db.sql("DELETE FROM `tabGL Entry` WHERE company = %s", company)
		frappe.db.sql("DELETE FROM `tabJournal Entry Account` WHERE parent IN (SELECT name FROM `tabJournal Entry` WHERE company = %s)", company)
		frappe.db.sql("DELETE FROM `tabJournal Entry` WHERE company = %s", company)

		# 1. Create the second JV (create_acc_jv_2026_00060)
		self.create_cost_centers_if_missing()
		ensure_parties_exist(company)
		
		original_get_doc = frappe.get_doc
		def custom_get_doc(*args, **kwargs):
			if args and isinstance(args[0], dict):
				replace_abbr_recursive(args[0], "TGD", self.company_abbr, "Test GmbH (Demo)", company)
			return original_get_doc(*args, **kwargs)
			
		frappe.get_doc = custom_get_doc
		try:
			self.create_acc_jv_2026_00060()
		finally:
			frappe.get_doc = original_get_doc

		# 2. Execute report and intercept local messages
		filters = self.get_report_filters()
		frappe.local.message_log = []
		
		execute(filters)
		
		# 3. Verify warning message is logged
		warning_found = False
		for msg in frappe.local.message_log:
			msg_dict = json.loads(msg) if isinstance(msg, str) else msg
			msg_txt = msg_dict.get("message") if isinstance(msg_dict, dict) else str(msg_dict)
			if "Found general ledger entries that should have a cost center type assigned but do not." in msg_txt:
				warning_found = True
				self.assertIn("6392 - Zuwendungen, Spenden", msg_txt)
				self.assertIn("11111.0", msg_txt)
				self.assertIn("CC_HERSTELLUNG", msg_txt)
				
		self.assertTrue(warning_found, "Expected warning about missing cost center type was not logged")

# Bind helper methods from test_data
for name, func in vars(test_data).items():
	if name.startswith("create_acc_jv"):
		setattr(TestGuVUKVHGB275, name, func)


