from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import random
import re
import os
import getpass
from PIL import Image

base_url = "http://www.pexels.com"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent, }

tags = ['forest', 'travel', 'texture', 'adventure', 'sunset', 'camera', 'music', 'abstract', 'night', 'black and white',
        'creative', 'animals', 'blur']

global i_name
global loc


def make_soup(url):
    request = Request(url, None, headers)
    html = urlopen(request).read()
    return BeautifulSoup(html, "lxml")


def get_search_url():
    number_of_tags = random.randrange(3, 5)
    tags_for_search = random.sample(tags, number_of_tags)
    base_search_url = base_url + '/search/' + ' '.join(tags_for_search)
    return base_search_url


def get_image_links(url):
    soup = make_soup(url)
    regex = r"href=\"(/.*/)\""
    reg = re.compile(regex)
    article = str(soup.find_all("article"))
    addresses = reg.findall(article)
    for i, address in enumerate(addresses):
        addresses[i] = base_url + address
    return addresses


def get_one():
    global i_name
    url = get_search_url()
    addresses = get_image_links(url)
    image = str(random.choice(addresses))
    i_name = image.split("/")[-2]
    i_name += ".jpeg"
    print("Image Name : ", i_name)
    return image


def this_image():
    soup = make_soup(get_one())
    address = str(soup.find("form", id="download-size"))
    regex = r"""data-alt-url=\"(.*)\" data-name=\"original\""""
    reg = re.compile(regex)
    download_link = ''.join(reg.findall(address))
    return download_link


def download_image():
    print("Started Fetching")
    download_url = this_image()
    username = getpass.getuser()
    location = "/home/" + username + "/Desktop/.desktop/originals/"
    if not os.path.isdir(location):
        os.mkdir(location)
    request = Request(download_url, None, headers)
    image_name = location + i_name
    if os.path.isfile(image_name):
        download_image()
    f = open(image_name, 'wb')
    f.write(urlopen(request).read())
    f.close()
    return image_name, i_name


def resize_image():
    loc, name = download_image()
    I = Image.open(loc)
    I = I.resize((1366, 768), Image.ANTIALIAS)
    name  = loc.split('/')[-1]
    location = "/".join(loc.split('/')[:-2])+"/"
    name = name.split('.')[0]
    name = location + name + "-1366x768.jpeg"
    I.save(name, quality=100)
    return name


