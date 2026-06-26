__version__ = "0.0.1"

import frappe

def patch_pl_statement():
	try:
		import erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement as pl
		
		# Prevent double patching
		if hasattr(pl, "_original_execute"):
			return
			
		pl._original_execute = pl.execute
		
		def custom_execute(filters=None):
			if filters:
				filters = frappe._dict(filters)
			if filters and filters.get("report_template") == "GuV UKV HGB 275":
				from ukv_reporting.ukv_reporting.report.guv_ukv_hgb_275.guv_ukv_hgb_275 import execute as execute_ukv
				cols, rows, message, chart, report_summary, primitive_summary = execute_ukv(filters)
				return cols, rows, message, chart, report_summary, primitive_summary
				
			return pl._original_execute(filters)
			
		pl.execute = custom_execute
	except ImportError:
		pass

# Apply patch at startup
patch_pl_statement()

