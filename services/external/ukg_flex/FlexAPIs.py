import asyncio
import requests

username = "HarshulGupta"
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
        url = f"https://{hostname}/api/v1/scheduling/employee_schedule"
        json = await self.get_my_info()
        params = {
            "employee_id": json['employeeId'],
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

    async def get_my_info(self):
        emp_uri = f"https://{self.hostname}/api/v1/commons/persons/current_user_info"
        headers = {
            "accept": "application/json",
            'appkey': self.app_key,
            "Authorization": self.access_token
        }
        response = requests.get(url=emp_uri, headers=headers)
        return response.json()


async def main():
    flexObj: Flex= Flex(hostname, username, password, client_id, client_secret, app_key)
    print(await flexObj.get_my_info())
    print(await flexObj.get_my_shifts("2023-07-13", "2023-07-13"))

asyncio.run(main())