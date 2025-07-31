# models.py

from flask_sqlalchemy import SQLAlchemy

# setting up the database connection
db = SQLAlchemy()

# this is the table where we will store quotes
class Quote(db.Model):
    # every quote has a unique id
    id = db.Column(db.Integer, primary_key=True)

    # the text of the quote (what it says)
    text = db.Column(db.String(500), nullable=False)

    # who said the quote
    author = db.Column(db.String(100), nullable=False)

    # extra tags like "life", "motivation" (comma-separated)
    tags = db.Column(db.String(200))

