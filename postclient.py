import requests
import json
import getpass
import sys
from bs4 import BeautifulSoup, Comment
username = sys.argv[1]
path = sys.argv[2]

# password = getpass.getpass("Enter Password:\n")

username = 'maia1'
password = '123123'

data = {
    "request_type": "json",
    "username": username,
    "password": password
}
print(f'Authenticating as {username}')

response = requests.post('http://127.0.0.1:5001/auth/login', data=data)
if response.status_code == 200:
    try:
        token = json.loads(response.text)['token']
    except JSONDecodeError:
        print('Unexpected response from server')
        print('Exiting...')
        exit()

    print('Token recieved.')
else:
    print(f'Bad status ({response.status_code})')

cookies = {
    'access_token_cookie': token
}

print('Verifying Token...')
auth_response = requests.get('http://127.0.0.1:5001/auth/verify', cookies=cookies)

json_data = json.loads(auth_response.text)
verified = json_data['logged_in']
if not verified:
    print('Could not verify token.')

print(f'Successfully logged in as {json_data["user"]}')

print('Building request from file')

with open(f'{path}') as f:
    post_content = f.read()
    soup = BeautifulSoup(post_content, 'html.parser')
    for element in soup.descendants:
        if isinstance(element, Comment):
            element.extract()
    post_json = {
        'title': soup.title.text,
        'html_content': soup.content.text,
        'summary': soup.summary.text,
        'tags': soup.tags.text
        }

    pics = soup.find_all('pic')
    pics.append(soup.thumbnail)
    i=0
    post_files = {}
    for p in pics:
        try:
            i+=1
            pic = open(f'{p.text}', 'rb')
            post_files[f'file{i}'] = pic

        except FileNotFoundError:
            print('Missing an image file, aborting.')
            exit()
    response = requests.post('http://127.0.0.1:5001/api/v1/posts/add', data=post_json, files=post_files)
    print(response.text)
