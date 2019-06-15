from flask import Flask, render_template, request, make_response, jsonify

import random
app = Flask(__name__)

wrong_guess = []


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        response = make_response(render_template("index.html"))
        if not request.cookies.get('secret_number', False): # Si no hay cookie la genera
            response.set_cookie('secret_number', str(random.randint(1, 30)))
        return response

    elif request.method == "POST":
        if request.form.get('guess', False): # Para evitar trampas de aplicaciones que hagan request directas
            secret_number = request.cookies.get('secret_number', False) # Recoge la cookie para saber el resultado con el que comparar lo que hemos metido
            guess = request.form.get('guess', False)
            if secret_number == guess : # Si ha acertado:
                data = {'result': True, "wrong_guess": wrong_guess} # Mostramos un acertado y los numeros fallidos anteriormente
                response = make_response(render_template("index.html", data=data))
                response.set_cookie('secret_number', str(random.randint(1, 30)))
            else:                              # Si no hemos acertado damos una pista para que pueda acertar
                if int(secret_number) < int(guess):
                    data = {'result': False, 'tip': "Demasiado grande, prueba algo mas pequeño"}
                else:
                    data = {'result': False, 'tip': "Demasiado pequeño, prueba algo mas grande"}
                response = make_response(render_template("index.html", data=data))
                wrong_guess.append(request.form.get('guess', False))
            return response # Devolver response por pantalla,mostrando un mensaje segun si ha acertado o si ha puesto un numero mayor o menor
        wrong_guess.clear()
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

