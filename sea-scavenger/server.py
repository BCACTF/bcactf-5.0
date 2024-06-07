from flask import Flask, render_template, send_from_directory, request, make_response

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
    response = make_response(render_template('shipwreck.html'))
    response.headers['Flag_Part_4'] = 'd_th3_tr'
    return response

@app.route('/whale')
def whale():
    return render_template('whale.html')

@app.route('/treasure')
def treasure():
    return render_template('treasure.html')

@app.route('/treasure/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 4321)