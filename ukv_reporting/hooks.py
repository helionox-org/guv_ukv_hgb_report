app_name = "ukv_reporting"
app_title = "Ukv Reporting"
app_publisher = "Helionox GmbH"
app_description = "HGB Paragraph 275 Cost of Sales Method Profit and Loss Report"
app_email = "contact@helionox.eu"
app_license = "GPLv3"

# Installation and Migration hooks
after_install = "ukv_reporting.setup.after_install"
after_migrate = "ukv_reporting.setup.after_migrate"

# Document events for validation rules
doc_events = {
	"Cost Center": {
		"validate": "ukv_reporting.setup.validate_cost_center"
	}
}
