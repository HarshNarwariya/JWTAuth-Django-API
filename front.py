import requests

class API:
    def __init__(self, host='http://127.0.0.1:8000/api/'):
        self.host = host
        self.endpoints = {
            'login': 'login/',
            'register': 'register/',
            'profile': 'profile/',
            'changepassword': 'changepassword/',
            'sendpasswordresetemail': 'sendpasswordresetemail/',
            'resetpassword': 'resetpassword/',
        }
    
    def url(self, endpoint):
        return self.host + self.endpoints.get(endpoint, '')
    
    def print_details(self, response):
        output = f'''
        Url:         {response.url}
        Status Code: {response.status_code}
        '''            
        print(output)
    
    def login(self, email, password, endpoint='login'):
        payload = {
            'email': email,
            'password': password,
        }
        url = self.url(endpoint)
        response = requests.post(url, data=payload)
        self.print_details(response)
        return response.json()

    def register(self, email, name, password, password2, endpoint='register'):
        payload = {
            'email': email,
            'name': name,
            'password': password,
            'password2': password2,
        }
        url = self.url(endpoint)
        response = requests.post(url, data=payload)
        self.print_details(response)
        return response.json()

    def profile(self, token, endpoint='profile'):
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        url = self.url(endpoint)
        response = requests.get(url, headers=headers)
        self.print_details(response)
        return response.json()

    def changepassword(self, password, password2, token, endpoint='changepassword'):
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        data = {
            'password': password,
            'password2': password2,
        }
        url = self.url(endpoint)
        response = requests.post(url, headers=headers, data=data)
        self.print_details(response)
        return response.json()

    def sendpasswordresetemail(self, email, endpoint='sendpasswordresetemail'):
        data = {
            'email': email,
        }
        url = self.url(endpoint)
        response = requests.post(url, data=data)
        self.print_details(response)
        return response.json()

    def resetpassword(self, password, password2, uid, token, endpoint='resetpassword'):
        data = {
            'password': password,
            'password2': password2,
        }
        url = self.url(endpoint) + uid + '/' + token + '/'
        print(url)
        response = requests.post(url, data=data)
        self.print_details(response)
        return response.json()
    
    def getusers(self, token, page=1, endpoint='getusers'):
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        url = self.url(endpoint) + f'?page={page}'
        response = requests.get(url, headers=headers)
        self.print_details(response)
        return response.json()


api = API()

EMAIL = 'harshverma790932611@gmail.com'
PASSWORD = 'testing456'

# # Register User
# data = api.register(
#     email=EMAIL,
#     name='example',
#     password=PASSWORD,
#     password2=PASSWORD,
# )
# print(data)

# # Login and get access token
# data = api.login(
#     email=EMAIL,
#     password=PASSWORD,
# )
# # print(data)
# token = data['access']


# # View Profile (TO GET THIS WORK RUN 'Login and get access token')
# data = api.profile(token)
# print(data)

# # Change Password
# PASSWORD = 'testing123'
# data = api.changepassword(
#     password=PASSWORD,
#     password2=PASSWORD,
#     token=token,
# )
# print(data)

# # Send email to reset password
# data = api.sendpasswordresetemail(
#     email=EMAIL,
# )
# print(data)

# # reset password
# PASSWORD = 'testing456'
# data = api.resetpassword(
#     password=PASSWORD,
#     password2=PASSWORD,
#     uid="MQ",
#     token="b3ookp-dc672fa7edf904c82d7a78ca99b35767",
# )
# print(data)

# # Get Users (admin only)
    # data = api.getusers(token, page=2)
    # print(data)
