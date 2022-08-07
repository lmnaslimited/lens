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
        count = 0
        # The data is transmitted via keyword argument
        
        #indiamart_settings = json.loads(frappe._dict(kwargs).doc)
        indiamart_settings = get_indiamart_settings()
        print('indiamart Settings', indiamart_settings.crm_key)
        integration_control = get_integration_control(indiamart_settings)
        
        endpoint = get_endpoint(indiamart_settings, integration_control, end_time)
        print(endpoint)
        
        
        #data = {'CODE': 200, 'STATUS': 'SUCCESS', 'MESSAGE': '', 'TOTAL_RECORDS': 48, 'RESPONSE': [{'UNIQUE_QUERY_ID': '2205434837', 'QUERY_TYPE': 'W', 'QUERY_TIME': '2022-08-01 21:24:10', 'SENDER_NAME': 'Nikhil', 'SENDER_MOBILE': '+91-9893832746', 'SENDER_EMAIL': 'nj3101988@gmail.com', 'SENDER_COMPANY': 'Neminath Collection', 'SENDER_ADDRESS': 'Chandavarkar Rd, Bagh, Madhya Pradesh,         400092', 'SENDER_CITY': 'Bagh', 'SENDER_STATE': 'Madhya Pradesh', 'SENDER_COUNTRY_ISO': 'IN', 'SENDER_MOBILE_ALT': '', 'SENDER_EMAIL_ALT': '', 'QUERY_PRODUCT_NAME': 'FIVE FINGERS Automatic Multifunctional Non Woven Box Bag With Handle Fixing Machine, 200 mm - 600 m', 'QUERY_MESSAGE': 'I am interested in FIVE FINGERS Automatic Multifunctional Non Woven Box Bag With Handle Fixing Machine, 200 mm - 600 m<br>', 'CALL_DURATION': '', 'RECEIVER_MOBILE': ''}, {'UNIQUE_QUERY_ID': '401868541', 'QUERY_TYPE': 'P', 'QUERY_TIME': '2022-08-01 19:44:30', 'SENDER_NAME': 'Vijay Kumar', 'SENDER_MOBILE': '+91-9880983981', 'SENDER_EMAIL': 'vzingade58@gmail.com', 'SENDER_COMPANY': '', 'SENDER_ADDRESS': 'Koppal, Karnataka', 'SENDER_CITY': 'Koppal', 'SENDER_STATE': 'Karnataka', 'SENDER_COUNTRY_ISO': 'IN', 'SENDER_MOBILE_ALT': '', 'SENDER_EMAIL_ALT': '', 'QUERY_PRODUCT_NAME': '', 'QUERY_MESSAGE': '', 'CALL_DURATION': '', 'RECEIVER_MOBILE': ''}, {'UNIQUE_QUERY_ID': '2205368256', 'QUERY_TYPE': 'W', 'QUERY_TIME': '2022-08-01 19:43:01', 'SENDER_NAME': 'Vijay Kumar', 'SENDER_MOBILE': '+91-9880983981', 'SENDER_EMAIL': 'vzingade58@gmail.com', 'SENDER_COMPANY': '', 'SENDER_ADDRESS': 'Koppal, Karnataka', 'SENDER_CITY': 'Koppal', 'SENDER_STATE': 'Karnataka', 'SENDER_COUNTRY_ISO': 'IN', 'SENDER_MOBILE_ALT': '', 'SENDER_EMAIL_ALT': '', 'QUERY_PRODUCT_NAME': 'Automatic Non woven W/U Cut Bag Making Machine', 'QUERY_MESSAGE': 'I am interested in Automatic Non woven W/U Cut Bag Making Machine<br>', 'CALL_DURATION': '', 'RECEIVER_MOBILE': ''}, {'UNIQUE_QUERY_ID': '2205345624', 'QUERY_TYPE': 'W', 'QUERY_TIME': '2022-08-01 19:11:23', 'SENDER_NAME': 'Manish Jaimini', 'SENDER_MOBILE': '+91-9899924200', 'SENDER_EMAIL': 'manish9899924200@yahoo.com', 'SENDER_COMPANY': 'Yoz Tech India', 'SENDER_ADDRESS': 'B-9, Thapar Chamber, Paharganj, New Delhi, Delhi,         110055', 'SENDER_CITY': 'New Delhi', 'SENDER_STATE': 'Delhi', 'SENDER_COUNTRY_ISO': 'IN', 'SENDER_MOBILE_ALT': '+91-9990081818', 'SENDER_EMAIL_ALT': '', 'QUERY_PRODUCT_NAME': 'Paper Slitting Rewinding Machine', 'QUERY_MESSAGE': 'I want to buy Paper Slitting Rewinding Machine.\r\rKindly send me price and other details.<br> Quantity :   1<br> Quantity Unit :   Piece<br> Probable Order Value :   Rs. 2 to 5 Lakh<br> Probable Requirement Type :   Business Use<br>', 'CALL_DURATION': '', 'RECEIVER_MOBILE': ''}, {'UNIQUE_QUERY_ID': '401857762', 'QUERY_TYPE': 'P', 'QUERY_TIME': '2022-08-01 18:49:23', 'SENDER_NAME': 'BUYER', 'SENDER_MOBILE': '+91-9329143842', 'SENDER_EMAIL': '', 'SENDER_COMPANY': '', 'SENDER_ADDRESS': '', 'SENDER_CITY': '', 'SENDER_STATE': '', 'SENDER_COUNTRY_ISO': 'IN', 'SENDER_MOBILE_ALT': '', 'SENDER_EMAIL_ALT': '', 'QUERY_PRODUCT_NAME': '', 'QUERY_MESSAGE': '', 'CALL_DURATION': '121', 'RECEIVER_MOBILE': '9655286755'}, {'UNIQUE_QUERY_ID': '401847896', 'QUERY_TYPE': 'P', 'QUERY_TIME': '2022-08-01 18:16:16', 'SENDER_NAME': 'Sebastian Joseph', 'SENDER_MOBILE': '+91-6282606443', 'SENDER_EMAIL': 'bbenteretr@gmail.com', 'SENDER_COMPANY': '', 'SENDER_ADDRESS': 'Kottayam, Kerala', 'SENDER_CITY': 'Kottayam', 'SENDER_STATE': 'Kerala', 'SENDER_COUNTRY_ISO': 'IN', 'SENDER_MOBILE_ALT': '', 'SENDER_EMAIL_ALT': '', 'QUERY_PRODUCT_NAME': '', 'QUERY_MESSAGE': '', 'CALL_DURATION': '122', 'RECEIVER_MOBILE': '9655286755'}, {'UNIQUE_QUERY_ID': '401845866', 'QUERY_TYPE': 'P', 'QUERY_TIME': '2022-08-01 18:10:31', 'SENDER_NAME': 'Karthik', 'SENDER_MOBILE': '+91-9843964473', 'SENDER_EMAIL': 'aarudhraatraders@gmail.com', 'SENDER_COMPANY': 'Aarudhraa Traders', 'SENDER_ADDRESS': 'No. 38, Chandhrasekar Layout, Udumalpet, Tamil Nadu,         642126', 'SENDER_CITY': 'Udumalpet', 'SENDER_STATE': 'Tamil Nadu', 'SENDER_COUNTRY_ISO': 'IN', 'SENDER_MOBILE_ALT': '+91-7639563926', 'SENDER_EMAIL_ALT': '', 'QUERY_PRODUCT_NAME': 'Non woven Roll Slitting Winding Machine', 'QUERY_MESSAGE': '', 'CALL_DURATION': '21', 'RECEIVER_MOBILE': '9655286755'}, {'UNIQUE_QUERY_ID': '401805511', 'QUERY_TYPE': 'P', 'QUERY_TIME': '2022-08-01 16:58:08', 'SENDER_NAME': 'Anand', 'SENDER_MOBILE': '+91-9623067877', 'SENDER_EMAIL': 'uglaea353@gmail.com', 'SENDER_COMPANY': '', 'SENDER_ADDRESS': 'Nashik, Maharashtra', 'SENDER_CITY': 'Nashik', 'SENDER_STATE': 'Maharashtra', 'SENDER_COUNTRY_ISO': 'IN', 'SENDER_MOBILE_ALT': '', 'SENDER_EMAIL_ALT': '', 'QUERY_PRODUCT_NAME': '', 'QUERY_MESSAGE': '', 'CALL_DURATION': '12', 'RECEIVER_MOBILE': '9655222655'}, {'UNIQUE_QUERY_ID': '2205239826', 'QUERY_TYPE': 'W', 'QUERY_TIME': '2022-08-01 16:55:34', 'SENDER_NAME': 'Anand', 'SENDER_MOBILE': '+91-9623067877', 'SENDER_EMAIL': 'uglaea353@gmail.com', 'SENDER_COMPANY': '', 'SENDER_ADDRESS': 'Nashik, Maharashtra', 'SENDER_CITY': 'Nashik', 'SENDER_STATE': 'Maharashtra', 'SENDER_COUNTRY_ISO': 'IN', 'SENDER_MOBILE_ALT': '', 'SENDER_EMAIL_ALT': '', 'QUERY_PRODUCT_NAME': 'Papermachines', 'QUERY_MESSAGE': 'I want to purchase Papermachines. Kindly send me price and other details.<br> Capacity :   0-10  ton/day<br> Automation Grade :   Automatic<br> Probable Requirement Type :   Business Use<br>', 'CALL_DURATION': '', 'RECEIVER_MOBILE': ''}, {'UNIQUE_QUERY_ID': '2205230944', 'QUERY_TYPE': 'W', 'QUERY_TIME': '2022-08-01 16:41:22', 'SENDER_NAME': 'Vilas Salavi', 'SENDER_MOBILE': '+91-7666042732', 'SENDER_EMAIL': 'vilassalavi@gmail.com', 'SENDER_COMPANY': 'Vilas Shop', 'SENDER_ADDRESS': 'Kolhapur, Maharashtra', 'SENDER_CITY': 'Kolhapur', 'SENDER_STATE': 'Maharashtra', 'SENDER_COUNTRY_ISO': 'IN', 'SENDER_MOBILE_ALT': '', 'SENDER_EMAIL_ALT': '', 'QUERY_PRODUCT_NAME': 'Greenland Drinking Straw Making Machine', 'QUERY_MESSAGE': 'I want to purchase Greenland Drinking Straw Making Machine. Kindly send me price and other details.<br> Probable Requirement Type :   Business Use<br>', 'CALL_DURATION': '', 'RECEIVER_MOBILE': ''}]}
        #request = data
        
        
        r = requests.get(endpoint)
        request = r.json()
        
        if request:
            if not request['MESSAGE'] == '':
                frappe.throw(request['MESSAGE'], '', request['STATUS'])
        
        for lead_data in request['RESPONSE']:
            lead = add_lead(lead_data)
            if lead.name:
                count += 1
        frappe.msgprint(_("{0} Lead(s) Created").format(count))
        update_integration_control(integration_control, end_time)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("IndiaMART Sync Error"))

def get_indiamart_settings():
    return frappe.get_doc('Indiamart Settings')
def get_integration_control(interface):
    return frappe.get_last_doc('Integration Control', filters={'integration_name': interface.name})
def update_integration_control(integration_control, end_time):
    integration_control.last_run_time = end_time
    integration_control.save(
        ignore_permissions=True, # ignore write permissions during insert
        ignore_version=True # do not create a version record
    )
def get_endpoint(indiamart_settings, integration_control, end_time):
    endpoint = indiamart_settings.api_url + '/?' + 'glusr_crm_key' + '=' + indiamart_settings.crm_key + \
        '&' + 'start_time' + '=' + str(integration_control.last_run_time) + \
            '&' + 'end_time' + '=' + str(end_time)

    return endpoint


def add_lead(lead_data):
    try:
        if not frappe.db.exists("Lead", {"indiamart_id": lead_data['UNIQUE_QUERY_ID']}):
            new_lead = frappe.get_doc({
                    'doctype' : 'Lead',
                    'lead_name' : lead_data["SENDER_NAME"],
                    'email_address' : lead_data["SENDER_EMAIL"],
                    'phone' : lead_data["SENDER_MOBILE"],
                    'notes' : lead_data["QUERY_MESSAGE"],
                    'indiamart_id' : lead_data["UNIQUE_QUERY_ID"],
                    'source' : 'IndiaMART',
                    'company_name' : lead_data['SENDER_COMPANY'],

                })
            new_lead.insert(ignore_permissions=True)
            return new_lead
            """
            print('Lead already exist')
            lead = frappe.get_last_doc('Lead', filters={"indiamart_id": lead_data['UNIQUE_QUERY_ID']})

            print('Lead Found', lead.name)
            
            return lead
          
            doc = frappe.get_doc(dict(
				doctype="Lead",
				lead_name=lead_data["SENDER_NAME"],
				email_address=lead_data["SENDER_EMAIL"],
				phone=lead_data["SENDER_MOBILE"],
				notes=lead_data["QUERY_MESSAGE"],
				india_mart_id=lead_data["UNIQUE_QUERY_ID"],
				source="India Mart"
			)).insert(ignore_permissions=True)
            """
            
                

    except Exception as e:
        frappe.log_error(frappe.get_traceback())

    
   