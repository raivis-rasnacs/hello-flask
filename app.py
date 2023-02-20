from flask import Flask, render_template

app = Flask(__name__,
            static_url_path="/static",
            static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/greeting")
def greeting():
    return render_template("greeting.html")

@app.route("/students")
def show_students():
    students = [
        {"name":"Alice",
        "class":"8a"},
        {"name":"Jeremy",
        "class":"10b"}
    ]
    return render_template("students.html", data=students)

if __name__ == "__main__":
    app.run(debug=True)