from collections import defaultdict
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///players.db"
db.init_app(app)

# Make the database table and create it
class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    highestScore = db.Column(db.Integer, unique=False, nullable=False)  
with app.app_context():
    db.create_all()

# Database class with static methods
class Database:
    
    # Creates a new player
    @staticmethod
    def create_player(name):
        with app.app_context():

            # Create a new instance of the Books class.
            player = Players(name=name, highestScore=0)

            # Add the new instance to the database.
            db.session.add(player)

            # Commit the changes to the database.
            db.session.commit()    
    
    # Return a bool depending no whether if a player
    # exists in the database
    @staticmethod
    def find_player(name):      
        try:
            with app.app_context():
                player = db.session.execute(db.select(Players).where(Players.name == name)).scalar()
                name = player.name
                result = True
        except:
            result = False
            
        return result
    
    # Reset database
    @staticmethod
    def reset_database():
        with app.app_context():
            db.session.query(Players).delete()
            db.session.commit()
            
    # Modifiers             
    @staticmethod
    def update_score(name, score):
        with app.app_context():
            player = db.session.execute(db.select(Players).where(Players.name == name)).scalar()
            player.highestScore = score
            db.session.commit()
     
    # Accessors   
    @staticmethod
    def get_score(name):
        with app.app_context():
            player = db.session.execute(db.select(Players).where(Players.name == name)).scalar()
            return player.highestScore
        
    @staticmethod
    def get_top_players():
        with app.app_context():        
            result = db.session.execute(db.select(Players).order_by(Players.highestScore.desc()))
            players = result.scalars()
            top_players = {}
            
            for player in players:
                top_players[player.name] = player.highestScore

            return top_players
        

        


        