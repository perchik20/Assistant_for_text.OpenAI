from flask import Flask, render_template, request, jsonify
from func import get_data
from itertools import groupby

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
            print(f'search word -> {search_word}')
            employee = get_data(f"SELECT * FROM Users WHERE question LIKE '%{search_word}%' AND album_name = '{var}'")

        for i in employee:
            mass.append(i[1])
            mass.append(i[2])
            glob_mass.append(mass)
            mass = []
        print(f'mass -> {glob_mass}')

    return jsonify({'htmlresponse': render_template('response.html', mass=glob_mass, var=var)})


if __name__ == "__main__":
    app.run(debug=True)



