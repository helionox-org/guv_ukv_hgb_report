app_name = "guv_ukv_hgb_report"
app_title = "Ukv Reporting"
app_publisher = "Helionox GmbH"
app_description = "HGB Paragraph 275 Cost of Sales Method Profit and Loss Report"
app_email = "contact@helionox.eu"
app_license = "GPLv3"

# Installation and Migration hooks
after_install = "guv_ukv_hgb_report.setup.after_install"
after_migrate = "guv_ukv_hgb_report.setup.after_migrate"

# Document events for validation rules
doc_events = {
	"Cost Center": {
		"validate": "guv_ukv_hgb_report.setup.validate_cost_center"
	}
}
