from flask import Flask, render_template

app = Flask(__name__)

app.static_folder = 'images'

@app.route('/')
def home():
    return render_template('sea.html')

if __name__ == '__main__':
    app.run(debug=True)