from flask import Flask, render_template, jsonify
import datetime as dt
import requests

app = Flask(__name__)

# Globally defined name for reuse in rendering templates.
MY_NAME = 'Gavin "Siris" Martin'

@app.route('/')
@app.route('/home')
def home():
    current_year = dt.datetime.now().year
    try:
        blog_url = "https://api.npoint.io/674f5423f73deab1e9a7"
        blog_response = requests.get(blog_url)
        blog_response.raise_for_status()  # Ensures we proceed only if the response was successful.
        all_posts = blog_response.json()
        # Adding author and date where missing
        for post in all_posts:
            post['author'] = "Dr. Angela Yu" if 'author' not in post else post['author']
            post['date'] = dt.datetime.now().strftime("%B %d, %Y") if 'date' not in post else post['date']
    except requests.RequestException:
        all_posts = []  # If the API call fails, continue with an empty list for posts.
    return render_template('index.html', posts=all_posts, CURRENT_YEAR=current_year, MY_NAME=MY_NAME)

@app.route('/about')
def about():
    current_year = dt.datetime.now().year
    # Adding copyright notice.
    copyright = f'Copyright {current_year} {MY_NAME}. All Rights Reserved.'
    return render_template('about.html', CURRENT_YEAR=copyright, page='about')

@app.route('/contact')
def contact():
    current_year = dt.datetime.now().year
    # Same copyright notice as in about.
    copyright = f'Copyright {current_year} {MY_NAME}. All Rights Reserved.'
    return render_template('contact.html', CURRENT_YEAR=copyright, page='contact')

if __name__ == "__main__":
    app.run(debug=True)
