from flask import Flask, render_template, request
import importlib
import os
main = importlib.import_module("flag_transmitter", "rad-be-damned.src")

app = Flask(__name__)

@app.route('/')
def index(): #Gets the main page
    return render_template('index.html')

@app.route('/flag')
def getFlag():
    #Get flag from flag.txt
    with open("flag.txt") as f:
        flag = f.read()
        encoded = main.main(flag)
        print(encoded)

        #Encoded string printout
        total_str = ""
        for letter in encoded:
            total_str += chr(int(letter[:-5], base = 2))
        print(total_str)
        for letter in encoded:
            print(letter, end = ' ')
    #Encrypt with crc_encrypt
    return render_template('index.html', flag = "Flag")
    #Get flag from flag.txt
    #Encrypt with crc_encrypt

if __name__ == '__main__':
    app.run(debug=True)
