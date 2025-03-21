import os

from flask import Flask, render_template, request, redirect, url_for, flash

#This is just to initialize the flask app. 
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #This is the route to the starting html page.
    #If any information from the database wants to go into the starting page this is where the query should be placed.
    @app.route('/')
    def index():
        return render_template('index.html')
    
    #Import the database and initialize it within the start up of the flask app.
    import db
    db.init_app(app)

    #Import the menu flask and register the blueprint to be used.
    import menu
    app.register_blueprint(menu.bp)

    import auth
    app.register_blueprint(auth.bp)
    
    import kitchen
    app.register_blueprint(kitchen.bp)
    #We can make seperate blueprints for the kitchen ui and the waiter staff ui backends also.

    return app

