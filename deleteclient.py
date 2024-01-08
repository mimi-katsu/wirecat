import requests
import json
import os
import sys

username = 'mimi'
key = '2697348d02d9471727f854a31a6a648f790bcdc8b2725362cb536b7af8c643fe'

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

