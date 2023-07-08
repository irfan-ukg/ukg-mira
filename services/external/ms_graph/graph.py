from configparser import SectionProxy
from requests import post, get


class Graph:
    settings: SectionProxy
    LoginUri = None
    clientId = None
    tenantId = None
    graph_scopes = []

    def __init__(self, config: SectionProxy):
        self.settings = config
        self.client_id = self.settings['clientId']
        self.tenant_id = self.settings['tenantId']
        self.graph_scopes = self.settings['graphUserScopes'].split(' ')
        self.user_uri = 'https://graph.microsoft.com/v1.0/users'
        self.LoginUri = f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token'

        return

    async def get_access_token(self):
        body = {
            'client_id': self.settings['clientId'],
            'scope': 'https://graph.microsoft.com/.default',
            'client_secret': self.settings['clientSecret'],
            'grant_type': 'client_credentials',
            'tenant': self.settings['tenantId']
        }
        headers = {
            'Host': 'login.microsoftonline.com',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = post(url=self.LoginUri, headers=headers, data=body)
        response.raise_for_status()
        response_body = response.json()
        return 'Bearer ' + response_body['access_token']

    async def get_user_details(self, users, key):
        userList = []
        access_token = await self.get_access_token()
        for i in users:
            nameFilter = i
            uri = self.user_uri+f"?$filter=startswith(displayName,'{nameFilter}')"
            headers = {
                'Accept': 'application/json',
                'Authorization': access_token
            }
            response = get(url=uri, headers=headers)
            response.raise_for_status()
            response_body = response.json()
            print(response_body)
            # print(response_body['value'][0][key])
            userList.append(response_body['value'][0][key])
        return userList

    async def get_schedule(self, user):
        userList = await self.get_user_details(user, 'userPrincipalName')
        access_token = await self.get_access_token()
        eventList = []
        for i in userList:
            uri = self.user_uri+f"/{i}/calendar/events"
            headers = {
                'Accept': 'application/json',
                'Authorization': access_token
            }
            response = get(url=uri, headers=headers)
            response.raise_for_status()
            response_body = response.json()

            for event in response_body['value']:
                eventDetails = {
                    'Name': event['subject'],
                    'Location':event['location']['displayName'],
                    'Attendees':[x['emailAddress']['name'] for x in event['attendees']],
                    'Organizer': event['organizer']['emailAddress']['name'],
                    'Start Time': event['start']['dateTime'],
                    'End Time': event['end']['dateTime'],
                    'Time Zone': event['end']['timeZone'],
                }
                eventList.append(eventDetails)
        return eventList


    async def schedule_meeting(self, users, starTime, endTime, duration):
        userList = await self.get_user_details(users, 'mail')
        return
    #
    # async def get_inbox(self):
    #     query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
    #         # Only request specific properties
    #         select=['from', 'isRead', 'receivedDateTime', 'subject'],
    #         # Get at most 25 results
    #         top=25,
    #         # Sort by received time, newest first
    #         orderby=['receivedDateTime DESC']
    #         )
    #     request_config = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
    #         query_parameters= query_params
    #     )
    #
    #     messages = await self.user_client.me.mail_folders.by_mail_folder_id('inbox').messages.get(
    #         request_configuration=request_config)
    #     return messages





