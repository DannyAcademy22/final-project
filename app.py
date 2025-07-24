from flask import Flask, render_template, request
from models import db, Quote
import random

app = Flask(__name__)
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'quotes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    all_quotes = Quote.query.all()
    random_quote = random.choice(all_quotes) if all_quotes else None
    return render_template('index.html', quote=random_quote)

@app.route('/search')
def search():
    author = request.args.get('author')
    tag = request.args.get('tag')

    query = Quote.query

    if author:
        query = query.filter(Quote.author.ilike(f'%{author}%'))
    if tag:
        query = query.filter(Quote.tags.ilike(f'%{tag}%'))

    results = query.all()
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

