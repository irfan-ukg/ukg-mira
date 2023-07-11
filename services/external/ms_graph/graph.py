from configparser import SectionProxy
from requests import post, get
from datetime import datetime

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

    async def setup_me_data(self, me_user, timeZone):
        self.me_user.append(me_user)
        name_list = await self.get_user_details(self.me_user, 'userPrincipalName', timeZone=timeZone)
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

    async def get_user_details(self, users, key, timeZone):
        userList = []
        access_token = await self.get_access_token()
        for i in users:
            nameFilter = i
            uri = self.user_uri+f"?$filter=startswith(displayName,'{nameFilter}')"
            headers = {
                'Accept': 'application/json',
                'Authorization': access_token,
                'Prefer':f'outlook.timezone="{timeZone}"'
            }
            response = get(url=uri, headers=headers)
            response.raise_for_status()
            response_body = response.json()
            # print(response_body)
            # print(response_body['value'][0][key])
            userList.append(response_body['value'][0][key])
        return userList

    async def check_availability(self, userEmails, startTime, endTime, timeZone, duration):
        access_token = await self.get_access_token()
        # try:
        #     duration = int((datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S.%f")).total_seconds()/60)
        # except:
        #     duration = int((datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S")).total_seconds()/60)

        # print(duration)
        uri = self.user_uri+f"/{self.me_PrincipalName}/calendar/getSchedule"
        body = {
            "schedules": userEmails,
            "startTime": {
                "dateTime": startTime,
                "timeZone": timeZone
            },
            "endTime": {
                "dateTime": endTime,
                "timeZone": timeZone
            },
            "availabilityViewInterval": duration
        }
        headers = {
            'Accept': 'application/json',
            'Authorization': access_token,
            'Prefer':f'outlook.timezone="{timeZone}"'
        }
        # print(body)
        # print(headers)
        response = post(url=uri, headers=headers, json=body)
        response.raise_for_status()
        response_body = response.json()
        userSchedules = []
        for i in response_body["value"]:
            name = " ".join(i['scheduleId'].split("@")[0].split("."))
            busy = []
            if i['scheduleItems'] == []:
                pass
            else:
                for j in i['scheduleItems']:
                    busy.append([f"{j['start']['dateTime']} to {j['end']['dateTime']}"])
            userSchedules.append({name: busy})
        print(userSchedules)

        return


    async def get_schedule(self, timeZone, subject = '', startTime = None, endtime = None):
        # ?$filter=start/dateTime eq '2022-07-14T12:30:00Z' and subject eq 'Testing'
        access_token = await self.get_access_token()
        eventList = []
        uri = self.user_uri+f"/{self.me_PrincipalName}/calendarview"

        params = {
            'startdatetime' : startTime,
            'enddatetime' : endtime
        }
        print(params)
        headers = {
            'Accept': 'application/json',
            'Authorization': access_token,
            'Prefer':f'outlook.timezone="{timeZone}"'
        }
        response = get(url=uri, headers=headers, params=params)
        print(response.url)
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


    async def schedule_meeting(self, users, subject, starTime, timeZone, endTime,occuranceType=None,interval=None, occuranceStartDate=None, occuranceEndDate=None,daysOfWeek=None, recurringEvent = False):
        mailList = await self.get_user_details(users, 'mail', timeZone=timeZone)
        # await self.check_availability(mailList, starTime, endTime, timeZone)
        scheduleMettingUri = self.user_uri + f"/{self.me_PrincipalName}/calendar/events"
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
            "isOnlineMeeting":"true",
        }
        # print(body)
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
        # print(body)
        headers = {
            'Accept': 'application/json',
            'Authorization': access_token,
            'Prefer':f'outlook.timezone="{timeZone}"'
        }

        if recurringEvent:
            if occuranceType == 'daily':
                body["recurrence"]= {
                    "pattern": {
                        "type": occuranceType,
                        "interval": interval,
                        "daysOfWeek": daysOfWeek
                    },
                    "range": {
                        "type": "endDate",
                        "startDate": occuranceStartDate,
                        "endDate": occuranceEndDate
                    }
                }
            elif occuranceType == 'weekly':
                body["recurrence"]= {
                    "pattern": {
                        "type": occuranceType,
                        "interval": interval,
                        "daysOfWeek": daysOfWeek
                    },
                    "range": {
                        "type": "endDate",
                        "startDate": occuranceStartDate,
                        "endDate": occuranceEndDate
                    }
                }

        response = post(url=scheduleMettingUri, headers=headers, json=body)
        response.raise_for_status()
        response_body = response.json()
        # print(response_body)
        return
    #
    async def get_inbox(self, timeZone):
        access_token = await self.get_access_token()
        messageList = []
        uri = self.user_uri+f"/{self.me_PrincipalName}/mailfolders/inbox/messages"
        headers = {
            'Accept': 'application/json',
            'Authorization': access_token,
            'Prefer':f'outlook.timezone="{timeZone}"'
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





