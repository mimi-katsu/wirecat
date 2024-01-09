import requests
import json
import os
import sys

username = 'mimi'
key = '6dbf9802e05ee3446a5f15ef949df8bc35fcb4726681b87b9ddce55c0b931dfe'

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

