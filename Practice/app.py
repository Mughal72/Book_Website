import csv

from flask import Flask, render_template, request, redirect, flash, session, jsonify, url_for
from flask_mysqldb import MySQL
import os
import random
import string
import pandas as pd

app = Flask(__name__)

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "mydatabase"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Secret key for flashing messages
app.secret_key = "8f4e74efb806979fbaa51faa46d66088"


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

    # Insert default user profile data into the user_profiles table
    sql = "INSERT INTO user_profiles (username) VALUES (%s)"
    val = (username,)
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
        isbn = request.form['isbn']
        rating = request.form['rating']
        reading_frequency = request.form['reading_frequency']
        book_format = request.form['book_format']
        receive_recommendations = request.form['receive_recommendations']
        reading_topics = request.form['reading_topics']
        book_type = request.form['book_type']

        # Save interest data to the CSV file
        with open('C:/Users/A R Y/PycharmProjects/practice/data/users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, location, age, ', '.join(genres), ', '.join(authors), last_book, isbn,
                             rating, reading_frequency, book_format, receive_recommendations, reading_topics,
                             book_type])

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


def get_popular_books():
    # Load the dataset
    books_df = pd.read_csv('C:/Users/A R Y/PycharmProjects/practice/data/books.csv', encoding='latin1')

    # Calculate the average ratings for each book
    book_ratings = books_df.groupby('Book-Title').agg(
        {'Ratings': 'mean', 'Author-Name': 'first', 'Image-URL': 'first'}).reset_index()

    # Sort the books based on average ratings in descending order
    popular_books = book_ratings.sort_values('Ratings', ascending=False).head(30)

    return popular_books


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

        # Get the popular books
        popular_books = get_popular_books()

        # # Remove username after 4 seconds
        # time.sleep(4)
        # session.pop('username', None)

        return render_template('welcome.html', username=username, email=user_data['email'],
                               password=user_data['password'], popular_books=popular_books)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    return redirect('/login')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        # Fetch the user profile information from the database
        username = session['username']
        cur = mysql.connection.cursor()

        # Fetch user data from the accounts table
        sql = "SELECT username, email, password FROM accounts WHERE username = %s"
        val = (username,)
        cur.execute(sql, val)
        user = cur.fetchone()

        # Check if user profile data exists in the user_profiles table
        sql = "SELECT * FROM user_profiles WHERE username = %s"
        cur.execute(sql, val)
        user_profile = cur.fetchone()

        if request.method == 'POST':
            # Get the form data from the JSON data
            data = request.form.to_dict()

            # Convert the country value to lowercase
            data['country'] = data.get('country').lower()

            if user_profile:
                # Update the user profile data in the user_profiles table
                sql = """UPDATE user_profiles
                         SET first_name = %s, last_name = %s, password = %s, email = %s, 
                         phone_number = %s, country = %s, home_address = %s
                         WHERE username = %s"""
                val = (data.get('first-name'), data.get('last-name'), data.get('password'), data.get('email'),
                       data.get('phone-number'), data.get('country'), data.get('home-address'), username)
                cur.execute(sql, val)
            else:
                # Insert new user profile data into the user_profiles table
                sql = """INSERT INTO user_profiles (username, first_name, last_name, password, email, 
                         phone_number, country, home_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                val = (username, data.get('first-name'), data.get('last-name'), data.get('password'), data.get('email'),
                       data.get('phone-number'), data.get('country'), data.get('home-address'))
                cur.execute(sql, val)

            mysql.connection.commit()
            cur.close()

            # Redirect the user to the "welcome" page after successfully saving the data
            return redirect('/welcome')

        cur.close()

        return render_template('profile.html', user=user, user_profile=user_profile)
    else:
        return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
