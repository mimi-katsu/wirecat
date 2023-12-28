import os
import secrets
from hashlib import sha256
from hmac import HMAC, compare_digest

class Secrets:
    def sha_256_hash(self, content):
        sha_hash = sha256(content.encode('UTF-8')).hexdigest()
        return sha_hash

    def new_api_key(self):
        api_key = secrets.token_hex(32)
        key_hash = self.sha_256_hash(api_key)
        #push hash to database
        #distribute key to client
        return api_key, key_hash

    def verify_key(self, request, user):
        request_key = request.headers.get('auth')
        user_key = wirecat.db.get_user(user).api_key
        if self.sha_256_hash(user_key) == api_key:
            return True
        else:
            return False

    def verify_key_hmac(self, request, user):
        recv_hash = request.headers.get('Sha-256-Signature')
        user_secret = wirecat.db.get_user(user).secret_key
        signature = HMAC(key=user_key, msg=request.data, digestmod=sha256).hexdigest()
        if signature == recv_hash:
            return True
        else:
            return False

    def get_author_key(self):
        # s = os.environ.get('KEY').encode()
        # recv = req.headers.get('X-Hub-Signature-256').split('sha256=')[-1].strip()
        # sign = HMAC(key=s, msg=req.data, digestmod=sha256).hexdigest()
        # return compare_digest(recv, sign)        
        return os.environ.get('WIRECAT_AUTHOR_KEY')

if __name__=='__main__':
    main()