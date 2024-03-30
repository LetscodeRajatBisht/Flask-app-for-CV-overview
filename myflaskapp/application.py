from flask import Flask, render_template, redirect, url_for, request, session, flash
import feedparser

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

def fetch_cybersecurity_news():
    """Fetches the latest cybersecurity news from The Hacker News."""
    feed_url = 'https://feeds.feedburner.com/TheHackersNews'
    news_feed = feedparser.parse(feed_url)
    news_items = [{'title': entry.title, 'description': entry.description, 'link': entry.link} for entry in
                  news_feed.entries[:5]]
    return news_items

@app.route('/')
def index():
    """Homepage route."""
    news_items = fetch_cybersecurity_news()
    return render_template('index.html', news_items=news_items)

@app.route('/about')
def about():
    """About page route."""
    if not session.get('registered'):
        flash('Please register to access this page.', 'warning')
        return redirect(url_for('register'))
    return render_template('about.html')

@app.route('/logout')
def logout():
    """Logout route."""
    session.pop('registered', None)  # Remove 'registered' from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))  # Redirect to the home page after logout

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page route."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Simulate registration success
        session['registered'] = True
        flash('Registration successful!', 'success')
        return redirect(url_for('about'))

    news_items = fetch_cybersecurity_news()
    return render_template('register.html', news_items=news_items)

if __name__ == '__main__':
    app.run(debug=True)
