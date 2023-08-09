import openai
import requests
import time
from sqlalchemy import create_engine
import mysql.connector
import pandas as pd
from mySQL_credentials import USERNAME, PASSWORD

openai.api_key = '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'
MAX_TOKENS_PER_MINUTE = 150000

conn = create_engine(url=f'mysql+pymysql://{USERNAME}:{PASSWORD}@localhost:3306/Pokemons')
cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host='localhost', database='Pokemons')
select_pokemons = 'SELECT * FROM pokemons'

def get_list_pokemons():
    db = pd.read_sql(select_pokemons, conn)
    names = db["name"]
    return names

def calculate_delay(tokens):
    tokens_per_second = MAX_TOKENS_PER_MINUTE / 60
    seconds_per_token = 1 / tokens_per_second
    return tokens * seconds_per_token

def get_pokemon_description(pokemon: str):
    prompt = f"Generate a description of {pokemon} the pokemon and give information about his generation, type, evolutions, and his story in the pokemon manga."
    # Generate a description
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=700,
    n=1,
    stop=None,
    temperature=0.7
    )

    # Get the generated description
    description = response.choices[0].text.strip()
    
    tokens_used = response['usage']['total_tokens']
    delay = calculate_delay(tokens_used)
    
    return description, delay

def perform_generation():
    
    
    # Add to database
    pokemons = get_list_pokemons()
    # all_des = []
    for i, pokemon in enumerate(pokemons):
        description, delay = get_pokemon_description(pokemon)
        insert_query = 'INSERT INTO Description (id, name, description) VALUES ( %s, %s, %s )'
        
        # With info, add to database
        with cnx.cursor() as cursor:
            try:
                # cursor.executemany(insert_query, all_des)
                cursor.execute(insert_query, (i+1, pokemon, description))
                cnx.commit()
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
        # Wait for the calculated delay before making the next request
        time.sleep(delay)
        
    
    print('DONE')


if __name__ == '__main__':
    perform_generation()