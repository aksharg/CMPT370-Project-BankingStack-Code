import json
import sys
import mimetypes
from http.server import BasedHTTPRequestHandler, ThreadingHTTPServer

class plaidHTTPServer(BasedHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
    
    def fileServe(self, file_path: str):
        """[summary]

        Args:
            file_path (str): [description]
        """
        pass
    
    def send404(self):
        """[summary]
        """
        pass

    def requestPOST(self):
        """[summary]
        """
        pass

    def requestGET(self):
        """[summary]
        """
        pass

def createPlaidHandler(*args, **kwargs):
    """[summary]

    Returns:
        [type]: [description]
    """
    return plaidHTTPServer(*args, **kwargs)

def serveWebpage(environemt: str, client_name: str, public_token: str, page_title: str, account_name: str, account_type: str) -> Dict:
    """[summary]

    Args:
        environemt (str): [description]
        client_name (str): [description]
        public_token (str): [description]
        page_title (str): [description]
        account_name (str): [description]
        account_type (str): [description]

    Returns:
        Dict: [description]
    """
    param_json = dict(env=environemt, 
                      client_name=client_name, 
                      public_token=public_token, 
                      page_title=page_title,
                      account_name=account_name,
                      account_type=account_type)
    
    # with ThreadingHTTPServer(('127.0.0.1',8000), createPlaidHandler) as httpd:

if __name__ == '__main__':
    serveWebpage({})