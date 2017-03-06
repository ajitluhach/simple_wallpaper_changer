from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import random, os, re


base_url = "http://www.pexels.com"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent,}

tags = ['forest', 'travel', 'texture', 'adventure', 'sunset', 'camera', 'music', 'abstract', 'night', 'black and white', 'creative', 'animals', 'blur']


def make_soup(url):
    request = Request(url, None, headers)
    html = urlopen(request).read()
    return BeautifulSoup(html)


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
    for i,address in enumerate(addresses):
        addresses[i] = base_url + address
    return addresses

def choose(addresses):
    image = str(random.choice(addresses))
    return image

def which_image():
    url = get_search_url()
    addresses = get_image_links(url)
    return choose(addresses)

def this_image():
    soup = make_soup(which_image())
    address = str(soup.find("form", id="download-size"))
    regex = r"""data-alt-url=\"(.*)\" data-name=\"original\""""
    reg = re.compile(regex)
    download_link = ''.join(reg.findall(address))
    return download_link

def download_image():
    download_url = this_image()
    print(download_url)
    print(os.getcwd())
    image_name = download_url.split('/')[-1]
    print(image_name)
    request = Request(download_url, None, headers)
    f = open(image_name, 'wb')
    f.write(urlopen(request).read())
    f.close()


download_image()
