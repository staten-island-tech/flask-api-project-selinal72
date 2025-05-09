from flask import Flask, render_template
import requests

app = Flask(__name__)

# Route for the home page
@app.route("/")
def index():
    # We ask the Pokémon API for the first 150 Pokémon.
    response = requests.get("https://api.thecatapi.com/v1/images/search?limit=10")
    data = response.json()
    cats_list = data['results']
    
    # We create a list to store details for each Pokémon.
    cats = []
    
    for cat in cats_list:
        # Each Pokémon has a URL like "https://pokeapi.co/api/v2/pokemon/1/"
        url = cat['url']
        parts = url.strip("/").split("/")
        id = parts[-1]  # The last part of the URL is the Pokémon's ID
        
        # We use the ID to build an image URL.
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
        
        cats.append({
            'name': cat['name'].capitalize(),
            'id': id,
            'image': cat['url']
        })
    
    # We tell Flask to show the 'index.html' page and pass the list of Pokémon.
    return render_template("index.html", cats=cats)

# Route for the Pokémon details page
@app.route("/pokemon/<int:id>")
def pokemon_detail(id):
    # We get detailed info for a specific Pokémon using its id.
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    data = response.json()
    
    # We extract extra details like types, height, weight, and stats.
    types = [t['type']['name'] for t in data['types']]
    height = data.get('height')
    weight = data.get('weight')
    name = data.get('name').capitalize()
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
    
    # Get the Pokémon’s base stats (like hp, attack, defense, etc.)
    stat_names = [stat['stat']['name'] for stat in data['stats']]
    stat_values = [stat['base_stat'] for stat in data['stats']]
    
    # We tell Flask to show the 'pokemon.html' page with all these details.
    return render_template("pokemon.html", pokemon={
        'name': name,
        'id': id,
        'image': image_url,
        'types': types,
        'height': height,
        'weight': weight,
        'stat_names': stat_names,
        'stat_values': stat_values
    })

if __name__ == '__main__':
    app.run(debug=True)