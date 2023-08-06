import requests
from .objects import *

class seclibb:
    def __init__(self):
        self.api = "https://www.1secmail.com/api/v1/"

    def generate_email(self):
        r = requests.get(f"{self.api}?action=genRandomMailbox&count=1").text
        r = r.replace(']', "")
        r = r.replace('[', "")
        r = r.replace('"', "")
        self.email = r
        return self.email

    def get_messages(self,email):
        self.email = email[0:email.index("@")]
        self.domain = email[email.index("@"):][1:]
        r = requests.get(f"{self.api}?action=getMessages&login={self.email}&domain={self.domain}").text
        return Get_Messages(r)

    def fetch_messaage(self,email, id):
        self.email = email[0:email.index("@")]
        self.domain = email[email.index("@"):][1:]
        self.id = id
        r = requests.get(f"{self.api}?action=readMessage&login={self.email}&domain={self.domain}&id={self.id}").text
        return Fetch_Message(r)
