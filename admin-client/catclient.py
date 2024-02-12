import argparse
import os
import json
import getpass
import sys
import requests
from bs4 import BeautifulSoup, Comment
import secrets

class Option:
    def __init__(self, func, help:str):
        self.func = func
        self.help = help

    def execute(self, args):
        self.func(args)

def create_parser():
    parser = argparse.ArgumentParser(description="Client for interacting with the wirecat api.")

    parser.add_argument("method", type=str, help="The type of action to take. ['announce','post', 'delete', 'highlight', 'unhighlight','publish','hide','flush','ban','unban', 'hidden', 'newuser']")
    parser.add_argument("--host", type=str, help="Host domain or ip address", required=True)
    parser.add_argument("-u", type=str, help="Username to authenticate with", required=True)
    parser.add_argument("-k", type=str, help="Path to api key to authenticate with", required=True)
    parser.add_argument("-p", type=str, help="Display prompt to enter your password for authentication")
    parser.add_argument("--id", type=str, help="Identify target post or user by id")
    parser.add_argument("--name", type=str, help="Identify target post or user by name (url slug or user name)")
    parser.add_argument("-f", type=str, help="HTML file path to upload as a post.")
    parser.add_argument("--email", type=str, help="Specify email for user creation or identification")
    parser.add_argument("--password", type=str, help="Specify password for new user creation")
    parser.add_argument("--access", type=str, help="Specify access level of user to create or modify. ['admin',author,'user']")
    parser.add_argument("--message", type=str, help="The message to display on the front page of the site.")


    return parser

def announce(args):
    if not args.u:
        print("Please specify a username to authenticate as")
        return
    username = args.u
    if not args.k:
        print("Please specify your password or api key")
        return

    if not args.message:
        print("Please specify the message to display on the front page of the site.")
        return
    
    with open(f'./{args.k}', 'r') as f:
        key = f.read()

        data = {
            # "request_type": "json",
            "username": username,
            "key": key,
            "announcement": args.message
        }
        print(f'Authenticating as {username}')

        response = requests.post("http://127.0.0.1:5001/api/v1/announcements/add", data=data)
        print(response.text)

def post(args):
    if not args.u:
        print("Please specify a username to authenticate as")
        return
    username = args.u
    if not args.k:
        print("Please specify your password or api key")
        return

    if not args.f:
        print("Please specify the file path of your HTML document")
        return
    
    with open(f'./{args.k}', 'r') as f:
        key = f.read()

        data = {
            # "request_type": "json",
            "username": username,
            "key": key
        }
        print(f'Authenticating as {username}')

        with open(f'{args.f}') as f:
            post_content = f.read()
            soup = BeautifulSoup(post_content, 'html.parser')
            for element in soup.descendants:
                if isinstance(element, Comment):
                    element.extract()
            data['title']= soup.title.text
            data['html_content']= soup.content.decode_contents()
            data['summary']= soup.summary.decode_contents()
            data['thumbnail'] = soup.thumbnail.decode_contents()
            data['tags']= soup.tags.text
            data['category']=soup.category.text
            img_soup = BeautifulSoup(post_content, 'html.parser')
            post_files = {}
            images = img_soup.find_all('img')
            j=0
            for i in images:
                try:
                    j+=1
                    pic = open(f'{i["src"]}', 'rb')
                    if i['class'][0] == 'thumbnail':
                        post_files['thumbnail'] = pic
                        data['thumbnail'] = i['src']
                    else:
                        post_files[f'file{i}'] = pic
                except FileNotFoundError:
                    print('Missing an image file, aborting.')
                    exit()
            response = requests.post('http://127.0.0.1:5001/api/v1/posts/add', data=data, files = post_files)
            for n,f in post_files.items():
                f.close()
            print('Server response:\n\n')    
            print(response.text)    

def highlight(args):
    if not args.u:
        print("Please specify a username to authenticate as")
        return

    if not args.k:
        print("Please specify your password or api key")
        return

    if args.name:
        id_type = 'slug'
        target = args.name

    if args.id:
        id_type = 'id'
        target = args.id

    data = {'username': args.u}

    if args.k:
        with open(f'{args.k}', 'r') as key:
            data['key'] = key
            print(f'Sending request to highlight:\n\n "{target}"\n\n')
            response = requests.get(f'http://127.0.0.1:5001/api/v1/posts/highlight/add/{id_type}/{target}', data=data)
            # print(response.text)
            try:
                r = json.loads(response.text)
            except json.JSONDecodeError:
                print("Unexpected response from server")
                exit()
            print(f'''Status: {r['success']}''')
            print(f'''Message: {r['msg']}''')
            print(f'''Type: {r['type']}''')
            print('\n\n')

def unhighlight(args):
    if not args.u:
        print("Please specify a username to authenticate as")
        return

    if not args.k:
        print("Please specify your password or api key")
        return

    if args.name:
        id_type = 'slug'
        target = args.name

    if args.id:
        id_type = 'id'
        target = args.id

    data = {'username': args.u}

    if args.k:
        with open(f'{args.k}', 'r') as key:
            data['key'] = key
            print(f'Sending request to highlight:\n\n "{target}"\n\n')
            response = requests.get(f'http://127.0.0.1:5001/api/v1/posts/highlight/remove/{id_type}/{target}', data=data)
            # print(response.text)
            try:
                r = json.loads(response.text)
            except json.JSONDecodeError:
                print("Unexpected response from server")
                exit()
            print(f'''Status: {r['success']}''')
            print(f'''Message: {r['msg']}''')
            print(f'''Type: {r['type']}''')
            print('\n\n')

def publish(args):
    if not args.u:
        print("Please specify a username to authenticate as")
        return

    if not args.k:
        print("Please specify your password or api key")
        return

    if args.name:
        id_type = 'slug'
        target = args.name

    if args.id:
        id_type = 'id'
        target = args.id

    data = {'username': args.u}

    if args.k:
        with open(f'{args.k}', 'r') as key:
            data['key'] = key
            print(f'Sending request to highlight:\n\n "{target}"\n\n')
            response = requests.get(f'http://127.0.0.1:5001/api/v1/posts/publish/{id_type}/{target}', data=data)
            # print(response.text)
            try:
                r = json.loads(response.text)
            except json.JSONDecodeError:
                print("Unexpected response from server")
                exit()
            print(f'''Status: {r['success']}''')
            print(f'''Message: {r['msg']}''')
            print(f'''Type: {r['type']}''')
            print('\n\n')

def hide(args):
    if not args.u:
        print("Please specify a username to authenticate as")
        return

    if not args.k:
        print("Please specify your password or api key")
        return

    if args.name:
        id_type = 'slug'
        target = args.name

    if args.id:
        id_type = 'id'
        target = args.id

    data = {'username': args.u}

    if args.k:
        with open(f'{args.k}', 'r') as key:
            data['key'] = key
            print(f'Sending request to highlight:\n\n "{target}"\n\n')
            response = requests.get(f'http://127.0.0.1:5001/api/v1/posts/hide/{id_type}/{target}', data=data)
            # print(response.text)
            try:
                r = json.loads(response.text)
            except json.JSONDecodeError:
                print("Unexpected response from server")
                exit()
            print(f'''Status: {r['success']}''')
            print(f'''Message: {r['msg']}''')
            print(f'''Type: {r['type']}''')
            print('\n\n')
def delete(args):
    if not args.u:
        print("Please specify a username to authenticate as")
        return

    if not args.k:
        print("Please specify your password or api key")
        return

    if args.name:
        id_type = 'slug'
        target = args.name

    if args.id:
        id_type = 'id'
        target = args.id

    data = {'username': args.u}

    if args.k:
        with open(f'{args.k}', 'r') as key:
            data['key'] = key
            print(f'Sending request to delete:\n\n "{target}"\n\n')
            conf = input("Are you sure you want to do this?\n")
            if conf != "yes":
                print('\naborting\n')
                exit()
            response = requests.delete(f'http://127.0.0.1:5001/api/v1/posts/delete/{id_type}/{target}', data=data)
            print(response.text)
            try:
                r = json.loads(response.text)
            except json.JSONDecodeError:
                print("Unexpected response from server")
                exit()
            print(f'''\nStatus: {r['success']}''')
            print(f'''Message: {r['msg']}''')
            print(f'''Type: {r['type']}''')
            print('\n\n')

def get_hidden(args):
    if not args.u:
        print("Please specify a username to authenticate as")
        return

    if not args.k:
        print("Please specify your password or api key")
        return

    data = {'username': args.u}

    if args.k:
        with open(f'{args.k}', 'r') as key:
            data['key'] = key
            print(f'Sending request to get unpublished posts')
            response = requests.get(f'http://127.0.0.1:5001/api/v1/posts/get/hidden', data=data)
            # print(response.text)
            try:
                r = json.loads(response.text)
                for k, v in r.items():
                    print(f"{k}: {v}")
                print(f'''Status: {r['success']}''')
                print(f'''Type: {r['type']}\n\n''')
            except json.JSONDecodeError:
                print("Unexpected response from server")
                exit()
            try:
                for p in r['msg']:
                    for key, value in p.items():
                        print(f'{key}: {value}')
                    print('\n\n')
            except AttributeError:
                print('Either there are no posts or something went wrong')
# def flush(args):
# 
# def ban(args):
# 
# def unban(args):
# 
def register_user(args):
    if not args.u:
        print("Please specify a username to authenticate as")
        return

    if not args.k:
        print("Please specify your password or api key")
        return

    data = {'username': args.u}

    if not args.name:
        user = input('Enter username:\n')
    
    data['newuser'] = args.name

    if not args.email:
        email = input('Enter user email address:\n')

    data['email'] = args.email


    if not args.password:
        password = getpass.getpass('Enter user password:\n')
        if password == '':
            password = secrets.token_hex(10)

    data['password'] = args.password

    if not args.access:
        access = input('Enter user access level (user, author, admin) Default is "user"\n')
        if access == '':
            access = None

    if args.access:
        access = args.access
    data['access_level'] = access

    if args.k:
        with open(f'{args.k}', 'r') as key:
            data['key'] = key
            print(data)
            print(f'Sending request to register user:\n\n "{args.name}"\n\n')
            response = requests.get(f'http://127.0.0.1:5001/api/v1/users/register', data=data)
            # print(response.text)
            try:
                r = json.loads(response.text)
            except json.JSONDecodeError:
                print("Unexpected response from server")
                exit()
            print(f'''Status: {r['success']}''')
            print(f'''Message: {r['msg']}''')
            print(f'''Type: {r['type']}''')
            print('\n\n')
 

def create_options():
    return {
        'post': Option(post, "The path to the post's html document"),
        'delete': Option(delete, "Delete a post completely. This removes its contents from the database as well."),
        'highlight': Option(highlight, "Add a post to the featured category"),
        'unhighlight': Option(unhighlight, "Remove a post from the featured category"),
        'publish': Option(publish, "Make a post visible to all users on the site"),
        'hide': Option(hide, "Make a post visible only to it's author and admins"),
        'hidden': Option(get_hidden, "Get a JSON formatted list of all unpublished posts"),
        'newuser': Option(register_user, "Create a new user"),
        'announce': Option(announce, "Make new announcement")
        # 'flush': Option(flush, "flush out the site caches"),
        # 'ban': Option(ban,"Ban a users account"),
        # 'unban': Option(unban, "Unban a users account")

    }



def main():
    options = create_options()

    parser = create_parser()
    args = parser.parse_args()


    action = args.method
    options[f'{action}'].execute(args)


if __name__=='__main__':
    main()