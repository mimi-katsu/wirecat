import os

class Secrets:
    def get_author_key(self):
        ## TODO: implement HMAC
        return os.environ.get('WIRECAT_AUTHOR_KEY')
