import requests
import json
import getpass
import sys
from bs4 import BeautifulSoup, Comment
username = sys.argv[1]
path = sys.argv[2]

# password = getpass.getpass("Enter Password:\n")

username = 'mimi'
key = '27845d491a579791eff9cd372c41ca501ae12f36ee983587e28e19ceba26820f'

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
        data['html_content']= soup.content.text,
        data['summary']= soup.summary.text,
        data['tags']= soup.tags.text

    pics = soup.find_all('pic')
    pics.append(soup.thumbnail)
    if not pics:
        pass
    else:
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
    response = requests.post('http://127.0.0.1:5001/api/v1/posts/add', data=data, files = post_files)
    
    print(response.text)
    print('Server response:\n')



