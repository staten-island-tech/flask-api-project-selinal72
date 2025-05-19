from flask import Flask, render_template
import requests

app = Flask(__name__)

""" API_KEY = '94692e6f-677f-4348-85fe-637ae013248' """

# Route for the home page
@app.route("/")
def index():
    url = "https://api.nookipedia.com/villagers"
    key = '94692e6f-677f-4348-85fe-637ae013248'
    headers = {
        "X-API-KEY": '94692e6f-677f-4348-85fe-637ae013248',
        "Accept-Version": "1.7.0"
    }
    response = requests.get(url)
    print
    """ try:
        # get species data from nookipedia api
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        villager_list = response.json()
        print(villager_list)
    except requests.exceptions.HTTPError as e:
        print(f"http error: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"network error: {e}") """
    
    # We create a list to store details for each species.
    villagers = []

    for villager in villager_list:
        """ # try to get this data
        try:
            name = person['name']
            gender = person['gender']
            age = person['age']
            eye_color = person['eye_color']
            hair_color = person['hair_color']
            species_links = person['']
        # if no data found set as unknown
        except KeyError:
            name = 'Unknown'
            gender = 'Unknown'
            eye_color = 'Unknown'
            hair_color = 'Unknown'
        else: 
            people.append({
                'name': name,
                'gender': gender,
                'eye_color': eye_color,
                'hair_color': hair_color
            }) """
        
        url = villager['url']
        parts = url.strip("/").split("/")
        id = parts[-1]  # The last part is the villager's ID
        
        # We use the ID to build an image URL.
        image_url = villager['image_url']
        
        villagers.append({
            'name': villager['name'].capitalize(),
            'id': id,
            'image': image_url
        })
    
    # We tell Flask to show the 'index.html' page and pass the list of Pokémon.
    return render_template("index.html", villagers=villagers)
# Route for the Pokémon details page
@app.route("/person/<id>")
def villager_detail(id):
    # We get detailed info for a specific Pokémon using its id.
    response = requests.get(f"https://api.nookipedia.com/villagers/{id}")
    data = response.json()
    
    # We tell Flask to show the 'pokemon.html' page with all these details.
    return render_template("person.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
