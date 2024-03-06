from flask import Flask, render_template, request
app = Flask(__name__)

from src.flag_bearer import crc_encrypt

@app.route('/')
def index(): #Gets the main page
    return render_template('index.html')

@app.route('/flag')
def getFlag():
    #Get flag from flag.txt
    with open("flag.txt") as f:
        flag = f.read()
        print(flag)
    #Encrypt with crc_encrypt
    return render_template('index.html', flag = "Flag")
    #Get flag from flag.txt
    #Encrypt with crc_encrypt

if __name__ == '__main__':
    app.run(debug=True)
