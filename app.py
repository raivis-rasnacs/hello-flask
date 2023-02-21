from flask import Flask, render_template, request
from helpers import error_page

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