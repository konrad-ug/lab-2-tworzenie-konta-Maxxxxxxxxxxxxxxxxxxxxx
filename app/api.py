from flask import Flask, request, jsonify
from RejestrKont import RejestrKont
from Account import Account

app = Flask(__name__)
@app.route("/konta/stworz_konto", methods=['POST'])
def stworz_konto():
    dane = request.get_json()
    print(f"Request o stworzenie konta z danymi: {dane}")

    konto = Account(dane["imie"], dane["nazwisko"], dane["pesel"])
    print(f"pesel: {konto.pesel}")
    RejestrKont.dodaj(konto)

    return jsonify("Konto stworzone"), 201

@app.route("/konta/ile_kont", methods=['GET'])
def ile_kont():
    liczba = RejestrKont.count()
    return jsonify(liczba), 200

@app.route("/konta/konto/<pesel>", methods=['GET'])
def wyszukaj_konto_z_peselem(pesel):
    found = RejestrKont.find(pesel)
    return jsonify(name=found.name, surname=found.surname, pesel=found.pesel, balance=found.balance), 200