import csv
from flask import Flask, render_template, request, redirect, flash, session, jsonify, url_for
from flask_mysqldb import MySQL
import os
import random
import string
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

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

# Load the books and users datasets
books_df = pd.read_csv("data/books.csv", encoding='latin-1')
users_df = pd.read_csv("data/users.csv", encoding='latin-1')

# Combine relevant columns from books and users datasets
books_df['Features'] = books_df['Genres'] + ' ' + books_df['Author-Name']
users_df['Features'] = users_df['Genres'] + ' ' + users_df['Author-Name'] + ' ' + users_df['Preferred Topics']

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the TF-IDF vectors for books and users
books_tfidf_matrix = tfidf_vectorizer.fit_transform(books_df['Features'])
users_tfidf_matrix = tfidf_vectorizer.transform(users_df['Features'])

# Compute the cosine similarity between books and users
cosine_sim = linear_kernel(users_tfidf_matrix, books_tfidf_matrix)


def get_personalized_recommendations(user_name, num_recommendations=10):
    user_idx = users_df[users_df['User-ID'] == user_name].index
    if not user_idx.empty:
        user_idx = user_idx[0]
        sim_scores = list(enumerate(cosine_sim[user_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations + 1]
        book_indices = [i[0] for i in sim_scores]
        return books_df.iloc[book_indices]
    else:
        # Handle the case where the user is not found
        return pd.DataFrame()  # Return an empty DataFrame or any other appropriate response


def generateRandomPrice():
    return round(random.uniform(10.0, 100.0), 2)


# Function to get featured books (you can customize this)
def get_featured_books(min_rating=4.0, num_books=15):
    # Get books with ratings above the specified threshold
    featured_books = books_df[books_df['Ratings'] > min_rating].head(num_books)
    return featured_books


@app.route('/')
def index():
    # Get the popular books
    popular_books = get_popular_books()

    # Get featured books
    featured_books = get_featured_books()

    return render_template('index.html', popular_books=popular_books, featured_books=featured_books)


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        # Get the search query from the form
        search_query = request.form['search_query'].lower()

        # Split the search query into keywords
        keywords = search_query.split()

        # Initialize an empty DataFrame for search results
        search_results = pd.DataFrame()

        # Search by book title or author
        title_author_results = books_df[
            books_df['Book-Title'].str.lower().str.contains(search_query) |
            books_df['Author-Name'].str.lower().str.contains(search_query)
        ]

        # Search by keywords in the 'Genres' column
        for keyword in keywords:
            keyword_results = books_df[books_df['Genres'].str.lower().str.contains(keyword)]
            search_results = pd.concat([search_results, keyword_results])

        # Combine the results from title, author, and keyword searches
        search_results = pd.concat([search_results, title_author_results])

        # Deduplicate the results
        search_results = search_results.drop_duplicates(subset='Book-Title')

        if not search_results.empty:
            print("Search Results Found:", search_results)
            # Render the results template
            return render_template('search_results.html', search_results=search_results)
        else:
            print("No Results Found")
            # If no results are found, get book suggestions from your dataset
            # You can use any logic to generate book suggestions, for example, top-rated books
            book_suggestions = get_book_suggestions()

            # Render the "not in stock" template with book suggestions
            return render_template('not_in_stock.html', search_query=search_query, book_suggestions=book_suggestions)


def get_book_suggestions():
    # Example: Get top-rated books as suggestions (you can modify this)
    top_rated_books = books_df.sort_values(by='Ratings', ascending=False).head(5)
    return top_rated_books


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
    # Get the popular books
    popular_books = get_popular_books()

    return render_template('index.html', popular_books=popular_books)


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
    popular_books = book_ratings.sort_values('Ratings', ascending=False).head(24)

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

        # Get the personalized book recommendations
        recommendations = get_personalized_recommendations(username, num_recommendations=15)

        return render_template('welcome.html', username=username, email=user_data['email'],
                               password=user_data['password'], popular_books=popular_books,
                               recommendations=recommendations, generateRandomPrice=generateRandomPrice)
    else:
        return redirect('/login')

    # # Remove username after 4 seconds
    # time.sleep(4)
    # session.pop('username', None)


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


@app.route('/shop')
def shop():
    featured_books = get_featured_books()

    # Render the shop.html template with initial book data
    return render_template('shop.html', featured_books=featured_books)


@app.route('/about')
def about():
    return render_template('about-us.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
