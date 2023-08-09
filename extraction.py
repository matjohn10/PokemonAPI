import mechanicalsoup
import json
from PIL import Image
import requests
from io import BytesIO

URL = "https://www.pokemon.com/us/pokedex/"
TYPES = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', ' fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']

class Extraction():
    def __init__(self):
        self.counter = '0001'
        self.browser = mechanicalsoup.Browser()
        self.url = self.update_URL()
    
    def update_URL(self):
        url = URL + self.counter
        return url
    
    def extract_name_type(self, poke_range: str):
        pokedex = []
        types_lst = []
        while self.counter != poke_range:
            page = self.browser.get(self.url)
            #Get name:
            name_class = 'pokedex-pokemon-pagination-title'
            name_div = page.soup.find('div', name_class)
            name_child = name_div.findChildren('div', recursive=False)
            name = name_child[0].text.strip().split(' ')[0].strip()

            #Get types:
            types = page.soup.find('div', 'dtm-type')
            li = types.findChildren('li')
            for l in li:
                types_lst.append((l.find('a').text))
                types_lst.sort()
            while len(types_lst) < 3:
                types_lst.append(None)
            # poke_dct[self.counter] = {name: types_lst.copy()}
            pokedex.append((int(self.counter), name, types_lst[0], types_lst[1], types_lst[2]))
            printProgressBar(int(self.counter), int(poke_range))
            self.add_counter()
            self.url = URL + self.counter
            types_lst.clear()
        return pokedex
    
    def get_images(self, poke_range: str):
        all_images = []
        while self.counter != poke_range:
            page = self.browser.get(self.url)
            info = page.soup.find('div', 'profile-images')
            img = info.findChildren('img')[0]['src']
            
            #JUST SAVE THE LINK IN DB
            # response = requests.get(img)
            # pil_img = Image.open(BytesIO(response.content))
            # image_bytes = BytesIO()
            # pil_img.save(image_bytes, format='PNG')
            # pil_img.save(f'./img/{name}.png')
            all_images.append((self.counter, img))
            # printProgressBar(int(self.counter), int(poke_range))
            self.add_counter()
            self.url = URL + self.counter
        return all_images
    
    
    def get_all(self, poke_range: str):
        all_images = []
        pokedex = []
        types_lst = []
        while self.counter != poke_range:
            page = self.browser.get(self.url)
            info = page.soup.find('div', 'profile-images')
            img = info.findChildren('img')[0]['src']
            
            name_class = 'pokedex-pokemon-pagination-title'
            name_div = page.soup.find('div', name_class)
            name_child = name_div.findChildren('div', recursive=False)
            name = name_child[0].text.strip().split(' ')[0].strip()
            
            types = page.soup.find('div', 'dtm-type')
            li = types.findChildren('li')
            for l in li:
                types_lst.append((l.find('a').text))
                types_lst.sort()
            while len(types_lst) < 3:
                types_lst.append(None)
            pokedex.append((int(self.counter), name, types_lst[0], types_lst[1], types_lst[2]))
            all_images.append((self.counter, img))
            
            printProgressBar(int(self.counter), int(poke_range))
            self.add_counter()
            self.url = URL + self.counter
            types_lst.clear()
        return [pokedex, all_images]
            
    def add_counter(self):
        # self.counter.replace('0', '')
        self.counter = str(int(self.counter) + 1)
        while len(self.counter) < 4:
            self.counter = '0' + self.counter
    
    def reset(self):
        self.counter = '0001'


class Types():
    def __init__(self):
        self.url = 'https://www.xfire.com/all-pokemon-types/' #'https://pokemondb.net/type/'
        self.browser = mechanicalsoup.Browser()
        self.types = TYPES
    
    def extract(self):
        all_types = []
        all_att = []
        all_def = []
        page = self.browser.get(self.url)
        table = page.soup.find('table')
        rows = table.findChildren('tr')         
        for row in rows:
            poke_type, attack, bad_defence = [x.text for x in row.findChildren('td')]
            # print(f'{poke_type}: ', attack, ' + ', bad_defence, '\n---------')
            att_lst = attack.split(', ')
            def_lst = bad_defence.split(', ')
            all_types.append((poke_type, json.dumps(att_lst), json.dumps(def_lst)))
            # all_types.append(poke_type)
            # all_att.append(att_lst)
            # all_def.append(def_lst)
        return all_types


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        print('COMPLETED')


if __name__ == '__main__':
    e = Extraction()
    e.get_images('0003')