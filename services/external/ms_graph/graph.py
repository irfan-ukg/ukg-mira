from configparser import SectionProxy
from requests import post, get


class Graph:
    settings: SectionProxy
    LoginUri = None
    clientId = None
    tenantId = None
    user_uri = None
    me_user = []
    me_PrincipalName = None
    graph_scopes = []

    def __init__(self, config: SectionProxy, me_user):
        self.settings = config
        self.client_id = self.settings['clientId']
        self.tenant_id = self.settings['tenantId']
        self.graph_scopes = self.settings['graphUserScopes'].split(' ')
        self.user_uri = 'https://graph.microsoft.com/v1.0/users'
        self.LoginUri = f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token'
        return

    async def setup_me_data(self, me_user):
        self.me_user.append(me_user)
        name_list = await self.get_user_details(self.me_user, 'userPrincipalName')
        self.me_PrincipalName = name_list[0]
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
            # print(response_body)
            # print(response_body['value'][0][key])
            userList.append(response_body['value'][0][key])
        return userList

    async def get_schedule(self):
        access_token = await self.get_access_token()
        eventList = []
        uri = self.user_uri+f"/{self.me_PrincipalName}/calendar/events"
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


    async def schedule_meeting(self, users, subject, starTime, timeZone, endTime, duration=None):
        mailList = await self.get_user_details(users, 'mail')
        scheduleMettingUri = self.user_uri + f"/{self.me_PrincipalName}/events"
        access_token = await self.get_access_token()
        body = {
            "subject":subject,
            "start":{
                "dateTime":starTime,
                "timeZone":timeZone
            },
            "end":{
                "dateTime":endTime,
                "timeZone":timeZone
            },
            "Attendees": [],
            "isOnlineMeeting":"true"
        }

        n = len(users)
        for i in range(n):
            attende = {
                "EmailAddress": {
                    "Address": mailList[i],
                    "Name": users[i]
                },
                "Type": "Required"
            }
            body['Attendees'].append(attende)
        print(body)
        headers = {
            'Accept': 'application/json',
            'Authorization': access_token
        }

        response = post(url=scheduleMettingUri, headers=headers, json=body)
        response.raise_for_status()
        # response_body = response.json()
        # print(response_body)
        return
    #
    async def get_inbox(self):
        access_token = await self.get_access_token()
        messageList = []
        uri = self.user_uri+f"/{self.me_PrincipalName}/mailfolders/inbox/messages"
        headers = {
            'Accept': 'application/json',
            'Authorization': access_token
        }
        response = get(url=uri, headers=headers)
        response.raise_for_status()
        response_body = response.json()

        for mail in response_body['value']:
            message = {
                'Subjet': mail['subject'],
                'Received On':mail['receivedDateTime'],
                'From':mail['from']['emailAddress']['name']
            }
            messageList.append(message)
        return messageList





