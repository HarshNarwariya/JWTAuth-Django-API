##### For application overview go to the link given below
<a href="https://github.com/HarshNarwariya/JWTAuth-Django-API/blob/main/App%20Explanation.md" target="_blank">link</a>

##### To work with API use
+ https://harsh2.pythonanywhere.com/api/login/
+ https://harsh2.pythonanywhere.com/api/register/
+ https://harsh2.pythonanywhere.com/api/profile/
+ https://harsh2.pythonanywhere.com/api/changepassword/
+ https://harsh2.pythonanywhere.com/api/sendpasswordresetemail/
+ https://harsh2.pythonanywhere.com/api/resetpassword/
+ https://harsh2.pythonanywhere.com/api/getusers/

or simple put host = "https://harsh2.pythonanywhere.com/api/" in front.py API class.

# Authentication API

Endpoints of the user authentication API
```python
endpoints = {
    'login': 'login/',
    'register': 'register/',
    'profile': 'profile/',
    'changepassword': 'changepassword/',
    'sendpasswordresetemail': 'sendpasswordresetemail/',
    'resetpassword': 'resetpassword/',
    'getusers': 'getusers/'
}
```

### Register

To register user go to register endpoint and pass following params:
+ email
+ name
+ password
+ password2

**code**
```python
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
```

On successfull registration, register endpoint returns access token and refresh token for further use.
```python
STATUS_CODE = 201
{
'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0OTY5NzUxMCwiaWF0IjoxNjQ5NjExMTEwLCJqdGkiOiJmYTJmNGRlMWI5Yjg0ZDJiOTRiYzA2NzIxYWIwYzYyYyIsInVzZXJfaWQiOjEwfQ.HAHlGQZoVeqz1eip-Jl5Jz3Zvja0vMQnqFBSVCiy14Y', 
'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjExNDEwLCJpYXQiOjE2NDk2MTExMTAsImp0aSI6ImVkYjdmZjk4ZWZjMTQwODhhZjZjOTJmYjJiY2FlNDk4IiwidXNlcl9pZCI6MTB9.3RoQtV_t694Jc1-RjAHwR0R3L2OujWLD4SJbQQq1xfE'
}
```


### Login

To login user go to login endpoint and pass following params:
+ email
+ password

**code**
```python
def login(self, email, password, endpoint='login'):
    payload = {
        'email': email,
        'password': password,
    }
    url = self.url(endpoint)
    response = requests.post(url, data=payload)
    self.print_details(response)
    return response.json()
```
On successfull login, login endpoint returns access and refresh token for further use.
```python
STATUS_CODE = 200
{
'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0OTY5NzUxMCwiaWF0IjoxNjQ5NjExMTEwLCJqdGkiOiJmYTJmNGRlMWI5Yjg0ZDJiOTRiYzA2NzIxYWIwYzYyYyIsInVzZXJfaWQiOjEwfQ.HAHlGQZoVeqz1eip-Jl5Jz3Zvja0vMQnqFBSVCiy14Y', 
'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjExNDEwLCJpYXQiOjE2NDk2MTExMTAsImp0aSI6ImVkYjdmZjk4ZWZjMTQwODhhZjZjOTJmYjJiY2FlNDk4IiwidXNlcl9pZCI6MTB9.3RoQtV_t694Jc1-RjAHwR0R3L2OujWLD4SJbQQq1xfE'
}
```

### Profile

To view profile, first generate access token via login or register endpoint (as it requires authentication), and pass it to profile endpoint which uses Bearer Authentication.

```python
def profile(self, token, endpoint='profile'):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    url = self.url(endpoint)
    response = requests.get(url, headers=headers)
    self.print_details(response)
    return response.json()
```

On success
```python
STATUS_CODE = 200
{
    'id': 10, 
    'email': 'example@gmail.com', 
    'name': 'example', 
    'tc': False,
}
```

### Get all profiles (Only Admin have access)
```python
def getusers(self, token, page=1, endpoint='getusers'):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    url = self.url(endpoint) + f'?page={page}'
    response = requests.get(url, headers=headers)
    self.print_details(response)
    return response.json()
```

### Change password

To change password access token and new password confirmation is required at changepassword endpoint

```python
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
```
On success
```python
STATUS_CODE = 200
{
    'success': 'password changed successfully'
}
```

### Send password reset email

To reset password via mail, pass email to sendpasswordresetemail endpoint
```python
def sendpasswordresetemail(self, email, endpoint='sendpasswordresetemail'):
    data = {
        'email': email,
    }
    url = self.url(endpoint)
    response = requests.post(url, data=data)
    self.print_details(response)
    return response.json()
```
on success 
```python
STATUS_CODE = 200
{
    'success': 'password reset link sent successfully, please check your email.'
}
```

This mail gives uid and token for further use in reseting password.

### Reset password
To reset password first confirm new password and pass uid and token.


```python
# Example
uid = 'MTA'
token = 'b3ot40-3e871b775cebc05c07b24e447a83f7d6'
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

```
On success password will be changed
```python
STATUS_CODE = 200
```

# For Api reference consider the following python code

```python
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

EMAIL = 'example@gmail.com'
PASSWORD = 'testing321'

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
```


### To run the application at local server
#### First Migarte
```python
python manage.py makemigrations
python manage.py migrate
```

#### Finally run server
```python
python manage.py runserver
```

### Requirement
```python
pip install Django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
```
