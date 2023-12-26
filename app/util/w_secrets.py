import os
import secrets
from hashlib import sha256
from hmac import HMAC, compare_digest

def main():
    api_key = secrets.token_hex(32)
    print(api_key)

class Secrets:
    def get_author_key(self):
        # s = os.environ.get('KEY').encode()
        # recv = req.headers.get('X-Hub-Signature-256').split('sha256=')[-1].strip()
        # sign = HMAC(key=s, msg=req.data, digestmod=sha256).hexdigest()
        # return compare_digest(recv, sign)        
        return os.environ.get('WIRECAT_AUTHOR_KEY')

if __name__=='__main__':
    main()