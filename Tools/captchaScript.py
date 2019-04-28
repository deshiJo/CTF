#!/user/bin/python4
#import cv2
import sys
import time
import numpy as np
import requests
from pytesseract import image_to_string 
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO
expectedChars = 'abcdefghiklmnopqrstuvwxyz'

def solveSingleCaptcha(path,b):
    # Load the image and convert it to grayscale
    #imgage = rgb2gray(imread(path));
    #image = cv2.imread(path)
    threshold = 191  
    #image = cv2.imdecode(b, -1)
    kernel = np.ones((1,1),np.uint8)
    kernel2 = np.ones((1,1),np.uint8)
    #remove gray 
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # threshold the image (convert it to pure black and white)
    #thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY_INV)[1]

    #thresh = cv2.threshold(thresh, 170, 255, cv2.THRESH_BINARY_INV)[1]
    #thresh = cv2.dilate(thresh,kernel2,iterations = 1)
    #thresh = cv2.blur(thresh,(2,2))
    #thresh = cv2.erode(thresh,kernel,iterations = 1) 
    #thresh = cv2.threshold(thresh, 170, 255, cv2.THRESH_BINARY_INV)[1]
    #thresh = cv2.resize(thresh,(600,200))
    #contours,hierarchy = cv2.findContours(thresh, 1,1)
    #contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #thresh = cv2.resize(thresh,(90,30))

    captcha = image_to_string(thresh, config="-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz -l eng --oem 0").replace(' ', '')
    captcha = captcha.replace('\n', '')
    #cv2.imwrite(savePath2, thresh)
    print(captcha)
    return captcha

def captchaPIL(im):
    threshold = 191  
    im = im.point(lambda p: p > threshold and 255) 
    #im = im.filter(ImageFilter.DETAIL)
    im = im.filter(ImageFilter.SHARPEN)
    #im = im.filter(ImageFilter.EDGE_ENHANCE)
    #enhancer = ImageEnhance.Contrast(im)
    #im = enhancer.enhance(4)
    im = im.resize(((5 * im.width), (5 * im.height)), Image.ANTIALIAS)
    #im = im.point(lambda p: p > threshold and 255) 
    #im.show()
    #im = im.filter(ImageFilter.MedianFilter(3))
    #im = advanced_filters_image(im)
    captcha = image_to_string(im, config="-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz -l eng --oem 0 --psm 8").replace(' ', '')
    #captcha = image_to_string(im, config="-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz -l eng --oem 0").replace(' ', '')
    #captcha = captcha.replace('\n', '')
    #print(captcha)
    return captcha

def advanced_filters_image(image):
    kernelD = np.ones((2,1),np.uint8)
    kernelE = np.ones((2,1),np.uint8)
    #open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    #contours = cv2.findContours(open_cv_image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #open_cv_image = cv2.erode(open_cv_image,kernelE,iterations = 1) 
    #open_cv_image = cv2.dilate(open_cv_image,kernelD,iterations = 1)
    #contours, hierarchy = cv2.findContours(open_cv_image, 1, 2)
    #cnt = contours[4]
    #cv2.drawContours(open_cv_image, contours,  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imwrite(savePath2, open_cv_image)
    return open_cv_image

def split_and_save(image):
    pathFolder = "/home/user/Documents/CTF/Delloite/Delloite19Hackazon/Captcha/splitted/"
    path = pathFolder + "currentGray.png"
    #pix = np.array(Image.open(path).convert("L"))
    pix = np.array()
    # threshold image
    pix = (pix > 100) * 255

    col_ranges = [
        [5, 5 + 8],
        [14, 14 + 8],
        [23, 23 + 8],
        [32, 32 + 8]
    ]
    # split and save
    for col_range in col_ranges:
        letter = pix[:, col_range[0]: col_range[1]]
        im = Image.fromarray(np.uint8(letter))
        save_path =  pathFolder+ str(uuid.uuid4()) + ".png"
        im.save(save_path)

def start():
    #split_and_save("")
    todo = 100
    start = time.time()
    s = requests.Session()
    times = 0
    #while todo > 0: 
    while True:
        #times += 1
        #s.cookies.set_cookie(myCookie)
        r1 = s.get(requestURL)
        if r1.status_code == 200:
            #with open(savePath, 'wb') as f:
            #    r1.raw.decode_content = True
            #    f.write(r1.content)
            #b = np.asarray(bytearray(r1.content))
            #captcha = solveSingleCaptcha(savePath,b)
            image = Image.open(BytesIO(r1.content))
            captcha = captchaPIL(image)
            if captcha == '':
                continue
            data = {'captcha':captcha}
            r = s.post(url = endpoint, data = data)
            response = r.text
            if 'CTF' in response:
                print(response)
                return True
            #if 'Correct CAPTCHA!' in response:
            if ' 0 more' in response:
                #print("correct ! ", todo)
                print(response)
                #todo = todo - 1
                #if (todo == 50):
                #    print("50 done !")
        else:
            print("connection error")
    end = time.time()
    #r1 = s.get(requestURL)
    #print(r1.text) 
    #print("ACCURACY ! is ", int(100/times*100))
    #print("FINISHED ! in %d seconds" % (int(end)-int(start)))
    return False


if __name__ == '__main__':
    done = False
    endpoint = sys.argv[1]
    requestURL = endpoint+"craptcha.php"
    print(endpoint)
    print(requestURL)
    while not done:
        done = start()
