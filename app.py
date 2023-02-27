from flask import Flask, render_template, request, flash, redirect, url_for
from helpers import error_page
from uuid import uuid4
import sqlite3

con = sqlite3.connect("gramatas.db", check_same_thread=False)
cur = con.cursor()

app = Flask(__name__,
            static_url_path="/static",
            static_folder="static")

app.register_error_handler(404, error_page)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/greeting")
def greeting():
    return render_template("greeting.html")

@app.route("/new-student")
def new_student():
    return render_template("new_student.html")

@app.route("/books")
def show_books():
    res = cur.execute('''SELECT gramatas_id, 
                                isbn_kods, 
                                nosaukums, 
                                valoda, 
                                lpp_skaits, 
                                izd_gads,
                                autori.vards || " " || autori.uzvards 
                                FROM gramatas
                                JOIN autori ON autori.autora_id = gramatas.autors''')
    all_books = res.fetchall()
    return render_template("books.html", data=all_books)

@app.route("/new-book", methods=["POST", "GET"])
def new_book():

    # Pārbauda, vai POST pieprasījums
    if request.method == "POST":
        # Ielasa datus no formas
        isbn = request.form["isbn"]
        nos = request.form["nosaukums"]
        valoda = request.form["valoda"]
        lpp_skaits = request.form["lpp_skaits"]
        izd_gads = request.form["izd_gads"]
        autors = request.form["autors"]

        id = str(uuid4())
        sql = '''INSERT INTO gramatas (gramatas_id,
                                    isbn_kods,
                                    nosaukums,
                                    valoda,
                                    lpp_skaits,
                                    izd_gads,
                                    autors)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                '''
        cur.execute(sql, (id, 
                          isbn, 
                          nos, 
                          valoda, 
                          lpp_skaits, 
                          izd_gads,
                          autors))
        con.commit()
        return redirect(url_for("show_books"))
    else:
        res = cur.execute("SELECT * FROM autori")
        autori = res.fetchall()
        print(autori)
        return render_template("new_book.html", data=autori)

@app.route("/new-author", methods=["POST", "GET"])
def new_author():
    if request.method == "POST":
        vards = request.form["vards"]
        uzvards = request.form["uzvards"]
        dz_gads = request.form["dz_gads"]
        id = str(uuid4())
        try:
            sql = '''INSERT INTO autori (autora_id, 
                                        vards, 
                                        uzvards, 
                                        dz_gads)
                    VALUES (?, ?, ?, ?)
                    '''
            cur.execute(sql, (id, vards, uzvards, dz_gads))
            con.commit()
        except:
            return "Operācija neveiksmīga!"
        return redirect(url_for("show_books"))
    else:
        return render_template("new_author.html")


@app.route("/students", methods=["POST", "GET"])
def show_students():
    students = [
            {"name":"Alice",
            "class":"8a"},
            {"name":"Jeremy",
            "class":"10b"}
        ]
    if request.method == "POST":
        student_name = request.form["student_name"]
        student_class = request.form["student_class"]
        students.append({})
        students[len(students) - 1]["name"] = student_name
        students[len(students) - 1]["class"] = student_class

    return render_template("students.html", data=students)

if __name__ == "__main__":
    app.run(debug=True)