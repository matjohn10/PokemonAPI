from flask import Flask, jsonify, render_template, request
from apiFunctions import PokeInformation
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

app = Flask(__name__, static_folder="./static")
CORS(app)
auth = HTTPBasicAuth()

app.config['UPLOAD_FOLDER'] = '../img'
POKEMONS = PokeInformation()

USERS = {
    "mathieu": "1234"
}
@auth.verify_password
def verify_password(user, password):
    if user in USERS and USERS.get(user) == password:
        return user
    
@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/docs')
def show_docs():
    return render_template('docs.html')

@app.route('/api/')
def get_all():
    return jsonify(POKEMONS.all_info()), 200

@app.route('/api/pokemons/')
def get_pokemons():
    return jsonify(POKEMONS.pokemon_info()), 200

@app.route('/api/pokemons/<poke_id>')
def get_id(poke_id):
    try: 
        i = int(poke_id)
        if i < 0 or i > 1008:
            return jsonify({"error": "Out of Bounds"}), 404
        return jsonify(POKEMONS.pokemon_from_id(poke_id))
    except ValueError:
        if POKEMONS.is_pokemon(poke_id.capitalize()):
            return jsonify(POKEMONS.pokemon_from_name(poke_id))
        else:
            return jsonify({'error': 'Not supported path.', 'endpoint': f'/api/pokemons/{poke_id}'})

@app.route('/api/types-combat/')
def get_types():
    return jsonify(POKEMONS.type_info()), 200

@app.route('/api/types-combat/<type>')
def get_type(type):
    try:
        t = POKEMONS.type_from_type(type)
        final = {type: t}
        return jsonify(final), 200
    except KeyError:
            return jsonify({'Error': 'Type not found in the API'}), 404

@app.route('/api/types/')
def get_poke_all_types():
    return jsonify(POKEMONS.pokemons_per_type())

@app.route('/api/types/<type>')
def get_poke_per_type(type):
    try:
        return jsonify(POKEMONS.pokemons_per_type(type))
    except:
        return jsonify({'Error': 'Type not found in the API'}), 404

@app.route('/api/pokemon-images/')
def get_images():
    return jsonify(POKEMONS.image_info()), 200

@app.route('/api/pokemon-images/<img_id>')
def get_img_id(img_id: str):
    try:
        i = int(img_id)
        if i < 0 or i > 1008:
            return jsonify({"error": "Out of Bounds"}), 404
        return jsonify(POKEMONS.image_from_id(img_id))
    except ValueError:
        if POKEMONS.is_pokemon(img_id.capitalize()):
            return jsonify(POKEMONS.image_from_name(img_id))
        else:
            return jsonify({'error': 'Not supported path.', 'endpoint': f'/api/pokemon-images/{img_id}'})

@app.route('/api/pokemon-images/<img_id>/show')
def show_img(img_id):
    try:
        # img_url = POKEMONS.image_from_id(img_id)
        i = int(img_id)
        if i < 0 or i > 1008:
            return jsonify({'Error': 'OUT OF BOUNDS INDEX'}), 404
        path = f'img/pokemon{img_id}.jpg'
        return render_template('image.html', poke_img=path)
    except ValueError:
        if POKEMONS.is_pokemon(img_id.capitalize()):
            id = POKEMONS.image_from_name(img_id)
            path = f'img/pokemon{id}.jpg'
            return render_template('image.html', poke_img=path)
        else:
            return jsonify({'error': 'Not supported path.', 'endpoint': f'/api/pokemon-images/{img_id}/show'})

@app.route('/api/description/')
def show_descriptions():
    return jsonify(POKEMONS.get_description())

@app.route('/api/description/<des_id>')
def show_description(des_id):
    try:
        i = int(des_id)
        if i < 0 or i > 1008:
            return jsonify({"error": "Out of Bounds"}), 404
        return jsonify(POKEMONS.des_from_id(i))
    except ValueError:
        if POKEMONS.is_pokemon(des_id.capitalize()):
            return jsonify(POKEMONS.des_from_name(des_id))
        else:
            return jsonify({'error': 'Not supported path.', 'endpoint': f'/api/pokemon-images/{des_id}'})


@app.route('/api/image-paths/')
def get_paths():
    return jsonify(POKEMONS.get_paths())
    
@app.route('/api/image-paths/<name>')
def get_img_path(name: str):
    id = list(POKEMONS.name_to_id).index(name.capitalize()) + 1
    path = "images/pokemon" + str(id) + '.jpg'
    if id < 0 or id > 1008:
            return jsonify({"error": "Out of Bounds"}), 404
    return jsonify({name: path})


#Test auth access
@app.route('/test')
@auth.login_required
def test():
    return f'Hello {auth.current_user().capitalize()}!'


#Catch ALL
@app.route('/', defaults={'my_path': ''})
@app.route('/<path:my_path>')
def catch_all(my_path):
    if request.headers['Accept'] == '*/*':
        return jsonify({'error': 'Not supported path.', 'endpoint': f'/{my_path}'})
    else:
        return render_template('not_supported.html', endpoint=my_path)


if __name__ == "__main__":
  app.run(debug=True)
