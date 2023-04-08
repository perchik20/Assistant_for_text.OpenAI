from flask import Flask, render_template, request, jsonify
from func import get_data
from itertools import groupby
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

app = Flask(__name__)


@app.route('/')
def main():
    mass = []
    variants = get_data('SELECT * FROM Users')
    for i in variants:
        mass.append(i[3])
    mass = [el for el, _ in groupby(mass)]
    return render_template('main.html', var=mass)


@app.route('/search/<var>')
def index(var):
    return render_template('index.html', var=var)


@app.route("/ajaxlivesearch/<var>", methods=["POST", "GET"])
def ajaxlivesearch(var):
    if request.method == 'POST':
        mass=[]
        glob_mass=[]
        search_word = request.form['query']
        if search_word == '':
            employee = get_data("SELECT * from employee ORDER BY id")

        else:
            employee = get_data(f"SELECT * FROM Users WHERE album_name = '{var}'")

        counter_fuzzy = 70
        while len(glob_mass) == 0:
            for i in employee:
                if fuzz.partial_ratio(i[1], search_word) > counter_fuzzy:
                    mass.append(i[1])
                    mass.append(i[2])
                    glob_mass.append(mass)
                    mass = []
                else:
                    continue

            if len(glob_mass) == 0:
                counter_fuzzy -= 5
            else:
                break

    return jsonify({'htmlresponse': render_template('response.html', mass=glob_mass, var=var)})




if __name__ == "__main__":
    app.run(debug=True)



