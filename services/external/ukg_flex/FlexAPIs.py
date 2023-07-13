import asyncio
import requests

username = "HarshPundir"
password = "Pr0mensi0ns@UKG"
client_id = "mQeGf3jyuXvySOEOvuTs20HKNZcjIjlo"
client_secret = "vF5mbhJFz4uRBt7G"
hostname = "u-u-harshulk8jul23-u-u-harshulk8jul23.dev.mykronos.com"
app_key = "pncv2EoXpmKnA3jLGA7IgA5OfABJZtAZ"

class Flex:
    app_key = None
    username = None
    password = None
    client_id = None
    client_secret = None
    hostname = None
    access_token = None
    refresh_token = None

    def __init__(self, hostname, username, password, client_id, client_secret, app_key):
        self.app_key = app_key
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.hostname = hostname
        response_json = self.authenticate()
        self.access_token = response_json['access_token']
        self.refresh_token = response_json['refresh_token']
        return

    def authenticate(self):
        auth_uri = f"https://{self.hostname}/api/authentication/access_token"
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'appkey': self.app_key
        }

        data = {
            "username" : self.username,
            "password" : self.password,
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "grant_type" : "password",
            "auth_chain" : "OAuthLdapService"
        }

        response = requests.post(auth_uri, headers=header, data=data)
        return response.json()

    async def get_my_shifts(self, startdate, enddate):
        '''This api can only be used by employees to see their own shifts'''
        url = f"https://{hostname}/api/v1/scheduling/employee_schedule"
        json = await self.get_my_info()
        params = {
            "person_number": json['personNumber'],
            "start_date": startdate,
            "end_date": enddate,
            "symbolic_period": "current_schedule"
        }
        headers = {"accept": "application/json",
                   'appkey': self.app_key,
                   "Authorization": self.access_token
                   }

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    async def get_employee_shifts(self, user_name, startdate, enddate):
        '''This api can only be used by managers or people with access to see other people shifts'''
        url = f"https://{hostname}/api/v1/scheduling/employee_schedule"
        response_json = {}
        for i in user_name:
            json_list = await self.get_employees_info_by_username([i])
            response_json[i] = []
            for json in json_list:
                params = {
                    "person_number": json['employeeExtension']['personNumber'],
                    "start_date": startdate,
                    "end_date": enddate,
                    "symbolic_period": "current_schedule"
                }
                headers = {"accept": "application/json",
                           'appkey': self.app_key,
                           "Authorization": self.access_token
                }
                response = requests.get(url, headers=headers, params=params)
                response_json[i].append(response.json())
        return response_json

    async def get_my_info(self):
        '''This api can only be used by employees to see their own information'''
        emp_uri = f"https://{self.hostname}/api/v1/commons/persons/current_user_info"
        headers = {
            "accept": "application/json",
            'appkey': self.app_key,
            "Authorization": self.access_token
        }
        response = requests.get(url=emp_uri, headers=headers)
        
        return response.json()

    async def get_employees_info_by_username(self, username_list):
        '''This api can only be used by managers or people with access to see other people information'''
        emp_uri = f"https://{self.hostname}/api/v1/commons/persons/extensions/multi_read"
        headers = {
            "accept": "application/json",
            'appkey': self.app_key,
            "Authorization": self.access_token
        }
        body = {
            "where": {
                "employees": {
                    "key": "username",
                    "values": username_list
                },
                "extensionType": "employee"
            }
        }
        response = requests.post(url=emp_uri, headers=headers, json = body)
        
        return response.json()

    async def get_employees_info_by_id(self, emp_id):
        '''This api can only be used by managers or people with access to see other people information'''
        emp_uri = f"https://{self.hostname}/api/v1/commons/persons/extensions/multi_read"
        headers = {
            "accept": "application/json",
            'appkey': self.app_key,
            "Authorization": self.access_token
        }
        body = {
            "where": {
                "employees": {
                    "key": "personid",
                    "values": emp_id
                },
                "extensionType": "employee"
            }
        }
        response = requests.post(url=emp_uri, headers=headers, json = body)

        return response.json()

    async def get_open_shifts(self, startdate, enddate):
        url = f"https://{self.hostname}/api/v1/scheduling/employee_self_schedule_requests/open_shifts/multi_read"

        payload = {
            "where":{
                "endDate": enddate,
                "startDate": startdate,
                "requestSubtypeRef": {
                    "id": 255
                }
            }
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            'appkey': self.app_key,
            "Authorization": self.access_token
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    async def request_time_off_full_day_me(self, startdate, enddate):
        url = f"https://{hostname}/api/v1/scheduling/employee_timeoff"
        json = await self.get_my_info()
        payload = {
            # "employee": { "id": json['employeeId'] },
            "periods": [
                {
                    "payCode": { "id": 413 },
                    "symbolicAmount": { "id": -1 },
                    "endDate": enddate,
                    "startDate": startdate
                }
            ],
            "requestSubType": { "id": 153 }
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            'appkey': self.app_key,
            "Authorization": self.access_token
        }
        response = requests.post(url, json=payload, headers=headers)
        
        return response.json()

    async def get_time_off_requests_me(self, startdate, enddate, status = None):
        '''
        This method will omit the cancelled timeoff requests and will show only SUBMITTED or CANCELSUBMITTED requests
        :param startdate: start date filter in format YYYY-MM-DD
        :param enddate: end date filter in format YYYY-MM-DD
        :param status: current status, accespts the following values: [CANCELSUBMITTED, CANCELLED, SUBMITTED, APPROVED]
        :return:
        '''
        url = f"https://{hostname}/api/v1/scheduling/employee_timeoff/multi_read"
        json = await self.get_my_info()
        payload = { "where": { "employee": {
            "employeeRef": { "id": json['employeeId'] },
            "endDate": enddate,
            "startDate": startdate
        } } }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            'appkey': self.app_key,
            "Authorization": self.access_token
        }
        response = requests.post(url, json=payload, headers=headers)
        
        response = response.json()
        response_list = []
        if status == None:
            response_list = response
        else:
            for res in response:
                if res['currentStatus']["symbolicId"] == status:
                    response_list.append(res)
        return response_list

    async def get_time_off_requests_employee(self,employee_list, startdate, enddate, status = "SUBMITTED"):
        '''
        :param startdate: start date filter in format YYYY-MM-DD
        :param enddate: end date filter in format YYYY-MM-DD
        :param status: current status, accespts the following values: [COMPLETE, INCOMPLETE]
        :return:
        '''
        url = f"https://{hostname}/api/v1/scheduling/timeoff/multi_read"
        response_list = {}
        for i in employee_list:
            response_list[i] = []
            json_list = await self.get_employees_info_by_username([i])
            empId_list = [x['employeeExtension']['personId'] for x in json_list]
            payload = {
                    "where": {
                        "states": {
                            "completionState": "INCOMPLETE",
                            "employeeRefs": {
                                "ids": empId_list
                            },
                            "endDate": "2023-07-15",
                            "startDate": "2023-07-15"
                        }
                    }
                }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                'appkey': self.app_key,
                "Authorization": self.access_token
            }
            response = requests.post(url, json=payload, headers=headers)
            response = response.json()
            for res in response:
                if res['currentStatus']["symbolicId"] == status:
                    response_list[i].append(res)
        return response_list

    async def cancel_time_off_request(self, timeoff_request_id):
        url = f"https://{hostname}/api/v1/scheduling/employee_timeoff/apply_update"

        payload = { "changeState": {
            "do": { "toStatus": { "id": 8 } },
            "where": { "timeOffRequestId": timeoff_request_id }
        } }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            'appkey': self.app_key,
            "Authorization": self.access_token
        }

        response = requests.post(url, json=payload, headers=headers)
        # 
        return response.json()




async def main():
    flexObj: Flex= Flex(hostname, username, password, client_id, client_secret, app_key)
    # print(await flexObj.get_my_info())
    # print(await flexObj.get_my_shifts("2023-07-13", "2023-07-14"))
    # print(await flexObj.get_employees_info_by_username(['harshpundir']))
    # print(await flexObj.get_employee_shifts(['harshpundir'], "2023-07-13", "2023-07-13"))
    # print(await flexObj.get_open_shifts("2023-07-15", "2023-07-15"))
    # print(await flexObj.request_time_off_full_day_me("2023-07-25", "2023-07-25"))
    # print(await flexObj.get_time_off_requests_me("2023-07-25", "2023-07-25", "SUBMITTED"))
    # print(await flexObj.cancel_time_off_request(1353))
    print(await flexObj.get_time_off_requests_employee(['harshpundir'],"2023-07-15", "2023-07-15"))
    # print(await flexObj.get_employees_info_by_id([1454]))

asyncio.run(main())