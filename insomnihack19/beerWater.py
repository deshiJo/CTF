#!/usr/bin/env python3
import requests
from base64 import b64decode


def enc(recipient, drink):
    #url = 
    payload = {
            'recipientName': recipient,
            'drink': drink
            }
    r = requests.post(url, json=payload)
    return r.status_code, r.text

def dec(encryptedVoucher, passphrase):
    #url = 
    payload = {
            'encryptedVoucher': encryptedVoucher,
            'passphrase': passphrase
            }
    r = requests.post(url, json=payload)
    return r.status_code, r.text

def caluclatePassphrase():
    mode = 'beer'
    result = "||"
    #result = "G1MME_B33R_1M_S0_V3RY"
    startSize = 10000
    times = 10
    while(times > 0):
        currentSize = startSize
        multibleValues = False
        for i in range(48,127):
            if chr(i).isprintable():
                var = result + chr(i)
                status_code, withBeer = enc(var, mode)
                raw = "".join(withBeer.split('\n')[2:-3])
                length = len(b64decode(raw))
                print("try :",chr(i) ,":", var, "with length", length)
                if length == currentSize:
                    multibleValues = True
                elif length < currentSize:
                    multibleValues = False
                    currentSize = length
                    currentSmallest = chr(i)
                    print("new smalest:", chr(i))
            if(i==126):
                if multibleValues:
                    currentSize = startSize
                    print("multiple encryptions with the same size ! Calulating again")
                    times -= 1
                    continue
                result += currentSmallest
                print("current result :" + result)
                times = 10
    return result

def pwn():
    result = caluclatePassphrase()
    print("calulation finished or there are multible possible characters after", result)
    print("continue calculation with one of the possible characters")
    #status_code, data = dec(withBeer, result)
    #print(data)


if __name__=="__main__":
    pwn()

