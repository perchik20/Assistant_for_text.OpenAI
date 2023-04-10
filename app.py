from flask import Flask, render_template, request, jsonify
from edit_data import get_data
from itertools import groupby
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

app = Flask(__name__)

variant = 'loh'


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/get_variant", methods=["POST", "GET"])
def get_variant():
    global variant
    if request.method == 'POST':
        variant = request.form['variant']
    return variant


@app.route("/ajaxlivesearch", methods=["POST", "GET"])
def ajaxlivesearch():
    if request.method == 'POST':
        mass=[]
        glob_mass=[]

        search_word = request.form['query']

        print(search_word, variant)

        if search_word == '':
            employee = get_data("SELECT * from employee ORDER BY id")
        else:
            employee = get_data(f"SELECT * FROM Users WHERE album_name = '{variant}'")

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

    return jsonify({'htmlresponse': render_template('response.html', mass=glob_mass, var=variant)})


# @app.route("/grade", methods=["POST", "GET"])
# def grade():
#     grade = request.form['contact']
#     print(grade)
#     return grade


if __name__ == "__main__":
    app.run(debug=True)



