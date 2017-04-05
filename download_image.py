import getpass
from urllib.request import urlopen, Request

import os
import random
import re
from PIL import Image
from bs4 import BeautifulSoup

base_url = "http://www.pexels.com"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent, }

tags = ['forest', 'travel', 'texture', 'adventure', 'sunset', 'camera', 'music', 'abstract', 'night', 'black and white',
        'creative', 'animals', 'blur', 'dark']

global i_name
global loc


def make_soup(url):
    """Making the soup"""
    request = Request(url, None, headers)
    html = urlopen(request).read()
    return BeautifulSoup(html, "lxml")


def get_search_url():
    """generate a search URL from random tags more than 3 and between five"""
    number_of_tags = random.randrange(3, 5)
    tags_for_search = random.sample(tags, number_of_tags)
    base_search_url = base_url + '/search/' + ' '.join(tags_for_search)
    return base_search_url


def get_image_links(url):
    """get all the image links on the page"""
    # Soup the soup first
    soup = make_soup(url)
    regex = r"href=\"(/.*/)\""
    reg = re.compile(regex)
    article = str(soup.find_all("article"))
    addresses = reg.findall(article)
    for i, address in enumerate(addresses):
        addresses[i] = base_url + address
    return addresses


def get_one():
    """Return one Image Link from all the image links"""
    global i_name
    # get the search URL
    url = get_search_url()
    # get all the image addresses on that URL
    addresses = get_image_links(url)
    # Choose one image from the addresses
    image = str(random.choice(addresses))
    # Print the image Name to be downloaded
    i_name = image.split("/")[-2]
    i_name += ".jpeg"
    print("Image Name : ", i_name)
    return image


def this_image():
    """get the download link of the image"""
    # Make soup of the chosen image URL
    soup = make_soup(get_one())
    address = str(soup.find("form", id="download-size"))
    regex = r"""data-alt-url=\"(.*)\" data-name=\"original\""""
    reg = re.compile(regex)
    download_link = ''.join(reg.findall(address))
    return download_link


def download_image():
    """Download the Image"""
    print("Started Fetching")
    download_url = this_image()
    # get users name to find the config file and saving the downloaded files in Desktop/.desktop
    username = getpass.getuser()
    # Save location of Original downloaded file
    location = "/home/" + username + "/Desktop/.desktop/originals/"
    if not os.path.isdir(location):
        os.mkdir(location)
    request = Request(download_url, None, headers)
    image_name = location + i_name
    if os.path.isfile(image_name):
        print("File already present, getting new file")
        download_image()
    f = open(image_name, 'wb')
    f.write(urlopen(request).read())
    f.close()
    return image_name, i_name


def resize_image():
    loc, name = download_image()
    I = Image.open(loc)
    I = I.resize((1366, 768), Image.ANTIALIAS)
    name = loc.split('/')[-1]
    location = "/".join(loc.split('/')[:-2]) + "/"
    name = name.split('.')[0]
    name = location + name + "-1366x768.jpeg"
    I.save(name, quality=100)
    return name
