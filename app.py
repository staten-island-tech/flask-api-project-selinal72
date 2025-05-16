from flask import Flask, render_template
import requests

app = Flask(__name__)

# Route for the home page
@app.route("/")
def index():
    

    # get species data from ghibli api
    response = requests.get("https://ghibliapi.vercel.app/people")
    people_list = response.json()
    
    # We create a list to store details for each species.
    people = []

    for person in people_list:
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
        
        url = person['url']
        parts = url.strip("/").split("/")
        id = parts[-1]  # The last part is the Pokémon's ID
        
        """ # We use the ID to build an image URL.
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png" """
        
        people.append({
            'name': person['name'].capitalize(),
            'id': id
        })
    
    # We tell Flask to show the 'index.html' page and pass the list of Pokémon.
    return render_template("index.html", people=people)

# Route for the Pokémon details page
@app.route("/person/<id>")
def person_detail(id):
    # We get detailed info for a specific Pokémon using its id.
    response = requests.get(f"https://ghibliapi.vercel.app/people/{id}")
    data = response.json()
    
    # We tell Flask to show the 'pokemon.html' page with all these details.
    return render_template("person.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
