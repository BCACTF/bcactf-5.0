from flask import Flask, render_template

app = Flask(__name__)

app.static_folder = 'resources'

@app.route('/')
def home():
    return render_template('sea.html')

@app.route('/shark')
def shark():
    return render_template('shark.html')

@app.route('/squid')
def squid():
    return render_template('squid.html')

@app.route('/clam')
def clam():
    return render_template('clam.html')

@app.route('/shipwreck')
def shipwreck():
    return render_template('shipwreck.html')

@app.route('/whale')
def whale():
    return render_template('whale.html')

@app.route('/dolphin')
def dolphin():
    return render_template('dolphin.html')

@app.route('/jellyfish')
def jellyfish():
    return render_template('jellyfish.html')

@app.route('/treasure')
def treasure():
    return render_template('treasure.html')

if __name__ == '__main__':
    app.run(debug=True)