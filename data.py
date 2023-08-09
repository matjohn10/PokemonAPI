from mySQL_credentials import USERNAME, PASSWORD
import mysql.connector
from extraction import Extraction, Types
import os
from sqlalchemy import create_engine
from mySQL_credentials import USERNAME, PASSWORD
import pandas as pd
import re

def insert_pokemons():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host='localhost', database='Pokemons')
    describe_query = 'DESCRIBE pokemons'
    insert_query = 'INSERT INTO pokemons (ID, name, type1, type2, type3) VALUES ( %s, %s, %s, %s, %s )'
    e = Extraction()
    records = e.extract_name_type('1009')
    with cnx.cursor() as cursor:
        try:
            cursor.executemany(insert_query, records)
            cnx.commit()
        except Exception as e:
            print(e)
    print('DONE')
    cnx.close()
    

def insert_types():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host='localhost', database='Pokemons')
    insert_query = 'INSERT INTO types (type, attack, defence) VALUES ( %s, %s, %s )'
    t = Types()
    types = t.extract()
    print(types)
    with cnx.cursor() as cursor:
        try:
            cursor.executemany(insert_query, types)
            cnx.commit()
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

    print('DONE')
    cnx.close()


def insert_images():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host='localhost', database='Pokemons')
    e = Extraction()
    images = e.get_images('1009')
    insert_query = 'INSERT INTO poke_images (ID, image) VALUES ( %s, %s )'
    type_query = 'INSERT INTO pokemons (ID, name, type1, type2, type3) VALUES ( %s, %s, %s, %s, %s )'
    with cnx.cursor() as cursor:
        try:
            cursor.executemany(insert_query, images)
            cnx.commit()
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
    print('DONE')
    cnx.close()
    
def insert_all():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host='localhost', database='Pokemons')
    e = Extraction()
    pokedex, images = e.get_all('1009')
    image_query = 'INSERT INTO poke_images (ID, image) VALUES ( %s, %s )'
    poke_query = 'INSERT INTO pokemons (ID, name, type1, type2, type3) VALUES ( %s, %s, %s, %s, %s )'
    with cnx.cursor() as cursor:
        try:
            cursor.executemany(image_query, images)
            cursor.executemany(poke_query, pokedex)
            cnx.commit()
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
    print('DONE')
    cnx.close()
    
def update_img_table():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host='localhost', database='Pokemons')
    conn = create_engine(url=f'mysql+pymysql://{USERNAME}:{PASSWORD}@localhost:3306/Pokemons')
    image_query = 'INSERT INTO image_paths (id, name, paths) VALUES ( %s, %s, %s )'
    path = os.path.join(os.curdir, 'static/img')
    target_files = os.listdir(path)
    target_files.remove('api_img.jpg')
    select_pokemons = 'SELECT * FROM pokemons'
    names = list(pd.read_sql(select_pokemons, conn)['name'])
    for i, item in enumerate(target_files):
        if item == 'api_img.jpg':
            continue
        num = [i for i in re.split(r'([A-Za-z]+)', item.split('.')[0]) if i][1]
        with cnx.cursor() as cursor:
            try:
                cursor.execute(image_query, (num, names[int(num)-1], f'images/{item}'))
                cnx.commit()
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
    
    

def modify_file_names(folder: str):
    path = os.path.join(os.curdir, folder)
    target_files = os.listdir(path)
    conn = create_engine(url=f'mysql+pymysql://{USERNAME}:{PASSWORD}@localhost:3306/Pokemons')
    select_pokemons = 'SELECT * FROM pokemons'
    names = pd.read_sql(select_pokemons, conn)['name']
    full_path = os.path.join(os.path.abspath(os.getcwd()), folder)
    for i, target in enumerate(target_files):
        filenum = [i for i in re.split(r'([A-Za-z]+)', target.split('.')[0]) if i][1]
        name = names[int(filenum) - 1]
        os.rename(os.path.join(full_path, target), os.path.join(full_path, name + '.jpg'))
        print(i+1)
    

if __name__ == '__main__':
    update_img_table()