const REPORT_NAME = "GuV UKV HGB 275";

frappe.query_reports[REPORT_NAME] = $.extend(true, {}, erpnext.financial_statements, {
	initial_depth: 0,
	after_refresh: function (report) {
		if (report.$tree_footer) {
			report.$tree_footer.find("#tree-level").val(1);
		}
	}
});

// Update default values of standard filters
let from_fy_filter = frappe.query_reports[REPORT_NAME].filters.find(f => f.fieldname === "from_fiscal_year");
if (from_fy_filter) {
	from_fy_filter.default = erpnext.utils.get_fiscal_year(frappe.datetime.get_today(), false, false) || "2026";
}

let to_fy_filter = frappe.query_reports[REPORT_NAME].filters.find(f => f.fieldname === "to_fiscal_year");
if (to_fy_filter) {
	to_fy_filter.default = erpnext.utils.get_fiscal_year(frappe.datetime.get_today(), false, false) || "2026";
}

// Push additional filters
frappe.query_reports[REPORT_NAME].filters.push(
	{
		fieldname: "selected_view",
		label: __("Select View"),
		fieldtype: "Select",
		options: [
			{ value: "Report", label: __("Report View") },
			{ value: "Growth", label: __("Growth View") },
			{ value: "Margin", label: __("Margin View") },
		],
		default: "Report",
		reqd: 1,
	},
	{
		fieldname: "accumulated_values",
		label: __("Accumulated Values"),
		fieldtype: "Check",
		default: 0,
	},
	{
		fieldname: "include_default_book_entries",
		label: __("Include Default FB Entries"),
		fieldtype: "Check",
		default: 0,
	},
	{
		fieldname: "show_zero_values",
		label: __("Show zero values"),
		fieldtype: "Check",
		default: 0,
	}
);

erpnext.utils.add_dimensions(REPORT_NAME, 10);
