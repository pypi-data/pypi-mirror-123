import requests

''' Python wrapper for Contactually API v2. Refer to Readme.md for examples'''


class Request:
    _host = "https://api.contactually.com/v2"
   
    def __init__(self, ctoken, method, dest, payload=None, params=None, headers=None):
        self.method = method
        self.url = self._host + dest
        self.payload = payload
        self.params = params
        if headers: 
            self.headers = headers
        else: 
            self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {ctoken}',
            'Content-type': 'application/json'
        }

    def submit(self):
        response = requests.request(self.method, self.url, headers=self.headers, json=self.payload, params=self.params)
        return response.json()

class Contactually:
    _reserved = ['self', 'payload', 'dest', 'method']

    def __init__(self, ctoken, host='https://api.contactually.com/v2'):
        self.token = ctoken

    def _payload_fact(self, params, data_dict=True, exclude=None):
        payload = {'data':{}} if data_dict else {}
        suffixes = ['before','after','none','min','max']
        exclude = exclude+self._reserved if exclude else self._reserved


        for key, val in params:
            if key not in exclude and val: 
                for suffix in suffixes: 
                    if key[-len(suffix):] == suffix:
                        key = f'{key[:-len(suffix)-1]}.{suffix}'
                    if key == 'query_string':
                        key = 'q'
                if data_dict:
                    payload['data'][key] = val
                else:
                    payload[key] = val
        return payload

    def fetch_current_user(self):
        method = 'GET'
        dest = '/me'
        return Request(self.token, method, dest)

    def update_current_user(self, first_name=None, last_name=None, email=None, avatar_url=None, 
                            phone_number=None, contactually_goal=None, default_message_account_id=None, 
                            default_message_subject=None, default_message_bcc=None, onboarding_step=None, 
                            onboarding_video_seconds=None, show_events_on_dash=None, nps_prompt_due=None, 
                            dismissed_getting_started=None, organization_id=None, job_title=None, 
                            website=None, street_1=None, street_2=None, city=None, state=None, 
                            country=None, zip_code=None, prompted_referral_at=None, contact_columns:list=None, 
                            partner_user_columns=None, partner_user_aggregation_columns=None, 
                            partner_rollup_reporting_columns=None, partner_user_health_columns=None,
                            chrome_plugin_version=None, show_recommendation_onboarding=None, 
                            dismissed_recommendation_onboarding_at=None, task_email_days_enabled=None, 
                            task_email_time=None, email_signature=None, time_zone=None, industry_id=None):
        params = ['first_name','last_name','email','avatar_url','phone_number']
        settings_params = [key for key in locals().keys() if key not in params and key != 'self']
        payload = self._payload_fact(locals().items(), exclude=settings_params + ['settings_params','params'])
        settings = self._payload_fact(locals().items(), exclude=params + ['settings_params', 'params'])
       
        if settings: 
            payload['settings'] = settings

        dest = '/me'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)


    
    def fetch_buckets(self, id=None, id_not=None, created_at_before=None, created_at_after=None,
                      created_at_none=None, updated_at_before=None, updated_at_after=None,
                      query_string=None, order=None, page=None, page_size=None, offset=None):

        params = self._payload_fact(locals().items(),data_dict=False)
        method = 'GET'
        dest = '/buckets'
        return Request(self.token, method, dest, params=params)

    
    def fetch_bucket(self, bucket_id: str):
        method = 'GET'
        dest = f'/buckets/{bucket_id}'
        return Request(self.token, method, dest)

    
    def create_bucket(self, name=None, goal=None, reminder_interval=None, cloned_from_id=None):
        payload = {'data': {'name': name, 'goal': goal,
                            'reminder_interval': reminder_interval, 'cloned_from_id': cloned_from_id}}
        method = 'POST'
        dest = '/buckets'
        return Request(self.token, method, dest, payload=payload)

    
    def update_bucket(self, bucket_id: str, name=None, goal=None, reminder_interval: int=None):
        params = {'name': name, 'goal': goal,
                  'reminder_interval': reminder_interval}
        method = 'PUT'
        dest = f'/buckets/{bucket_id}'
        return Request(self.token, method, dest, params=params)

    
    def delete_bucket(self, bucket_id):
        method = 'DELETE'
        dest = f'/buckets/{bucket_id}'
        return Request(self.token, method, dest)

    
    def fetch_all_bucket_contacts(self, bucket_id, id=None, id_not=None, created_at_before=None, created_at_after=None,
                                  created_at_none=None, updated_at_before=None, updated_at_after=None, updated_at_none=None,
                                  audiences=None, audiences_all=None, audiences_not=None, company=None, location=None,
                                  connected_to=None, tags=None, tags_not=None, connected_accounts=None, external_id=None,
                                  external_id_not=None, external_id_presence=None, last_bucketed_at_before=None,
                                  last_bucketed_at_after=None, last_bucketed_at_none=None, is_overdue=None,
                                  status=None, status_not=None, last_contacted_before=None, last_contacted_after=None,
                                  last_contacted_none=None, inbound_last_contacted_at_before=None, inbound_last_contacted_at_after=None,
                                  inbound_last_contacted_at_none=None, times_contacted_min=None, times_contacted_max=None,
                                  times_contacted_inbound_min=None, times_contacted_inbound_max=None, total_interaction_count_min=None,
                                  total_interaction_count_max=None, relationship_types=None, days_to_followup_min=None, days_to_followup_max=None,
                                  days_overdue_min=None, days_overdue_max=None, recurring_type=None, recurring_type_not=None,
                                  recurring_next_due_date_before=None, recurring_next_due_date_after=None, deals=None, assigned_to=None,
                                  assigned_to_not=None, lead_pools=None, email=None, email_not=None, address=None, bucketed_at_before=None,
                                  bucketed_at_after=None, bucketed_at_none=None, query_string=None, order=None, page=None, page_size=None, offset=None):


        params = self._payload_fact(locals().items(),data_dict=False,exclude=['bucket_id'])
        method = 'GET'
        dest = f'/buckets/{bucket_id}/contacts'
        print(dest)
        return Request(self.token, method, dest, params=params)

    
    def fetch_contacts(self, method='GET', id=None, id_not=None, created_at_before=None, created_at_after=None, create_at_none=None,
                       updated_at_before=None, updated_at_after=None, updated_at_none=None, audiences=None, audiences_all=None,
                       audiences_not=None, company=None, location=None, connected_to=None, tags=None, tags_all=None, tags_not=None,
                       connected_accounts=None, external_id=None, external_id_not=None, external_id_presence=None, last_bucketed_at_before=None,
                       last_bucketed_at_after=None, last_bucketed_at_none=None, is_overdue=None, status=None, status_not=None, last_contacted_before=None, last_contacted_after=None,
                       last_contacted_none=None, inbound_last_contacted_at_before=None, inbound_last_contacted_at_after=None,
                       inbound_last_contacted_at_none=None, times_contacted_min=None, times_contacted_max=None,
                       times_contacted_inbound_min=None, times_contacted_inbound_max=None, total_interaction_count_min=None,
                       total_interaction_count_max=None, relationship_types=None, days_to_followup_min=None, days_to_followup_max=None,
                       days_overdue_min=None, days_overdue_max=None, recurring_type=None, recurring_type_not=None,
                       recurring_next_due_date_before=None, recurring_next_due_date_after=None, archived_at_before=None, archived_at_after=None,
                       archived_at_none=None, buckets=None, buckets_all=None, buckets_not=None, deals=None, assigned_to=None, assigned_to_not=None,
                       lead_pools=None, email=None, email_not=None, address=None, archived=None, with_archived=None, team_search=None,
                       q_fields=None, custom_field_id=None, custom_field_id_param=None, custom_field_before=None, custom_field_after=None,
                       custom_field_min=None, custom_field_max=None, query_string=None, notes=None, order=None, page=None, page_size=None, offset=None, list_ids=False):

        params = self._payload_fact(locals().items(), data_dict=False, exclude=[x for x in locals() if 'custom' in x])

        dest = '/contacts'

        if custom_field_id:
            custom_field_str = f'custom_field_{custom_field_id}'
            params[custom_field_str] = custom_field_id_param
            params[f'{custom_field_str}.before'] = custom_field_before
            params[f'{custom_field_str}.after'] = custom_field_after
            params[f'{custom_field_str}.min'] = custom_field_min
            params[f'{custom_field_str}.max'] = custom_field_max

        if list_ids:
            dest += '/resolve'

        elif method == "POST" and not fetch_ids:
            dest += '/search'
            payload = {'data': {x[0]: x[1] for x in params.items() if x[1]}}
            print(payload)
            return Request(self.token, method, dest, payload=payload)

        return Request(self.token, method, dest, params=params)

    
    def create_new_contact(self, contact:dict):

        payload = {'data':contact}
        dest = '/contacts'
        method = "POST"

        return Request(self.token, method, dest, payload=payload)

    def generate_contact(self, first_name: str, last_name: str, company: str=None, location: str=None,
                         title: str=None, avatar_url: str=None, days_to_followup: int=None, created_at=None,
                         relationship_types: str=None, tags: str=None, assigned_to_id: str=None, external_id: str=None,
                         audience_list=None, addresses: list=None, custom_fields: list=None, email_addresses: list=None,
                         phone_numbers: list=None, social_media_profiles: list=None, websites: list=None, grouping_ids: str=None,
                         bucket_ids: str=None, tag_ids: str=None, audience_ids: str=None, create_contact=False):
        ''' 
        Generates a new contact. List parameters should contain dict with parameter data. 
        Ex. an address parameter: 
                            [{"label":"Home",
                            "street_1": "123 Sesame St.",
                            "city": "Boston",
                            "state": "Massachusetts",
                            "zip": "02101",
                            "country": "United States"} }]

        Set create_contact to True to save generated contact to Contactually or pass to Contactually.create_new_contact
        '''

        contact = self._payload_fact(locals().items(), data_dict=False, exclude=['create_contact'])
        
        if create_contact:
            return self.create_new_contact(contact)

        return contact


    
    def create_multiple_contacts(self, contacts:list):
        ''' 
        Creates multiple contacts. List parameters should contain dict with parameter data. 
        Ex. an address parameter: 
                            [{"label":"Home",
                            "street_1": "123 Sesame St.",
                            "city": "Boston",
                            "state": "Massachusetts",
                            "zip": "02101",
                            "country": "United States"} }]
        '''

        payload = {'data':contacts}
        dest = '/contacts/bulk_create'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    
    def delete_contact(self, contact_id: str):
        dest = f'/contacts/{contact_id}'
        method = 'DELETE'
        
        return Request(self.token, method, dest)

    
    def bulk_delete_contacts(self, contact_ids: list):
        dest = '/contacts'
        method = 'DELETE'
        payload = {'data': {'contact_ids': contact_ids}}

        return Request(self.token, method, dest, payload=payload)

    
    def fetch_contact(self, contact_id, with_archived=False):
        dest = f'/contacts/{contact_id}'
        method = 'GET'
        payload = {'with_archived':with_archived}

        return Request(self.token, method, dest, payload=payload)

    
    def update_contact(self, contact_id, first_name: str=None, last_name: str=None, company: str=None, location: str=None,
                           title: str=None, avatar_url: str=None, days_to_followup: int=None, created_at=None,
                           relationship_types: str=None, tags: str=None, assigned_to_id: str=None, external_id: str=None,
                           audience_list=None, addresses: list=None, custom_fields: list=None, email_addresses: list=None,
                           phone_numbers: list=None, social_media_profiles: list=None, websites: list=None, grouping_ids: str=None,
                           bucket_ids: str=None, tag_ids: str=None, audience_ids: str=None):

        payload = self._payload_fact(locals().items())
        dest = f'/contacts/{contact_id}'
        method = 'PUT'
        

        return Request(self.token, method, dest, payload=payload)

    
    def update_multiple_contacts(self, contact_ids,field, changes:dict):
        payload = {'data':{'contact_ids':contact_ids,'field':field, 'changes':[{"value":value, "type":change_type} for value,change_type in changes.items()] }}
        dest = '/contacts/bulk-change'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    
    def merge_contacts(self, contact_id, contact_ids:list):
        payload = {'data': {'contact_ids':contact_ids}}
        dest = f'/contacts/{contact_id}/merge'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    
    def archive_contact(self, contact_id, contact_ids:list):
        dest = f'/contacts/{contact_id}/archive'
        method = 'POST'

        return Request(self.token, method, dest)

    
    def unarchive_contact(self, contact_id, contact_ids:list):
        dest = f'/contacts/{contact_id}/unarchive'
        method = 'POST'

        return Request(self.token, method, dest)

    
    def archive_multiple_contacts(self, contact_ids:list):
        payload = {'data':{'contact_ids':contact_ids}}
        dest = '/contacts/archive-multiple'

    
    def unarchive_multiple_contacts(self, contact_ids:list):
        payload = {'data':{'contact_ids':contact_ids}}
        dest = '/contacts/unarchive-multiple'

    
    def export_contacts_to_csv(self, assigned_to:list=None, buckets:list=None, company:list=None, connected_accounts:list=None, 
                                connected_to:list=None, created_at_after=None, created_at_before=None, custom_field_id=None, 
                                custom_field_param=None, contact_ids:list=None, last_contacted_after=None, 
                                last_contacted_before=None, location:list=None, query_string=None, status:list=None, 
                                tags:list=None, times_contacted_min:int=None, times_contacted_max:int=None, team_search:bool=False, order:str=None, 
                                include_notes:bool=True):
       
        filters = self._payload_fact(locals().items(), data_dict=False, exclude=['include_notes'])
        payload = {'data':{'filters':filters},"include_notes":include_notes}
        dest='/contacts/export'
        method = 'POST'
        print(payload)
        return Request(self.token, method, dest, payload=payload)

    
    def fetch_job(self, job_id):
        dest = f'/jobs/{job_id}'
        method = 'GET'

        return Request(self.token, method, dest)

    
    def fetch_companies(self, id=None, id_not=None, created_at_before=None, created_at_after=None, created_at_none=None, updated_at_before=None, updated_at_after=None,
                        update_at_none=None, query_string=None, order:list=None, page:int=None, page_size:int=None, offset=None):
        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/companies'
        method = 'POST'

        return Request(self.token, method, dest, params=params)

    
    def create_company(self, name):
        payload = {'data':{'name':name}}
        dest = '/companies'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    
    def update_company(self, company_id, name):
        payload = {'data':{'name':name}}
        dest = f'/companies/{company_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    
    def delete_company(self, company_id):
        dest = f'/companies/{company_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    
    def fetch_linked_contacts(self, contact_id, id=None, id_not=None, created_at_before=None, created_at_none=None, updated_at_before=None, updated_at_after=None,
                              updated_at_none=None, order=None, page=None, page_size=None, offset=None):
        
        params = self._payload_fact(locals().items(), data_dict=False)
        dest = f"/contacts/{contact_id}/linked-contacts"
        method = "GET"

        return Request(self.token, method, dest, params=params)

    
    def create_linked_contacts(self, contact_id, data:dict):
        ''' 
        Creates link between two contacts. Submit data as dict object containing 
        parameters where key is contact_id and value is label.
        ex: 
                        {'12345':'agent', '67890':'friend'} 

        Valid labels: 
                        agent, coworker, child, friend, client, other, father_mother, 
                        partner, relative, sibling, spouse, referrer, referee
        '''

        payload = {'data':[{'label':label, 'contact_id':contact_id} for contact_id, label in data.items()]}
        dest = f'/contacts/{contact_id}/linked-contacts'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def delete_linked_contacts(self, contact_id, data:dict): 
        '''
        Deletes a linked contact. Submit data as dict object containing
        parameters where key is contact_id and value is label. 
        ex: 
                        {'12345':'agent', '67890':'friend'} 

        Valid labels: 
                        agent, coworker, child, friend, client, other, father_mother, 
                        partner, relative, sibling, spouse, referrer, referee
        '''

        payload = {'data':[{'label':label, 'contact_id':contact_id} for contact_id, label in data.items()]}
        dest = f'/contacts/{contact_id}/linked-contacts'
        method = 'DELETE'

        return Request(self.token, method, dest, payload=payload)

    def fetch_custom_field(self, custom_field_id):
        '''
        Fetch a custom field
        '''

        dest = f'/team/custom-fields/{custom_field_id}'
        method = 'GET'

        return Request(self.token, method, dest)

    def fetch_custom_fields(self, id=None, id_not=None, created_at_before=None, created_at_after=None, created_at_none:bool=None, updated_at_before=None, updated_at_after=None, 
                            updated_at_none:bool=None, type:list=None, type_not:list=None, query_string=None, order=None, page=None, page_size=None, offset=None):
        '''
        Fetch custom fields.  
        Available types: 
                        textfield
                        textarea
                        dropdown
                        boolean
                        date
                        decimal
        '''
        
        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/team/custom-fields'
        method = 'GET'

        return Request(self.token, method, dest, params=params)


    def create_custom_field(self, name, type=None, default_value=None, dropdown_options:list=None):
        '''
        Create a custom field. 
        Available types: 
                        textfield
                        textarea
                        dropdown
                        boolean
                        date
                        decimal
        '''

        payload = self._payload_fact(locals().items())
        dest = '/team/custom-fields'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def update_custom_field(self, custom_field_id, name=None, default_value=None, dropdown_options:list=None):
        payload = self._payload_fact(locals().items(), exclude=['custom_field_id'])
        dest = f'/custom-fields/{custom_field_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def delete_custom_field(self, custom_field_id):
        dest = f'/team/custom-fields/{custom_field_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def fetch_deal(self, deal_id):
        dest = f'/deals/{deal_id}'
        method = 'GET'

        return Request(self.token, method, dest)

    def fetch_contact_deals(self, contact_id, id=None, id_not=None, created_at_before=None, created_at_after=None, created_at_none=None, updated_at_before=None,
                            updated_at_after=None, updated_at_none:bool=None, pipelines:list=None, stages:list=None, order:list=None, page=None,
                            page_size=None, offset=None):
        '''
        List deals associated with a contact
        '''

        params = self._payload_fact(locals().items(), data_dict=False, exclude=['contact_id'])
        dest = f'/contacts/{contact_id}/deals'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def fetch_pipeline_deals(self, pipeline_id, id=None, id_not=None, created_at_before=None, created_at_after=None, created_at_none=None, updated_at_before=None,
                            updated_at_after=None, updated_at_none:bool=None, pipelines:list=None, stages:list=None, order:list=None, page=None,
                            page_size=None, offset=None):
        '''
        List deals associated with a pipeline
        '''
        params = self._payload_fact(locals().items(), data_dict=False, exclude=['pipeline_id'])
        dest = f'/pipelines/{pipeline_id}/deals'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def create_deal(self, name, stage_id, id=None, created_at=None, updated_at=None, value=None, status=None):
        payload = self._payload_fact(locals().items())
        dest = '/deals'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def update_deal(self, deal_id, id=None, created_at=None, updated_at=None, value=None, status=None):
        payload = self._payload_fact(locals().items(), exclude=['deal_id'])
        dest = f'/deals/{deal_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def advance_deal(self, deal_id):
        dest = f'/deals/deal_id/advance'
        method = 'POST'

        return Request(self.token, method, dest)

    def regress_deal(self, deal_id):
        dest = f'/deals/deal_id/regress'
        method = 'POST'

        return Request(self.token, method, dest)

    def fetch_contact_interactions(self, contact_id, id=None, id_not=None, created_at_before=None, created_at_after=None, created_at_none=None, updated_at_before=None,
                                   updated_at_after=None, updated_at_none:bool=None, timestamp_before=None, timestamp_after=None, timestamp_none=None, type:list=None, type_not:list=None,
                                   subtype:list=None, subtype_not:list=None, order:list=None, page=None, page_size=None, offset=None):

        params = self._payload_fact(locals().items(), exclude=['contact_id'], data_dict=False)
        dest = f'/contacts/{contact_id}/interactions'
        method = 'GET'

        return Request(self.token, method, dest, params=params)


    def fetch_interaction(self, interaction_id):
        dest = f'/interactions/{interaction_id}'
        method = 'GET'

        return Request(self.token, method, dest)


    def fetch_interactions(self, id=None, id_not=None, created_at_before=None, created_at_after=None, created_at_none=None, updated_at_before=None,
                           updated_at_after=None, updated_at_none:bool=None, timestamp_before=None, timestamp_after=None, timestamp_none=None, type:list=None, type_not:list=None,
                           subtype:list=None, subtype_not:list=None, order:list=None, page=None, page_size=None, offset=None):
        '''
        Fetch interactions for the current user
        '''

        params = self._payload_fact(locals().items(), data_dict=False)
        dest = f'/me/interactions'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def fetch_interaction_content(self, interaction_id):
        dest = f'/interactions/{interaction_id}/content'
        method = 'GET'

        return Request(self.token, method, dest)

    def fetch_interaction_participants(self, interaction_id):
        dest = f'/interactions/{interaction_id}/participants'
        method = 'Get'

    def create_interaction(self, body=None, initiated_by_contact=None, subject=None, timestamp=None, type:str=None, thread_id=None, 
                           ends_at=None, subtype=None, placeholder=None, message_id=None, participants:dict=None):
        '''
        Create an interaction. 
        Available types: 
                        calendar_event
                        email
                        custom_interaction
                        facebook
                        other
                        in_person
                        linked_in
                        mad_mimi
                        mail_chimp
                        phone
                        sms
                        twitter
                        zapier
        Participants parameter should be submitted as dict with contact_id as key and handle as value. 
        ex: 
                        {'12345':'friend'}
        '''

        payload = self._payload_fact(locals().items(), exclude=['participants'])

        if participants:
            payload['data']['participants'] = [{'contact_id':contact_id, 'handle':handle} for contact_id, handle in participants.items()]

        dest = '/interactions'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def update_interactions(self, interaction_id, body=None, initiated_by_contact=None, subject=None, timestamp=None, type:str=None, thread_id=None, 
                           ends_at=None, subtype=None, placeholder=None, message_id=None, participants:dict=None):
        '''
        Update an interaction. 
        Available types: 
                        calendar_event
                        email
                        custom_interaction
                        facebook
                        other
                        in_person
                        linked_in
                        mad_mimi
                        mail_chimp
                        phone
                        sms
                        twitter
                        zapier
        Participants parameter should be submitted as dict with contact_id as key and handle as value. 
        ex: 
                        {'12345':'friend'}
        '''

        payload = self._payload_fact(locals().items(), exclude=['interaction_id'])
        dest = f'/interactions/{interaction_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def delete_interaction(self, interaction_id):
        dest = f'/interactions/{interaction_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def fetch_merge_suggestions(self, id=None, id_not=None, created_at_before=None, created_at_after=None, created_at_none:bool=None, updated_at_before=None, updated_at_after=None, 
                                updated_at_none=None, contact_id:list=None, contact_id_not=None, order=None, page=None, page_size=None, offset=None, list_ids=False):
        '''
        Get existing merge suggestions (duplicates). 
        Combines 'Fetch Existing Merge Suggestions' and 'Fetch Contact IDs for the merge suggestion' 
        '''

        params = self._payload_fact(locals().items(), data_dict=False, exclude=['list_ids'])
        dest = '/merge-suggestions'
        method = 'GET'

        if list_contact_ids: 
            dest += '/resolve'

        return Request(self.token, method, dest, params=params)

    def generate_merge_submissions(self, merge_suggestion_id, accepted_contacts:list=None, rejected_contacts:list=None):
        merge_id = f'merge_suggestion_{merge_suggestion_id}'
        contacts_to_merge = {merge_id:{}}

        if accepted_contacts:
            contacts_to_merge[merge_id]['accepted'] = ['contact_'+x for x in accepted_contacts]

        if rejected_contacts:
            contacts_to_merge[merge_id]['rejected'] = ['contact_'+x for x in rejected_contacts]
        return contacts_to_merge

    def process_merge_suggestions(self, contacts_to_process:list):
        payload = {'data':{'merge_suggestions':{}}}
        dest = '/merge-suggestions/reviews'
        method = 'POST'

        for contacts_dict in contacts_to_process:
            for key, val in contacts_dict.items():
                payload['data']['merge_suggestions'][key] = val
        
        return Request(self.token, method, dest, payload=payload)

    def fetch_messages(self, id=None, id_not=None, created_at_before=None, created_at_after=None, created_at_none=None, updated_at_before=None, updated_at_after=None, 
                       updated_at_none=None, bulk_message_id:list=None, bulk_message_id_not:list=None, event_type:list=None, event_type_not:list=None, sent_at_before=None,
                       sent_at_after=None, sent_at_none=None, status=None, status_not=None, enable_open_tracking:bool=None, cnable_click_tracking:bool=None, 
                       enable_response_tracking:bool=None, require_response:bool=None, sent_in_bulk:bool=None, query_string=None, order=None, page=None, 
                       page_size=None, offset=None, list_ids=False):
        params = self._payload_fact(locals().items(), data_dict=False, exclude=['list_ids'])
        dest = '/messages'

        if list_ids:
            dest += '/resolve'
            method = 'POST'
        else:
            method = 'GET'

        return Request(self.token, method, dest, params=params)

    def fetch_message(self, message_id):
        dest = f'/messages/{message_id}'
        method = 'GET'

        return Request(self.token, method, dest)

    def create_message(self, account_id, contact_id=None, subject=None, body=None, message_template_id=None, external_template_id=None, response_tracking_enabled=True, 
                       open_tracking_enabled=False, click_tracking_enabled=False, response_required_by=None, default_bcc_disabled:bool=None, open_notification_enabled:bool=None,
                       thread_id=None, in_reply_to=None, references=None, action_plan=None, auto_send=None, object_id=None, recipients:list=None, attachments:list=None):

        payload = self._payload_fact(locals().items(), exclude=['account_id', 'action_plan', 'auto_send', 'object_id'])

        dest = '/messages'
        method = 'POST'

        if any([action_plan, auto_send, object_id]):
            payload['metadata'] = {key:val for key, val in locals().items() if key in ['action_plan', 'auto_send', 'object_id'] and val}

        return Request(self.token, method, dest, payload=payload)

    def create_recipient(self, contact_id, contact_identity_id, handle=None, recipient_type=None):
        ''' 
        Simple helper function to quickly create recipient dictionary for create_message(). 
        '''

        recipient = {'contact_id':contact_id, 'contact_identity_id':contact_identity_id}

        if handle:
            recipient['handle'] = handle

        if recipient_type:
            recipient['type'] = recipient_type

        return recipient

    def create_attachment(self, filename, url, mimetype=None):
        '''
        Simple helper function to quickly create attachment dictionary for create_messaeg(). 
        '''

        attachment = {'filename':filename, 'url':url}

        if mimetype:
            attachment['mimetype'] = mimetype

        return attachment

    def delete_messages(self, message_ids:list):
        payload = {'data':[message_ids]}
        dest = '/messages'
        method = 'DELETE'

        return Request(self.token, method, dest, payload=payload)

    def delete_message(self, message_id):
        dest = f'/messages/{message_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def preview_message(self, account_id, contact_id=None, subject=None, body=None, message_template_id=None, external_template_id=None, 
                        response_tracking_enabled=True, open_tracking_enabled=False, client_tracking_enabled=False, response_required_by=None, default_bcc_disable:bool=None, 
                        open_notification_enabled:bool=None, thread_id=None, in_reply_to=None, references=None, action_plan=None, auto_send=None, object_id=None, 
                        recipients:list=None, attachments:list=None, include_signature:bool=None):

        payload = self._payload_fact(locals().items(), exclude=['account_id', 'action_plan', 'auto_send', 'object_id'])

        dest = '/messages/preview'
        method = 'POST'

        if any([action_plan, auto_send, object_id]):
            payload['metadata'] = {key:val for key, val in locals().items() if key in ['action_plan', 'auto_send', 'object_id'] and val}

        return Request(self.token, method, dest, payload=payload)

    def update_message(self, message_id, account_id, contact_id=None, subject=None, body=None, message_template_id=None, external_template_id=None, 
                        response_tracking_enabled=True, open_tracking_enabled=False, client_tracking_enabled=False, response_required_by=None, default_bcc_disable:bool=None, 
                        open_notification_enabled:bool=None, thread_id=None, in_reply_to=None, references=None, action_plan=None, auto_send=None, object_id=None, 
                        recipients:list=None, attachments:list=None, include_signature:bool=None):
        payload = self._payload_fact(locals().items(), exclude=['account_id', 'action_plan', 'auto_send', 'object_id'])

        dest = f'/messages/{message_id}'
        method = 'PUT'

        if any([action_plan, auto_send, object_id]):
            payload['metadata'] = {key:val for key, val in locals().items() if key in ['action_plan', 'auto_send', 'object_id'] and val}

        return Request(self.token, method, dest, payload=payload)

    def deliver_drafted_message(self, message_id, scheduled_at=None):
        dest = f'/messages/{message_id}/deliver'
        payload = {'data':{'scheduled_at':scheduled_at}}
        method = POST

        return Request(self.token, method, dest, payload=payload)

    def fetch_message_templates(id=None, id_not=None, created_at_before=None, created_at_after=None, created_at_none=None, updated_at_before=None, updated_at_after=None, 
                                updated_at_none=None, email_categories:list=None, cloned_from_id:list=None, cloned_from_id_not=None, last_used_at_before=None, 
                                last_used_at_after=None, last_used_at_none=None, usage_count_min=None, usage_count_max=None, cloned_from_id_presence=None,
                                query_string=None, order=None, page=None, page_size=None, offset=None):

        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/message_templates'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def fetch_message_template(self, message_id):
        dest = f'/message-templates/{message_id}'
        method = 'GET'

        return Request(self.token, method, dest)

    def create_message_template(self, name=None, goal=None, subject=None, body=None, include_signature:bool=None, 
                                attachments:dict=None, email_categories:list=None, cloned_from_id=None):
        payload = self._payload_fact(locals().items())
        dest = '/message_templates'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def update_message_template(self, message_id, name=None, goal=None, subject=None, body=None, include_signature:bool=None, 
                                attachments:dict=None, email_categories:list=None, cloned_from_id=None):
        payload = self._payload_fact(locals().items(), exclude=['message_id'])
        dest = f'messages-templates/{message_id}'
        method = 'PUT' 

        return Request(self.token, method, dest, payload=payload)

    def delete_message_template(self, message_id):
        dest = f'/message-templates/{message_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def populate_message_template(self, message_id, contact_id):
        payload = {'data':{'contact_id':contact_id}}
        dest = f'/message-templates/{message_id}/populate'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def add_external_ids_to_templates(self, template_mapping):
        payload = {'data':{'template_mapping':template_mapping}}
        dest = '/message-templates/migrate'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def fetch_contact_notes(self, contact_id, id=None, id_not=None, created_at_before=None, created_at_after=None, 
                           created_at_none=None, updated_at_before=None, updated_at_after=None, updated_at_none=None,
                           order=None, page=None, page_size=None, offset=None):

        params = self._payload_fact(locals().items(),exclude=['contact_id'])
        dest = f'/contacts/{contact_id}/notes'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def fetch_notes(self, id=None, id_not=None, created_at_before=None, created_at_after=None, 
                    created_at_none=None, updated_at_before=None, updated_at_after=None, updated_at_none=None,
                    order=None, page=None, page_size=None, offset=None):

        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/notes'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def fetch_note(self, note_id):
        dest = f'/notes/{note_id}'
        method = 'GET'

        return Request(self.token, method, dest)

    def create_note(self, body=None, contact_id=None, timestamp=None):
        payload = self._payload_fact(locals().items())
        dest = '/notes'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def update_note(self, note_id, body=None, contact_id=None, timestamp=None):
        payload = self._payload_fact(locals().items(), exclude=['note_id'])
        dest = f'/notes/{note_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def delete_note(self, note_id): 
        dest = f'/notes/{note_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def fetch_notifications(self, id=None, id_not=None, created_at_before=None, created_at_after=None, 
                            created_at_none=None, updated_at_before=None, updated_at_after=None, 
                            updated_at_none:bool=None, read_at_before:bool=None, read_at_after:bool=None, read_at_none:bool=None, 
                            read:bool=None): 
        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/notifications'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def mark_as_read(self, notification_id):
        dest = f'/notifications/{notification_id}'
        method = 'POST'

        return Request(self.token, method, dest)

    def fetch_partner_team_contacts(self, id=None, id_not=None, created_at_before=None, created_at_after=None, 
                                    created_at_none=None, updated_at_before=None, updated_at_after=None, 
                                    updated_at_none:bool=None, email:list = None, email_not:list=None, 
                                    external_id:list=None, external_id_not:list=None, external_id_presence:bool=None,
                                    tags=None, tags_all=None, tags_not=None, order=None, page=None,
                                    page_size=None, offset=None):

        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/partners/contacts'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def update_partner_team_contact(self, contact_id, **kwargs):
        request = self.update_contact(contact_id, **kwargs)
        request.url = f'{request._host}/partners/{contact_id}'
        return request

    def fetch_partner_custom_field(self, custom_field_id):
        dest = '/partners/custom-field'
        method = 'GET'
        return Request(self.token, method, dest)

    def fetch_partner_custom_fields(self, id=None, id_not=None, created_at_before=None, created_at_after=None, 
                                    created_at_none=None, updated_at_before=None, updated_at_after=None, 
                                    updated_at_none:bool=None, type:list=None, type_not:list=None, query_string=None,
                                    order:list=None, page=None, page_size=None, offset=None):
        
        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/partners/custom-fields'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def create_partner_custom_fields(self, name=None, type=None, default_value=None, dropdown_options:list=None):
        payload = self._payload_fact(locals().items())
        dest = '/partners/custom-fields'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def delete_partner_custom_field(self, custom_field_id):
        dest = f'/partners/custom-fields/{custom_field_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def fetch_users(self, id=None, id_not=None, created_at_before=None, created_at_after=None, 
                    created_at_none=None, updated_at_before=None, updated_at_after=None, 
                    updated_at_none:bool=None, status=None, status_not=None, 
                    team_id=None, office_tags=None, user_tags=None, categories=None,
                    query_string=None, order:list=None, page=None, page_size=None, offset=None, list_ids=False):

        params = self._payload_fact(locals().items(), data_dict=False, exclude=['list_ids'])
        dest = '/partners/users'
        method = 'GET'

        if list_ids:
            dest += 'resolve'

        return Request(self.token, method, dest, params=params)

    def create_user(self, first_name, last_name, email=None, avatar_url=None, role=None, 
                    status=None, phone_number=None, external_id=None, team_id=None, office_tag=None, user_tags=None):
        payload = self._payload_fact(locals().items())
        dest='/partners/users'
        method='POST'

        return Request(self.token, method, dest, payload=payload)

    def update_user(self, user_id, first_name=None, last_name=None, email=None, avatar_url=None, role=None,
                    status=None, phone_number=None, external_id=None, team_id=None, office_tag=None, user_tags=None,
                    partner_membership_plan=None):

        payload = self._payload_fact(locals().items(), exclude=['user_id'])
        dest = f'/partners/users/{user_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def fetch_user_buckets(self, user_id):
        dest = f'/{user_id}/buckets'
        method = 'GET'

        return Request(self.token, method, dest)

    def create_user_bucket(self, user_id, name=None, goal=None, reminder_interval=None, cloned_from_id=None):
        payload = self._payload_fact(locals().items(), exclude=['user_id'])
        dest = f'/{user_id}/buckets'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def create_user_contact(self, user_id, upsert=False, **kwargs): 
        request = self.create_new_contact(self.generate_contact(**kwargs))
        request.url = f'{request._host}/partners/users/{user_id}/contacts'

        if upsert: 
            params = {'upsert':upsert}
            request.params = params

        return request

    def create_user_contact_interaction(self, user_id, contact_id, **kwargs):
        request = self.create_interaction(contact_id, **kwargs)
        request.url = f'{request._host}/partners/users/{user_id}/{contact_id}'
        return request

    def update_user_contact_interaction(self, user_id, contact_id, interaction_id, **kwargs):
        request = self.update_interactions(interaction_id, **kwargs)
        request.url = f'{request._host}/partners/users/{user_id}/contacts/{contact_id}/interactions/{interaction_id}'
        return request

    def create_user_contact_note(self, user_id, contact_id, **kwargs):
        request = self.create_note(contact_id=contact_id, **kwargs)
        request.url = f'{request._host}/partners/users/{user_id}/contacts/{contact_id}/notes'
        return request

    def update_user_contact_note(self, user_id, contact_id, note_id, **kwargs):
        request = self.update_note(note_id=note_id, contact_id=contact_id, **kwargs)
        request.url = f'{request._host}/partners/users/{user_id}/contacts/{contact_id}/notes/{note_id}'
        return request

    def bucket_user_contact(self, user_id, contact_id, bucket_id, update=False, delete=False):
        payload = {'data':{'id':bucket_id}}
        dest = f'/partners/users/{user_id}/contacts/{contact_id}/buckets'
        if update: 
            method = 'PUT'
        elif delete:
            method = 'DELETE'
        else: 
            method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def update_user_contact_bucket(self, **kwargs):
        return bucket_user_contact(**kwargs, update=True)

    def unbucket_user_contact(self, **kwargs):
        return bucket_user_contact(**kwargs, delete=True)

    def move_user(self, user_id, team_id):
        payload = {'data':{'team_id':team_id}}
        dest = f'/partners/users/{user_id}/team'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def bulk_update_users(self, user_ids:list, field:str, changes:dict):
        payload = {'data':{'contact_ids':contact_ids,'field':field, 'changes':[{"value":value, "type":change_type} for value,change_type in changes.items()]}}
        dest = '/partners/users/bulk-change'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def remove_team_from_partner(self, team_id): 
        dest = '/partners/teams{team_id}/membership'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def change_team_owner(self, team_id, user_id): 
        payload = {'data':{'user_id':user_id}}
        dest = f'/teams/{team_id}/owner'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def show_all_pipelines(self, order=None, id=None, id_not=None, created_at_before=None, 
                           created_at_none=None, updated_at_after=None, updated_at_none=None,
                           query_string=None, page=None, page_size=None, offset=None):
        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/pipelines'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def create_new_pipeline(self, name, goal=None, stages:list=None, cloned_from_id=None):
        payload = self._payload_fact(locals().items())
        dest = '/pipelines'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def show_pipeline(self, pipeline_id):
        dest = f'/pipelines/{pipeline-id}'
        method = 'GET'

        return Request(self.token, method, dest)

    def update_pipeline(self, pipeline_id, name=None, goal=None, stages:list=None, cloned_from_id=None): 
        payload = self._payload_fact(locals().items(), exclude=['pipeline_id'])
        dest = f'/pipelines/{pipeline_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def delete_pipeline(self, pipelind_id): 
        dest = f'/pipelines/{pipeline_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def fetch_user_prompts(self, id=None, id_not=None, created_at_before=None, created_at_after=None,
                           created_at_none=None, updated_at_before=None, updated_at_after=None, 
                           updated_at_none=None, due_at_before=None, due_at_after=None, 
                           type=None, order=None, page=None, page_size=None, offset=None):

        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/me/prompts'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def create_prompt(self, force:bool):
        params = {'force':force}
        dest = '/me/prompts/generate'
        method = 'POST'

        return Request(self.token, method, dest, params=params)

    def postpone_prompt(self, prompt_id, postpone_until):
        payload = {'data':{'postpone_until':postpone_until}}
        dest = f'/me/prompts/{prompt_id}/postpone'
        method = 'PUT'
        
        return Request(self.token, method, dest, payload=payload)

    def delete_prompt(self, prompt_id):
        dest = f'/me/prompts/{prompt_id}'
        method='DELETE'

        return Request(self.token, method, dest)

    def list_all_reccuring_events(self, id=None, id_not=None, created_at_before=None, created_at_after=None,
                           created_at_none=None, updated_at_before=None, updated_at_after=None, 
                           updated_at_none=None, event_type=None, event_type_not=None, next_due_date_before=None, 
                           next_due_date_after=None, with_archived=None, order:list=None, page=None, 
                           page_size=None, offset=None): 

        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/recurring_events'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def show_contact_recurring_events(self, contact_id, with_team:bool=None, page=None, page_size=None, offset=None):
        params = self._payload_fact(locals().items(), data_dict=False, exclude=['contact_id'])
        dest = f'/contacts/{contact_id}/recurring_events'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def create_event(self, contact_id, event_type, title, due_date, next_due_date=None):
        event = {'event_type':event_type, 'title':title, 'due_date':due_date,
                  'contact_id':contact_id}
        if next_due_date:
            event['next_due_date'] = next_due_date

        return event

    def create_recurring_event(self, contact_id, events:list):
        payload = {'data':[event for event in events]}
        dest = f'/contacts/{contact_id}/recurring_events'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def update_recurring_event_collection(self, contact_id, events:list):
        payload = {'data':[event for event in events]}
        dest = f'/contacts/{contact_id}/recurring_events'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def show_subscription(self):
        dest = '/team/subscription'
        method = 'GET'

        return Request(self.token, method, dest)

    def show_saved_search(self, saved_search_id):
        dest = f'/saved-searches/{saved_search_id}'
        method = 'GET'

        return Request(self.token, method, dest)

    def show_saved_searches(self, order=None, id=None, id_not=None, created_at_before=None, 
                            created_at_after=None, updated_at_before=None, updated_at_after=None, 
                            updated_at_none=None, page=None, page_size=None, offset=None):

        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/saved-searches'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def create_new_saved_search(self, user_id, name, search_type):
        payload = self._payload_fact(locals().items())
        dest = '/saved-searches'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def update_saved_search(self, saved_search_id, user_id=None, name=None, search_type=None):
        payload = self._payload_fact(locals().items())
        dest = f'/saved-searches/{saved_search_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def delete_saved_search(self, saved_search_id):
        dest = f'/saved-searches/{saved_search_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def fetch_all_tags(self, id=None, id_not=None, created_at_before=None,created_at_after=None, 
                       updated_at_before=None, updated_at_after=None, updated_at_none=None, 
                       query_string=None, page=None, page_size=None, offset=None):

        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/tags'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def create_new_tag(self, name):
        payload = {'data':{'name':name}}
        dest = '/tags'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def update_tag(self, tag_id, name): 
        payload = {'data':{'name':name}}
        dest = f'/tags/{tag_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)

    def delete_tag(self, tag_id): 
        dest = f'/tags/{tag_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def fetch_task(self, task_id):
        dest = f'/tasks/{task_id}'
        method = 'GET'

        return Request(self.token, method, dest)

    def fetch_tasks(self, id=None, id_not=None, created_at_before=None,created_at_after=None, 
                    updated_at_before=None, updated_at_after=None, updated_at_none=None, 
                    due_at_before=None, due_at_after=None, due_at_none=None, completed_at_before=None,
                    completed_at_none=None, completed:bool=None, order=None, page=None, page_size=None,
                    offset=None):

        params = self._payload_fact(locals().items(), data_dict=False)
        dest = '/me/tasks/'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def list_contact_tasks(self, contact_id, id=None, id_not=None, created_at_before=None,created_at_after=None, 
                    updated_at_before=None, updated_at_after=None, updated_at_none=None, 
                    due_at_before=None, due_at_after=None, due_at_none=None, completed_at_before=None,
                    completed_at_none=None, completed:bool=None, order=None, page=None, page_size=None,
                    offset=None):

        params = self._payload_fact(locals().items(), data_dict=False, exclude=['contact_id'])
        dest = f'/contacts/{contact_id}/tasks'
        method = 'GET'

        return Request(self.token, method, dest, params=params)

    def create_task(self, contact_id, due_at, title, assigned_to_id=None, external_description=None):
        payload = self._payload_fact(locals().items())
        dest = '/tasks'
        method = 'POST'

        return Request(self.token, method, dest, payload=payload)

    def update_task(self, task_id, contact_id, due_at, title, assigned_to_id=None, external_description=None):
        payload = self.payload_fact(locals().items(), exclude=['task_id'])
        dest = f'/tasks/{task_id}'
        method = 'PUT'

        return Request(self.token, method, dest, payload=payload)
        
    def delete_task(self, task_id):
        dest = f'/tasks/{task_id}'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def complete_task(self, task_id):
        dest = f'/tasks/{task_id}/complete'
        method = 'POST'

        return Request(self.token, method, dest)

    def restart_task(self, task_id):
        dest = f'/tasks/{task_id}/complete'
        method = 'DELETE'

        return Request(self.token, method, dest)

    def fetch_users_stats(self, id=None, id_not=None, created_at_before=None,created_at_after=None, 
                    updated_at_before=None, updated_at_after=None, updated_at_none=None, user_id=None, 
                    user_id_not=None, account_created_count_min=None, account_created_count_max=None, 
                    attempted_to_connect_account_count_min=None, attempted_to_connect_account_count_max=None,
                    session_created_count_max=None, contact_created_count_min=None, contact_created_count_max=None, 
                    contact_updated_count_min=None, contact_updated_count_max=None, 
                    contact_merged_count_min=None, contact_merged_count_max=None, 
                    contact_bucketed_count_min=None, contact_bucketed_count_max=None, 
                    contact_tagged_count_min=None, contact_tagged_count_max=None,
                    contact_muted_count_min=None, contact_muted_count_max=None, 
                    contact_archived_count_min=None, contact_archived_count_max=None, 
                    contact_unarchived_count_min=None, contact_unarchived_count_max=None, 
                    messaged_created_count_min=None, messaged_created_count_max=None, 
                    bulk_message_created_count_min=None, bulk_messaged_created_count_max=None, 
                    recipients_from_bulk_messages_count_min=None, recipients_from_bulk_messages_count_max=None,
                    messages_sent_in_bulk_min=None, messages_sent_in_bulk_max=None, 
                    messages_sent_via_program_min=None, messages_sent_via_program_max=None,
                    messages_sent_individually_min=None, messages_sent_individually_max=None, 
                    opened_messages_min=None, opened_messages_max=None, 
                    clicked_messages_min=None, clicked_messages_max=None, 
                    replied_messages_min=None, replied_messages_max=None, 
                    bucket_created_count_min=None, bucket_created_count_max=None, 
                    program_completed_count_min=None, program_completed_count_max=None, 
                    calendar_event_contact_history_created_count_min=None, 
                    calendar_event_contact_history_created_count_max=None, 
                    email_contact_history_created_count_min=None, 
                    email_contact_history_created_count_max=None, 
                    facebook_contact_history_created_count_min=None, 
                    facebook_contact_history_created_count_max=None, 
                    generic_contact_history_created_count_min=None, 
                    generic_contact_history_created_count_max=None, 
                    in_person_meeting_contact_history_created_count_min=None, 
                    in_person_meeting_contact_history_created_count_max=None, 
                    linked_in_contact_history_created_count_min=None, 
                    linked_in_contact_history_created_count_max=None, 
                    madmimi_contact_history_created_count_min=None, 
                    madmimi_contact_history_created_count_max=None, 
                    mail_chimp_contact_history_created_count_min=None, 
                    mail_chimp_contact_history_created_count_max=None, 
                    manual_contact_history_created_count_min=None, 
                    manual_contact_history_created_count_max=None, 
                    phone_call_contact_history_created_count_min=None, 
                    phone_call_contact_history_created_count_max=None, 
                    physical_message_contact_history_created_count_min=None, 
                    physical_message_contact_history_created_count_max=None, 
                    sms_contact_history_created_count_min=None, 
                    sms_contact_history_created_count_max=None, 
                    twitter_contact_history_created_count_max=None, 
                    zapier_contact_history_created_count_min=None, 
                    zapier_contact_history_created_count_max=None, 
                    task_created_count_min=None, 
                    task_created_count_max=None, 
                    task_snoozed_count_min=None, 
                    task_snoozed_count_max=None, 
                    task_ignored_count_min=None, 
                    task_ignored_count_max=None, 
                    followup_task_completed_count_min=None, 
                    followup_task_completed_count_max=None, 
                    content_sharing_task_completed_count_min=None, 
                    content_sharing_task_completed_count_max=None, 
                    introduction_task_completed_count_min=None, 
                    introduction_task_completed_count_max=None, 
                    approval_task_completed_count_min=None, 
                    approval_task_completed_count_max=None, 
                    unresponded_message_task_completed_count_min=None,
                    unresponded_message_task_completed_count_max=None, 
                    recurring_event_task_completed_count_min=None, 
                    recurring_event_task_completed_count_max=None, 
                    merge_suggestion_created_count_min=None, 
                    merge_suggestion_created_count_max=None, 
                    merge_suggestion_reviewed_count_min=None, 
                    merge_suggestion_reviewed_count_max=None, 
                    email_template_created_count_min=None, 
                    email_template_created_count_max=None, 
                    email_template_populated_count_min=None, 
                    email_templated_populated_count_max=None, 
                    csv_import_created_count_max=None, 
                    csv_import_created_count_min=None, 
                    csv_import_processed_count_min=None, 
                    csv_import_processed_count_max=None, 
                    csv_export_processed_count_min=None, 
                    csv_export_processed_count_max=None, 
                    deal_created_count_min=None, 
                    deal_created_count_max=None, 
                    deal_updated_count_min=None, 
                    deal_updated_count_max=None, 
                    deal_destroyed_count_min=None,
                    deal_destroyed_count_max=None, 
                    deal_won_count_min=None, 
                    deal_won_count_max=None, 
                    deal_lost_count_min=None, 
                    deal_lost_count_max=None, 
                    deal_moved_count_min=None, 
                    deal_moved_count_max=None, 
                    tag_created_count_min=None, 
                    tag_created_count_max=None, 
                    tag_created_updated_count_min=None, 
                    tag_created_updated_count_max=None, 
                    tag_updated_count_min=None, 
                    tag_updated_count_max=None, 
                    tag_destroyed_count_min=None, 
                    tag_destroyed_count_max=None, 
                    library_content_created_count_min=None, 
                    library_content_created_count_max=None, 
                    library_content_updated_count_min=None, 
                    library_content_updated_count_max=None, 
                    library_content_destroyed_count_min=None, 
                    library_content_destroyed_count_max=None, 
                    note_created_count_min=None, 
                    note_created_count_max=None, 
                    document_created_count_min=None, 
                    document_created_count_max=None, 
                    document_updated_count_min=None, 
                    document_updated_count_max=None, 
                    document_destroyed_count_min=None, 
                    document_destroyed_count_max=None, 
                    lead_created_count_min=None, 
                    lead_created_count_max=None, 
                    lead_updated_count_min=None, 
                    lead_updated_count_max=None, 
                    lead_destroyed_count_min=None, 
                    lead_destroyed_count_max=None, 
                    contact_link_created_count_min=None, 
                    contact_link_created_count_max=None, 
                    contact_link_updated_count_min=None, 
                    contact_link_updated_count_max=None, 
                    contact_link_destroyed_count_min=None, 
                    contact_link_destroyed_count_max=None, 
                    total_seconds_in_app_min=None, 
                    total_seconds_in_app_max=None, 
                    total_seconds_on_web_min=None, 
                    total_seconds_on_web_max=None, 
                    total_seconds_on_mobile_min=None, 
                    total_seconds_on_mobile_max=None, 
                    total_sessions_min=None, 
                    total_sessions_max=None, 
                    total_web_sessions_min=None, 
                    total_web_sessions_max=None, 
                    total_mobile_sessions_min=None, 
                    total_mobile_sessions_max=None, 
                    total_task_completed_count_min=None, 
                    total_task_completed_count_max=None, 
                    appointment_count_min=None, 
                    appointment_count_max=None, 
                    query_string=None, order=None, 
                    page=None, page_size=None,
                    offset=None
                    ):
        params = self._payload_fact(locals().items(), data_dict=None)
        dest = '/partners/users/stats'
        method = 'GET'

        return Request(self.token, method, dest, params=params)
