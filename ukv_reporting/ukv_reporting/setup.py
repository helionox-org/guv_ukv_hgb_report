import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
	setup_app()

def after_migrate():
	setup_app()

def setup_app():
	setup_custom_fields()
	create_report_template()
	setup_workspaces()
	add_report_to_financial_reports_workspace()
	add_report_to_workspace_sidebar()
	setup_client_script()

def setup_custom_fields():
	custom_fields = {
		"Cost Center": [
			{
				"fieldname": "umsatzkostenverfahren_type",
				"label": "Umsatzkostenverfahren Type",
				"fieldtype": "Select",
				"options": "\nHerstellungskosten\nVertriebskosten\nVerwaltungskosten\nSonstige betriebliche Aufwendungen",
				"insert_after": "is_group",
				"translatable": 1,
			}
		]
	}
	create_custom_fields(custom_fields, ignore_validate=True, update=True)

def create_report_template():
	template_name = "GuV UKV HGB 275"
	if not frappe.db.exists("Financial Report Template", template_name):
		template = frappe.new_doc("Financial Report Template")
		template.template_name = template_name
		template.report_type = "Profit and Loss Statement"
		template.disabled = 0
		template.insert(ignore_permissions=True)
	else:
		template = frappe.get_doc("Financial Report Template", template_name)
		template.report_type = "Profit and Loss Statement"
		template.disabled = 0
		template.save(ignore_permissions=True)

def setup_workspaces():
	# Workspace Link for "Financial Report Template" DocType List
	ws_template_label = "Financial Report Templates"
	if not frappe.db.exists("Workspace", ws_template_label):
		ws1 = frappe.get_doc({
			"doctype": "Workspace",
			"label": ws_template_label,
			"title": ws_template_label,
			"type": "Link",
			"link_type": "DocType",
			"link_to": "Financial Report Template",
			"parent_page": "Financial Reports",
			"public": 1,
			"sequence_id": 1.0,
		})
		ws1.insert(ignore_permissions=True)
	else:
		ws1 = frappe.get_doc("Workspace", ws_template_label)
		ws1.label = ws_template_label
		ws1.title = ws_template_label
		ws1.type = "Link"
		ws1.link_type = "DocType"
		ws1.link_to = "Financial Report Template"
		ws1.parent_page = "Financial Reports"
		ws1.public = 1
		ws1.sequence_id = 1.0
		ws1.save(ignore_permissions=True)

	# Workspace Link for the Custom HGB Report
	ws_report_label = "GuV UKV HGB 275"
	if not frappe.db.exists("Workspace", ws_report_label):
		ws2 = frappe.get_doc({
			"doctype": "Workspace",
			"label": ws_report_label,
			"title": ws_report_label,
			"type": "Link",
			"link_type": "Report",
			"link_to": ws_report_label,
			"parent_page": "Financial Reports",
			"public": 1,
			"sequence_id": 2.0,
		})
		ws2.insert(ignore_permissions=True)
	else:
		ws2 = frappe.get_doc("Workspace", ws_report_label)
		ws2.label = ws_report_label
		ws2.title = ws_report_label
		ws2.type = "Link"
		ws2.link_type = "Report"
		ws2.link_to = ws_report_label
		ws2.parent_page = "Financial Reports"
		ws2.public = 1
		ws2.sequence_id = 2.0
		ws2.save(ignore_permissions=True)

	frappe.clear_cache()

def setup_client_script():
	script_name = "Cost Center - Umsatzkostenverfahren Type Validation"
	script_code = """
frappe.ui.form.on('Cost Center', {
	refresh(frm) {
		frm.trigger('toggle_umsatzkostenverfahren_type');
	},
	is_group(frm) {
		frm.trigger('toggle_umsatzkostenverfahren_type');
	},
	toggle_umsatzkostenverfahren_type(frm) {
		if (frm.doc.is_group) {
			frm.set_value('umsatzkostenverfahren_type', '');
			frm.set_df_property('umsatzkostenverfahren_type', 'read_only', 1);
		} else {
			frm.set_df_property('umsatzkostenverfahren_type', 'read_only', 0);
		}
	}
});
"""
	if not frappe.db.exists("Client Script", script_name):
		doc = frappe.get_doc({
			"doctype": "Client Script",
			"name": script_name,
			"dt": "Cost Center",
			"script": script_code,
			"enabled": 1,
		})
		doc.insert(ignore_permissions=True)
	else:
		doc = frappe.get_doc("Client Script", script_name)
		doc.script = script_code
		doc.enabled = 1
		doc.save(ignore_permissions=True)

def validate_cost_center(doc, method=None):
	if doc.is_group and doc.umsatzkostenverfahren_type:
		frappe.throw(_("Umsatzkostenverfahren Type must be empty for Group Cost Centers."))

def add_report_to_financial_reports_workspace():
	if not frappe.db.exists("Workspace", "Financial Reports"):
		return
	workspace = frappe.get_doc("Workspace", "Financial Reports")
	updated = False
	
	# Update old report link if present
	for link in workspace.links:
		if link.link_to == "GuV nach Umsatzkostenverfahren nach HGB 275 Abs 3":
			link.link_to = "GuV UKV HGB 275"
			link.label = "GuV UKV HGB 275"
			updated = True
			
	# If not updated and not present, append it after Profit and Loss Statement
	exists = any(link.link_to == "GuV UKV HGB 275" for link in workspace.links)
	if not exists:
		idx = 1
		for i, link in enumerate(workspace.links):
			if link.link_to == "Profit and Loss Statement":
				idx = i + 1
				break
		workspace.append("links", {
			"type": "Link",
			"link_type": "Report",
			"link_to": "GuV UKV HGB 275",
			"label": "GuV UKV HGB 275",
			"dependencies": "GL Entry",
			"is_query_report": 1,
			"idx": idx + 1
		})
		updated = True
		
	if updated:
		workspace.save(ignore_permissions=True)
		frappe.db.commit()

def add_report_to_workspace_sidebar():
	if not frappe.db.exists("Workspace Sidebar", "Financial Reports"):
		return
	sidebar = frappe.get_doc("Workspace Sidebar", "Financial Reports")
	updated = False
	
	# Update old report link if present
	for item in sidebar.items:
		if item.link_to in ("GuV nach Umsatzkostenverfahren nach HGB 275 Abs 3", "GuV UKV HGB 275") or item.label == "GuV HGB 275 (UKV)":
			item.link_to = "GuV UKV HGB 275"
			item.label = "GuV UKV HGB 275"
			item.link_type = "Report"
			item.type = "Link"
			updated = True
			
	# If not updated and not present, append it after Custom Financial Statement
	exists = any(item.link_to == "GuV UKV HGB 275" for item in sidebar.items)
	if not exists:
		idx = 1
		for i, item in enumerate(sidebar.items):
			if item.link_to == "Custom Financial Statement":
				idx = i + 1
				break
		sidebar.append("items", {
			"label": "GuV UKV HGB 275",
			"link_type": "Report",
			"link_to": "GuV UKV HGB 275",
			"type": "Link",
			"child": 1,
			"collapsible": 1,
			"indent": 0,
			"keep_closed": 0,
			"show_arrow": 0,
			"idx": idx + 1
		})
		updated = True
		
	if updated:
		sidebar.save(ignore_permissions=True)
		frappe.db.commit()
