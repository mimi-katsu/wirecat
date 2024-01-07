import requests
import json
import os
import sys

username = 'mimi'
key = '27845d491a579791eff9cd372c41ca501ae12f36ee983587e28e19ceba26820f'

data = {
    "username": username,
    "key": key
}

p = sys.argv[1]

print(f'Sending request to delete:\n\n "{p}"')
response = requests.post(f'http://127.0.0.1:5001/api/v1/posts/delete/{p}', data=data)

print(response.text)

# if data['success'] == True:
#     print(f'Post "{p}" was deleted successfully')

