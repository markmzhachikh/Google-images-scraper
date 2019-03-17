#_______________________________________________________________________________________________________________________
#The Script should be able to take the image query and number of images to be scraped.
#For example an input of 'cat' 23 should return 23 google images of cats.
#The download directory folder should be the name of the query.
#So a query for 'cats' should download the image files to a folder called cats
#_______________________________________________________________________________________________________________________
import os
import time
import urllib.request
import requests
from selenium import webdriver
from pathvalidate import sanitize_filename, ValidationError, validate_filename
from selenium.webdriver.common.keys import Keys

def get_webdriver():
    try:
        return webdriver.Chrome()
    except:
        try:
            return webdriver.Firefox()
        except:
            return None

def download_src(src, dir):
    global i
    local_filename = src.rsplit('/')
    local_filename = local_filename[len(local_filename) - 1]
    splitted = local_filename.rsplit('.')
    ext = splitted[-1]
    if len(splitted) < 2 \
        or ext.lower() not in VALID_EXTENSIONS:
            local_filename = local_filename + '.jpg'

    try:
        validate_filename(local_filename)
    except ValidationError:
        local_filename = sanitize_filename(local_filename)

    local_filename = './' + dir + '/' + local_filename

    if os.path.isfile(local_filename): return #this file had been downloaded already
    try:
        headers = requests.utils.default_headers()
        headers.update(
            {
                'User-Agent': 'mozilla/5.0',
            }
        )
        response = requests.get(src, headers=headers)
        f = open(local_filename, 'wb')
        f.write(response.content)
        f.close()
        i += 1
        print(str(i) + ': ' + local_filename)
    except:
        try:
            sleep05()
            urllib.request.urlretrieve(src, local_filename)
            i += 1
            print(str(i) + ': ' + local_filename)
        except Exception as e:
            print(str(e))

def sleep05(count=1):
    for j in range(count):
        time.sleep(0.5)
#_______________________________________________________________________________________________________________________
#main
#_______________________________________________________________________________________________________________________

#init
VALID_SIZES = ['l','m','s']
VALID_EXTENSIONS = ['jpg', 'png', 'jpeg', 'gif', 'svg']

i = 0

#user input
query = input('Enter query:')
num   = int(input('Pictures count:'))
size  = str(input('Select images size:\nL - Large\nM - Medium\nS - Small\nLeave empty for any\nChoose size: '))

#dir creation
if not os.path.isdir('./' + query):
    os.mkdir('./' + query)

#start browser
drv = get_webdriver()
if drv == None:
    print('Webdriver error')
    exit(1)
try:
    #load page and do query
    drv.get('https://images.google.com')
    q = drv.find_element_by_name('q')
    q.send_keys(query)
    q.send_keys(Keys.ENTER)
    sleep05(3)

    #set size
    size = size.lower().replace(' ', '')
    if size in VALID_SIZES:
        tools_btn = drv.find_element_by_id('hdtb-tls')
        tools_btn.click()
        sleep05()
        size_btn = drv.find_element_by_class_name('hdtb-mn-hd')
        size_btn.click()
        sleep05()
        size_opt = drv.find_element_by_id('isz_' + size.replace('s','i'))
        size_opt.click()
        sleep05()

    #open image properties form
    btns = drv.find_elements_by_class_name('rg_ic')
    sleep05(2)
    if len(btns):
        for btn in btns:
            try:
                btn.click()
                sleep05()
                break
            except:
                continue

        #download images in a loop
        btn_next = drv.find_element_by_id('irc-rab')
        while i < num:

            for img in drv.find_elements_by_class_name('irc_mi'):
                src = img.get_attribute('src')
                if src != None and i < num:
                    download_src(src, query)
            try:
                if not btn_next.is_displayed():
                    print('No more images mathing your search terms were found.')
                    break
                btn_next.click()
                sleep05()
            except Exception as e:
                print(str(e))
                sleep05()
                continue
    else:
        print('No results containing all your search terms were found.')
finally:
    drv.close()
