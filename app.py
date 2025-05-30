from flask import Flask, render_template
import requests

app = Flask(__name__)

# Route for the home page
@app.route("/")
def index():
    selected_month = request.args.get("month") # selected month
    url = "https://api.nookipedia.com/nh/sea"
    headers = {
        "X-API-KEY": '94692e6f-677f-4348-85fe-6375ae013248',
        "Accept-Version": "1.7.0"
    }

    params = {} # leave blank first bc dk if person wants to filter yet
    if selected_month: # if they select a month
        params['month'] = selected_month # set the value for the key

    
    try:
        # get species data from nookipedia api
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        creature_list = response.json()
    except requests.exceptions.HTTPError as e:
        print(f"http error: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"network error: {e}")
    
    # We create a list to store details for each species.
    creatures = []
    for creature in creature_list:
        url = creature['url']
        image_url = creature['image_url']
        
        creatures.append({
            'name': creature['name'].capitalize(),
            'id': id,
            'image': image_url
        })
    
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    # We tell Flask to show the 'index.html' page and pass the list of Pokémon.
    return render_template("index.html", creatures=creatures, months=months, selected_month=selected_month)


# Route for the Pokémon details page
@app.route("/creature/<id>")
def creature_detail(id):
    
    # We get detailed info for a specific Pokémon using its id.
    response = requests.get(f"https://api.nookipedia.com/nh/sea/{id}",  headers = {
        "X-API-KEY": '94692e6f-677f-4348-85fe-6375ae013248',
        "Accept-Version": "1.7.0"
    })
    data = response.json()
    # We tell Flask to show the 'creature.html' page with all these details.
    return render_template("creature.html", creature=data)

if __name__ == '__main__':
    app.run(debug=True)
