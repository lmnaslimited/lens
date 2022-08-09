from __future__ import unicode_literals
import imp
from urllib import request
from warnings import filters
import frappe
from frappe import throw, msgprint, _
from frappe.utils import now
from frappe import throw, msgprint, _
import json
import requests


@frappe.whitelist()
def sync(*args, **kwargs):
    try:
        """
        This function will be executed when the Sync Action Button is clicked
        """
        # Initialize variables
        end_time = now()
        inactive_integrations = 0
        
        #print(*args, kwargs)
        #During subsequent enhancement add filter to filter only
        #the integration app from the sync is triggered
        integration_control_list = get_integration_control()
  
        for integration_control in integration_control_list:
           
            integration_control_doc = get_integration_control_doc(integration_control.name)
            integration_app = get_integration_app(integration_control.name)
            #print('Integrations', integrations.integration_doctype)
            for integration_doctype in integration_control_doc.integration_doctype:
                if integration_doctype.status == 'Approved' and not integration_doctype.unsubscribe:
                    if integration_doctype.direction == 'Inbound':
                        endpoint = get_endpoint(integration_app, integration_doctype, end_time)               
                        r = requests.get(endpoint)
                        request = r.json()
                        handle_request(request, integration_app, integration_doctype, end_time)
                    else:
                        frappe.msgprint(_("Integration for {0} is not yet developed").format('Inbound'))
                else:
                    inactive_integrations += 1
            if inactive_integrations > 0:
                frappe.msgprint(_(" {0} Inactive integrations not synced").format(inactive_integrations))
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("IndiaMART Sync Error"))
   
def get_integration_control():
    return frappe.db.get_list('Integration Control')
def get_integration_control_doc(integration_name):
    return frappe.get_doc('Integration Control', integration_name)  
def get_integration_app(integration_name):
    return frappe.get_doc('Integration App', integration_name)
def get_indiamart_settings():
    return frappe.get_doc('Indiamart Settings')
def update_doctype_last_run(integration_doc, end_time):
    try:
        integration_doc.last_run_time = end_time
        integration_doc.save(
            ignore_permissions=True, # ignore write permissions during insert
            ignore_version=True # do not create a version record
        )
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("IndiaMART Sync Error"))
def get_endpoint(app, doctype, end_time):
   
    if app.name == 'IndiaMART':
        endpoint = get_indiamart_endpoint(app, doctype, end_time)
    else:
        #recontruct this logic with Params
        frappe.throw('Integration for the requested app is not yet developed')
    return endpoint

def get_indiamart_endpoint(app, doctype, end_time):
    endpoint = app.api_url + '/?' + 'glusr_crm_key' + '=' + app.api_key + \
        '&' + 'start_time' + '=' + str(doctype.last_run_time) + \
            '&' + 'end_time' + '=' + str(end_time)

    return endpoint
# This method should be made more generic in future releases to accomodate 
# postman like requests    
def handle_request(request, integration_app, integration_doctype, end_time):
    count = 0
    if integration_doctype.ref_doctype == 'Lead':
        if request:
            if not request['MESSAGE'] == '':
                frappe.throw(request['MESSAGE'], '', request['STATUS'])
            else:
        
                for lead_data in request['RESPONSE']:
                    lead = add_lead(lead_data)
                    if lead:
                        count += 1
                frappe.msgprint(_("{0} Lead(s) Created").format(count))
                update_doctype_last_run(integration_doctype, end_time)

    else:
        frappe.msgprint(_("Integration for doctype {0} is not yet developed").format(integration_doctype.ref_doctype))

def add_lead(lead_data):
    try:
        if not frappe.db.exists("Lead", {"indiamart_id": lead_data['UNIQUE_QUERY_ID']}):
            new_lead = frappe.get_doc({
                    'doctype' : 'Lead',
                    'lead_name' : lead_data["SENDER_NAME"],
                   # 'email_id' : lead_data["SENDER_EMAIL"],
                    'phone' : lead_data["SENDER_MOBILE"],
                    'notes' : lead_data["QUERY_MESSAGE"],
                    'indiamart_id' : lead_data["UNIQUE_QUERY_ID"],
                    'source' : 'IndiaMART',
                    'company_name' : lead_data['SENDER_COMPANY'],

                })
            new_lead.insert(ignore_permissions=True)
            return new_lead
            
            
                

    except Exception as e:
        frappe.log_error(frappe.get_traceback())

    
   