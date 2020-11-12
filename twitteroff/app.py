"""Main app and routing"""
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User #, insert_example_users 
from .twitter import add_or_update_user, update_all_users
from .predict import predict_user

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/') # http://12.0.0.1:5000/
    def root():
        return render_template(
            'base.html',
            title="Home", 
            users=User.query.all()
            )

    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user1'], 
            request.values['user2']]
            )
        if user0 == user1:
            message = "Users are the same!"
        else:
            prediction = predict_user(
                user0, user1, request.values['tweet_text']
                )
            message = '{} is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], 
                user1 if prediction else user0,
                user0 if prediction else user1
            )
        return render_template(
            "prediction.html", 
            title="Prediction", 
            message=message
            )

    @app.route("/user", methods=["POST"])
    @app.route("/user/<name>", methods=["GET"])
    def user(name=None, message=''):
        name=name or request.values['user_name']
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message="User {} was successfully added.".format(name)
            tweets=User.query.filter(User.name==name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template(
            "user.html", 
            title=name, 
            tweets=tweets, 
            message=message
            )

    @app.route("/update")
    def update():
        update_all_users()
        return render_template(
            'base.html', 
            title="Home", 
            users=User.query.all()
            )
    
    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template(
            'base.html', 
            title="All tweets have been updated.",
            users=User.query.all()
            )
    
    return app

