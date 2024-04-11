from flask import Flask, render_template
import flag_gen

app = Flask(__name__)

@app.route('/')
def index(): #Gets the main page
    return render_template('index.html')

@app.route('/flag')
def getFlag():
    #Get flag from flag.txt
    with open("flag.txt") as f:
        flag = f.read()
        encoded = flag_gen.main(flag)
        joined_flag = ""
        for byte in encoded:
            joined_flag += byte
        # print(encoded)
        
    return render_template('index.html', joined_flag = joined_flag, flag_string = encoded)

if __name__ == '__main__':
    app.run(debug=True)
