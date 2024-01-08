import requests
import json
import getpass
import sys
from bs4 import BeautifulSoup, Comment
username = sys.argv[1]
path = sys.argv[2]

# password = getpass.getpass("Enter Password:\n")

username = 'mimi'
key = '2697348d02d9471727f854a31a6a648f790bcdc8b2725362cb536b7af8c643fe'

data = {
    "request_type": "json",
    "username": username,
    "key": key
}
print(f'Authenticating as {username}')

with open(f'{path}') as f:
    post_content = f.read()
    soup = BeautifulSoup(post_content, 'html.parser')
    for element in soup.descendants:
        if isinstance(element, Comment):
            element.extract()
    data['title']= soup.title.text,
    data['html_content']= soup.content.decode_contents(),
    data['summary']= soup.summary.decode_contents(),
    data['tags']= soup.tags.text
    img_soup = BeautifulSoup(post_content, 'html.parser')
    images = img_soup.find_all('img')
    post_files = {}
    j=0
    for i in images:
        try:
            j+=1
            pic = open(f'{i["src"]}', 'rb')
            post_files[f'file{i}'] = pic
        except FileNotFoundError:
            print('Missing an image file, aborting.')
            exit()
    response = requests.post('http://127.0.0.1:5001/api/v1/posts/add', data=data, files = post_files)
    print('Server response:\n\n')    
    print(response.text)




