from flask import Flask, jsonify
from groupjar import *

app= Flask(__name__)
@app.route('/')
def index():
    return "WISE Group Jar API"

def initiate(amount):
    ac1= AccountHolder(1, "Aadarsh Mehdi",  500, "EUR")
    eur = Jar(123,'Family','EUR', ac1)
    ac2= AccountHolder(2, "Makhlug Jafarov", 2000, "EUR", right =False)
    ac3= AccountHolder(3, "Bayram", 5000, "EUR", right =False)
    eur.add_member(ac2)
    eur.add_member(ac3)

@app.route('/jar/<string: currency>/<int: amount>', methods=['GET', 'POST'])
def deposit(amount):
    ac1.deposite(eur,250 )
    return eur.to_dict()
if __name__ == "__main__":
    app.run(debug=True)