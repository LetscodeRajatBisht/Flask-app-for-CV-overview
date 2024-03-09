from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import feedparser
import requests
import logging
from logging.handlers import RotatingFileHandler


application = Flask(__name__)
application.config['SECRET_KEY'] = 'canyougetmeajob@4436318663'



application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:rajatbisht@flaskdatabase.c7wqgg8maypt.us-east-1.rds.amazonaws.com/flaskapp'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


def fetch_cybersecurity_news():
    """Fetches the latest cybersecurity news from The Hacker News."""
    feed_url = 'https://feeds.feedburner.com/TheHackersNews'
    news_feed = feedparser.parse(feed_url)
    news_items = [{'title': entry.title, 'description': entry.description,'link': entry.link} for entry in news_feed.entries[:5]]
    return news_items

@application.route('/')
def index():
    news_items = fetch_cybersecurity_news()
    return render_template('index.html', news_items=news_items)

@application.route('/about')
def about():
    if not session.get('registered'):
        flash('Please register to access this page.', 'warning')
        return redirect(url_for('register'))
    return render_template('about.html')

@application.route('/logout')
def logout():
    session.pop('registered', None)  # Remove 'registered' from session
    flash('You have been logged out.', 'info')
    # For simplicity, just redirecting back to the home page after logout
    return redirect(url_for('index'))


@application.route('/register', methods=['GET', 'POST'])
def register():

    news_items = fetch_cybersecurity_news()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
       
        user_exists = users.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))
        
        try:
            new_user = users(name=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['registered'] = True
            flash('Registration successful!', 'success')
            return redirect(url_for('about'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again later.', 'danger')

       
        # After registration, redirect to about page
        return redirect(url_for('about'))
    return render_template('register.html', news_items=news_items)



if __name__ == '__main__':
    application.run(debug=True)
