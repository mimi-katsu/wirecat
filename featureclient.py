import requests
import json
import os
import sys

username = 'mimi'

with open('mimi.key', 'r') as key:
    data = {
        "username": username,
        "key": key
    }
    
    p = sys.argv[1]
    
    print(f'Sending request to feature:\n\n "{p}"')
    response = requests.get(f'http://127.0.0.1:5001/api/v1/posts/highlight/{p}', data=data)
    
    print(response.text)
    