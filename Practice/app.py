import csv
from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "mydatabase"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Secret key for flashing messages
app.secret_key = "enter-your-key"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    # Get form data
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Insert user data into the database
    cur = mysql.connection.cursor()
    sql = "INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)"
    val = (username, email, password)
    cur.execute(sql, val)
    mysql.connection.commit()
    cur.close()

    # Store the username in the session
    session['username'] = username

    return redirect('/interest')


@app.route('/interest')
def interest():
    if 'username' in session:
        return render_template('interest_form.html')
    else:
        return redirect('/login')


@app.route('/submit_interests', methods=['POST'])
def submit_interests():
    # Get form data
    if 'username' in session:
        username = session['username']
        location = request.form['location']
        age = request.form['age']
        genres = request.form.getlist('genres')
        authors = request.form.getlist('authors')
        last_book = request.form['last_book']
        reading_frequency = request.form['reading_frequency']
        book_format = request.form['book_format']
        receive_recommendations = request.form['receive_recommendations']
        reading_topics = request.form['reading_topics']
        book_type = request.form['book_type']

        # Save interest data to the CSV file
        with open('C:/Users/A R Y/PycharmProjects/practice/users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, location, age, ', '.join(genres), ', '.join(authors), last_book,
                             reading_frequency, book_format, receive_recommendations, reading_topics, book_type])

        return redirect('/login')
    else:
        return redirect('/login')


@app.route('/login')
def login():
    return render_template('index.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Get form data
    email = request.form['email']
    password = request.form['password']

    # Check if user exists in the database
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM accounts WHERE email = %s AND password = %s"
    val = (email, password)
    cur.execute(sql, val)
    account = cur.fetchone()
    cur.close()

    if account:
        session['username'] = account['username']
        return redirect('/welcome')
    else:
        flash('Invalid email or password')
        return redirect('/login')


@app.route('/welcome')
def welcome():
    if 'username' in session:
        # Fetch signup information from the database
        username = session['username']
        cur = mysql.connection.cursor()
        sql = "SELECT email, password FROM accounts WHERE username = %s"
        val = (username,)
        cur.execute(sql, val)
        user_data = cur.fetchone()
        cur.close()

        return render_template('welcome.html', username=username, email=user_data['email'], password=user_data['password'])
    else:
        return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
