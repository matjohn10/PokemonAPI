import pandas as pd
from sqlalchemy import create_engine
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv(os.path.abspath('./.env'))


TYPES = ['Normal',
'Fire',
'Water',
'Grass',
'Electric',
'Ice',
'Fighting',
'Poison',
'Ground',
'Flying',
'Psychic',
'Bug',
'Rock',
'Ghost',
'Dark',
'Dragon',
'Steel',
'Fairy']

conn = create_engine(url=f'mysql+pymysql://{os.getenv("AWS_USERNAME")}:{os.getenv("AWS_PASSWORD")}@{os.getenv("AWS_ENDPOINT")}:3306/{os.getenv("AWS_DB_NAME")}')
select_pokemons = 'SELECT * FROM pokemons'
select_types = 'SELECT * FROM types'
select_images = 'SELECT * FROM poke_images'
select_description = 'SELECT * FROM Description'
select_paths = "SELECT * FROM image_paths"

class PokeInformation():
    def __init__(self):
        self.poke_df = pd.read_sql(select_pokemons, conn)
        self.pokemons = self.make_dct(self.poke_df)
        self.types = self.make_dct(pd.read_sql(select_types, conn))
        self.images = self.make_dct(pd.read_sql(select_images, conn))
        self.paths = pd.read_sql(select_paths, conn)
        self.description = self.make_dct(pd.read_sql(select_description, conn))
        self.name_to_id = self.poke_df['name']  # use list ID + 1 to get id or name
        
    def is_pokemon(self, name) -> bool:
        return name in self.name_to_id.values
    
    def all_info(self) -> dict:
        return {'pokemons': self.pokemons, 'types': self.types, 'descriptions': self.description, 'images': self.images}
    
    def pokemon_info(self):
        return self.pokemons
    
    def pokemon_from_id(self, id: str):
        dct = self.pokemons[int(id)]
        types = [dct['type1'], dct['type2'], dct['type3']]
        type_info = {}
        for type in types:
            if type == 'null' or type is None or not type:
                continue
            type_info[type] = self.types[type]
        dct['combat'] = type_info
        
        return dct    #self.pokemons[int(id)]
    
    def pokemon_from_name(self, name: str):
        name = name.capitalize()
        poke_id = list(self.name_to_id).index(name) + 1
        obj = self.pokemons[poke_id]
        obj["id"] = poke_id
        types = [obj['type1'], obj['type2'], obj['type3']]
        type_info = {}
        for type in types:
            if type == 'null' or type is None or not type:
                continue
            type_info[type] = self.types[type]
        obj['combat'] = type_info
        return obj
    
    def type_info(self):
        return self.types
    
    def type_from_type(self, type: str):
        type = type.capitalize()
        return self.types[type]
    
    def image_info(self):
        return self.images
    
    def image_from_id(self, id: str):
        return self.images[int(id)]
    
    def image_from_name(self, name: str):
        name = name.capitalize()
        poke_id = list(self.name_to_id).index(name) + 1
        return poke_id

    def make_dct(self, df: dict) -> dict:
    
        if 'name' in df.columns:
            try:
                new = df.set_index('ID').T.to_dict()
                return new
            except KeyError:
                new = df.set_index('id').T.to_dict()
                return new
        elif 'type' in df.columns:
            new = {}
            attack, defence = df.set_index('type').T.to_dict(orient='records')
            for type in attack:
                if type == 'Type':
                    pass
                else:
                    new[type] = {'Strong attack': json.loads(attack[type]), 'Weak defence': json.loads(defence[type])}
            return new
        else:
            new = df.set_index('ID')['image'].to_dict()
            return new

    def download_img(self):
        for id in self.images:
            img_url = self.images[id]
            img_data = requests.get(img_url).content
            with open(f'./img/pokemon{id}.jpg', 'wb') as handler:
                handler.write(img_data)
            print(id)

    def get_description(self):
        return self.description
    
    def des_from_id(self, id: int):
        return self.description[id]
    
    def des_from_name(self, name: str):
        name = name.capitalize()
        poke_id = list(self.name_to_id).index(name) + 1
        obj = self.description[poke_id]
        obj["id"] = poke_id
        return obj
    
    def pokemons_per_type(self, type_name=None):
        dct = {}
        for type in TYPES:
            names = list(self.poke_df[(self.poke_df['type1'] == type) | (self.poke_df['type2'] == type) | (self.poke_df['type3'] == type)]['name'])
            dct[type] = names
        if type_name is None:
            return dct
        else:
            return dct[type_name.capitalize()]
        
    def get_paths(self):
        paths = self.paths.set_index('name').T.to_dict()
        return paths



if __name__ == "__main__":
    # poke = pd.read_sql(select_pokemons, conn)
    # types = pd.read_sql(select_types, conn)
    # images = pd.read_sql(select_images, conn)
    p = PokeInformation()
    
