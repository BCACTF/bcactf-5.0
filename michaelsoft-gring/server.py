from flask import Flask, render_template, url_for
from random import randint
import sqlite3

# returns a random word, weighted by frequency
def rand_word():
    n = randint(0, rand_max)
    word = -1
    while n > words[word][1]:
        word += 1
        n -= words[word][1]
    return words[word][0]



# flask app
app = Flask(__name__)

@app.get("/")
def main_page(a=False):
    url_for("static", filename="styles.css")
    url_for("static", filename="images/search.png")
    url_for("static", filename="images/logo.png")
    return render_template("mainpage.html", a=a)

@app.get("/search/<search>")
def search_page(search):
    #reconnect sql (sqlite wants me to do that idk why)
    con = sqlite3.connect("file:search_results.db?mode=ro", uri=True)
    cur = con.cursor()
    
    # make search results
    search_results = []
    search_words = search.lower().split(" ")
    search_lower = search.lower()
    
    sql = ""
    # do sql injection here (it's very poorly coded because sqlite is very hard to make vulnerable to sql injection)
    for word in search_words:
        sql += "SELECT title FROM search WHERE title LIKE '%" + word + "%';"
    try: 
        for query in sql.split(";"):
            for row in cur.execute(query):
                search_results.append(row[0])
    except:
        return main_page(a=True)
    no_results = len(search_results) == 0
    
    # do web
    url_for("static", filename="search.css")
    url_for("static", filename="images/logo.png")
    url_for("static", filename="search.js")
    return render_template("searchpage.html", search=search, search_lower=search_lower, search_results=search_results, no_results=no_results, search_terms=search_words)


if __name__ == '__main__':
    #create DB with tables
    con = sqlite3.connect("search_results.db")
    cur = con.cursor()
    for table in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall():
        cur.execute("DROP TABLE " + table[0]) 

    con.commit()

    cur.execute("CREATE TABLE search(title)")
    cur.execute("CREATE TABLE flag(flag)")
    cur.execute("INSERT INTO flag VALUES ('bcactf{59L_1n1ECTeD_026821}')")
    con.commit()

    # load words with frequencies from words.txt
    word_file = open("words.txt", "r", errors="ignore")
    words = []
    rand_max = 0 # sum of all word frequencies (for horrible weighted random system (i'm bad at math))

    for line in word_file:
        words.append((line.split(",")[0], int(line.split(",")[1])))
        rand_max += int(line.split(",")[1])

    # create and add search results
    to_add = []
    for _ in range(10000):
        to_add.append([""])
        for __ in range(randint(3,12)):
            to_add[-1][0] += " " + rand_word()
    to_add = [tuple(n) for n in to_add]
    print(to_add)
    cur.executemany("INSERT INTO search VALUES (?)", to_add)
    con.commit()
    
    app.run(host = '0.0.0.0', port = 5000)