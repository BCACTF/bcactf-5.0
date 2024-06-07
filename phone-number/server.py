from flask import Flask, request

app = Flask(__name__)
flag = open("flag.txt","r").read()

@app.route("/")
def mainpage():
    return open("index.html","r").read() + \
        "<script>" + open("script.js","r").read() + "</script></html>"

@app.route("/flag", methods=["POST"])
def get_flag():
    print(request.data)
    if request.data == b"1234567890":
        return flag
    else:
        return ""
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)