from flask import Flask, request, redirect, url_for, render_template_string
import mysql.connector

app = Flask(__name__)

# ---- MySQL Connection ----
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shaban",
        database="crud"
    )

# ---- Create Student Table if not exists ----
conn = get_db()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    class VARCHAR(50) NOT NULL,
    subject VARCHAR(100) NOT NULL
)
""")
conn.commit()
cursor.close()
conn.close()

# ---- HTML Template ----
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Student CRUD - One File</title>
    <style>
        body{
            font-family:Poppins;
            background:#eef2f3;
            display:flex;
            justify-content:center;
            padding-top:30px;
        }
        .container{
            width:720px;
            background:white;
            padding:22px;
            border-radius:12px;
            box-shadow:0 0 12px rgba(0,0,0,0.15);
        }
        h2{text-align:center;margin-bottom:18px;}
        form{
            display:flex;
            gap:10px;
            margin-bottom:20px;
            flex-wrap:wrap;
        }
        input{
            flex:1;
            padding:10px;
            border:1px solid #bbb;
            border-radius:6px;
            min-width:150px;
        }
        button{
            padding:10px 15px;
            background:#27ae60;
            color:white;
            border:none;
            border-radius:6px;
            cursor:pointer;
        }
        button:hover{opacity:0.8;}
        table{width:100%;border-collapse:collapse;}
        th{
            background:#2c3e50;
            color:white;
            padding:10px;
        }
        td,th{border:1px solid #ddd;text-align:center;}
        td{padding:8px;}
        a{
            padding:5px 10px;
            border-radius:5px;
            text-decoration:none;
            color:white;
            font-size:14px;
        }
        .edit{background:#f39c12;}
        .delete{background:#e74c3c;}
    </style>
</head>
<body>
<div class="container">
    <h2>CRUD Operation</h2>

    {% if s %}
    <form action="/update/{{ s[0] }}" method="POST">
        <input type="number" name="roll" value="{{ s[0] }}" readonly>
        <input type="text" name="name" value="{{ s[1] }}" required>
        <input type="text" name="class" value="{{ s[2] }}" required>
        <input type="text" name="subject" value="{{ s[3] }}" required>
        <button type="submit">Update</button>
    </form>
    {% else %}
    <form action="/add" method="POST">
        <input type="number" name="roll" placeholder="Roll No" required>
        <input type="text" name="name" placeholder="Student Name" required>
        <input type="text" name="class" placeholder="Class" required>
        <input type="text" name="subject" placeholder="Subject" required>
        <button type="submit">Add Student</button>
    </form>
    {% endif %}

    <table>
        <tr><th>Roll No</th><th>Name</th><th>Class</th><th>Subject</th><th>Action</th></tr>
        {% for i in students %}
        <tr>
            <td>{{i[0]}}</td>
            <td>{{i[1]}}</td>
            <td>{{i[2]}}</td>
            <td>{{i[3]}}</td>
            <td>
                <a href="/edit/{{ i[0] }}" class="edit">Edit</a>
                <a href="/delete/{{ i[0] }}" class="delete">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
</body>
</html>
"""

# ---- Routes ----

# READ
@app.route("/")
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template_string(TEMPLATE, students=students, s=None)

# CREATE
@app.route("/add", methods=["POST"])
def add():
    roll = request.form["roll"]
    name = request.form["name"]
    stu_class = request.form["class"]
    subject = request.form["subject"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (roll, name, class, subject) VALUES (%s,%s,%s,%s)",
                   (roll, name, stu_class, subject))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("home"))

# EDIT
@app.route("/edit/<int:roll>")
def edit(roll):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE roll=%s", (roll,))
    s = cursor.fetchone()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template_string(TEMPLATE, students=students, s=s)

# UPDATE
@app.route("/update/<int:roll>", methods=["POST"])
def update(roll):
    name = request.form["name"]
    stu_class = request.form["class"]
    subject = request.form["subject"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=%s, class=%s, subject=%s WHERE roll=%s",
                   (name, stu_class, subject, roll))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("home"))

# DELETE
@app.route("/delete/<int:roll>")
def delete(roll):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE roll=%s", (roll,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
