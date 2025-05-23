from flask import Flask, render_template
import requests

app = Flask(__name__)

# Route for the home page
@app.route("/")
def index():
    url = "https://api.nookipedia.com/nh/sea"
    headers = {
        "X-API-KEY": '94692e6f-677f-4348-85fe-6375ae013248',
        "Accept-Version": "1.7.0"
    }

    try:
        # get species data from nookipedia api
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        creature_list = response.json()
        print(creature_list)
    except requests.exceptions.HTTPError as e:
        print(f"http error: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"network error: {e}")
    
    # We create a list to store details for each species.
    creatures = []

    for creature in creature_list:
        url = creature['url']
        parts = url.strip("/").split("/")
        id = parts[-1]  # The last part is the creature's ID
        
        # We use the ID to build an image URL.
        image_url = creature['image_url']
        
        creatures.append({
            'name': creature['name'].capitalize(),
            'id': id,
            'image': image_url
        })
    
    # We tell Flask to show the 'index.html' page and pass the list of Pokémon.
    return render_template("index.html", creatures=creatures)
# Route for the Pokémon details page
@app.route("/creature/<id>")
def creature_detail(id):
    
    
    # We get detailed info for a specific Pokémon using its id.
    response = requests.get(f"https://api.nookipedia.com/nh/sea/{id}")
    print(response)
    data = response.json()
    print(data)
    # We tell Flask to show the 'creature.html' page with all these details.
    return render_template("creature.html", creature=data)

if __name__ == '__main__':
    app.run(debug=True)
