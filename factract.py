import sat_extract
import san_extract
import sys
from bs4 import BeautifulSoup
import urllib
import wikipedia

reload(sys)
sys.setdefaultencoding('utf8')


def find_images(user_input):
    image_url = list()
    image = wikipedia.page(user_input)
    for i in image.images:
        x = i.find('jpg')
        if x != -1:
            image_url.append(i)
    return image_url


def get_image(user_input):
    try:
        pg = wikipedia.WikipediaPage(title=user_input)
    except wikipedia.exceptions.DisambiguationError:
        # p = wikipedia.search(query=user_input, suggestion=True)
        # user_input = p[0][1]
        # pg = wikipedia.WikipediaPage(title=user_input)
        return 'False'
    except Exception:
        return 'Error'
    html_page = pg.html()
    bs = BeautifulSoup(html_page, 'html.parser')
    use_less = "//upload.wikimedia.org/wikipedia/commons/thumb/9/98/Ambox_current_red.svg/42px-Ambox_current_red.svg.png"
    try:
        image = bs.findAll('img', height=True)[0]
        if (image.get('src') == use_less):
            image = bs.findAll('img')[1]
        return "https://"+image.get('src')[2:]
    except:
        pass


def factract(user_input):
    a = sat_extract.fact_extract(user_input)
    clean_list = san_extract.get_facts(user_input)
    if clean_list == '':
        return clean_list
    b = ' '.join(word.encode('utf-8') for word in clean_list[:10])
    b = b.replace(". ", ".\n\n")
    c = a.decode('utf-8') + '\n' + b.decode('utf-8')
    c = c.replace("(listen);", "")
    return c.encode('utf-8')
